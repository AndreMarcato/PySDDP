# coding=utf-8

import os
import numpy as np
from matplotlib import pyplot as plt
from PyHydro.pmo import pmo
from PyHydro.dadosgerais import dadosgerais


class mddh(object):
    # Classe contendo informacoes sobre os arquivos de entrada e saida
    caso = None
    dger = None
    npmc = 1

    # Define listas
    cadr_uh = []  # Lista com usinas hidraulicas do cadastro (HIDR.DAT)
    cadr_ut = []  # Lista com usinas termicas do cadastro (TERM.DAT)
    conf_ut = []  # Lista com usinas termicas da configuracao em estudo (CONFT.DAT)
    conf_uh = []  # Lista com usinas hidraulicas da configuracao em estudo (CONFHD.DAT)
    ree = []  # Lista com os reservatorios equivalentes de energia
    submercado = []  # Lista com os submercados
    intercambio = []  # Lista com intercambios entre submercados

    def __init__(self, diretorio):

        # Leitura de arquivos
        self.caso = pmo(diretorio)
        self.caso.le_caso()
        self.dger = dadosgerais(diretorio)
        self.cadr_uh = self.caso.le_hidr(self.cadr_uh)
        self.conf_uh = self.caso.le_confh(self.conf_uh, self.cadr_uh, self.dger.NAnosEstudo)
        self.cadr_ut = self.caso.le_term(self.cadr_ut, self.dger.NAnosEstudo)
        self.conf_ut = self.caso.le_conft(self.conf_ut, self.cadr_ut)
        self.conf_ut = self.caso.le_clast(self.conf_ut, self.dger.MesInicioEstudo, self.dger.NAnosEstudo)
        self.conf_uh = self.caso.le_modif(self.conf_uh, self.dger.AnoInicioEstudo, self.dger.NAnosEstudo)
        self.conf_uh = self.caso.le_exph(self.conf_uh, self.dger.AnoInicioEstudo, self.dger.NAnosEstudo)
        self.conf_uh = self.caso.le_desvagua(self.conf_uh)
        self.ree = self.caso.le_ree(self.ree)
        # Cria Sistema
        self.submercado, self.intercambio, self.npmc = self.caso.le_sistema(self.submercado, self.intercambio,
                                                                            self.dger.NAnosEstudo, self.npmc)

        # Calcula produtibilidades acumuladas
        for iusina in self.conf_uh:
            iusina.ProdAcum(self.conf_uh)

        # Calcula Energias e Parametros do Sistema Equivalente de Energia
        # for ires in self.ree:
        #     ires.CalcEArmMax(self.conf_uh)
        #     ires.CalcEArmMin(self.conf_uh)
        #     ires.CalcEArmMed(self.conf_uh)
        #     ires.CalcENA(self.conf_uh)
        #     ires.CalcFatorSep(self.conf_uh)
        #     ires.CalcParamFC(self.conf_uh)
        #     ires.CalcParamEVMin(self.conf_uh)
        #     ires.CalcParamEVP(self.conf_uh)
        #     ires.CalcEVM(self.conf_uh)

        # Calcula Energias e Parametros dos Submercados
        for isist in self.submercado:
            if isist.Ficticio == 0:
                isist.CalcEArmIni(self.conf_uh, self.dger.AnoInicioEstudo)
                isist.CalcEArmMax(self.conf_uh, self.dger.AnoInicioEstudo)
                isist.CalcEArmMin(self.conf_uh)
                isist.CalcEArmMed(self.conf_uh, self.dger.AnoInicioEstudo)
                isist.CalcParamGHMAX(self.conf_uh)
                isist.CalcENA(self.conf_uh)
                isist.CalcFatorSep(self.conf_uh)
                isist.CalcParamFC(self.conf_uh)
                isist.CalcParamEVMin(self.conf_uh)
                isist.CalcGTMin(self.conf_ut)
                isist.CalcParamEVP(self.conf_uh)
                isist.CalcEVM(self.conf_uh, self.dger.AnoInicioEstudo)
                isist.CalcVazDesv(self.conf_uh)

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
                motorizada[cont] = self.dger.NAnosEstudo * 12 - np.count_nonzero(usina.StatusMotoriz - 2)

                # Meses que a usina ainda nao iniciou o enchimento do volume morto
                vazia[cont] = self.dger.NAnosEstudo * 12 - np.count_nonzero(usina.StatusVolMorto)

                # Meses que a usina encontra-se enchendo o volume morto
                enchendo[cont] = self.dger.NAnosEstudo * 12 - np.count_nonzero(usina.StatusVolMorto - 1)

                # Meses que a usina encontra-se motorizando
                submotorizada[cont] = self.dger.NAnosEstudo * 12 - np.count_nonzero(usina.StatusMotoriz - 1)

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
        plt.xticks(np.arange(0, self.dger.NAnosEstudo * 12 + 2, 12))
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
        nr_lin = len(self.ree[0].EAMAX)
        nr_col = len(self.ree[0].EAMAX[0])
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
            y = ree.EAMAX[0:nr_lin][0:nr_col]
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
                y = mercado.EAMAX[0:nr_lin][0:nr_col]
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
