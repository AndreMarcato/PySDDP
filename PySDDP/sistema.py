# coding=utf-8

import os
import numpy as np
from matplotlib import pyplot as plt
from cvxopt.modeling import variable, solvers
from cvxopt.modeling import op
from PySDDP.pmo import pmo
from PySDDP.dadosgerais import dadosgerais
from itertools import product, tee
import time
from matplotlib import cm


class PySDDP(object):
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


class Classroom(object):
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
    # usina = {
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
    # lista_uhe.append(usina)

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
        "Carga": [50, 50., 50],  # Lista com carga a ser atendida por estágio
        "Nr_Disc": 3,  # Número de Discretizações
        "Nr_Est": 3,  # Número de Estágios
        "Nr_Cen": 2  # Número de Cenários de Afluências
    }

    #
    # d_gerais para o caso 2 UHE (Comentar o bloco acima e descomentar o bloco abaixo)
    #
    # d_gerais = {
    #    "CDef": 500.,
    #    "Carga": [ 100, 100., 100],
    #    "Nr_Disc": 5,
    #    "Nr_Est": 3,
    #    "Nr_Cen": 2
    # }

    #
    # Cria dicionário de dados com todas as informações do sistema em estudo
    #
    sistema = {
        "DGer": d_gerais,
        "UHE": lista_uhe,
        "UTE": lista_ute
    }

    def despacho_pdd(self, VI, VF, AFL, custofuturo, iest, imprime):

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

        if imprime and (problema.status == 'optmal'):
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
                    resultado = self.despacho_pdd(VI, VF, AFL, CustoFuturo, iest - 1, imprime=False)
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
            for i, usi in enumerate(self.sistema["UHE"]):
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
            lista_deficit.append(deficit[iest].value()[0])

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

        for i, usi in enumerate(self.sistema["UHE"]):
            AD += iusi["Prod"] * vt[i]

        for i, usi in enumerate(self.sistema["UTE"]):
            AD += gt[i]

        AD += deficit[0]

        restricoes.append(AD == self.sistema["DGer"]["Carga"][iest - 2])

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
                resultado = self.despacho_pddd(VI, AFL, pote_de_corte, iest + 1, imprime=False)
                if iteracao == 1:
                    print(iest, resultado)
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
                resultado = self.despacho_pddd(VI, AFL, pote_de_corte, iest + 1, imprime=False)
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
