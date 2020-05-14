import numpy as np
from matplotlib import pyplot as plt
from typing import List
from PySDDP.hidr import hidr


class submercado(object):
    # Classe contendo informacoes sobre os arquivos de entrada e saida
    Codigo = None
    Nome = None
    Mercado = None
    NaoSimuladas = None
    Ficticio = None

    def __init__(self, nanos):
        self.Mercado = np.zeros((nanos + 1, 12), 'd')
        self.NaoSimuladas = np.zeros((nanos, 12), 'd')
        self.CustoDeficit = np.zeros(4, 'd')
        self.ProfundidadeDeficit = np.zeros(4, 'd')

    # Parametros Temporais
    EArmMax = None  # Energia Armazenavel Maxima (iano,imes)
    ENA = None
    EFIO = None
    EC = None

    def CalcEArmMax(self, usinas: List[hidr]):
        self.EArmMax = np.zeros((5, 12), 'd')
        for iano in range(5):
            for imes in range(12):
                self.EArmMax[iano][imes] = 0.
                for iusina in usinas:
                    if iusina.VolUtil > 0 and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EArmMax[iano][imes] = self.EArmMax[iano][imes] + iusina.RoAcum[iano][
                            imes] * iusina.VolUtil / 2.63

    def CalcENA(self, usinas: List[hidr]):

        anos_hist = len(usinas[0].Vazoes)

        self.ENA = np.zeros((5, 12, anos_hist), 'd')
        self.EC = np.zeros((5, 12, anos_hist), 'd')
        self.EFIO = np.zeros((5, 12, anos_hist), 'd')

        for iano in range(5):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        if iusina.VolUtil > 0:
                            self.EC[iano, imes] = self.EC[iano, imes] + iusina.RoAcum[iano][imes] * iusina.QIncEntreRes(
                                usinas, iano, imes)
                        else:
                            if iusina.StatusMotoriz[iano][imes] == 2:
                                self.EFIO[iano, imes] = self.EFIO[iano, imes] + iusina.RoEquiv[iano][
                                    imes] * iusina.QIncEntreRes(usinas, iano, imes)

        self.ENA = self.EC + self.EFIO

    #############################################################################
    #############################################################################
    # Graficos Diversos
    #############################################################################
    #############################################################################

    def PlotaEArmMax(self, usinas: List[hidr]):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.EArmMax) - 1
        nr_col = len(self.EArmMax[0])
        total = np.zeros((nr_lin, nr_col), 'd')
        nanos = nr_lin

        y = self.EArmMax[0:nr_lin][0:nr_col]
        FioJusante = np.zeros((nanos, 12), 'd')
        ContJusante = np.zeros((nanos, 12), 'd')
        for iano in range(nanos):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.VolUtil > 0 and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        FioJusante[iano][imes] += iusina.RoAcum_B_Sist[iano][imes] * iusina.VolUtil / 2.63
                        ContJusante[iano][imes] += iusina.RoAcum_C_Sist[iano][imes] * iusina.VolUtil / 2.63

        cor = 'black'
        linha = '-'
        LineWidth = 3
        Texto = "EARMAX - Avg: " + str(np.trunc(np.mean(y)))
        ax.plot(np.arange(1, nr_lin * nr_col + 1), y.reshape(nr_lin * nr_col, ), linha, color=cor,
                lw=LineWidth, label=Texto)
        ax.fill_between(np.arange(1, nr_lin * nr_col + 1), (FioJusante + ContJusante).reshape(nr_lin * nr_col, ),
                        y.reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)

        cor = 'blue'
        linha = '--'
        LineWidth = 2
        Texto = "Parc Fio Jus - Avg: " + str(np.trunc(np.mean(FioJusante)))
        ax.plot(np.arange(1, nr_lin * nr_col + 1), FioJusante.reshape(nr_lin * nr_col, ), linha, color=cor,
                lw=LineWidth, label=Texto)
        ax.fill_between(np.arange(1, nr_lin * nr_col + 1), 0,
                        y.reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)

        cor = 'chocolate'
        linha = 'x'
        LineWidth = 2
        Texto = "Parc Cont Jus - Avg: " + str(np.trunc(np.mean(ContJusante)))
        ax.plot(np.arange(1, nr_lin * nr_col + 1), (FioJusante + ContJusante).reshape(nr_lin * nr_col, ),
                linha, color=cor, lw=LineWidth, label=Texto)
        ax.fill_between(np.arange(1, nr_lin * nr_col + 1), FioJusante.reshape(nr_lin * nr_col, ),
                        ContJusante.reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)

        titulo = 'Evolucao da Energia Armazenavel Maxima \n do Submercado ' + self.Nome
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armaz. Maxima (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    def PlotaMercado(self):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.Mercado) - 1
        nr_col = len(self.Mercado[0])

        if self.Ficticio == 0:
            carga = self.Mercado[0:nr_lin][0:nr_col]
            pq = self.NaoSimuladas
            ax.plot(np.arange(1, nr_lin * nr_col + 1), carga.reshape(nr_lin * nr_col, ), 'r-', lw=3,
                    label='Mercado Total')
            ax.plot(np.arange(1, nr_lin * nr_col + 1), pq.reshape(nr_lin * nr_col, ), 'g--', lw=2,
                    label='Usinas Nao Simuladas')
            ax.fill_between(np.arange(1, nr_lin * nr_col + 1), 0, pq.reshape(nr_lin * nr_col, ), facecolor='g',
                            alpha=0.1)
            ax.fill_between(np.arange(1, nr_lin * nr_col + 1), pq.reshape(nr_lin * nr_col, ),
                            carga.reshape(nr_lin * nr_col, ), facecolor='r', alpha=0.1)

        titulo = 'Evolucao do Mercado Total do ' + self.Nome
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Demanda de Energia (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    def PlotaENA(self):

        nanos = len(self.ENA)
        nmeses = len(self.ENA[0])
        nseries = len(self.ENA[0][0])

        f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        eixo_x = np.arange(1, nanos * nmeses + 1)

        ENAS = np.zeros((nseries, nanos * nmeses), 'd')
        ECS = np.zeros((nseries, nanos * nmeses), 'd')
        EFIOS = np.zeros((nseries, nanos * nmeses), 'd')

        contador = 0
        for iano in range(nanos):
            for imes in range(nmeses):
                for iserie in range(nseries):
                    ENAS[iserie][contador] = self.ENA[iano][imes][iserie]
                    ECS[iserie][contador] = self.EC[iano][imes][iserie]
                    EFIOS[iserie][contador] = self.EFIO[iano][imes][iserie]
                contador = contador + 1

        ax1.plot(eixo_x, ENAS.transpose(), 'c-')
        ax2.plot(eixo_x, ECS.transpose(), 'c-')
        ax3.plot(eixo_x, EFIOS.transpose(), 'c-')

        mediaENA = np.mean(ENAS, axis=0)
        mediaEC = np.mean(ECS, axis=0)
        mediaEFIO = np.mean(EFIOS, axis=0)

        ax1.plot(eixo_x, mediaENA, 'r-', lw=3)
        ax2.plot(eixo_x, mediaEC, 'r-', lw=3)
        ax3.plot(eixo_x, mediaEFIO, 'r-', lw=3)

        desvioENA = np.nanstd(ENAS, axis=0)
        desvioEC = np.nanstd(ECS, axis=0)
        desvioEFIO = np.nanstd(EFIOS, axis=0)

        ax1.plot(eixo_x, mediaENA + desvioENA, 'r-.', lw=2)
        ax1.plot(eixo_x, mediaENA - desvioENA, 'r-.', lw=2)
        ax2.plot(eixo_x, mediaEC + desvioEC, 'r-.', lw=2)
        ax2.plot(eixo_x, mediaEC - desvioEC, 'r-.', lw=2)
        ax3.plot(eixo_x, mediaEFIO + desvioEFIO, 'r-.', lw=2)
        ax3.plot(eixo_x, mediaEFIO - desvioEFIO, 'r-.', lw=2)

        ax1.set_xticks(np.arange(1, 60))
        ax1.set_ylabel('ENA (MWmes)')
        ax2.set_ylabel('EC (MWmes)')
        ax3.set_ylabel('EFIO (MWMes)')
        tituloENA = 'ENA do Submercado ' + self.Nome
        tituloEC = 'EC do Submercado ' + self.Nome
        tituloEFIO = 'EFIO do Submercado ' + self.Nome
        ax1.set_title(tituloENA, fontsize=13)
        ax2.set_title(tituloEC, fontsize=13)
        ax3.set_title(tituloEFIO, fontsize=13)

        plt.show()
