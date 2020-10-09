# coding=utf-8

import os

import cvxopt
import numpy as np
from matplotlib import pyplot as plt
from cvxopt.modeling import variable, solvers, op, matrix
from PySDDP.pmo import pmo
from PySDDP.dadosgerais import dadosgerais
from PySDDP.fcf import fcf
from itertools import product, tee
import time
from timeit import default_timer as timer
from functools import partial
from multiprocessing import Pool
from graphviz import Digraph
import random
from copy import copy, deepcopy

from matplotlib import cm


class ImportaPmo(object):
    # Classe contendo informacoes sobre os arquivos de entrada e saida
    caso = None
    dger = None
    npmc = 1

    # Define listas
    cadr_uh = []  # Lista com usinas hidraulicas do cadastro (HIDR.DAT)
    cadr_ut = []  # Lista com usinas termicas do cadastro (TERM.DAT)
    conf_ut = []  # Lista com usinas termicas da configuracao em estudo (CONFT.DAT)
    conf_uh = []  # Lista com usinas hidraulicas da configuracao em estudo (CONFHD.DAT)
    cfuturo = []  # Lista com funcoes de custo futuro obtidas pela PDE ou PDDE
    ree = []  # Lista com os reservatorios equivalentes de energia
    submercado = []  # Lista com os submercados
    intercambio = []  # Lista com intercambios entre submercados

    # Parametros Gerais
    ano_ini = 2018
    mes_ini = 12
    nanos = 5
    cdef = 4000
    mercado = 270
    ordmaxparp = 6

    def __init__(self, diretorio):

        # Leitura de arquivos
        self.caso = pmo(diretorio)
        self.caso.le_caso()

        self.cadr_uh = self.caso.le_hidr(self.cadr_uh)
        self.conf_uh = self.caso.le_confh(self.conf_uh, self.cadr_uh, self.nanos)
        self.cadr_ut = self.caso.le_term(self.cadr_ut)
        self.conf_ut = self.caso.le_conft(self.conf_ut, self.cadr_ut)
        self.conf_ut = self.caso.le_clast(self.conf_ut)
        self.conf_uh = self.caso.le_modif(self.conf_uh, self.ano_ini, self.nanos)
        self.conf_uh = self.caso.le_exph(self.conf_uh, self.ano_ini, self.nanos)
        self.ree = self.caso.le_ree(self.ree)
        # Cria Sistema
        self.dger = dadosgerais(self.nanos)
        self.submercado, self.intercambio, self.npmc = self.caso.le_sistema(self.submercado, self.intercambio,
                                                                            self.nanos, self.npmc)

        # Calcula produtibilidades acumuladas
        for iusina in self.conf_uh:
            iusina.ProdAcum(self.conf_uh)

        # Calcula Energias Armazenadas
        for ires in self.ree:
            ires.CalcEArmMax(self.conf_uh)
            ires.CalcENA(self.conf_uh)

        for isist in self.submercado:
            if isist.Ficticio == 0:
                isist.CalcEArmMax(self.conf_uh)
                isist.CalcENA(self.conf_uh)

    #############################################################################
    #############################################################################
    # Programacao Dinamica Estocastica Sequencial e Multiprocessing
    #############################################################################
    #############################################################################

    def pde(self, nr_discret, nr_estagios, nr_cenarios):

        t = timer()

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        # Define estados a serem visitados em cada estagio
        estados = []
        for i in range(nr_discret):
            estados.append(i / (nr_discret - 1))

        if nr_estagios > 12:
            print('Este exemplo didatico soh funciona para no maxima 12 estagios. Desculpe.')
            return

        # Cria Funcao objetivo, restricoes e inicializa rest. atend. dmenada
        objetivo = 0
        restricoes = []
        atendimentodemanda = 0

        # Cria variaveis de decisao Volume Final, Vertimento e Turbinamento
        vf = variable(len(self.conf_uh), 'vf')
        vv = variable(len(self.conf_uh), 'vv')
        vt = variable(len(self.conf_uh), 'vt')
        for i, iusina in enumerate(self.conf_uh):
            objetivo = objetivo + 0.001 * vv[i]
            # Limite inferior das variaveis hidraulicas
            restricoes.append(vf[i] >= iusina.VolMin)
            restricoes.append(vt[i] >= 0)
            restricoes.append(vv[i] >= 0)
            # Limite superior das variaveis hidraulicas
            restricoes.append(vf[i] <= iusina.VolMax)
            restricoes.append(vt[i] <= iusina.Engolimento)
            restricoes.append(vv[i] <= 100000)
            # Restricao de atendimento a demanda
            prod = float(iusina.Ro65[0][0])
            atendimentodemanda = atendimentodemanda + prod * vt[i]

        # Cria variaveis de decisao Geracao Termica
        gt = variable(len(self.conf_ut), 'gt')
        for i, iusina in enumerate(self.conf_ut):
            objetivo = objetivo + float(iusina.Custo[0]) * gt[i]
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + gt[i]
            # Limite inferior de gt
            restricoes.append(gt[i] >= 0)
            # Limite superior de gt
            restricoes.append(gt[i] <= iusina.Potencia)

        # Cria variaveis de decisao associadas ao deficit
        deficit = variable(1, 'deficit')
        objetivo = objetivo + self.cdef * deficit[0]
        restricoes.append(deficit >= 0)
        restricoes.append(deficit <= 100000)
        atendimentodemanda = atendimentodemanda + deficit[0]

        # Cria Variavel de decisao associada ao custo futuro
        alpha = variable(1, 'alpha')
        objetivo = objetivo + alpha[0]
        restricoes.append(alpha >= 0)
        restricoes.append(alpha <= 10000000)

        restricoes.append(atendimentodemanda == self.mercado)

        # Calcula funcoes objetivos por estado
        for imes in range(nr_estagios, 0, -1):  # Loop de estagio
            print('###############', imes)

            # Cria Função de Custo Futuro Vazia Associada ao Estagio (imes)
            self.cfuturo.append(fcf(imes))

            if len(self.cfuturo) > 1:
                rest_cortes = self.cfuturo[len(self.cfuturo) - 2].get_fcf(vf, alpha)
            else:
                rest_cortes = []

            apontador = len(restricoes)

            # Gera discretizacoes
            discret = product(estados, repeat=len(self.conf_uh))
            for idisc, idiscret in enumerate(discret):  # Loop de discretizacao
                # Inicializa volumes (estados) das usinas correspondentes a iteracao corrente
                VI = matrix(0, (len(self.conf_uh), 1), 'd')
                LAMBDA = matrix(0, (len(self.conf_uh), 1), 'd')
                CUSTO = 0
                for i, iusina in enumerate(self.conf_uh):
                    VI[i] = iusina.VolMin + iusina.VolUtil * idiscret[i]
                    for icen in range(1, nr_cenarios + 1):  # Loop de cenario
                        AFL = matrix(0, (len(self.conf_uh), 1), 'd')
                        for i, iusina in enumerate(self.conf_uh):
                            AFL[i] = float(iusina.Vazoes[icen - 1][imes - 1])
                            restricoes.append(vf[i] == VI[i] + 2.592 * AFL[i] - 2.592 * vt[i] - 2.592 * vv[i])

                        todas = self.reuni(restricoes, rest_cortes)
                        problema = op(objetivo, todas)

                        problema.solve('dense', 'glpk')

                        if problema.status == 'optimal':
                            for i, iusina in enumerate(self.conf_uh):
                                LAMBDA[i] = LAMBDA[i] + todas[apontador + i].multiplier.value
                            CUSTO = CUSTO + problema.objective.value()[0]
                            for i, iusina in enumerate(self.conf_uh):
                                CUSTO = CUSTO - vv[i].value() * 0.001
                        else:
                            print('oops')
                            print(problema.status)
                            problema.tofile('andre.mps')
                            return

                        # Apaga restricoes de Balanco Hidrico
                        ultimo = len(restricoes) - 1
                        for i, iusina in enumerate(self.conf_uh):
                            del restricoes[ultimo]
                            ultimo = ultimo - 1

                    self.cfuturo[len(self.cfuturo) - 1].add_corte(LAMBDA, CUSTO, VI, nr_cenarios)

            # self.plota_corte(imes, nr_discret)
        print(timer() - t)

    def reuni(self, restricoes, rest_cortes):
        tudo = []
        for i in range(0, len(restricoes)):
            tudo.append(restricoes[i])
        for i in range(0, len(rest_cortes)):
            tudo.append(rest_cortes[i])
        return tudo

    def pde_par(self, nr_discret, nr_estagios, nr_cenarios):

        t = timer()

        solvers.options['show_progress'] = False
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        # Define estados a serem visitados em cada estagio
        estados = []
        for i in range(nr_discret):
            estados.append(i / (nr_discret - 1))

        if nr_estagios > 12:
            print('Este exemplo didatico soh funciona para no maxima 12 estagios. Desculpe.')
            return

        # Cria Funcao objetivo, restricoes e inicializa rest. atend. dmenada
        objetivo = 0
        restricoes = []
        atendimentodemanda = 0

        # Cria variaveis de decisao Volume Final, Vertimento e Turbinamento
        vf = variable(len(self.conf_uh), 'vf')
        vv = variable(len(self.conf_uh), 'vv')
        vt = variable(len(self.conf_uh), 'vt')
        for i, iusina in enumerate(self.conf_uh):
            objetivo = objetivo + 0.001 * vv[i]
            # Limite inferior das variaveis hidraulicas
            restricoes.append(vf[i] >= iusina.VolMin)
            restricoes.append(vt[i] >= 0)
            restricoes.append(vv[i] >= 0)
            # Limite superior das variaveis hidraulicas
            restricoes.append(vf[i] <= iusina.VolMax)
            restricoes.append(vt[i] <= iusina.Engolimento)
            restricoes.append(vv[i] <= 100000)
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + iusina.Ro65 * vt[i]

        # Cria variaveis de decisao Geracao Termica
        gt = variable(len(self.conf_ut), 'gt')
        for i, iusina in enumerate(self.conf_ut):
            objetivo = objetivo + float(iusina.Custo[0]) * gt[i]
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + gt[i]
            # Limite inferior de gt
            restricoes.append(gt[i] >= 0)
            # Limite superior de gt
            restricoes.append(gt[i] <= iusina.Potencia)

        # Cria variaveis de decisao associadas ao deficit
        deficit = variable(1, 'deficit')
        objetivo = objetivo + self.cdef * deficit[0]
        restricoes.append(deficit >= 0)
        restricoes.append(deficit <= 100000)
        atendimentodemanda = atendimentodemanda + deficit[0]

        # Cria Variavel de decisao associada ao custo futuro
        alpha = variable(1, 'alpha')
        objetivo = objetivo + alpha[0]
        restricoes.append(alpha >= 0)
        restricoes.append(alpha <= 10000000)

        restricoes.append(atendimentodemanda == self.mercado)

        # Calcula funcoes objetivos por estado
        for imes in range(nr_estagios, 0, -1):  # Loop de estagio
            print('###############', imes)

            # Cria Função de Custo Futuro Vazia Associada ao Estagio (imes)
            self.cfuturo.append(fcf(imes))

            if len(self.cfuturo) > 1:
                rest_cortes = self.cfuturo[len(self.cfuturo) - 2].get_fcf(vf, alpha)
            else:
                rest_cortes = []

            apontador = len(restricoes)

            # Gera discretizacoes
            discret = product(estados, repeat=len(self.conf_uh))
            C = list(discret)  # Loop de discretizacao

            parametros = {'Sist': self,
                          'nr_cenarios': nr_cenarios,
                          'imes': imes,
                          'restricoes': restricoes,
                          'rest_cortes': rest_cortes,
                          'objetivo': objetivo,
                          'apontador': apontador,
                          'vv': vv,
                          'vt': vt,
                          'vf': vf}

            # self.TaskFcn( parametros, C[0] )
            pool = Pool(processes=4)

            funcao = partial(self.TaskFcn, param=parametros)

            # Resolve com multiprocessing
            res = pool.map(funcao, C)
            # res = map(funcao, C)

            for solucao in res:
                LAMBDA = solucao[2]
                CUSTO = solucao[1]
                VI = solucao[3]
                self.cfuturo[len(self.cfuturo) - 1].add_corte(LAMBDA, CUSTO, VI, nr_cenarios)

            # self.plota_corte(imes, nr_discret)

        print(timer() - t)

    def TaskFcn(self, C, param):

        idiscret = C
        nr_cenarios = param['nr_cenarios']
        sist = param['Sist']
        imes = param['imes']
        restricoes = param['restricoes']
        rest_cortes = param['rest_cortes']
        objetivo = param['objetivo']
        apontador = param['apontador']
        vv = param['vv']
        vt = param['vt']
        vf = param['vf']

        # Inicializa volumes (estados) das usinas correspondentes a iteracao corrente
        VI = matrix(0, (len(sist.conf_uh), 1), 'd')
        LAMBDA = matrix(0, (len(sist.conf_uh), 1), 'd')
        CUSTO = 0
        for i, iusina in enumerate(sist.conf_uh):
            VI[i] = iusina.VolMin + iusina.VolUtil * idiscret[i]
            for icen in range(1, nr_cenarios + 1):  # Loop de cenario
                AFL = matrix(0, (len(sist.conf_uh), 1), 'd')
                for i, iusina in enumerate(sist.conf_uh):
                    AFL[i] = float(iusina.Vazoes[icen - 1][imes - 1])
                    restricoes.append(vf[i] == VI[i] + 2.592 * AFL[i] - 2.592 * vt[i] - 2.592 * vv[i])

                todas = sist.reuni(restricoes, rest_cortes)
                problema = op(objetivo, todas)

                problema.solve('dense', 'glpk')

                if problema.status == 'optimal':
                    for i, iusina in enumerate(sist.conf_uh):
                        LAMBDA[i] = LAMBDA[i] + todas[apontador + i].multiplier.value
                    CUSTO = CUSTO + problema.objective.value()[0]
                    for i, iusina in enumerate(sist.conf_uh):
                        CUSTO = CUSTO - vv[i].value() * 0.001
                else:
                    print('oops')
                    print(problema.status)
                    problema.tofile('andre.mps')
                    return

                # Apaga restricoes de Balanco Hidrico
                ultimo = len(restricoes) - 1
                for i, iusina in enumerate(sist.conf_uh):
                    del restricoes[ultimo]
                    ultimo = ultimo - 1
        return idiscret, CUSTO, LAMBDA, VI

    ####################################################################
    ####################################################################
    # Plotagens Diversas
    ####################################################################
    ####################################################################

    def plota_corte(self, imes, nr_discret):
        for i, ifcf in enumerate(self.cfuturo):
            if ifcf.estagio == imes:
                if len(self.conf_uh) == 1:
                    fig, ax = plt.subplots(figsize=(8, 8))
                    volumes = np.linspace(self.conf_uh[0].VolMin, self.conf_uh[0].VolMax, nr_discret)
                    maior = 0
                    for i in range(0, ifcf.nr_cortes):
                        plt.plot(volumes, (ifcf.coef_vf[i] * volumes + ifcf.termo_i[i]).transpose(), 'b-', lw=3)
                        a = ifcf.coef_vf[i]
                        b = ifcf.termo_i[i]
                        custo = np.array(a * volumes + b)
                        custo.shape = (nr_discret,)
                        if max(custo) > maior:
                            maior = max(custo)
                        plt.fill_between(volumes, 0, custo, facecolor='blue', alpha=0.1)

                    plt.xlabel('Volume Inicial (hm^3)', fontsize=16)
                    titulo = 'Funcao de Custo Futuro do Mes ' + str(imes)
                    plt.title(titulo, fontsize=16)
                    plt.ylabel('Custo (R$)', fontsize=16)
                    plt.xlim(self.conf_uh[0].VolMin, self.conf_uh[0].VolMax)
                    # plt.ylim(0,max(ifcf.termo_i))
                    plt.ylim(0, maior)
                    plt.show()
                    return
                else:
                    print('Somente imprime fcf se existir apenas 1 uh')

    # Plota Usinas Não Existentes e Existentes em Expansao
    def Plota_Expansao_Uh(self):

        # Conta quantas usinas estao
        cont = 0
        nomes = []
        for usina in self.conf_uh:
            if usina.Status == 'EE' or usina.Status == 'NE':
                cont += 1
                nomes.append(usina.Nome)

        motorizada = np.zeros(cont)
        vazia = np.zeros(cont)
        enchendo = np.zeros(cont)
        submotorizada = np.zeros(cont)

        ind = np.arange(cont)
        cont = 0
        for usina in self.conf_uh:
            if usina.Status == 'EE' or usina.Status == 'NE':
                # Meses em que a usina esta motorizada
                motorizada[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusMotoriz - 2)

                # Meses que a usina ainda nao iniciou o enchimento do volume morto
                vazia[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusVolMorto)

                # Meses que a usina encontra-se enchendo o volume morto
                enchendo[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusVolMorto - 1)

                # Meses que a usina encontra-se motorizando
                submotorizada[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusMotoriz - 1)

                cont += 1

        width = 0.35  # the width of the bars: can also be len(x) sequence

        ax = plt.axes()
        p1 = plt.barh(ind, vazia, width, color='w')
        p2 = plt.barh(ind, enchendo, width, color='lime', left=vazia)
        p3 = plt.barh(ind, submotorizada, width, color='sienna', left=vazia + enchendo)
        p4 = plt.barh(ind, motorizada, width, color='black', left=vazia + enchendo + submotorizada)

        plt.ylabel('Usinas', fontsize=16)
        plt.title('Usinas Hidreletricas em Expansao', fontsize=16)
        plt.yticks(ind, nomes, fontsize=12)
        plt.xticks(np.arange(0, self.nanos * 12 + 2, 12))
        # plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Nao Entrou', 'Enchendo Vol. Morto', 'Submotorizada', 'Motorizada'),
                   fontsize=12)
        plt.xlabel('Meses do Estudo', fontsize=16)
        ax.xaxis.grid()

        plt.show()

    # Plota Mercado de Todos os Submercados
    def PlotaMercado(self):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.submercado[0].Mercado) - 1
        nr_col = len(self.submercado[0].Mercado[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for mercado in self.submercado:
            if mercado.Ficticio == 0:
                if mercado.Codigo == 1:
                    cor = 'lime'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 2:
                    cor = 'blue'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 3:
                    cor = 'chocolate'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 4:
                    cor = 'black'
                    linha = '-'
                    LineWidth = 3
                else:
                    cor = 'orange'
                y = np.arange(1, nr_lin * nr_col + 1)
                y = mercado.Mercado[0:nr_lin][0:nr_col]
                ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                        lw=LineWidth, label=mercado.Nome)
                ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                                (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
                total += y

        titulo = 'Evolucao da Demanda Total do Sistema'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Demanda de Energia (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    # Plota Energia Armazenada Maxima de Todos REEs
    def PlotaEArmMaxRee(self):

        f, (ax) = plt.subplots(1, 1)
        nr_lin = len(self.ree[0].EArmMax)
        nr_col = len(self.ree[0].EArmMax[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for ree in self.ree:
            linha = '--'
            LineWidth = 2
            if ree.Codigo == 0:
                cor = 'lime'
            elif ree.Codigo == 1:
                cor = 'blue'
            elif ree.Codigo == 2:
                cor = 'chocolate'
            elif ree.Codigo == 3:
                cor = 'darkgreen'
            elif ree.Codigo == 4:
                cor = 'fuchsia'
            elif ree.Codigo == 5:
                cor = 'gold'
            elif ree.Codigo == 6:
                cor = 'maroon'
            elif ree.Codigo == 7:
                cor = 'orangered'
            elif ree.Codigo == 8:
                cor = 'orchid'
            elif ree.Codigo == 9:
                cor = 'violet'
            elif ree.Codigo == 10:
                cor = 'yellowgreen'
            elif ree.Codigo == 11:
                cor = 'tan'
            else:
                cor = 'black'

            y = np.arange(1, nr_lin * nr_col + 1)
            y = ree.EArmMax[0:nr_lin][0:nr_col]
            ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                    lw=LineWidth, label=ree.Nome)
            ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                            (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
            total += y

        titulo = 'Evolução da Energia Armazenada Máxima \n Por Reservatorio Equivalente de Energia'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armazenada Maxima (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    # Plota Energia Armazenada Maxima de Todos Submercados
    def PlotaEArmMaxSist(self):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.submercado[0].Mercado) - 1
        nr_col = len(self.submercado[0].Mercado[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for mercado in self.submercado:
            if mercado.Ficticio == 0:
                linha = '--'
                LineWidth = 2
                if mercado.Codigo == 1:
                    cor = 'lime'
                elif mercado.Codigo == 2:
                    cor = 'blue'
                elif mercado.Codigo == 3:
                    cor = 'chocolate'
                elif mercado.Codigo == 4:
                    cor = 'darkgreen'
                else:
                    cor = 'acqua'

                y = np.arange(1, nr_lin * nr_col + 1)
                y = mercado.EArmMax[0:nr_lin][0:nr_col]
                ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                        lw=LineWidth, label=mercado.Nome)
                ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                                (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
                total += y

        titulo = 'Evolução da Energia Armazenada Máxima \n Por Submercado'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armazenada Maxima (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()


class Classroom(object):

    sistema = None

    def __init__(self):
        lista_uhe = []

        usina = {
            "Nome": "UHE DO MARCATO",  # Nome da Usina
            "Vmax": 100.,  # Volume Máximo em hm^3
            "Vmin": 20.,  # Volume Mínimo em hm^3
            "VI": 65.,
            "Prod": 0.95,  # Produtibilidade em MWmed/hm^3
            "Engol": 60.,  # Engolimento Máximo em hm^3
            "Afl": [  # Cenários de Afluências (linha: Estágio, coluna: cenário)
                    [23, 16],
                    [19, 14],
                    [15, 11]
                   ]
        }

        lista_uhe.append(usina)

        #
        # Retirar os comentários abaixo para considerar 2 UHEs
        #
        #usina2 = {
        #    "Nome": "UHE DO VASCAO",
        #    "Vmax": 200.,
        #    "Vmin": 40.,
        #    "VI": 80,
        #    "Prod": 0.85,
        #    "Engol": 100.,
        #    "Afl": [
        #            [ 46, 32],
        #            [ 38, 28],
        #            [ 30, 22]
        #    ]
        # }
        #lista_uhe.append(usina2)

        usina = {
            "Nome": "GT_1",  # Nome da Usina Térmica 1
            "Capac": 15.,  # Capacidade Máxima de Geração MWMed
            "Custo": 10.  # Custo de Operação $/MWMed
        }

        lista_ute = []

        lista_ute.append(usina)

        usina = {
            "Nome": "GT_2",  # Nome da Usina Térmica 2
            "Capac": 10.,  # Capacidade Máxima de Geração MWmed
            "Custo": 25.  # Custo de Operação $/MWMed
        }

        lista_ute.append(usina)

        #
        # d_gerais para o caso 1 UHE
        #
        d_gerais = {
            "CDef": 500.,  # Custo de Déficit $/MWMed
            "Carga": [50., 50., 50.],  # Lista com carga a ser atendida por estágio
            "Nr_Disc": 3,  # Número de Discretizações
            "Nr_Est": 3,  # Número de Estágios
            "Nr_Cen": 2  # Número de Cenários de Afluências
        }

        #
        # d_gerais para o caso 2 UHE (Comentar o bloco acima e descomentar o bloco abaixo)
        #
        #d_gerais = {
        #    "CDef": 500.,
        #    "Carga": [ 100, 100., 100],
        #    "Nr_Disc": 5,
        #    "Nr_Est": 3,
        #    "Nr_Cen": 2
        # }

        #
        # Cria dicionário de dados com todas as informações do sistema em estudo
        #
        self.sistema = {
            "DGer": d_gerais,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

    def despacho_pdd(self, VI, VF, AFL, custofuturo, iest, imprime):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Cria Variáveis de Decisão
        #

        vt = variable(Num_UHE, "Volume Turbinado na Usina")
        vv = variable(Num_UHE, "Volume Vertido na Usina")
        gt = variable(Num_UTE, "Geração na Usina Térmica")
        deficit = variable(1, "Déficit de Energia no Sistema")

        # Construção da Função Objetivo

        fob = 0

        for i, iusi in enumerate(self.sistema["UTE"]):
            fob += iusi['Custo'] * gt[i]

        fob += self.sistema["DGer"]["CDef"] * deficit[0]

        for i, iusi in enumerate(self.sistema["UHE"]):
            fob += 0.01 * vv[i]

        # Definição das Restrições

        restricoes = []

        # Balanço Hídrico

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(float(VF[i]) == float(VI[i]) + float(AFL[i]) - vt[i] - vv[i])

        # Atendimento à Demanda

        AD = 0

        for i, usi in enumerate(self.sistema["UHE"]):
            AD += iusi["Prod"] * vt[i]

        for i, usi in enumerate(self.sistema["UTE"]):
            AD += gt[i]

        AD += deficit[0]

        restricoes.append(AD == self.sistema["DGer"]["Carga"][iest])

        # Restricoes Canalização

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vt[i] >= 0)
            restricoes.append(vt[i] <= iusi["Engol"])
            restricoes.append(vv[i] >= 0)

        for i, iusi in enumerate(self.sistema["UTE"]):
            restricoes.append(gt[i] >= 0)
            restricoes.append(gt[i] <= iusi["Capac"])

        restricoes.append(deficit[0] >= 0)

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        if problema.status == 'optimal':  # Tem água para ir de VI a VF

            #
            # Armazena resultados do problema em um dicionário de dados
            #

            Dger = {
                "Deficit": deficit[0].value()[0],
                "CustoTotal": fob.value()[0] + custofuturo,
                "CustoFut": custofuturo,
                "CMO": restricoes[Num_UHE].multiplier.value[0]
            }

            lista_uhe = []
            for i, iusi in enumerate(self.sistema["UHE"]):
                resultado = {
                    "vf": VF[i],
                    "vt": vt[i].value()[0],
                    "vv": vv[i].value()[0],
                    "cma": restricoes[i].multiplier.value[0]
                }
                lista_uhe.append(resultado)

            lista_ute = []
            for i, iusi in enumerate(self.sistema["UTE"]):
                resultado = {
                    "gt": gt[i].value()[0]
                }
                lista_ute.append(resultado)

        else:  # Não tem água para ir de VI a VF
            Dger = {
                "Deficit": 0,
                "CustoTotal": np.inf,
                "CustoFut": custofuturo,
                "CMO": np.inf
            }
            lista_uhe = []
            lista_ute = []

        resultado = {
            "DGer": Dger,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        #
        # Imprime resultados em tela
        #

        if imprime and (problema.status == 'optimal'):
            print("Custo Total:", fob.value())

            for i, usi in enumerate(self.sistema["UHE"]):
                print(vt.name, i, "é", vt[i].value(), "hm3")
                print(vv.name, i, "é", vv[i].value(), "hm3")

            for i, usi in enumerate(self.sistema["UTE"]):
                print(gt.name, i, "é", gt[i].value(), "MWmed")

            print(deficit.name, "é", deficit[0].value(), "MWmed")

            print("----- x ------ ")

        #
        # Retorna da função exportando os resultados
        #

        return resultado

    def pdd(self, cenario, imprime):

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Calcula o tamanho do passo percentual (distância entre cada discretização)
        #

        passo = 100 / (self.sistema["DGer"]["Nr_Disc"] - 1)

        #
        # Calcula um iterator com todas as combinações possíveis
        #

        discretizacoes = product(np.arange(0, 100 + passo, passo), repeat=Num_UHE)

        #
        # Transforma o iterator em uma lista
        #

        discretizacoes = list(discretizacoes)

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        #
        # Laço ou Loop mais externo de estágios (de trás para frente ou backward)
        #
        arvore = []
        for iest in np.arange(self.sistema["DGer"]["Nr_Est"], 0, -1):

            #
            # Pega cenário de afluencia do estágio
            #

            AFL = []
            for i, iusi in enumerate(self.sistema["UHE"]):
                AFL.append(iusi["Afl"][iest - 1][cenario])

            #
            # Laço ou loop intermediário (percorre todas as discretizações para cada
            # Estágio)
            #
            for disc_atual in discretizacoes:
                #
                # Conforme for a discretização calcula o VI (Volume Inicial) em hm^3
                # para cada UHE
                #
                VI = []
                for i, iusi in enumerate(self.sistema["UHE"]):
                    VI.append(iusi["Vmin"] + (iusi["Vmax"] - iusi["Vmin"]) * disc_atual[i] / 100)

                #
                # Laço ou loop mais interno. Varre todos os cenários para cada discretização
                #
                todos = []
                menor = np.inf
                posicao_menor = 99999
                posicao = 0
                for disc_futura in discretizacoes:
                    #
                    # Conforme for a discretização futura calcula o VF (Volume Inicial) em hm^3
                    # para cada UHE
                    #
                    VF = []
                    for i, iusi in enumerate(self.sistema["UHE"]):
                        VF.append(iusi["Vmin"] + (iusi["Vmax"] - iusi["Vmin"]) * disc_futura[i] / 100)

                    #
                    # Encontra Custu Futuro associado a disc_futura
                    #
                    CustoFuturo = 0
                    for folha in arvore:
                        if (folha["VI"] == VF) and (folha["Est"] == iest):
                            CustoFuturo = folha["Dger"]["CustoTotal"]

                    #
                    # Chama função de despacho hidrotérmico
                    #
                    resultado = self.despacho_pdd(VI, VF, AFL, CustoFuturo, iest - 1, imprime)
                    todos.append([iest - 1, VI, VF, resultado])
                    if (resultado["DGer"]["CustoTotal"] < menor):
                        menor = resultado["DGer"]["CustoTotal"]
                        posicao_menor = posicao
                    posicao += 1
                melhor = {
                    "Est": todos[posicao_menor][0],
                    "VI": todos[posicao_menor][1],
                    "VF": todos[posicao_menor][2],
                    "Dger": todos[posicao_menor][3]["DGer"],
                    "UHE": todos[posicao_menor][3]["UHE"],
                    "UTE": todos[posicao_menor][3]["UTE"]
                }
                arvore.append(melhor)
        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido na PDD", time.time() - t)

        # for folha in arvore:
        # print(folha)

        #
        # A parir dos Volumes Iniciais das UHEs, é obtida a estratégia operativa para
        # todo o período de planejamento. Ao mesmo tempo, é preparado o dicionário de
        # dados resultado com o mesmo formato do algoritmo pl_unico desenvolvido na
        # aula anterior
        #

        #
        # A condição inicial deve ser levada para uma das discretizações em cada UHE
        # Por exemplo, se as discretizações são 20hm^3, 60hm^3 e 100hm^3 e o volume
        # inicial da UHE é de 65hm^3, ele deve ser considerado como 60hm^3 pois é a
        # discretização viável mais próxima
        #

        Cond_Inicial = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            if iusi["VI"] < iusi["Vmax"]:
                for idisc in np.arange(0, 100 + passo, passo):
                    vdisc = iusi["Vmin"] + (iusi["Vmax"] - iusi["Vmin"]) * idisc / 100
                    if vdisc > iusi["VI"]:
                        Cond_Inicial.append(iusi["Vmin"] + (iusi["Vmax"] - iusi["Vmin"]) * (idisc - passo) / 100)
                        break
            else:
                Cond_Inicial.append(iusi["Vmax"])

        #
        # Inicializa listas com as variáveis de decisão que serão preenchidas
        # com as informações dos diferentes estágios
        #

        vf = []
        vt = []
        vv = []
        cma = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            vf.append([])
            vt.append([])
            vv.append([])
            cma.append([])
        gt = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            gt.append([])

        cmo = []
        deficit = []
        custo_total = 0.

        #
        # Preenche listas
        #
        for iest in range(0, self.sistema["DGer"]["Nr_Est"]):
            for folha in arvore:
                if (folha["Est"] == iest) and (folha["VI"] == Cond_Inicial):
                    for i in range(Num_UHE):
                        vf[i].append(folha["UHE"][i]["vf"])
                        vt[i].append(folha["UHE"][i]["vt"])
                        vv[i].append(folha["UHE"][i]["vv"])
                        cma[i].append(folha["UHE"][i]["cma"])
                    for i in range(Num_UTE):
                        gt[i].append(folha["UTE"][i]["gt"])
                    cmo.append(folha["Dger"]["CMO"])
                    deficit.append(folha["Dger"]["Deficit"])
                    custo_total += folha["Dger"]["CustoTotal"] - folha["Dger"]["CustoFut"]
                    Cond_Inicial = folha["VF"]
                    break

        #
        # Monta lista_uhe
        #
        lista_uhe = []
        for i in range(Num_UHE):
            elemento = {
                "vf": vf[i],
                "vt": vt[i],
                "vv": vv[i],
                "cma": cma[i]
            }
            lista_uhe.append(elemento)

        #
        # Monta lista_ute
        #
        lista_ute = []
        for i in range(Num_UTE):
            elemento = {
                "gt": gt[i],
            }
            lista_ute.append(elemento)

        #
        # Preenche dicionário de dados com a saída
        #
        resultado = {
            "DGer": {
                "CustoTotal": custo_total,
                "CMO": cmo,
                "Deficit": deficit
            },
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        return resultado

    def pl_unico(self, cenario, imprime):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        #
        # Cria função de despacho hidrotérmico
        #

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Cria Variáveis de Decisão Organizadas Matricialmente
        # Exemplo de acesso à variável de decisão de volume final
        # vf[usina][estagio]
        #

        vf = []
        vt = []
        vv = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            vf.append(variable(self.sistema["DGer"]["Nr_Est"], "Volume Final na Usina " + iusi["Nome"]))
            vt.append(variable(self.sistema["DGer"]["Nr_Est"], "Volume Turbinado na Usina " + iusi["Nome"]))
            vv.append(variable(self.sistema["DGer"]["Nr_Est"], "Volume Vertido na Usina " + iusi["Nome"]))
        gt = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            gt.append(variable(self.sistema["DGer"]["Nr_Est"], "Geração na Usina Térmica " + iusi["Nome"]))
        deficit = variable(self.sistema["DGer"]["Nr_Est"], "Déficit de Energia no Sistema")

        #
        # Construção da Função Objetivo
        #

        fob = 0

        for i_est in range(self.sistema["DGer"]["Nr_Est"]):
            for i, iusi in enumerate(self.sistema["UTE"]):
                fob += iusi['Custo'] * gt[i][i_est]

            fob += self.sistema["DGer"]["CDef"] * deficit[i_est]

            for i, iusi in enumerate(self.sistema["UHE"]):
                fob += 0.01 * vv[i][i_est]

        #
        # Definição das Restrições
        #

        restricoes = []

        #
        # Balanço Hídrico
        #

        for i, iusi in enumerate(self.sistema["UHE"]):
            for i_est in range(self.sistema["DGer"]["Nr_Est"]):
                if i_est == 0:
                    restricoes.append(
                        vf[i][i_est] == float(iusi["VI"]) + float(iusi["Afl"][i_est][cenario]) - vt[i][i_est] - vv[i][
                            i_est])
                else:
                    restricoes.append(
                        vf[i][i_est] == vf[i][i_est - 1] + float(iusi["Afl"][i_est][cenario]) - vt[i][i_est] - vv[i][
                            i_est])

                    #
        # Atendimento à Demanda
        #

        for i_est in range(self.sistema["DGer"]["Nr_Est"]):
            AD = 0
            for i, iusi in enumerate(self.sistema["UHE"]):
                AD += iusi["Prod"] * vt[i][i_est]
            for i, usi in enumerate(self.sistema["UTE"]):
                AD += gt[i][i_est]
            AD += deficit[i_est]
            restricoes.append(AD == self.sistema["DGer"]["Carga"][i_est])

        #
        # Restricoes Canalização
        #

        for i_est in range(self.sistema["DGer"]["Nr_Est"]):
            for i, iusi in enumerate(self.sistema["UHE"]):
                restricoes.append(vf[i][i_est] >= iusi["Vmin"])
                restricoes.append(vf[i][i_est] <= iusi["Vmax"])
                restricoes.append(vt[i][i_est] >= 0)
                restricoes.append(vt[i][i_est] <= iusi["Engol"])
                restricoes.append(vv[i][i_est] >= 0)
            for i, iusi in enumerate(self.sistema["UTE"]):
                restricoes.append(gt[i][i_est] >= 0)
                restricoes.append(gt[i][i_est] <= iusi["Capac"])
            restricoes.append(deficit[i_est] >= 0)

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido na PL Único", time.time() - t)

        #
        # Prepara dicionário de dados com resultados
        #

        lista_uhe = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            pula = i * self.sistema["DGer"]["Nr_Est"]
            cma = []
            volf = []
            volt = []
            volv = []
            for iest in range(self.sistema["DGer"]["Nr_Est"]):
                cma.append(restricoes[pula + i_est].multiplier.value[0])
                volf.append(vf[i][iest].value()[0])
                volt.append(vt[i][iest].value()[0])
                volv.append(vv[i][iest].value()[0])
            elemento = {
                "vf": volf,
                "vt": volt,
                "vv": volv,
                "cma": cma
            }
            lista_uhe.append(elemento)

        lista_ute = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            gerter = []
            for iest in range(self.sistema["DGer"]["Nr_Est"]):
                gerter.append(gt[i][iest].value()[0])
            elemento = {
                "gt": gerter,
            }
            lista_ute.append(elemento)

        pula = Num_UHE * self.sistema["DGer"]["Nr_Est"]
        cmo = []
        lista_deficit = []
        for i_est in range(self.sistema["DGer"]["Nr_Est"]):
            cmo.append(restricoes[pula + i_est].multiplier.value[0])
            lista_deficit.append(deficit[i_est].value()[0])

        Dger = {
            "CustoTotal": fob.value()[0],
            "CMO": cmo,
            "Deficit": lista_deficit
        }

        resultado = {
            "DGer": Dger,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        #
        # Imprime resultados em tela
        #

        if imprime:
            print("Custo de Operação de Todos os estágios:", fob.value())

            print("Volume Final por UHE em cada Estágio em (hm^3) ")
            for i, usi in enumerate(self.sistema["UHE"]):
                print(vf[i])
                print(vt[i])
                print(vv[i])

            print("Geração por UTE em cada Estágio em (MWMed)")
            for i, usi in enumerate(self.sistema["UTE"]):
                print(gt[i])

            print("Déficit de Energia em cada Estágio em (MWMed)")
            print(deficit)

            print("----- x ------ ")

        return resultado

    def despacho_pddd(self, VI, AFL, pote_de_corte, iest, imprime):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Cria Variáveis de Decisão
        #

        vf = variable(Num_UHE, "Volume Final na Usina")
        vt = variable(Num_UHE, "Volume Turbinado na Usina")
        vv = variable(Num_UHE, "Volume Vertido na Usina")
        gt = variable(Num_UTE, "Geração na Usina Térmica")
        deficit = variable(1, "Déficit de Energia no Sistema")
        alpha = variable(1, "Custo Futuro")

        # Construção da Função Objetivo

        fob = 0

        for i, iusi in enumerate(self.sistema["UTE"]):
            fob += iusi['Custo'] * gt[i]

        fob += self.sistema["DGer"]["CDef"] * deficit[0]

        for i, iusi in enumerate(self.sistema["UHE"]):
            fob += 0.01 * vv[i]

        fob += 1.0 * alpha[0]

        # Definição das Restrições

        restricoes = []

        # Balanço Hídrico

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] == float(VI[i]) + float(AFL[i]) - vt[i] - vv[i])

        # Atendimento à Demanda

        AD = 0

        for i, iusi in enumerate(self.sistema["UHE"]):
            AD += iusi["Prod"] * vt[i]

        for i, usi in enumerate(self.sistema["UTE"]):
            AD += gt[i]

        AD += deficit[0]

        restricoes.append(AD == self.sistema["DGer"]["Carga"][iest - 1])

        # Restricoes Canalização

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] >= iusi["Vmin"])
            restricoes.append(vf[i] <= iusi["Vmax"])
            restricoes.append(vt[i] >= 0)
            restricoes.append(vt[i] <= iusi["Engol"])
            restricoes.append(vv[i] >= 0)

        for i, iusi in enumerate(self.sistema["UTE"]):
            restricoes.append(gt[i] >= 0)
            restricoes.append(gt[i] <= iusi["Capac"])

        restricoes.append(deficit[0] >= 0)

        restricoes.append(alpha[0] >= 0)

        #
        # Insere inequações correspondentes aos cortes
        #

        for icorte in pote_de_corte:
            if icorte['Estagio'] == iest:
                equacao = 0
                for iusi in range(Num_UHE):
                    equacao += float(icorte['Coefs'][iusi]) * vf[iusi]
                equacao += float(icorte['Termo_Indep'])
                restricoes.append(alpha[0] >= equacao)

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        #
        # Armazena resultados do problema em um dicionário de dados
        #

        Dger = {
            "Deficit": deficit[0].value()[0],
            "CMO": restricoes[Num_UHE].multiplier.value[0],
            "CustoTotal": fob.value()[0],
            "CustoFuturo": alpha[0].value()[0]
        }

        lista_uhe = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            resultado = {
                "vf": vf[i].value()[0],
                "vt": vt[i].value()[0],
                "vv": vv[i].value()[0],
                "cma": restricoes[i].multiplier.value[0]
            }
            lista_uhe.append(resultado)

        lista_ute = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            resultado = {
                "gt": gt[i].value()[0]
            }
            lista_ute.append(resultado)

        resultado = {
            "DGer": Dger,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        #
        # Imprime resultados em tela
        #

        if imprime:
            print("Custo Total:", fob.value())

            for i, usi in enumerate(self.sistema["UHE"]):
                print(vf.name, i, "é", vf[i].value(), "hm3")
                print(vt.name, i, "é", vt[i].value(), "hm3")
                print(vv.name, i, "é", vv[i].value(), "hm3")

            for i, usi in enumerate(self.sistema["UTE"]):
                print(gt.name, i, "é", gt[i].value(), "MWmed")

            print(deficit.name, "é", deficit[0].value(), "MWmed")

            print(alpha.name, "é", alpha[0].value(), "$")

            for i, iusi in enumerate(self.sistema["UHE"]):
                print("O valor da água na usina", i, "é: ", restricoes[i].multiplier.value)

            print("O Custo Marginal de Operação é: ", restricoes[Num_UHE].multiplier.value)

            print("----- x ------ ")

        #
        # Retorna da função exportando os resultados
        #

        return resultado

    def pddd(self, cenario, imprime):

        Num_UHE = len(self.sistema["UHE"])
        Num_UTE = len(self.sistema["UTE"])

        #
        # Esta é uma lista com dicionários contendo todos os cortes criados
        # Inicia vazia
        #

        pote_de_corte = []

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        tol = 0.01
        iteracao = 0
        ZINF = [0.]
        ZSUP = [np.inf]

        while np.abs(ZSUP[iteracao] - ZINF[iteracao]) > tol:
            #
            # Forward - Laço ou Loop direto de estágios (do início para o fim)
            #
            memoria = []
            ZSUP[iteracao] = 0.
            for iest in range(self.sistema["DGer"]["Nr_Est"]):
                VI = []
                if iest == 0:
                    for i, iusi in enumerate(self.sistema["UHE"]):
                        VI.append(iusi["VI"])
                else:
                    for i, iusi in enumerate(resultado["UHE"]):
                        VI.append(iusi["vf"])
                AFL = []
                for i, iusi in enumerate(self.sistema["UHE"]):
                    AFL.append(iusi["Afl"][iest][cenario])
                #
                # Chama função de despacho hidrotérmico
                #
                resultado = self.despacho_pddd(VI, AFL, pote_de_corte, iest + 1, imprime)
                #if iteracao == 1:
                #    print(iest, resultado)
                ZSUP[iteracao] += resultado["DGer"]["CustoTotal"] - resultado["DGer"]["CustoFuturo"]
                if iest == 0:
                    ZINF[iteracao] = resultado["DGer"]["CustoTotal"]
                memoria.append(resultado)

            if np.abs(ZSUP[iteracao] - ZINF[iteracao]) <= tol:
                break
            ZINF.append(ZINF[iteracao])
            ZSUP.append(ZSUP[iteracao])
            iteracao += 1
            #
            # Backward - Laço ou Loop reverso de estágios (do fim para o início)
            #
            for iest in np.arange(self.sistema["DGer"]["Nr_Est"] - 1, -1, -1):
                VI = []
                if iest == 0:
                    for i, iusi in enumerate(self.sistema["UHE"]):
                        VI.append(iusi["VI"])
                else:
                    for i, iusi in enumerate(memoria[iest - 1]["UHE"]):
                        VI.append(iusi["vf"])
                AFL = []
                for i, iusi in enumerate(self.sistema["UHE"]):
                    AFL.append(iusi["Afl"][iest][cenario])
                #
                # Chama função de despacho hidrotérmico
                #
                resultado = self.despacho_pddd(VI, AFL, pote_de_corte, iest + 1, imprime)
                term_indep = resultado["DGer"]["CustoTotal"]
                coefs = []
                for i, iusi in enumerate(resultado["UHE"]):
                    coefs.append(-iusi["cma"])
                    term_indep -= VI[i] * coefs[i]
                #
                # Calcula o corte (inequação) correspondente a uma discretização
                #
                corte = {
                    "Estagio": iest,
                    "Termo_Indep": term_indep,
                    "Coefs": coefs
                }
                #
                # Insere o corte no final da lista pote_de_corte
                #
                pote_de_corte.append(corte)

        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido na PDDD", time.time() - t)
        # print(pote_de_corte)

        #
        # Inicializa listas com as variáveis de decisão que serão preenchidas
        # com as informações dos diferentes estágios
        #
        vf = []
        vt = []
        vv = []
        cma = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            vf.append([])
            vt.append([])
            vv.append([])
            cma.append([])
        gt = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            gt.append([])

        cmo = []
        deficit = []
        custo_total = 0.

        #
        # Preenche listas
        #
        for decisao in memoria:
            for i in range(Num_UHE):
                vf[i].append(decisao["UHE"][i]["vf"])
                vt[i].append(decisao["UHE"][i]["vt"])
                vv[i].append(decisao["UHE"][i]["vv"])
                cma[i].append(decisao["UHE"][i]["cma"])
            for i in range(Num_UTE):
                gt[i].append(decisao["UTE"][i]["gt"])
            cmo.append(decisao["DGer"]["CMO"])
            deficit.append(decisao["DGer"]["Deficit"])
            custo_total += decisao["DGer"]["CustoTotal"] - decisao["DGer"]["CustoFuturo"]

        #
        # Monta lista_uhe
        #
        lista_uhe = []
        for i in range(Num_UHE):
            elemento = {
                "vf": vf[i],
                "vt": vt[i],
                "vv": vv[i],
                "cma": cma[i]
            }
            lista_uhe.append(elemento)

        #
        # Monta lista_ute
        #
        lista_ute = []
        for i in range(Num_UTE):
            elemento = {
                "gt": gt[i],
            }
            lista_ute.append(elemento)

        #
        # Preenche dicionário de dados com a saída
        #
        resultado = {
            "DGer": {
                "CustoTotal": custo_total,
                "CMO": cmo,
                "Deficit": deficit,
                "ZINF": ZINF,
                "ZSUP": ZSUP,
                "Nr_Iteracoes": iteracao
            },
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        return resultado

    def plot_tree(self, Cenario, Estagios, Aberturas, Nome_Arq):
        """Gera um pdf com estágios e aberturas.

        Keyword arguments:
        Cenario -- Especifique o cenario de afluencia a ser utilizado no primeiro estagio
        Estagios -- Especifique a profundidade da árvore, ou seja, quantas camadas terá a árvore
        Aberturas -- Especifique o número aberturas para cada nó
        Nome_Arq -- Especifique o Nome do arquivo de saída
        """

        if Aberturas > self.sistema["DGer"]["Nr_Cen"]:
            print ("Número de Cenários Menor que Número de Aberturas")
            print ("Método plot_tree interrompido!")
            return

        if Cenario > self.sistema["DGer"]["Nr_Cen"]:
            print ("Cenario escolhido superior ao Número de Cenários disponíveis")
            print ("Método plot_tree interrompido!")
            return

        if Estagios > self.sistema["DGer"]["Nr_Est"]:
            print ("Número de Estágios Superior aos dados informados no problema.")
            print("Método plot_tree interrompido!")
            return

        def cria_tree(lista, CasoEstudo, Aberturas, Estagios):

          estagio = lista[-1]["Estagio"] + 1
          anterior = lista[-1]["Ordem"]
          if estagio == Estagios:
            return
          for icen in range(Aberturas):
            elemento = { "Anterior": anterior,
                         "Estagio": estagio,
                         "Afluencia": CasoEstudo.sistema["UHE"][0]["Afl"][estagio][icen],
                         "Ordem": len(lista),
                       }
            lista.append(elemento)
            cria_tree(lista, CasoEstudo, Aberturas, Estagios)

        estagio = 0
        elemento = {
                      "Anterior" : None,
                      "Estagio" : 0,
                      "Afluencia" : self.sistema["UHE"][0]["Afl"][estagio][0],
                      "Ordem" : 0,
                   }

        lista = []
        lista.append(elemento)
        cria_tree(lista, self, Aberturas, Estagios)

        g = Digraph('G', filename=Nome_Arq)
        for elemento in lista:
          if (elemento["Anterior"] != None):
            probabilidade = 100/(Aberturas**elemento["Estagio"])
            g.edge(str(elemento["Anterior"]), str(elemento["Ordem"]),
                   label=str(round(probabilidade,2))+'%')

        for elemento in lista:
          g.node(str(elemento["Ordem"]),label= " Afl: "+ str(elemento["Afluencia"]))

        g.node("0", style="filled", fillcolor="green")

        for iest in range(self.sistema["DGer"]["Nr_Est"]):
          if (iest%2) == 0:
            Cor = 'red'
            Preenche = 'green:cyan'
          else:
            Cor = 'red'
            Preenche = 'lightblue:cyan'

          with g.subgraph(name='cluster'+str(iest+1)) as c:
            c.attr(fillcolor=Preenche,
                   label='Estágio '+str(iest+1),
                   fontcolor=Cor,
                   style='filled',
                   gradientangle='270')
            c.attr('node',
                   shape='box',
                   fillcolor='red:yellow',
                   style='filled',
                   gradientangle='90')
            for elemento in lista:
              if elemento["Estagio"]==iest:
                c.node(str(elemento["Ordem"]))

        g.attr("graph",pad="0.5", nodesep="1", ranksep="2")

        g.view()

    def pl_unico_tree(self, Cenario, imprime = False):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        #
        # Cria Variáveis de Decisão
        # vf, vt, vv, gt ===> [iest][abertura][0][usina]
        # deficit ===> [iest][abertura]
        #

        vf = []
        vt = []
        vv = []
        gt = []
        deficit = []

        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            vf.append([])
            vt.append([])
            vv.append([])
            gt.append([])
            deficit.append([])
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                vf[iest].append([])
                vt[iest].append([])
                vv[iest].append([])
                gt[iest].append([])
                deficit[iest].append([])
                vf[iest][iabertura].append(variable(len(self.sistema["UHE"]),
                                                    "Volume Final no Estagio " +
                                                    str(iest) +
                                                    " Abertura " +
                                                    str(iabertura)))
                vt[iest][iabertura].append(variable(len(self.sistema["UHE"]),
                                                    "Volume Turbinado no Estagio " +
                                                    str(iest) +
                                                    " Abertura " +
                                                    str(iabertura)))
                vv[iest][iabertura].append(variable(len(self.sistema["UHE"]),
                                                    "Volume Vertido no Estagio " +
                                                    str(iest) +
                                                    " Abertura " +
                                                    str(iabertura)))
                gt[iest][iabertura].append(variable(len(self.sistema["UTE"]),
                                                    "Geração Térmica no Estagio " +
                                                    str(iest) +
                                                    " Abertura " +
                                                    str(iabertura)))
                deficit[iest][iabertura].append(variable(1,
                                                         "Déficit no Estagio " +
                                                         str(iest) +
                                                         " Abertura " +
                                                         str(iabertura)))
        #
        # Define Função Objetivo (fob)
        #

        fob = 0
        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                constante = 1 / (self.sistema["DGer"]["Nr_Cen"] ** iest)
                for iusi, termica in enumerate(self.sistema["UTE"]):
                    fob += float(constante) * termica["Custo"] * gt[iest][iabertura][0][iusi]
                fob += float(constante) * self.sistema["DGer"]["CDef"] * deficit[iest][iabertura][0]
                for iusi, hidreletrica in enumerate(self.sistema["UHE"]):
                    fob += float(constante) * 0.001 * vv[iest][iabertura][0][iusi]

        # Constrói Conjunto de Restrições

        restricoes = []

        #
        # Balanço Hídrico
        # Para cada nó existe uma restrição de Balanço Hídrico por Usina
        #

        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            abertura_anterior = 0
            contador = 0
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                if contador == self.sistema["DGer"]["Nr_Cen"]:
                    contador = 0
                    abertura_anterior += 1
                for iusi, uhe in enumerate(self.sistema["UHE"]):
                    if iest == 0:
                        restricoes.append(vf[iest][iabertura][0][iusi] ==
                                          float(self.sistema["UHE"][iusi]["VI"]) +
                                          float(self.sistema["UHE"][iusi]["Afl"][iest][Cenario]) -
                                          vt[iest][iabertura][0][iusi] -
                                          vv[iest][iabertura][0][iusi])
                    else:
                        restricoes.append(vf[iest][iabertura][0][iusi] ==
                                          vf[iest - 1][abertura_anterior][0][iusi] +
                                          float(self.sistema["UHE"][iusi]["Afl"][iest][contador]) -
                                          vt[iest][iabertura][0][iusi] -
                                          vv[iest][iabertura][0][iusi])

                contador += 1

        #
        # Atendimento à Demanda
        # Para cada nó existe uma Restrição de Atendimento à Demanda
        #

        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                demanda = 0
                for iusi, uhe in enumerate(self.sistema["UHE"]):
                    demanda += float(self.sistema["UHE"][iusi]["Prod"]) * vt[iest][iabertura][0][iusi]
                for iusi, ute in enumerate(self.sistema["UTE"]):
                    demanda += gt[iest][iabertura][0][iusi]
                demanda += deficit[iest][iabertura][0]
                restricoes.append(demanda == self.sistema["DGer"]["Carga"][iest])

        #
        # Restricoes de Canalização
        #

        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                for iusi, uhe in enumerate(self.sistema["UHE"]):
                    restricoes.append(vf[iest][iabertura][0][iusi] >= self.sistema["UHE"][iusi]["Vmin"])
                    restricoes.append(vf[iest][iabertura][0][iusi] <= self.sistema["UHE"][iusi]["Vmax"])
                    restricoes.append(vt[iest][iabertura][0][iusi] >= 0)
                    restricoes.append(vt[iest][iabertura][0][iusi] <= self.sistema["UHE"][iusi]["Engol"])
                    restricoes.append(vv[iest][iabertura][0][iusi] >= 0)
                for iusi, ute in enumerate(self.sistema["UTE"]):
                    restricoes.append(gt[iest][iabertura][0][iusi] >= 0)
                    restricoes.append(gt[iest][iabertura][0][iusi] <= self.sistema["UTE"][iusi]["Capac"])
                restricoes.append(deficit[iest][iabertura][0] >= 0)

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido no PL Único - Árvore Completa", time.time() - t)

        #
        # Armazena Resultado
        #

        ResNos = []
        Contador = 0
        Pula = len(self.sistema["UHE"])*(self.sistema["DGer"]["Nr_Cen"]**self.sistema["DGer"]["Nr_Est"]-1)/(self.sistema["DGer"]["Nr_Cen"]-1)
        Pula = int(Pula)
        for iest in range(self.sistema["DGer"]["Nr_Est"]):
            for iabertura in range(self.sistema["DGer"]["Nr_Cen"] ** iest):
                lista_uhe = []
                CustoTotal = 0.
                for i, iusi in enumerate(self.sistema["UHE"]):
                    elemento = {
                                    "vf": vf[iest][iabertura][0][i].value()[0],
                                    "vt": vt[iest][iabertura][0][i].value()[0],
                                    "vv": vv[iest][iabertura][0][i].value()[0],
                                    "cma": restricoes[Contador].multiplier.value[0]
                               }
                    CustoTotal += 0.01 * vv[iest][iabertura][0][i].value()[0]
                    lista_uhe.append(elemento)
                    Contador += 1
                lista_ute = []
                for i, iusi in enumerate(self.sistema["UTE"]):
                    elemento = {
                                    "gt": gt[iest][iabertura][0][i].value()[0]
                               }
                    CustoTotal += iusi["Custo"] * gt[iest][iabertura][0][i].value()[0]
                    lista_ute.append(elemento)
                CustoTotal += self.sistema["DGer"]["CDef"] * deficit[iest][iabertura][0].value[0]
                DGer = {
                         "Deficit": deficit[iest][iabertura][0].value[0],
                         "CMO": restricoes[Pula].multiplier.value[0],
                         "CustoImediato": CustoTotal
                       }
                Pula += 1
                No = { "Dger": DGer,
                       "UHE": lista_uhe,
                       "UTE": lista_ute,
                     }
                NoCompleto = {
                                "Estagio": iest,
                                "Ordem": iabertura,
                                "Resultado": No
                             }
                ResNos.append(NoCompleto)

        return(ResNos, fob.value()[0])


    def despacho_pddd_est(self, VI, AFL, pote_de_corte, iest, ordem, imprime):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Cria Variáveis de Decisão
        #

        vf = variable(Num_UHE, "Volume Final na Usina")
        vt = variable(Num_UHE, "Volume Turbinado na Usina")
        vv = variable(Num_UHE, "Volume Vertido na Usina")
        gt = variable(Num_UTE, "Geração na Usina Térmica")
        deficit = variable(1, "Déficit de Energia no Sistema")
        alpha = variable(1, "Custo Futuro")

        # Construção da Função Objetivo

        fob = 0

        for i, iusi in enumerate(self.sistema["UTE"]):
            fob += iusi['Custo'] * gt[i]

        fob += self.sistema["DGer"]["CDef"] * deficit[0]

        for i, iusi in enumerate(self.sistema["UHE"]):
            fob += 0.01 * vv[i]

        fob += 1.0 * alpha[0]

        # Definição das Restrições

        restricoes = []

        # Balanço Hídrico

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] == float(VI[i]) + float(AFL[i]) - vt[i] - vv[i])

        # Atendimento à Demanda

        AD = 0

        for i, iusi in enumerate(self.sistema["UHE"]):
            AD += iusi["Prod"] * vt[i]

        for i, usi in enumerate(self.sistema["UTE"]):
            AD += gt[i]

        AD += deficit[0]

        restricoes.append(AD == self.sistema["DGer"]["Carga"][iest - 1])

        # Restricoes Canalização

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] >= iusi["Vmin"])
            restricoes.append(vf[i] <= iusi["Vmax"])
            restricoes.append(vt[i] >= 0)
            restricoes.append(vt[i] <= iusi["Engol"])
            restricoes.append(vv[i] >= 0)

        for i, iusi in enumerate(self.sistema["UTE"]):
            restricoes.append(gt[i] >= 0)
            restricoes.append(gt[i] <= iusi["Capac"])

        restricoes.append(deficit[0] >= 0)

        restricoes.append(alpha[0] >= 0)

        #
        # Insere inequações correspondentes aos cortes
        #

        for icorte in pote_de_corte:
            if icorte['Estagio'] == iest and icorte["Ordem"] == ordem:
                equacao = 0
                for iusi in range(Num_UHE):
                    equacao += float(icorte['Coefs'][iusi]) * vf[iusi]
                equacao += float(icorte['Termo_Indep'])
                restricoes.append(alpha[0] >= equacao)

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        #
        # Armazena resultados do problema em um dicionário de dados
        #

        Dger = {
            "Deficit": deficit[0].value()[0],
            "CMO": restricoes[Num_UHE].multiplier.value[0],
            "CustoTotal": fob.value()[0],
            "CustoFuturo": alpha[0].value()[0]
        }

        lista_uhe = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            resultado = {
                "vf": vf[i].value()[0],
                "vt": vt[i].value()[0],
                "vv": vv[i].value()[0],
                "cma": restricoes[i].multiplier.value[0]
            }
            lista_uhe.append(resultado)

        lista_ute = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            resultado = {
                "gt": gt[i].value()[0]
            }
            lista_ute.append(resultado)

        resultado = {
            "DGer": Dger,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        #
        # Imprime resultados em tela
        #

        if imprime:
            print("Custo Total:", fob.value())

            for i, usi in enumerate(self.sistema["UHE"]):
                print(vf.name, i, "é", vf[i].value(), "hm3")
                print(vt.name, i, "é", vt[i].value(), "hm3")
                print(vv.name, i, "é", vv[i].value(), "hm3")

            for i, usi in enumerate(self.sistema["UTE"]):
                print(gt.name, i, "é", gt[i].value(), "MWmed")

            print(deficit.name, "é", deficit[0].value(), "MWmed")

            print(alpha.name, "é", alpha[0].value(), "$")

            for i, iusi in enumerate(self.sistema["UHE"]):
                print("O valor da água na usina", i, "é: ", restricoes[i].multiplier.value)

            print("O Custo Marginal de Operação é: ", restricoes[Num_UHE].multiplier.value)

            print("----- x ------ ")

        #
        # Retorna da função exportando os resultados
        #

        return resultado

    def pddd_tree(self, Cenario, imprime = False):


        def recursiva(Caso, VI, AFL, Estagio, Ordem, PoteDeCorte, ResNos, imprime = False):
            Ordem_Deste_No = Ordem
            #
            # Somente no Estágio Inicial Existe um Nó Somente
            #
            if Estagio == 0:
                Fator = float(1)
            #
            # Em todos os outros nós existirão Tantas bifurcações quanto o número de cenários
            #
            else:
                Fator = float(Caso.sistema["DGer"]["Nr_Cen"])
            #
            # Despacha Nó - Forward
            #
            resultado_fwd = Caso.despacho_pddd_est(VI, AFL, PoteDeCorte, Estagio+1, Ordem_Deste_No, imprime)
            CI = (resultado_fwd["DGer"]["CustoTotal"] - resultado_fwd["DGer"]["CustoFuturo"])
            CT = resultado_fwd["DGer"]["CustoTotal"]
            Guarda = {
                        "Estagio": Estagio,
                        "Ordem": Ordem_Deste_No,
                        "Resultado": resultado_fwd
                     }
            ResNos.append(Guarda)
            #
            # Caso o nó resolvido seja de último estágio não há necessidade de bifurcar mais
            #
            if Estagio == Caso.sistema["DGer"]["Nr_Est"]-1:
                term_indep = resultado_fwd["DGer"]["CustoTotal"]
                coefs = []
                for i, iusi in enumerate(resultado_fwd["UHE"]):
                    coefs.append(-iusi["cma"])
                    term_indep -= VI[i] * coefs[i]
                Corte = {
                            "Estagio": Estagio,
                            "Ordem": Ordem,
                            "Termo_Indep": term_indep/Fator,
                            "Coefs": [ coef/Fator for coef in coefs ]
                        }
                return (CT, CI/Fator, Corte, Ordem, ResNos)
            #
            # Caso o nó resolvido não seja de último estágio deve-se bifurcar o número de cenários
            #
            VF = []
            for iusi in resultado_fwd["UHE"]:
                VF.append(iusi["vf"])
            #
            # Cria Corte Médio (Inicializa com Zero)
            #
            Corte = {
                        "Estagio": Estagio+1,
                        "Ordem": Ordem_Deste_No,
                        "Termo_Indep": 0.,
                        "Coefs": [0.] * len(Caso.sistema["UHE"])
                    }
            for icen in range(Caso.sistema["DGer"]["Nr_Cen"]):
                AFL_CEN = []
                for iusi in Caso.sistema["UHE"]:
                    AFL_CEN.append(iusi["Afl"][Estagio+1][icen])
                Ordem += 1
                [CTMedio, CIMedio, CorteMedio, Ordem, ResNos] = recursiva(Caso, VF, AFL_CEN, Estagio+1, Ordem, PoteDeCorte, ResNos, imprime)
                Corte["Termo_Indep"] += CorteMedio["Termo_Indep"]
                for i in range(len(CorteMedio["Coefs"])):
                    Corte["Coefs"][i] += CorteMedio["Coefs"][i]
                CI += CIMedio
            PoteDeCorte.append(Corte)
            resultado_bkd = Caso.despacho_pddd_est(VI, AFL, PoteDeCorte, Estagio+1, Ordem_Deste_No, imprime)
            term_indep = resultado_bkd["DGer"]["CustoTotal"]
            coefs = []
            for i, iusi in enumerate(resultado_bkd["UHE"]):
                coefs.append(-iusi["cma"])
                term_indep -= VI[i] * coefs[i]
            Corte = {
                "Estagio": Estagio,
                "Ordem": Ordem,
                "Termo_Indep": term_indep/Fator,
                "Coefs": [ coef/Fator for coef in coefs ]
            }

            return (CT, CI/Fator, Corte, Ordem, ResNos)

        tol = 0.01
        iteracao = 1
        Estagio = 0
        VI = []
        AFL = []
        PoteDeCorte = []
        for iusi in self.sistema["UHE"]:
            VI.append(iusi["VI"])
            AFL.append(iusi["Afl"][Estagio][Cenario])

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        zinf_lista = []
        zsup_lista = []
        while True:
            Estagio = 0
            Ordem = 0
            ResNos = []
            [ ZINF, ZSUP, Corte, Ordem, ResNos] = recursiva(self, VI, AFL, Estagio, Ordem, PoteDeCorte, ResNos, imprime)
            zinf_lista.append(ZINF)
            zsup_lista.append(ZSUP)

            if np.abs(ZSUP - ZINF) < tol:
                break
            else:
                iteracao += 1

        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido na PDDD - Árvore Completa", time.time() - t)

        return(ResNos, ZINF, zinf_lista, zsup_lista)

    def plot_tree_pdde(self, Estagios, Aberturas, caminhos, Nome_Arq):
        """Gera um pdf com estágios e aberturas.

        Keyword arguments:
        Cenario -- Especifique o cenario de afluencia a ser utilizado no primeiro estagio
        Estagios -- Especifique a profundidade da árvore, ou seja, quantas camadas terá a árvore
        Aberturas -- Especifique o número aberturas para cada nó
        caminhos -- Lista com caminhos a serem destacados
        Nome_Arq -- Especifique o Nome do arquivo de saída
        """

        if Aberturas > self.sistema["DGer"]["Nr_Cen"]:
            print ("Número de Cenários Menor que Número de Aberturas")
            print ("Método plot_tree interrompido!")
            return

        if Estagios > self.sistema["DGer"]["Nr_Est"]:
            print ("Número de Estágios Superior aos dados informados no problema.")
            print("Método plot_tree interrompido!")
            return

        def cria_tree(lista, CasoEstudo, Aberturas, Estagios):

            if not lista:
                estagio = 0
                anterior = None
            else:
                estagio = lista[-1]["Estagio"] + 1
                anterior = lista[-1]["Ordem"]
            if estagio == Estagios:
                return
            for icen in range(Aberturas):
                elemento = { "Anterior": anterior,
                         "Estagio": estagio,
                         "Afluencia": CasoEstudo.sistema["UHE"][0]["Afl"][estagio][icen],
                         "Ordem": len(lista),
                       }
                lista.append(elemento)
                cria_tree(lista, CasoEstudo, Aberturas, Estagios)

        lista = []
        cria_tree(lista, self, Aberturas, Estagios)

        #
        # Cria Grafo
        #

        g = Digraph('G', filename=Nome_Arq, strict=True)


        #
        # Cria nós do grafo com nome e label
        #

        for elemento in lista:
          g.node(str(elemento["Ordem"]),label= " Afl: "+ str(elemento["Afluencia"]))


        #
        # Cria arestas do grafo ( o label é a probabilidade
        #

        for elemento in lista:
          if (elemento["Anterior"] != None):
            probabilidade = 100/(Aberturas**(elemento["Estagio"]+1))
            g.edge(str(elemento["Anterior"]), str(elemento["Ordem"]),
                   label=str(round(probabilidade,2))+'%')


        #g.node("0", style="filled", fillcolor="green")

        Cor = 'red'
        for iest in range(Estagios):
            if (iest%2) == 0:
                Preenche = 'green:cyan'
            else:
                Preenche = 'lightblue:cyan'

            #
            # Cria um cluster para cada estágio
            #
            with g.subgraph(name='cluster'+str(iest+1)) as c:
                #
                # Define parâmetros do cluster
                #
                c.attr(fillcolor=Preenche,
                   label='Estágio '+str(iest+1),
                   fontcolor=Cor,
                   style='filled',
                   gradientangle='270')
                c.attr('node',
                       shape='box',
                       fillcolor='red:yellow',
                       style='filled',
                       gradientangle='90')

                #
                # Joga para dentro do cluster todos os nós do estágio iest
                #
                for elemento in lista:
                    if elemento["Estagio"]==iest:
                        c.node(str(elemento["Ordem"]))

        g.attr("graph",pad="0.5", nodesep="1", ranksep="2")


        #caminhos = [ 3, 7, 12, 15]

        for posicao in caminhos:
            contador = 0
            for elemento in lista:
                if elemento["Estagio"] == Estagios-1:
                    contador = contador + 1
                    if contador == posicao:
                        break

            while elemento["Anterior"] != None:
                probabilidade = 100 / (Aberturas ** (elemento["Estagio"] + 1))
                g.edge(str(elemento["Anterior"]), str(elemento["Ordem"]),
                       label=str(round(probabilidade, 2)) + '%', fontcolor = 'red', color='red', penwidth='6.0')
                for candidato in lista:
                    if candidato["Ordem"] == elemento["Anterior"]:
                        elemento = candidato
                        break


        g.view()


    def plot_pente_pdde(self, Estagios, Cenarios, Aberturas, SeqForw, Nome_Arq):
        """Gera um pdf com estágios e aberturas.

        Keyword arguments:
        Estagios -- Especifique a profundidade da árvore, ou seja, quantas camadas terá a árvore
        Cenarios -- Especifique o número cenarios a serem considerados
        Aberturas -- Especifique o número de aberturas
        SeqForw -- Especifique o número de sequências forward
        Nome_Arq -- Especifique o Nome do arquivo de saída
        """

        if Cenarios > self.sistema["DGer"]["Nr_Cen"]:
            print ("Número de Cenários Menor que Número de Aberturas")
            print ("Método plot_pente_pdde interrompido!")
            return

        if Estagios > self.sistema["DGer"]["Nr_Est"]:
            print ("Número de Estágios Superior aos dados informados no problema.")
            print("Método plot_pente_pdde interrompido!")
            return

        if Aberturas > Cenarios:
            print ("Número de Aberturas Superior ao número de Cenários.")
            print("Método plot_pente_pdde interrompido!")
            return


        Ordem = 0
        lista = []
        random.seed(30)
        for iest in range(Estagios):
            escolhidos = random.sample(range(Cenarios), Aberturas)
            for icen in range(Cenarios):
                valida = False
                for procura in escolhidos:
                    if procura == icen:
                        valida = True
                elemento =  {   "Estagio": iest,
                                "Afluencia": self.sistema["UHE"][0]["Afl"][iest][icen],
                                "Ordem": Ordem,
                                "Abertura": valida
                            }
                lista.append(elemento)
                Ordem += 1

        #
        # Cria Grafo
        #

        g = Digraph('G', filename=Nome_Arq, strict=True)

        #
        # Cria nós do grafo com nome e label
        #

        for elemento in lista:
            if elemento["Abertura"]:
                g.node(str(elemento["Ordem"]),label= " Afl: "+ str(elemento["Afluencia"]), color="red", fillcolor="red", style="filled")
            else:
                g.node(str(elemento["Ordem"]),label= " Afl: "+ str(elemento["Afluencia"]))

        #
        # Cria arestas do grafo ( o label é a probabilidade
        #

        probabilidade = 100 / Cenarios
        for elemento in lista:
            if (elemento["Estagio"] != 0):
                for candidato in lista:
                    if candidato["Estagio"] == elemento["Estagio"]-1:
                        g.edge(str(candidato["Ordem"]), str(elemento["Ordem"]))
                               # label=str(round(probabilidade,2))+'%')

        Cor = 'red'
        for iest in range(Estagios):
            if (iest%2) == 0:
                Preenche = 'green:cyan'
            else:
                Preenche = 'lightblue:cyan'

            #
            # Cria um cluster para cada estágio
            #
            with g.subgraph(name='cluster'+str(iest+1)) as c:
                #
                # Define parâmetros do cluster
                #
                c.attr(fillcolor=Preenche,
                   label='Estágio '+str(iest+1),
                   fontcolor=Cor,
                   style='filled',
                   gradientangle='270')
                c.attr('node',
                       shape='box',
                       fillcolor='red:yellow',
                       style='filled',
                       gradientangle='90')

                #
                # Joga para dentro do cluster todos os nós do estágio iest
                #
                for elemento in lista:
                    if elemento["Estagio"]==iest:
                        c.node(str(elemento["Ordem"]))


        g.attr("graph",pad="0.5", nodesep="1", ranksep="2")

        g.view()

        #
        # Cria Pente
        #

        pente = Digraph('Pente', filename=Nome_Arq+"Pente")

        for iest in range(Estagios):
            for ifwd in range(SeqForw):
                codigo = iest*SeqForw+ifwd
                if ifwd%2 == 1:
                    Cor = "red"
                else:
                    Cor = "green"
                pente.node(str(codigo),label= " Afl: " + str(codigo), color=Cor, fillcolor=Cor, style="filled")
                if iest >= 1:
                    pente.edge(str((iest-1)*SeqForw+ifwd), str(iest*SeqForw+ifwd), color= Cor)

        Cor = 'red'
        for iest in range(Estagios):
            if (iest%2) == 0:
                Preenche = 'gray:cyan'
            else:
                Preenche = 'gray:cyan'

            #
            # Cria um cluster para cada estágio
            #
            with pente.subgraph(name='cluster'+str(iest+1)) as c:
                #
                # Define parâmetros do cluster
                #
                c.attr(fillcolor=Preenche,
                   label='Estágio '+str(iest+1),
                   fontcolor=Cor,
                   style='filled',
                   gradientangle='270')
                c.attr('node',
                       shape='box',
                       fillcolor='red:yellow',
                       style='filled',
                       gradientangle='90')

                #
                # Joga para dentro do cluster todos os nós do estágio iest
                #
                for ifwd in range(SeqForw):
                    c.node(str(iest*SeqForw+ifwd))




        h = deepcopy(g)

        for copia in range(SeqForw):

            g = deepcopy(h)

            g.filename = g.filename + '_' + str(copia)

            iest = Estagios - 1
            no = random.randint(0,Aberturas-1)

            conta = 0

            for elemento_front in lista:
                if elemento_front["Estagio"] == iest and elemento_front["Abertura"]:
                    if conta == no:
                        break
                    else:
                        conta += 1

            pente.node(str(iest*SeqForw+copia),label="Afl: " + str(elemento_front["Afluencia"]))

            while iest > 0:
                iest -= 1
                no = random.randint(0,Aberturas-1)
                conta = 0
                for elemento_back in lista:
                    if elemento_back["Estagio"] == iest and elemento_back["Abertura"]:
                        if conta == no:
                            break
                        else:
                            conta += 1

                g.edge(str(elemento_back["Ordem"]), str(elemento_front["Ordem"]), color='red', penwidth='2.0')

                elemento_front = elemento_back

                pente.node(str(iest*SeqForw+copia),label="Afl: " + str(elemento_front["Afluencia"]))

            g.view()


        pente.view()

    def despacho_pdde(self, VI, AFL, pote_de_corte, iest, imprime):

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        Num_UHE = len(self.sistema["UHE"])

        Num_UTE = len(self.sistema["UTE"])

        #
        # Cria Variáveis de Decisão
        #

        vf = variable(Num_UHE, "Volume Final na Usina")
        vt = variable(Num_UHE, "Volume Turbinado na Usina")
        vv = variable(Num_UHE, "Volume Vertido na Usina")
        gt = variable(Num_UTE, "Geração na Usina Térmica")
        deficit = variable(1, "Déficit de Energia no Sistema")
        alpha = variable(1, "Custo Futuro")

        # Construção da Função Objetivo

        fob = 0

        for i, iusi in enumerate(self.sistema["UTE"]):
            fob += iusi['Custo'] * gt[i]

        fob += self.sistema["DGer"]["CDef"] * deficit[0]

        for i, iusi in enumerate(self.sistema["UHE"]):
            fob += 0.01 * vv[i]

        fob += 1.0 * alpha[0]

        # Definição das Restrições

        restricoes = []

        # Balanço Hídrico

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] == float(VI[i]) + float(AFL[i]) - vt[i] - vv[i])

        # Atendimento à Demanda

        AD = 0

        for i, iusi in enumerate(self.sistema["UHE"]):
            AD += iusi["Prod"] * vt[i]

        for i, usi in enumerate(self.sistema["UTE"]):
            AD += gt[i]

        AD += deficit[0]

        restricoes.append(AD == self.sistema["DGer"]["Carga"][iest - 1])

        # Restricoes Canalização

        for i, iusi in enumerate(self.sistema["UHE"]):
            restricoes.append(vf[i] >= iusi["Vmin"])
            restricoes.append(vf[i] <= iusi["Vmax"])
            restricoes.append(vt[i] >= 0)
            restricoes.append(vt[i] <= iusi["Engol"])
            restricoes.append(vv[i] >= 0)

        for i, iusi in enumerate(self.sistema["UTE"]):
            restricoes.append(gt[i] >= 0)
            restricoes.append(gt[i] <= iusi["Capac"])

        restricoes.append(deficit[0] >= 0)

        restricoes.append(alpha[0] >= 0)

        #
        # Insere inequações correspondentes aos cortes
        #

        for icorte in pote_de_corte:
            if icorte['Estagio'] == iest:
                equacao = 0
                for iusi in range(Num_UHE):
                    equacao += float(icorte['Coefs'][iusi]) * vf[iusi]
                equacao += float(icorte['Termo_Indep'])
                restricoes.append(alpha[0] >= equacao)

        #
        # Cria problema de otimização
        #

        problema = op(fob, restricoes)

        #
        # Chama solver GLPK e resolve o problema de otimização linear
        #

        problema.solve('dense', 'glpk')

        #
        # Armazena resultados do problema em um dicionário de dados
        #

        Dger = {
            "Deficit": deficit[0].value()[0],
            "CMO": restricoes[Num_UHE].multiplier.value[0],
            "CustoTotal": fob.value()[0],
            "CustoFuturo": alpha[0].value()[0]
        }

        lista_uhe = []
        for i, iusi in enumerate(self.sistema["UHE"]):
            resultado = {
                "vf": vf[i].value()[0],
                "vt": vt[i].value()[0],
                "vv": vv[i].value()[0],
                "cma": restricoes[i].multiplier.value[0]
            }
            lista_uhe.append(resultado)

        lista_ute = []
        for i, iusi in enumerate(self.sistema["UTE"]):
            resultado = {
                "gt": gt[i].value()[0]
            }
            lista_ute.append(resultado)

        resultado = {
            "DGer": Dger,
            "UHE": lista_uhe,
            "UTE": lista_ute
        }

        #
        # Imprime resultados em tela
        #

        if imprime:
            print("Custo Total:", fob.value())

            for i, usi in enumerate(self.sistema["UHE"]):
                print(vf.name, i, "é", vf[i].value(), "hm3")
                print(vt.name, i, "é", vt[i].value(), "hm3")
                print(vv.name, i, "é", vv[i].value(), "hm3")

            for i, usi in enumerate(self.sistema["UTE"]):
                print(gt.name, i, "é", gt[i].value(), "MWmed")

            print(deficit.name, "é", deficit[0].value(), "MWmed")

            print(alpha.name, "é", alpha[0].value(), "$")

            for i, iusi in enumerate(self.sistema["UHE"]):
                print("O valor da água na usina", i, "é: ", restricoes[i].multiplier.value)

            print("O Custo Marginal de Operação é: ", restricoes[Num_UHE].multiplier.value)

            print("----- x ------ ")

        #
        # Retorna da função exportando os resultados
        #

        return resultado


    def pdde(self, nr_est, nr_aberturas, nr_forwards, imprime):
        """Gera um pdf com estágios e aberturas.

        Keyword arguments:
        nr_est -- Define horizonte de estudo
        nr_aberturas -- Número de aberturas
        nr_forwards -- Número de seqüências forward
        """

        if nr_aberturas > self.sistema["DGer"]["Nr_Cen"]:
            print ("Número de Aberturas Superior ao número de Cenários.")
            print ("Método pdde interrompido!")
            return

        if nr_est > self.sistema["DGer"]["Nr_Est"]:
            print ("Número de Estágios Superior aos dados informados no problema.")
            print("Método pdde interrompido!")
            return

        random.seed(30)

        # Calcula as aberturas

        MatrizAberturas = np.zeros( (nr_est,nr_aberturas), dtype=int)

        for i in range(nr_est):
            sorteados = random.sample(range(0,self.sistema["DGer"]["Nr_Cen"]),nr_aberturas)
            MatrizAberturas[i] = sorteados

        # Calcula as sequencias forward

        SeqForward = np.zeros( (nr_est,nr_forwards), dtype=int)

        for iest in range(nr_est):
            for ifwd in range(nr_forwards):
                posicao = random.randint(0,nr_aberturas-1)
                SeqForward[iest,ifwd] = MatrizAberturas[iest,posicao]

        Num_UHE = len(self.sistema["UHE"])

        #
        # Esta é uma lista com dicionários contendo todos os cortes criados
        # Inicia vazia
        #

        pote_de_corte = []

        #
        # Computa o instante de tempo no qual o processo iterativo iniciou
        #
        t = time.time()

        iteracao = 0
        Convergiu = False

        ZSUP_MED = []
        ZINF_MED = []
        LINF = []
        LSUP = []

        while not Convergiu:

            #
            # Forward - Laço ou Loop direto de estágios (do início para o fim)
            #

            ZSUP_MED.append(0.)
            ZINF_MED.append(0.)

            memoria = []
            ZSUP = np.zeros(nr_forwards, dtype=float)

            for iest in range(nr_est):
                linha = list()
                for ifwd in range(nr_forwards):
                    VI = []
                    if iest == 0:
                        for i, iusi in enumerate(self.sistema["UHE"]):
                            VI.append(iusi["VI"])
                    else:
                        resultado = memoria[iest-1][ifwd]
                        for i, iusi in enumerate(resultado["UHE"]):
                            VI.append(iusi["vf"])
                    AFL = []
                    for i, iusi in enumerate(self.sistema["UHE"]):
                        AFL.append(iusi["Afl"][iest][SeqForward[iest,ifwd]])

                    #
                    # Chama função de despacho hidrotérmico
                    #
                    resultado = self.despacho_pdde(VI, AFL, pote_de_corte, iest + 1, imprime)

                    ZSUP[ifwd] += resultado["DGer"]["CustoTotal"] - resultado["DGer"]["CustoFuturo"]
                    if iest == 0:
                        ZINF_MED[iteracao] += resultado["DGer"]["CustoTotal"]
                    linha.append(resultado)
                memoria.append(linha)

            ZINF_MED[iteracao] = ZINF_MED[iteracao] / nr_forwards
            for ifwd in range(nr_forwards):
                ZSUP_MED[iteracao] = ZSUP_MED[iteracao] + ZSUP[ifwd]
            ZSUP_MED[iteracao] = ZSUP_MED[iteracao] / nr_forwards

            # Calcula Desvio Padrão do ZSUP
            desvio = 0
            for ifwd in range(nr_forwards):
                desvio = desvio + (ZSUP_MED[iteracao] - ZSUP[ifwd])**2
            desvio = np.sqrt(desvio)/nr_forwards
            LINF.append(ZSUP_MED[iteracao] - 1.96*desvio)
            LSUP.append(ZSUP_MED[iteracao] + 1.96*desvio)

            if ZINF_MED[iteracao] >= LINF[iteracao] and ZINF_MED[iteracao] <= LSUP[iteracao]:
                Convergiu = True
                break

            print(f"Fim da Iteração {(iteracao+1)}")

            # Backward

            for iest in np.arange(nr_est-1,0,-1):
                for ifwd in range(nr_forwards):
                    #
                    # Corte Médio
                    #
                    Corte_Medio = {
                        "Estagio": iest,
                        "Termo_Indep": 0.,
                        "Coefs": [0.] * Num_UHE
                    }

                    for iabt in range(nr_aberturas):
                        resultado = memoria[iest-1][ifwd]
                        VI = []
                        for i, iusi in enumerate(resultado["UHE"]):
                            VI.append(iusi["vf"])
                        AFL = []
                        for i, iusi in enumerate(self.sistema["UHE"]):
                            AFL.append(iusi["Afl"][iest][MatrizAberturas[iest, iabt]])
                        #
                        # Chama função de despacho hidrotérmico
                        #
                        resultado = self.despacho_pdde(VI, AFL, pote_de_corte, iest + 1, imprime)

                        Corte = {
                            "Estagio": iest,
                            "Termo_Indep": resultado["DGer"]["CustoTotal"],
                            "Coefs": [0.] * Num_UHE
                        }

                        for i, iusi in enumerate(resultado["UHE"]):
                            Corte["Coefs"][i] = -iusi["cma"]
                            Corte["Termo_Indep"] -= VI[i] * Corte["Coefs"][i]

                        Corte_Medio["Termo_Indep"] = Corte_Medio["Termo_Indep"] + Corte["Termo_Indep"]
                        for i in range(Num_UHE):
                            Corte_Medio["Coefs"][i] = Corte_Medio["Coefs"][i] + Corte["Coefs"][i]

                    Corte_Medio["Termo_Indep"] = Corte_Medio["Termo_Indep"]/nr_aberturas
                    for i in range(Num_UHE):
                        Corte_Medio["Coefs"][i] = Corte_Medio["Coefs"][i]/nr_aberturas

                    #
                    # Insere o corte no final da lista pote_de_corte
                    #
                    pote_de_corte.append(Corte_Medio)

            iteracao = iteracao + 1

            if iteracao == 20:
                Convergiu = True
                print("Execução interrompida após vigésima iteração por número máximo de iteraçoes")

        #
        # Calcula o tempo decorrido desde o início do algoritmo
        #
        print("Tempo decorrido na PDDE", time.time() - t)

        return(ZINF_MED, ZSUP_MED, LINF, LSUP, pote_de_corte)

