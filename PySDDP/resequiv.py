from typing import List
from PySDDP.hidr import hidr
import numpy as np
from matplotlib import pyplot as plt


class resequiv(object):
    # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)
    Codigo = None  # Codigo do Reservatorio Equivalente
    Nome = None  # Nome do Reservatorio Equivalente
    Submercado = None  # Submercado ao qual o REE pertence

    # Parametros Temporais
    EAMAX = None  # Energia Armazenavel Maxima (iano,imes)
    EAMIN = None  # Energia Armazenavel Maxima (iano,imes)
    EAMED = None  # Energia Armazenavel Maxima (iano,imes)
    ENA = None
    EFIOB = None
    EC = None
    EVMin = None
    EVP = None
    EVM = None
    FatorSeparacao = None
    ParamFC = None
    ParamEVMin = None
    ParamEVP = None

    def CalcEArmMax(self, usinas: List[hidr]):

        for iano in range(5):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.VolUtil > 0 and iusina.Ree == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EAMAX[iano][imes] = self.EAMAX[iano][imes] + iusina.RoAcum[iano][
                            imes] * iusina.VolUtil / 2.63

    def CalcEArmMin(self, usinas: List[hidr]):
        self.EAMIN = np.zeros((5, 12), 'd')
        # for iano in range(5):
        #     for imes in range(12):
        #         for iusina in usinas:
        #             if iusina.VolUtil > 0 and iusina.Ree == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
        #                 self.EAMIN[iano][imes] = self.EAMIN[iano][imes] + iusina.RoAcum[iano][imes]*iusina.VolUtil/2.63

    def CalcEArmMed(self, usinas: List[hidr]):
        self.EAMED = np.zeros((5, 12), 'd')
        for iano in range(5):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.VolUtil > 0 and iusina.Ree == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EAMED[iano][imes] = self.EAMED[iano][imes] + iusina.RoAcum[iano][
                            imes] * iusina.VolUtil * 0.65 / 2.63

    def CalcENA(self, usinas: List[hidr]):

        anos_hist = len(usinas[0].Vazoes)

        self.ENA = np.zeros((anos_hist, 12), 'd')
        self.EC = np.zeros((anos_hist, 12), 'd')
        self.EFIOB = np.zeros((anos_hist, 12), 'd')

        for iano in range(anos_hist):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.Ree == self.Codigo:
                        if iusina.TipoReg == b'M':
                            self.EC[iano, imes] = self.EC[iano, imes] + iusina.RoAcum[0, 0] * iusina.QIncHistEntreRes(
                                usinas, iano, imes)
                        else:
                            self.EFIOB[iano, imes] = self.EFIOB[iano, imes] + iusina.RoEquiv[
                                0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
        self.ENA = self.EC + self.EFIOB

    def CalcFatorSep(self, usinas: List[hidr]):

        anos_hist = len(usinas[0].Vazoes)

        aux_1 = 0
        aux_2 = 0
        for iano in range(anos_hist):
            for imes in range(12):
                aux_1 += self.ENA[iano, imes] * self.EC[iano, imes]
                aux_2 += self.ENA[iano, imes] * self.ENA[iano, imes]
        self.FatorSeparacao = aux_1 / aux_2

    def CalcParamFC(self, usinas: List[hidr]):

        aux_1 = 0
        aux_2 = 0
        aux_3 = 0
        aux_4 = 0
        for iusina in usinas:
            if iusina.Ree == self.Codigo:
                aux_1 += iusina.RoAcumMax[0, 0] * iusina.QIncHistEntreRes(usinas, 0, 0)
                aux_2 += iusina.RoAcumMin[0, 0] * iusina.QIncHistEntreRes(usinas, 0, 0)
                aux_3 += iusina.RoAcumMed[0, 0] * iusina.QIncHistEntreRes(usinas, 0, 0)
                aux_4 += iusina.RoAcum[0, 0] * iusina.QIncHistEntreRes(usinas, 0, 0)
        fcmax = aux_1 / aux_4
        fcmin = aux_2 / aux_4
        fcmed = aux_3 / aux_4

        if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
            param = np.array([0., 0., fcmed])
        else:
            param = np.polyfit(np.array([self.EAMIN[0, 0], self.EAMED[0, 0], self.EAMAX[0, 0]]),
                               np.array([fcmin, fcmed, fcmax]), deg=2)

        self.ParamFC = param

    def CalcParamEVMin(self, usinas: List[hidr]):

        self.EVMin = 0

        evmin_max = 0
        evmin_min = 0
        evmin_med = 0
        for iusina in usinas:
            if iusina.Ree == self.Codigo:
                self.EVMin += iusina.VazMin * iusina.RoAcum[0, 0]
                evmin_max += iusina.VazMin * iusina.RoAcumMax[0, 0]
                evmin_min += iusina.VazMin * iusina.RoAcumMin[0, 0]
                evmin_med += iusina.VazMin * iusina.RoAcum[0, 0]

        if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
            param = np.array([0., 0., evmin_med])
        else:
            param = np.polyfit(np.array([self.EAMIN[0, 0], self.EAMED[0, 0], self.EAMAX[0, 0]]),
                               np.array([evmin_min, evmin_med, evmin_max]), deg=2)

        self.ParamEVMin = param

    def CalcParamEVP(self, usinas: List[hidr]):

        self.EVP = np.zeros((1, 12), 'd')
        self.ParamEVP = np.zeros((3, 12), 'd')

        for imes in range(12):
            evp_max = 0
            evp_min = 0
            evp_med = 0
            for iusina in usinas:
                if iusina.Ree == self.Codigo:
                    area_max = iusina.PolCotaArea[0] + iusina.PolCotaArea[1] * iusina.CotaMax + iusina.PolCotaArea[
                        2] * iusina.CotaMax ** 2 + \
                               iusina.PolCotaArea[3] * iusina.CotaMax ** 3 + iusina.PolCotaArea[4] * iusina.CotaMax ** 4
                    area_min = iusina.PolCotaArea[0] + iusina.PolCotaArea[1] * iusina.CotaMin + iusina.PolCotaArea[
                        2] * iusina.CotaMin ** 2 + \
                               iusina.PolCotaArea[3] * iusina.CotaMin ** 3 + iusina.PolCotaArea[4] * iusina.CotaMin ** 4
                    cota_med = iusina.PolCotaVol[0] + iusina.PolCotaVol[1] * (iusina.VolUtil * 0.65) + \
                               iusina.PolCotaVol[2] * (iusina.VolUtil * 0.65) ** 2 + \
                               iusina.PolCotaVol[3] * (iusina.VolUtil * 0.65) ** 3 + iusina.PolCotaVol[4] * (
                                       iusina.VolUtil * 0.65) ** 4
                    area_med = iusina.PolCotaArea[0] + iusina.PolCotaArea[1] * cota_med + iusina.PolCotaArea[
                        2] * cota_med ** 2 + \
                               iusina.PolCotaArea[3] * cota_med ** 3 + iusina.PolCotaArea[4] * cota_med ** 4

                    evp_med += (1 / (1000 * 2.63)) * area_med * iusina.RoAcum[0, 0]
                    evp_max += (1 / (1000 * 2.63)) * area_max * iusina.RoAcumMax[0, 0]
                    evp_min += (1 / (1000 * 2.63)) * area_min * iusina.RoAcumMin[0, 0]

            self.EVP[0, imes] = evp_med

            if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
                param = np.array([0., 0., evp_med])
            else:
                param = np.polyfit(np.array([self.EAMIN[0, 0], self.EAMED[0, 0], self.EAMAX[0, 0]]),
                                   np.array([evp_min, evp_med, evp_max]), deg=2)

            self.ParamEVP[:, imes] = param

    def CalcEVM(self, usinas: List[hidr]):

        self.EVM = np.zeros((5, 12), 'd')

        for iusina in usinas:
            if iusina.Ree == self.Codigo:
                for iano in range(5):
                    for imes in range(12):
                        self.EVM[iano, imes] += (1 / 2.63) * iusina.VolMortoTempo[iano, imes] * iusina.RoAcum[0, 0]

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
                    if iusina.VolUtil > 0 and iusina.Ree == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        FioJusante[iano][imes] = FioJusante[iano][imes] + iusina.RoAcum_B_Ree[iano][
                            imes] * iusina.VolUtil / 2.63
                        ContJusante[iano][imes] = ContJusante[iano][imes] + iusina.RoAcum_C_Ree[iano][
                            imes] * iusina.VolUtil / 2.63

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

        titulo = 'Evolucao da Energia Armazenavel Maxima \n do Reser. Equiv. de Energia ' + self.Nome
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armaz. Maxima (MWmes)', fontsize=14)
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
        tituloENA = 'ENA do REE ' + self.Nome
        tituloEC = 'EC do REE ' + self.Nome
        tituloEFIO = 'EFIO do REE ' + self.Nome
        ax1.set_title(tituloENA, fontsize=13)
        ax2.set_title(tituloEC, fontsize=13)
        ax3.set_title(tituloEFIO, fontsize=13)

        plt.show()
