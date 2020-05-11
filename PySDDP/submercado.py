import numpy as np
from matplotlib import pyplot as plt
from typing import List
from PySDDP.hidr import hidr
from scipy import stats
from math import sqrt
from scipy.optimize import minimize
from scipy.stats import chi2
import random as rd
from timeit import default_timer as timer
import math
from calendar import monthrange


class submercado(object):
    # Classe contendo informacoes sobre os arquivos de entrada e saida
    Codigo = None
    Nome = None
    Mercado = None
    NaoSimuladas = None
    Ficticio = None

    # Parametros Temporais
    EAIni = None  # Energia Armazenavel Inicial
    EAMAX = None  # Energia Armazenavel Maxima (iano,imes)
    EAMIN = None  # Energia Armazenavel Mínima (iano,imes)
    EAMED = None  # Energia Armazenavel Média (iano,imes)
    ENA = None
    EFIO = None
    FatorSeparacao = None
    ParamFC = None
    ParamEVMin = None
    ParamGHMAX = None
    EDESVC = None
    EDESVF = None
    GHMAX = None
    GTMIN = None
    EVMin = None
    EVP = None
    ParamEVP = None
    EC = None
    EVM = None

    def __init__(self, nanos):
        self.Mercado = np.zeros((nanos + 1, 12), 'd')
        self.NaoSimuladas = np.zeros((nanos, 12), 'd')
        self.CustoDeficit = np.zeros(4, 'd')
        self.ProfundidadeDeficit = np.zeros(4, 'd')

    def CalcENA(self, usinas: List[hidr]):

        anos_hist = len(usinas[0].Vazoes)

        self.ENA = np.zeros((anos_hist, 12), 'd')
        self.EC = np.zeros((anos_hist, 12), 'd')
        self.EFIO = np.zeros((anos_hist, 12), 'd')

        # self.EC2 = np.zeros((anos_hist, 12), 'd')
        # self.EFIO2 = np.zeros((anos_hist, 12), 'd')
        # self.EFIOB = np.zeros((anos_hist, 12), 'd')

        for iano in range(anos_hist):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.Sist == self.Codigo:
                        if iusina.TipoReg == b'M':
                            self.EC[iano, imes] = self.EC[iano, imes] + iusina.RoAcum[0, 0] * iusina.QIncHistEntreRes(
                                usinas, iano, imes)
                            # self.EC2[iano, imes] = self.EC2[iano, imes] + iusina.RoAcumFiodAguaEquiv[0, 0]*iusina.Vazoes[iano, imes]
                        else:
                            self.EFIO[iano, imes] = self.EFIO[iano, imes] + iusina.RoEquiv[
                                0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
                            # parc_1 = iusina.Engolimento - iusina.QMin(usinas, iano, imes)
                            # parc_2 = iusina.Vazoes[iano, imes] - iusina.QMontante(usinas, iano, imes)
                            # # parc_2 = iusina.QIncHistEntreRes(usinas, iano, imes)
                            # self.EFIO2[iano, imes] = self.EFIO2[iano, imes] + iusina.RoEquiv[0, 0]*min(parc_1, parc_2)
                            # self.EFIOB[iano, imes] = self.EFIOB[iano, imes] + iusina.RoEquiv[0, 0]*parc_2

        self.ENA = self.EC + self.EFIO
        # self.ENA2 = self.EC2 + self.EFIO2

        # print('teste')

        ###############################################################################################
        ########## Modelo de geração de séries sintéticas de vento/densidade de potência ##############
        ###############################################################################################

    def CalcEArmIni(self, usinas: List[hidr], ano_ini):
        self.EAIni = 0.
        # FATOR = 24*60*60*monthrange(ano_ini+iano, imes+1)[1]/1000000
        FATOR = 2.63
        for iusina in usinas:
            if iusina.TipoReg == b'M' and iusina.Sist == self.Codigo and iusina.StatusVolMorto[0][0] == 2:
                self.EAIni = self.EAIni + (1 / FATOR) * iusina.RoAcum[0][0] * (iusina.VolIni / 100) * iusina.VolUtil

    def CalcEArmMax(self, usinas: List[hidr], ano_ini):
        self.EAMAX = np.zeros((5, 12), 'd')
        for iano in range(5):
            for imes in range(12):
                # FATOR = 24*60*60*monthrange(ano_ini+iano, imes+1)[1]/1000000
                FATOR = 2.63
                for iusina in usinas:
                    if iusina.TipoReg == b'M' and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EAMAX[iano][imes] = self.EAMAX[iano][imes] + (1 / FATOR) * iusina.RoAcum[iano][
                            imes] * iusina.VolUtil

    def CalcEArmMin(self, usinas: List[hidr]):
        self.EAMIN = np.zeros((5, 12), 'd')
        for iano in range(5):
            for imes in range(12):
                # FATOR = 24*60*60*monthrange(ano_ini+iano, imes+1)[1]/1000000
                FATOR = 2.63
                for iusina in usinas:
                    if iusina.TipoReg == b'M' and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EAMIN[iano][imes] = self.EAMIN[iano][imes] + (1 / FATOR) * iusina.RoAcumOperEquiv[iano][
                            imes] * (iusina.VolMinP[iano, imes] - iusina.VolMin)
                        # print(f'VolMinP - VOlMin: {iusina.VolMinP[iano, imes] - iusina.VolMin}   -> {iusina.Nome}')
                        # print('teste')

        # print('teste')

    def CalcEArmMed(self, usinas: List[hidr], ano_ini):
        self.EAMED = np.zeros((5, 12), 'd')
        for iano in range(5):
            for imes in range(12):
                # FATOR = 24*60*60*monthrange(ano_ini+iano, imes+1)[1]/1000000
                FATOR = 2.63
                for iusina in usinas:
                    if iusina.TipoReg == b'M' and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
                        self.EAMED[iano][imes] = self.EAMED[iano][imes] + (1 / FATOR) * iusina.RoAcum50[iano][
                            imes] * iusina.VolUtil * 0.5

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

        anos_hist = len(usinas[0].Vazoes)

        self.ParamFC = np.zeros((3, 12), 'd')

        for imes in range(12):
            aux_1 = 0
            aux_2 = 0
            aux_3 = 0
            aux_4 = 0
            for iano in range(anos_hist):
                for iusina in usinas:
                    if iusina.Sist == self.Codigo and iusina.TipoReg == b'M':
                        aux_1 += iusina.RoAcumMax[0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
                        aux_2 += iusina.RoAcumMin[0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
                        aux_3 += iusina.RoAcumMed[0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
                        aux_4 += iusina.RoAcum[0, 0] * iusina.QIncHistEntreRes(usinas, iano, imes)
            fcmax = aux_1 / aux_4
            fcmin = aux_2 / aux_4
            fcmed = aux_3 / aux_4

            if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
                param = np.array([0., 0., fcmin])
            else:
                param = np.polyfit(np.array([0, self.EAMED[0, 0], self.EAMAX[0, 0]]), np.array([fcmin, fcmed, fcmax]),
                                   deg=2)

            self.ParamFC[:, imes] = param

    def CalcParamEVMin(self, usinas: List[hidr]):

        self.EVMin = np.zeros((1, 12))
        self.ParamEVMin = np.zeros((3, 12))

        for imes in range(12):
            evmin_max = 0
            evmin_min = 0
            evmin_med = 0
            for iusina in usinas:
                if iusina.Sist == self.Codigo and iusina.TipoReg == b'M':
                    # self.EVMin[0, imes] += np.mean(iusina.VazMinT[:, imes] * iusina.RoAcumFiodAguaEquiv[:, imes])
                    # evmin_max += np.mean(iusina.VazMinT[:, imes] * iusina.RoAcumFiodAguaMax[:, imes])
                    # evmin_min += np.mean(iusina.VazMinT[:, imes] * iusina.RoAcumFiodAguaMin[:, imes])
                    # evmin_med += np.mean(iusina.VazMinT[:, imes] * iusina.RoAcumFiodAguaMed[:, imes])

                    self.EVMin[0, imes] += iusina.VazMin * iusina.RoAcumFiodAguaEquiv[0, imes]
                    evmin_max += iusina.VazMin * iusina.RoAcumFiodAguaMax[0, imes]
                    evmin_min += iusina.VazMin * iusina.RoAcumFiodAguaMin[0, imes]
                    evmin_med += iusina.VazMin * iusina.RoAcumFiodAguaMed[0, imes]

            if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
                param = np.array([0., 0., evmin_min])
            else:
                param = np.polyfit(np.array([0, self.EAMED[0, 0], self.EAMAX[0, 0]]),
                                   np.array([evmin_min, evmin_med, evmin_max]), deg=2)

            # self.ParamEVMin[:, imes] = param
            self.ParamEVMin[:, imes] = np.zeros(3)

    def CalcVazDesv(self, usinas: List[hidr]):

        self.EDESVC = np.zeros((5, 12), 'd')
        self.EDESVF = np.zeros((5, 12), 'd')

        for iano in range(5):
            for imes in range(12):
                for iusina in usinas:
                    if iusina.Sist == self.Codigo:
                        self.EDESVC[iano][imes] += iusina.RoAcumDesvAguaEquiv[iano, imes] * iusina.VazDesv[iano, imes]
                        if iusina.TipoReg != b'M':
                            self.EDESVF[iano][imes] += iusina.RoAcumFiodAguaEquiv[iano, imes] * iusina.VazDesv[
                                iano, imes]

    def CalcParamGHMAX(self, usinas: List[hidr]):

        GHMAX_max = 0
        GHMAX_min = 0
        GHMAX_med = 0
        for iusina in usinas:
            if iusina.Sist == self.Codigo:
                if iusina.TipoTurb != 0:

                    if iusina.TipoTurb == 1:
                        const_turb = 1.5
                    elif iusina.TipoTurb == 2:
                        const_turb = 1.2
                    elif iusina.TipoTurb == 3:
                        const_turb = 1.5

                    if iusina.TipoPerda == 2:
                        hliq_max = iusina.CotaMax - iusina.CFMed - iusina.PerdaHid
                        hliq_med = iusina.CotaMed - iusina.CFMed - iusina.PerdaHid
                        hliq_min = iusina.CotaMin - iusina.CFMed - iusina.PerdaHid

                    else:
                        hliq_max = (iusina.CotaMax - iusina.CFMed) * (1. - iusina.PerdaHid / 100)
                        hliq_med = (iusina.CotaMed - iusina.CFMed) * (1. - iusina.PerdaHid / 100)
                        hliq_min = (iusina.CotaMin - iusina.CFMed) * (1. - iusina.PerdaHid / 100)

                    pnom_max, pnom_min, pnom_med = 0, 0, 0
                    for maq in range(iusina.NumConjMaq):
                        # pnom_max += iusina.MaqporConj[maq]*iusina.PEfporConj[maq]*min(1, ((iusina.CotaMax)/iusina.AltEfetConj[maq])**const_turb)
                        # pnom_min += iusina.MaqporConj[maq]*iusina.PEfporConj[maq]*min(1, ((iusina.CotaMin)/iusina.AltEfetConj[maq])**const_turb)
                        # pnom_med += iusina.MaqporConj[maq]*iusina.PEfporConj[maq]*min(1, ((iusina.CotaMed)/iusina.AltEfetConj[maq])**const_turb)

                        pnom_max += iusina.MaqporConj[maq] * iusina.PEfporConj[maq] * min(1, (
                                    iusina.CotaMax / iusina.AltEfetConj[maq]) ** const_turb)
                        pnom_min += iusina.MaqporConj[maq] * iusina.PEfporConj[maq] * min(1, (
                                    iusina.CotaMin / iusina.AltEfetConj[maq]) ** const_turb)
                        pnom_med += iusina.MaqporConj[maq] * iusina.PEfporConj[maq] * min(1, (
                                    iusina.CotaMed / iusina.AltEfetConj[maq]) ** const_turb)

                    GHMAX_max += (1 - (iusina.TEIF / 100)) * (1 - (iusina.IP / 100)) * pnom_max
                    GHMAX_min += (1 - (iusina.TEIF / 100)) * (1 - (iusina.IP / 100)) * pnom_min
                    GHMAX_med += (1 - (iusina.TEIF / 100)) * (1 - (iusina.IP / 100)) * pnom_med

                    # GHMAX_max += pnom_max
                    # GHMAX_min += pnom_min
                    # GHMAX_med += pnom_med

        self.GHMAX = GHMAX_max
        if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
            param = np.array([0., 0., GHMAX_med])
        else:
            param = np.polyfit(np.array([0, self.EAMED[0, 0], self.EAMAX[0, 0]]),
                               np.array([GHMAX_min, GHMAX_med, GHMAX_max]), deg=2)

        self.ParamGHMAX = param

    def CalcGTMin(self, usinas):

        self.GTMIN = np.zeros((5, 12))
        for iusina in usinas:
            if iusina.Sist == self.Codigo:
                self.GTMIN += iusina.GTMin

    def CalcParamEVP(self, usinas: List[hidr]):

        self.EVP = np.zeros((1, 12), 'd')
        self.ParamEVP = np.zeros((3, 12), 'd')

        for imes in range(12):
            # FATOR = 24 * 60 * 60 * monthrange(2019, imes + 1)[1] / 1000000
            FATOR = 2.63
            evp_max = 0
            evp_min = 0
            evp_med = 0
            for iusina in usinas:
                if iusina.Sist == self.Codigo and iusina.TipoReg == b'M':
                    area_max, area_min, cota_med, area_med = 0, 0, 0, 0
                    for i in range(5):
                        area_max += iusina.PolCotaArea[i] * (iusina.CotaMax ** i)
                        area_min += iusina.PolCotaArea[i] * (iusina.CotaMin ** i)
                        area_med += iusina.PolCotaArea[i] * (iusina.CotaMed ** i)

                    evp_med += (1 / (1000 * FATOR)) * iusina.CoefEvap[imes] * area_med * iusina.RoAcumMed[0, 0]
                    evp_max += (1 / (1000 * FATOR)) * iusina.CoefEvap[imes] * area_max * iusina.RoAcumMax[0, 0]
                    evp_min += (1 / (1000 * FATOR)) * iusina.CoefEvap[imes] * area_min * iusina.RoAcumMin[0, 0]

            self.EVP[0, imes] = evp_med

            if self.EAMAX[0, 0] == 0 and self.EAMIN[0, 0] == 0 and self.EAMED[0, 0] == 0:
                param = np.array([0., 0., evp_min])
            else:
                param = np.polyfit(np.array([0, self.EAMED[0, 0], self.EAMAX[0, 0]]),
                                   np.array([evp_min, evp_med, evp_max]), deg=2)

            self.ParamEVP[:, imes] = param

    def CalcEVM(self, usinas: List[hidr], ano_ini):

        self.EVM = np.zeros((5, 12), 'd')

        for iusina in usinas:
            if iusina.Sist == self.Codigo:
                for iano in range(5):
                    for imes in range(12):
                        # FATOR = 24 * 60 * 60 * monthrange(ano_ini+iano, imes + 1)[1] / 1000000
                        FATOR = 2.63
                        self.EVM[iano, imes] += (1 / FATOR) * iusina.VolMortoTempo[iano, imes] * iusina.RoAcum[
                            iano, imes]

    def parp(self, dados, ord_max):

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max), 'd')
        for ilag in range(ord_max):
            for imes in range(12):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (dados[iano][imes] - media[imes]) * (
                                dados[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

        # Calcula funcao de auto-correlacao parcial (uma para cada mes)
        self.FACP = np.zeros((12, ord_max), 'd')
        for ilag in np.arange(1, ord_max + 1):
            for imes in range(12):
                A = np.eye(ilag)
                B = np.zeros(ilag)
                # Preenche matriz triangular superior
                for ilin in range(len(A)):
                    for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                        if icol > ilin:
                            mes = imes - ilin - 1
                            if mes < 0:
                                mes = mes + 12
                            A[ilin][icol] = self.FAC[mes][icol - ilin - 1]
                    B[ilin] = self.FAC[imes][ilin]
                # Preenche matriz triangular inferior
                for ilin in range(len(A)):
                    for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                        if icol < ilin:
                            A[ilin][icol] = A[icol][ilin]
                phi = np.linalg.solve(A, B)
                self.FACP[imes][ilag - 1] = phi[-1]

        # Identificacao da ordem
        IC = 1.96 / math.sqrt(nanos - 1)
        self.Ordem = np.zeros(12, 'i')
        for imes in range(12):
            self.Ordem[imes] = 0
            for ilag in range(ord_max):
                if self.FACP[imes][ilag] > IC or self.FACP[imes][ilag] < -IC:
                    self.Ordem[imes] = ilag + 1

        # ############## GRAFICO AUTOCORRELACAO #############
        # meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        # for imes in range(12):
        #
        #     cores = []
        #     limitesup = []
        #     limiteinf = []
        #     for elemento in self.FACP[imes]:
        #         limitesup.append(IC)
        #         limiteinf.append(-IC)
        #         if elemento > IC or elemento < -IC:
        #             cores.append('r')
        #         else:
        #             cores.append('b')
        #
        #     f, ax2 = plt.subplots(1, 1, sharey=True)
        #     barWidth = 0.40
        #
        #     # titulo = 'Função de Autocorrelação Parcial - ' + meses[imes]
        #     # f.canvas.set_window_title(titulo)
        #
        #     # ax1.bar(np.arange(1, ord_max + 1), self.FAC[imes], barWidth, align='center')
        #     ax2.bar(np.arange(1, ord_max + 1), self.FACP[imes], barWidth, align='center', color=cores)
        #     ax2.plot(np.arange(1, ord_max + 1), limitesup, 'm--', lw=1, label='$IC=\dfrac{1,96}{\sqrt{N}}$')
        #     ax2.plot(np.arange(1, ord_max + 1), limiteinf, 'm--', lw=1)
        #
        #     # ax1.set_xticks(np.arange(1, ord_max + 1))
        #     ax2.set_xticks(np.arange(1, ord_max + 1))
        #     # tituloFAC = 'Função Autocorrelação'
        #     tituloFACP = 'Função Autocorrelação Parcial - ' + meses[imes]
        #     # # ax1.set_title(tituloFAC, fontsize=13)
        #     ax2.set_title(tituloFACP, fontsize=13)
        #     # ax1.set_xlabel('Lag')
        #     ax2.set_xlabel('Lag')
        #     plt.legend()
        #     plt.tight_layout()
        #     # ax1.ylabel('Autocorrelacao e Autocorrelacao Parcial')
        #
        #     plt.show()
        #
        #     galo = 13

        ###################################################

        # Calculo dos coeficientes
        self.CoefParp = np.zeros((12, ord_max), 'd')
        for imes in range(12):
            ilag = self.Ordem[imes]
            A = np.eye(ilag)
            B = np.zeros(ilag)
            # Preenche matriz triangular superior
            for ilin in range(len(A)):
                for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                    if icol > ilin:
                        mes = imes - ilin - 1
                        if mes < 0:
                            mes = mes + 12
                        A[ilin][icol] = self.FAC[mes][icol - ilin - 1]
                B[ilin] = self.FAC[imes][ilin]
            # Preenche matriz triangular inferior
            for ilin in range(len(A)):
                for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                    if icol < ilin:
                        A[ilin][icol] = A[icol][ilin]
            phi = np.linalg.solve(A, B)
            for iord in range(len(phi)):
                self.CoefParp[imes][iord] = phi[iord]

    def parp_bat(self, dados, ord_max):

        np.random.seed(1234)

        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def bat(dados, D, imes, Np, MaxIter, Amp, Pul, lb, ub):

            Q = np.zeros(Np)  # frequency
            Amplitude = np.ones(Np)  # vetor de loudness
            Pulso = np.zeros(Np)  # vetor de rate

            v = np.zeros((Np, D))  # velocity
            Sol = np.zeros((Np, D))  # population of solutions
            Fitness = np.zeros(Np)  # fitness

            # Incializacao das particulas, Amplitude, Pulso e Fitness
            for i in range(Np):
                Sol[i] = lb + (ub - lb) * np.random.uniform(0, 1, D)
                Fitness[i] = Fun(Sol[i], dados, D, imes)

            # Encontrar melhor solucao
            idx = np.argmin(Fitness)
            best = Sol[idx]

            # Inicio do Bat Algorithm
            iter = 0
            fmin = 99999999
            while iter < MaxIter and fmin > 0.001:

                for w in range(Np):

                    Q[w] = np.random.uniform(0, 1)
                    v[w] = v[w] + (Sol[w] - best) * Q[w]
                    SolTemp = Sol[w] + v[w]

                    if np.random.uniform(0, 1) > Pulso[w]:

                        for j in range(D):
                            SolTemp[j] = best[j] + (-1 + 2 * np.random.random_sample()) * np.mean(Amplitude)
                            SolTemp[j] = verifica_limites(SolTemp[j], lb[j], ub[j])

                    for j in range(D):
                        SolTemp[j] = verifica_limites(SolTemp[j], lb[j], ub[j])

                    Fnew = Fun(SolTemp, dados, D, imes)

                    if Fnew <= Fitness[w] or np.random.uniform(0, 1) < Amplitude[w]:
                        Sol[w] = SolTemp
                        Fitness[w] = Fnew
                        Pulso[w] = 1 - np.exp(-Pul * (iter + 1))
                        Amplitude[w] = Amp * Amplitude[w]

                    if Fnew < fmin:
                        fmin = Fnew
                        best = SolTemp

                iter += 1

            return fmin, best

        def verifica_limites(sol, lb, ub):

            if sol > ub:
                sol = ub

            if sol < lb:
                sol = lb

            return sol

        def Fun(x, dados, ord_max, imes):

            nanos = len(dados)

            media = np.mean(dados, axis=0)
            desv_pad = np.std(dados, axis=0)

            # Calcula funcao de auto-correlacao (uma para cada mes)
            FAC = np.zeros(ord_max, 'd')
            for ilag in range(ord_max):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    FAC[ilag] += (dados[iano][imes] - media[imes]) * (dados[ano_ant][mes_ant] - media[mes_ant])
                FAC[ilag] /= ((nanos - 1) * desv_pad[imes] * desv_pad[mes_ant])

            # # Calcula a variância do ruido
            variancia_ruido = 1
            for icoef in range(ord_max):
                variancia_ruido -= x[icoef] * FAC[icoef]
            # variancia_ruido = (desv_pad[imes] ** 2) * (1 + np.sum(FAC))  # outra fórmula
            if variancia_ruido <= 0 or variancia_ruido > 0.001 * (desv_pad[imes] ** 2):
                penal = 99999  # variancia_ruido = 1e-6
            else:
                penal = 0

            # Calcula a variância do ruido (método de Ricardo Reis, doutorado USP)
            # variancia_ruido = (desv_pad[imes] **2) * (1 + np.sum(FAC))

            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = (dados[iano][imes] - media[imes]) / desv_pad[imes]
                for ilag in range(ord_max):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= x[ilag] * ((dados[ano_ant][mes_ant] - media[mes_ant]) / desv_pad[mes_ant])
                residuos[iano - 1] = somatorio

            # Autocorrelação
            autocorrelacao = 0
            # ord_max = int(nanos/2)
            # ord_max = nanos-2
            ord_max = 6
            for ilag in range(ord_max):
                somatorio = 0
                for iano in np.arange(ilag, nanos - 1):
                    somatorio += residuos[iano] * residuos[iano - ilag - 1]
                somatorio /= (nanos - 1 - ilag)
                autocorrelacao += np.abs(somatorio)

            var_ruido_norm = (desv_pad / np.max(desv_pad)) ** 2

            fob = np.abs(np.var(residuos)) + np.abs(np.mean(residuos)) + autocorrelacao  # - variancia_ruido
            fob = fob + penal

            return fob

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max), 'd')
        for ilag in range(ord_max):
            for imes in range(12):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (dados[iano][imes] - media[imes]) * (
                            dados[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.Ordem = np.zeros(12, 'i')  # comentar se for usar outro metodo
        self.FOB = np.zeros(12, 'd')
        print('Modelo PAR(p)-BAT em execução....')
        for imes in range(12):
            # print('*******', imes + 1)
            best = 99999999
            t = timer()
            # for iord in np.arange(self.Ordem[imes], self.Ordem[imes]+1):
            for iord in np.arange(1, ord_max + 1):

                # Define limites e condicao inicial
                lb = np.zeros(iord)
                ub = np.zeros(iord)
                for i in range(iord):
                    lb[i] = -2
                    ub[i] = 2

                fitness, coef = bat(dados, iord, imes, 50, 20, 0.5, 0.1, lb, ub)

                if fitness < best:
                    best = fitness
                    ordem = iord
                    COEF = coef

            for iord in range(ordem):
                self.CoefParp[imes, iord] = COEF[iord]
            self.Ordem[imes] = ordem
            self.FOB[imes] = best

            print('Mês ' + str(imes + 1) + ' - Tempo: ', round(timer() - t, 2), 'seg')

        print('Aplicação do PAR(p)-BAT: OK')

    def gera_series_sinteticas_sem_tendencia(self, dados, nr_ser, nr_meses=60, plot: bool = False):

        np.random.seed(1234)

        nanos = len(dados)
        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calculo dos residuos
        self.residuos = np.zeros((nanos - 1, 12))
        for iano in np.arange(1, nanos):
            for imes in range(12):
                self.residuos[iano - 1][imes] = (dados[iano][imes] - media[imes]) / desvio[imes]
                somatorio = 0
                for ilag in np.arange(1, self.Ordem[imes]):
                    ano_ant = iano
                    mes_ant = imes - ilag
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    somatorio += self.CoefParp[imes][ilag] * (dados[ano_ant][mes_ant] - media[mes_ant]) / desvio[
                        mes_ant]
                self.residuos[iano - 1][imes] = self.residuos[iano - 1][imes] - somatorio

        desvio_ruido = np.ones(12)
        for imes in range(12):
            for icoef in range(int(self.Ordem[imes])):
                desvio_ruido[imes] -= self.CoefParp[imes][icoef] * self.FAC[imes][icoef]
            desvio_ruido[imes] = np.sqrt(desvio_ruido[imes])

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for irod in range(2):
            for iser in range(nr_ser):
                contador = -1
                for iano in range(int(nr_meses / 12)):
                    for imes in range(12):
                        contador += 1
                        delta = - media[imes] / desvio[imes]
                        valor = media[imes]
                        somatorio = 0
                        for ilag in range(int(self.Ordem[imes])):
                            mes_ant = imes - ilag - 1
                            ano_ant = iano
                            if mes_ant < 0:
                                mes_ant += 12
                                ano_ant -= 1
                            if (ano_ant < 0) and (irod == 0):
                                ventoant = media[mes_ant]
                            else:
                                ventoant = sintetica_adit[iser][contador - ilag - 1]
                            delta -= self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[mes_ant]
                            somatorio += self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[mes_ant]
                        valor += desvio[imes] * somatorio
                        teta = 1 + ((desvio_ruido[imes] ** 2) / ((-delta) ** 2))
                        mu = (1 / 2) * np.log((desvio_ruido[imes] ** 2) / (teta * (teta - 1)))
                        # mu = 0
                        sigma = np.sqrt(np.log(teta))  # np.sqrt()
                        epsilon = np.random.normal(mu, sigma, 1)
                        ruido = np.exp(epsilon) + delta
                        valor += desvio[imes] * ruido
                        sintetica_adit[iser][contador] = valor

        if plot:

            x_axis = np.arange(1, nr_meses + 1)
            plt.figure()
            plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
            plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
            plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                     label='Desvio Padrão - Séries Sintéticas')
            plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
            m = media
            d = desvio
            for iano in range(int(nr_meses / 12) - 1):
                m = np.concatenate([m, media])
                d = np.concatenate([d, desvio])
            plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
            plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
            plt.plot(x_axis, m - d, 'bo', lw=2)
            titulo = f"Séries Sintéticas de ENA - {self.Nome}"
            plt.title(titulo, fontsize=12)
            plt.xlabel('Meses', fontsize=10)
            plt.ylabel('$MWmed$', fontsize=10)
            plt.legend(loc='upper center', fontsize=10, ncol=2)
            plt.tight_layout()
            plt.show()

        self.series_sinteticas = sintetica_adit

    def parp_alexandre(self, dados, ord_max):

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max), 'd')
        for ilag in range(ord_max):
            for imes in range(12):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (dados[iano][imes] - media[imes]) * (
                            dados[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

        # Calcula funcao de auto-correlacao parcial (uma para cada mes)
        self.FACP = np.zeros((12, ord_max), 'd')
        for ilag in np.arange(1, ord_max + 1):
            for imes in range(12):
                A = np.eye(ilag)
                B = np.zeros(ilag)
                # Preenche matriz triangular superior
                for ilin in range(len(A)):
                    for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                        if icol > ilin:
                            mes = imes - ilin - 1
                            if mes < 0:
                                mes = mes + 12
                            A[ilin][icol] = self.FAC[mes][icol - ilin - 1]
                    B[ilin] = self.FAC[imes][ilin]
                # Preenche matriz triangular inferior
                for ilin in range(len(A)):
                    for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                        if icol < ilin:
                            A[ilin][icol] = A[icol][ilin]
                phi = np.linalg.solve(A, B)
                self.FACP[imes][ilag - 1] = phi[-1]

        # Identificacao da ordem
        IC = 1.96 / sqrt(nanos - 1)
        self.Ordem = np.zeros(12, 'i')
        for imes in range(12):
            self.Ordem[imes] = 0
            for ilag in range(ord_max):
                if self.FACP[imes][ilag] > IC or self.FACP[imes][ilag] < -IC:
                    self.Ordem[imes] = ilag + 1

        # Calculo dos coeficientes
        self.CoefParp = np.zeros((12, ord_max), 'd')
        for imes in range(12):
            ilag = self.Ordem[imes]
            A = np.eye(ilag)
            B = np.zeros(ilag)
            # Preenche matriz triangular superior
            for ilin in range(len(A)):
                for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                    if icol > ilin:
                        mes = imes - ilin - 1
                        if mes < 0:
                            mes = mes + 12
                        A[ilin][icol] = self.FAC[mes][icol - ilin - 1]
                B[ilin] = self.FAC[imes][ilin]
            # Preenche matriz triangular inferior
            for ilin in range(len(A)):
                for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                    if icol < ilin:
                        A[ilin][icol] = A[icol][ilin]
            phi = np.linalg.solve(A, B)
            for iord in range(len(phi)):
                self.CoefParp[imes][iord] = phi[iord]

    def parp_otimo_alexandre(self, dados, ord_max):

        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def objetivo(x, dados, ord_max, imes):

            nanos = len(dados)

            media = np.mean(dados, axis=0)
            desv_pad = np.std(dados, axis=0)

            # Calcula funcao de auto-correlacao
            FAC = np.zeros(ord_max, 'd')
            for ilag in range(ord_max):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    FAC[ilag] += (dados[iano][imes] - media[imes]) * (dados[ano_ant][mes_ant] - media[mes_ant])
                FAC[ilag] /= ((nanos - 1) * desv_pad[imes] * desv_pad[mes_ant])

            # TODO: Montagem da FOB
            coef = np.zeros(ord_max, 'd')
            for icoef in range(ord_max):
                coef[icoef] = x[icoef]

            # Calcula o desvio padrão do ruido
            variancia_ruido = 1
            for icoef in range(len(coef)):
                variancia_ruido -= coef[icoef] * FAC[icoef]
            # variancia_ruido = (desv_pad[imes] ** 2) * (1 + np.sum(FAC))  # outra fórmula

            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = (dados[iano][imes] - media[imes]) / desv_pad[imes]
                for ilag in range(ord_max):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= coef[ilag] * ((dados[ano_ant][mes_ant] - media[mes_ant]) / desv_pad[mes_ant])
                residuos[iano - 1] = somatorio

            # Autocorrelação
            autocorrelacao = 0
            for ilag in range(ord_max):
                somatorio = 0
                for iano in np.arange(ord_max, nanos - 1):
                    somatorio += residuos[iano] * residuos[iano - ilag - 1]
                autocorrelacao += np.abs(np.mean(somatorio))

            return np.abs(np.mean(residuos)) + np.abs((np.var(residuos) - variancia_ruido)) + autocorrelacao

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.Ordem = np.zeros(12, 'd')
        self.FOB = np.zeros(12, 'd')
        for imes in range(12):
            print('*******', imes + 1)
            best = 999999
            for iord in np.arange(1, (ord_max + 1)):

                # Define limites e condicao inicial
                x0 = np.zeros(iord)
                limites = []
                for i in range(iord):
                    x0[i] = 0.1
                    limites.append((-5, 5))

                solution = minimize(objetivo, x0, method='SLSQP', bounds=limites,
                                    args=(dados, iord, imes), options={'disp': False, 'maxiter': 10000})

                if solution.fun < best:
                    best = solution.fun
                    ordem = iord
                    COEF = solution.x

            for iord in range(ordem):
                self.CoefParp[imes, iord] = COEF[iord]
            self.Ordem[imes] = ordem
            self.FOB[imes] = best

        # USADA APENAS PARA GERAÇÃO DE SÉRIES SINTÉTICAS
        nanos = len(dados)
        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max), 'd')
        for ilag in range(ord_max):
            for imes in range(12):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (dados[iano][imes] - media[imes]) * (
                            dados[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

    def parp_otimo_bat_alexandre(self, dados, ord_max):

        np.random.seed(1234)

        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def bat(dados, D, imes, Np, MaxIter, Amp, Pul, lb, ub):

            Q = np.zeros(Np)  # frequency
            Amplitude = Amp * np.ones(Np)  # vetor de loudness
            Pulso = Pul * np.ones(Np)  # vetor de rate

            v = np.zeros((Np, D))  # velocity
            Sol = np.zeros((Np, D))  # population of solutions
            Fitness = np.zeros(Np)  # fitness

            # Incializacao das particulas, Amplitude, Pulso e Fitness
            for i in range(Np):
                Sol[i] = lb + (ub - lb) * np.random.uniform(0, 1, D)
                Fitness[i] = Fun(Sol[i], dados, D, imes)

            # Encontrar melhor solucao
            idx = np.argmin(Fitness)
            best = Sol[idx]

            # Inicio do Bat Algorithm
            iter = 0
            fmin = 99999999
            while iter < MaxIter and fmin > 0.001:

                for w in range(Np):

                    Q[w] = np.random.uniform(0, 1)
                    v[w] = v[w] + (Sol[w] - best) * Q[w]
                    SolTemp = Sol[w] + v[w]

                    if np.random.uniform(0, 1) > Pulso[w]:

                        for j in range(D):
                            SolTemp[j] = best[j] + np.random.uniform(-1, 1) * np.mean(Amplitude)
                            SolTemp[j] = verifica_limites(SolTemp[j], lb[j], ub[j])

                    for j in range(D):
                        SolTemp[j] = verifica_limites(SolTemp[j], lb[j], ub[j])

                    Fnew = Fun(SolTemp, dados, D, imes)

                    if Fnew <= Fitness[w] and np.random.uniform(0, 1) < Amplitude[w]:
                        Sol[w] = SolTemp
                        Fitness[w] = Fnew
                        Pulso[w] = 1 - np.exp(-0.9 * (iter + 1))
                        Amplitude[w] = 0.9 * Amplitude[w]

                        if Fnew < fmin:
                            fmin = Fnew
                            best = Sol[w]

                iter += 1

            print('iteracao: ', iter)

            return fmin, best

        def verifica_limites(sol, lb, ub):

            if sol > ub:
                sol = ub

            if sol < lb:
                sol = lb

            return sol

        def Fun(x, dados, ord_max, imes):

            nanos = len(dados)

            media = np.mean(dados, axis=0)
            desv_pad = np.std(dados, axis=0)

            # Calcula funcao de auto-correlacao
            FAC = np.zeros(ord_max, 'd')
            for ilag in range(ord_max):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    FAC[ilag] += (dados[iano][imes] - media[imes]) * (dados[ano_ant][mes_ant] - media[mes_ant])
                FAC[ilag] /= ((nanos - 1) * desv_pad[imes] * desv_pad[mes_ant])

            # # Calcula a variância do ruido
            variancia_ruido = 1
            for icoef in range(ord_max):
                variancia_ruido -= x[icoef] * FAC[icoef]
            if variancia_ruido < 0:
                penal = 9999999  # variancia_ruido = 1e-6
            else:
                penal = 0

            # Calcula a variância do ruido (método de Ricardo Reis, doutorado USP)
            # variancia_ruido = (desv_pad[imes] **2) * (1 + np.sum(FAC))

            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = (dados[iano][imes] - media[imes]) / desv_pad[imes]
                for ilag in range(ord_max):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= x[ilag] * ((dados[ano_ant][mes_ant] - media[mes_ant]) / desv_pad[mes_ant])
                residuos[iano - 1] = somatorio

            # Autocorrelação
            autocorrelacao = 0
            for ilag in range(ord_max):
                somatorio = 0
                for iano in np.arange(ord_max, nanos - 1):
                    somatorio += residuos[iano] * residuos[iano - ilag - 1]
                autocorrelacao += np.abs(np.mean(somatorio))

            fob = np.abs(np.mean(residuos)) + np.abs(np.var(residuos) - variancia_ruido)  # + autocorrelacao
            fob = fob + penal

            return fob

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.Ordem = np.zeros(12, 'd')
        self.FOB = np.zeros(12, 'd')
        for imes in range(12):
            print('*******', imes + 1)
            best = 99999999
            t = timer()
            for iord in np.arange(1, (ord_max + 1)):

                # Define limites e condicao inicial
                lb = np.zeros(iord)
                ub = np.zeros(iord)
                for i in range(iord):
                    lb[i] = -5
                    ub[i] = 5

                fitness, coef = bat(dados, iord, imes, 20, 100, 0.9, 0.1, lb, ub)

                if fitness < best:
                    best = fitness
                    ordem = iord
                    COEF = coef

            for iord in range(ordem):
                self.CoefParp[imes, iord] = COEF[iord]
            self.Ordem[imes] = ordem
            self.FOB[imes] = best

            print('Tempo/mês', round(timer() - t, 2), 'seg')

        # APENAS PARA SER USADA PELA GERAÇÃO DE SÉRIES
        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max), 'd')
        for ilag in range(ord_max):
            for imes in range(12):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (dados[iano][imes] - media[imes]) * (
                            dados[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

    def gera_series_aditivo_alexandre(self, dados, nr_ser, nr_meses):

        np.random.seed(1234)

        nanos = len(dados)
        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)
        assim = stats.skew(dados, axis=0)  # coeficiente de assimetria

        desvio_ruido = np.ones(12)
        for imes in range(12):
            for icoef in range(int(self.Ordem[imes])):
                desvio_ruido[imes] -= self.CoefParp[imes][icoef] * self.FAC[imes][icoef]
            desvio_ruido[imes] = np.sqrt(desvio_ruido[imes])

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for iser in range(nr_ser):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    delta = - media[imes] / desvio[imes]
                    valor = media[imes]
                    for ilag in range(int(self.Ordem[imes])):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            ventoant = media[mes_ant]
                        else:
                            ventoant = sintetica_adit[iser][contador - ilag - 1]
                        delta -= self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[mes_ant]
                        valor += desvio[imes] * self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[
                            mes_ant]
                    teta = 1 + ((desvio_ruido[imes] ** 2) / ((-delta) ** 2))
                    # aux1 = 1 + ((assim[imes] ** 2) / 2)
                    # aux2 = ((assim[imes] ** 2) + ((assim[imes] ** 4) / 4)) ** (1/2)
                    # teta = ((aux1 + aux2) ** (1/3)) + ((aux1 - aux2) ** (1/3)) - 1
                    mu = (1 / 2) * np.log((desvio_ruido[imes] ** 2) / (teta * (teta - 1)))
                    sigma = np.sqrt(np.log(teta))
                    # if sigma <= 0 or np.iscomplex(sigma) or teta <= 0:
                    #     print('sigma negativo ' + str(sigma))
                    # print('sigma = ' + str(sigma))
                    # print('teta = ' + str(teta))
                    # print('delta = ' + str(delta))
                    # print('desvio_ruido = ' + str(desvio_ruido))
                    epsilon = np.random.normal(mu, sigma, 1)
                    ruido = np.exp(epsilon) + delta  # desvio_ruido[imes] * np.random.normal(0, 1, 1)
                    valor += desvio[imes] * ruido
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_alexandre_sem_tendencia(self, dados, nr_ser, nr_meses):

        np.random.seed(1234)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        desvio_ruido = np.ones(12)
        for imes in range(12):
            for icoef in range(int(self.Ordem[imes])):
                desvio_ruido[imes] -= self.CoefParp[imes][icoef] * self.FAC[imes][icoef]
            desvio_ruido[imes] = np.sqrt(desvio_ruido[imes])

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for irod in range(2):
            for iser in range(nr_ser):
                contador = -1
                for iano in range(5):
                    for imes in range(12):
                        contador += 1
                        delta = - media[imes] / desvio[imes]
                        valor = media[imes]
                        for ilag in range(int(self.Ordem[imes])):
                            mes_ant = imes - ilag - 1
                            ano_ant = iano
                            if mes_ant < 0:
                                mes_ant += 12
                                ano_ant -= 1
                            if (ano_ant < 0) and (irod == 0):
                                ventoant = media[mes_ant]
                            else:
                                ventoant = sintetica_adit[iser][contador - ilag - 1]
                            delta -= self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[mes_ant]
                            valor += desvio[imes] * self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[
                                mes_ant]
                        teta = 1 + ((desvio_ruido[imes] ** 2) / ((-delta) ** 2))
                        mu = (1 / 2) * np.log((desvio_ruido[imes] ** 2) / (teta * (teta - 1)))
                        sigma = np.sqrt(np.log(teta))
                        epsilon = np.random.normal(mu, sigma, 1)
                        ruido = np.exp(epsilon) + delta
                        valor += desvio[imes] * ruido
                        sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_ricardo(self, dados, nr_ser, nr_meses):

        np.random.seed(1234)

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # PASSO 1: Ruídos
        ruidos = np.zeros((nanos - 1, 12))
        for imes in range(12):
            for iano in np.arange(1, nanos):
                somatorio = (dados[iano][imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= self.CoefParp[imes, ilag] * (
                            (dados[ano_ant][mes_ant] - media[mes_ant]) / desvio[mes_ant])
                ruidos[iano - 1, imes] = somatorio

        # PASSO 2: Média e variância do ruído
        media_ruido = np.mean(ruidos, axis=0)
        variancia_ruido = np.var(ruidos, axis=0)

        # PASSO 3: for para geração das séries
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        x0 = np.min(dados, axis=0)
        for iser in range(nr_ser):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    # PASSO: Estimativa de valor
                    valor = (media[imes] - x0[imes]) / desvio[imes]
                    for ilag in range(int(self.Ordem[imes])):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            ventoant = media[mes_ant]
                        else:
                            ventoant = sintetica_adit[iser][contador - ilag - 1]
                        valor += self.CoefParp[imes, ilag] * ((ventoant - media[mes_ant]) / desvio[mes_ant])

                    # PASSO 4: Estimativas dos parâmetros (teta, média e variância)
                    teta = 1 + (variancia_ruido[imes] / ((media_ruido[imes] - valor) ** 2))
                    var = np.log(teta)
                    med = 0.5 * np.log(variancia_ruido[imes] / ((teta ** 2) - teta))

                    # PASSO 6: Geração de números randômicos
                    num_rand = np.random.normal(med, np.sqrt(var), 1)

                    # PASSO 7: Geração da vazão sintética
                    sintetica_adit[iser, contador] = x0[imes] + desvio[imes] * np.exp(num_rand)

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_ricardo_sem_tendencia(self, dados, nr_ser, nr_meses):

        np.random.seed(1234)

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # PASSO 1: Ruídos
        ruidos = np.zeros((nanos - 1, 12))
        for imes in range(12):
            for iano in np.arange(1, nanos):
                somatorio = (dados[iano][imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= self.CoefParp[imes, ilag] * (
                            (dados[ano_ant][mes_ant] - media[mes_ant]) / desvio[mes_ant])
                ruidos[iano - 1, imes] = somatorio

        # PASSO 2: Média e variância do ruído
        media_ruido = np.mean(ruidos, axis=0)
        variancia_ruido = np.var(ruidos, axis=0)

        # PASSO 3: for para geração das séries
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        x0 = np.min(dados, axis=0)
        for irod in range(2):
            for iser in range(nr_ser):
                contador = -1
                for iano in range(5):
                    for imes in range(12):
                        contador += 1
                        # PASSO: Estimativa de valor
                        valor = (media[imes] - x0[imes]) / desvio[imes]
                        for ilag in range(int(self.Ordem[imes])):
                            mes_ant = imes - ilag - 1
                            ano_ant = iano
                            if mes_ant < 0:
                                mes_ant += 12
                                ano_ant -= 1
                            if ano_ant < 0 and irod == 0:
                                ventoant = media[mes_ant]
                            else:
                                ventoant = sintetica_adit[iser][contador - ilag - 1]
                            valor += self.CoefParp[imes, ilag] * ((ventoant - media[mes_ant]) / desvio[mes_ant])

                        # PASSO 4: Estimativas dos parâmetros (teta, média e variância)
                        teta = 1 + (variancia_ruido[imes] / ((media_ruido[imes] - valor) ** 2))
                        var = np.log(teta)
                        med = 0.5 * np.log(variancia_ruido[imes] / ((teta ** 2) - teta))

                        # PASSO 6: Geração de números randômicos
                        num_rand = np.random.normal(med, np.sqrt(var), 1)

                        # PASSO 7: Geração da vazão sintética
                        sintetica_adit[iser, contador] = x0[imes] + desvio[imes] * np.exp(num_rand)

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_flavia(self, dados, nr_ser, nr_meses):

        np.random.seed(1234)

        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)
        assim = stats.skew(dados, axis=0)  # coeficiente de assimetria

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for iser in range(nr_ser):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1

                    aux1 = 1 + ((assim[imes] ** 2) / 2)
                    aux2 = ((assim[imes] ** 2) + ((assim[imes] ** 4) / 4)) ** (1 / 2)
                    teta = ((aux1 + aux2) ** (1 / 3)) + ((aux1 - aux2) ** (1 / 3)) - 1
                    mu = (1 / 2) * np.log((desvio[imes] ** 2) / (teta * (teta - 1)))
                    sigma = np.sqrt(np.log(teta))
                    A = media[imes] - (desvio[imes] / ((teta - 1) ** (1 / 2)))
                    epsilon = np.random.normal(0, 1, 1)
                    sintetica_adit[iser][contador] = A + np.exp((epsilon * sigma) + mu)

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo(self, dados, nr_ser, nr_meses):

        rd.seed(1234)
        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calculo dos residuos
        residuos = np.zeros((nanos - 1, 12))
        for iano in np.arange(1, nanos):
            for imes in range(12):
                residuos[iano - 1][imes] = (dados[iano][imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    residuos[iano - 1][imes] -= self.CoefParp[imes][ilag] * (dados[ano_ant][mes_ant] - media[mes_ant]) / \
                                                desvio[mes_ant]

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for iser in range(nr_ser):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = rd.randint(0, nanos - 2)
                    valor = media[imes] + desvio[imes] * residuos[serie][imes]
                    for ilag in range(int(self.Ordem[imes])):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            ventoant = media[mes_ant]
                        else:
                            ventoant = sintetica_adit[iser][contador - 1 - ilag]
                        valor += desvio[imes] * self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[
                            mes_ant]
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_sem_tendencia(self, dados, nr_ser, nr_meses):

        rd.seed(1234)
        nanos = len(dados)

        media = np.mean(dados, axis=0)
        desvio = np.std(dados, axis=0)

        # Calculo dos residuos
        residuos = np.zeros((nanos - 1, 12))
        for iano in np.arange(1, nanos):
            for imes in range(12):
                residuos[iano - 1][imes] = (dados[iano][imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    residuos[iano - 1][imes] -= self.CoefParp[imes][ilag] * (dados[ano_ant][mes_ant] - media[mes_ant]) / \
                                                desvio[mes_ant]

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        for irod in range(2):
            for iser in range(nr_ser):
                contador = -1
                for iano in range(5):
                    for imes in range(12):
                        contador += 1
                        serie = rd.randint(0, nanos - 2)
                        valor = media[imes] + desvio[imes] * residuos[serie][imes]
                        for ilag in range(int(self.Ordem[imes])):
                            mes_ant = imes - ilag - 1
                            ano_ant = iano
                            if mes_ant < 0:
                                mes_ant += 12
                                ano_ant -= 1
                            if ano_ant < 0 and irod == 0:
                                ventoant = media[mes_ant]
                            else:
                                ventoant = sintetica_adit[iser][contador - 1 - ilag]
                            valor += desvio[imes] * self.CoefParp[imes][ilag] * (ventoant - media[mes_ant]) / desvio[
                                mes_ant]
                        sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), color='silver', linestyle='-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'k-', lw=3, label='Média - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'k--', lw=2,
                 label='Desvio Padrão - Séries Sintéticas')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'k--', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'ro', lw=3, label='Média - Série Histórica')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Desvio Padrão - Série Histórica')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = "Séries Sintéticas de Densidade de Potência do Vento"
        plt.title(titulo, fontsize=12)
        plt.xlabel('Meses', fontsize=10)
        plt.ylabel('$KW/m^{2}$', fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

        self.series_sinteticas = sintetica_adit

    def Teste_de_Media(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ttest_ind(a, b, equal_var=True)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Média das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE MÉDIA (Teste t)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Media

    def Teste_de_Variancia(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste de Levene
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.levene(a, b, center='mean')
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Variância das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE VARIÂNCIA (Levene)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

    def Teste_de_Variancia_bartlett(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste de Levene
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.bartlett(a, b)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Variância das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE VARIÂNCIA (Bartlett)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

    def Teste_de_Aderencia(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ks_2samp(a, b)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Aderência das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE ADERÊNCIA (Kolmogorov-Smirnov)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

    def Teste_de_Aderencia_qui(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.chisquare(a, b)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Aderência das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE ADERÊNCIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

    def Teste_de_Mediana(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]

        # Realizacao do Teste de Wilcoxon
        aprovados = 0
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ranksums(a, b)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Mediana das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE MEDIANA (Wilcoxon)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Mediana

    def Teste_de_Assimetria(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]

        # Realizacao do Teste de Assimetria
        aprovados = 0
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            z_valor1, p_valor1 = stats.skewtest(a)
            z_valor2, p_valor2 = stats.skewtest(b)
            aux = p_valor1 - p_valor2
            max_v = max(p_valor1, p_valor2)
            Teste[0, iteste] = abs(aux / max_v) * 100

            # Verificacao da quantidade de valores aprovados
            if Teste[0, iteste] >= float(5.):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Assimetria das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE ASSIMETRIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Assimetria

    def Teste_de_Assimetria_Wilcoxon(self, dados):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nestagios = self.series_sinteticas.shape[1]

        # Realizacao do Teste de Assimetria
        aprovados = 0
        Teste = np.zeros((1, nestagios))
        cont = 0
        for iteste in range(nestagios):
            aux = [dados[i][cont] for i in range(len(dados))]
            a = aux
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.wilcoxon(a, b)
            Teste[0, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Assimetria das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[0, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "TESTE DE ASSIMETRIA (Wilcoxon)"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Assimetria

    def Teste_de_Sequencia_Negativa(self, dados):

        # Determinação dos parâmetros de sequêcia negativa do histórico
        dados = np.asanyarray(dados)
        dados_historico = np.reshape(dados, np.size(dados))
        media_historico = np.tile(np.mean(dados, axis=0), len(dados))
        aux = []
        for k in range(len(dados_historico)):
            if dados_historico[k] <= media_historico[k]:
                aux.append(k)
        aux = np.asarray(aux)
        seq_negativa = np.split(aux, np.where(np.diff(aux) != 1)[0] + 1)

        comprimento_historico = np.zeros(len(seq_negativa))
        soma_historico = np.zeros(len(seq_negativa))
        intensidade_historico = np.zeros(len(seq_negativa))
        for k in range(len(seq_negativa)):
            comprimento_historico[k] = seq_negativa[k].size
            soma_historico[k] = np.sum(dados_historico[seq_negativa[k]] - media_historico[seq_negativa[k]])
            intensidade_historico[k] = soma_historico[k] / comprimento_historico[k]

        # Determinação dos parâmetros de sequêcia negativa das séries geradas
        dados_series = np.reshape(self.series_sinteticas, np.size(self.series_sinteticas))
        media_historico = np.tile(np.mean(dados, axis=0),
                                  int(self.series_sinteticas.shape[0] * self.series_sinteticas.shape[1] / 12))
        aux = []
        for k in range(len(dados_series)):
            if dados_series[k] <= media_historico[k]:
                aux.append(k)
        aux = np.asarray(aux)
        seq_negativa = np.split(aux, np.where(np.diff(aux) != 1)[0] + 1)

        comprimento_series = np.zeros(len(seq_negativa))
        soma_series = np.zeros(len(seq_negativa))
        intensidade_series = np.zeros(len(seq_negativa))
        for k in range(len(seq_negativa)):
            comprimento_series[k] = seq_negativa[k].size
            soma_series[k] = np.sum(dados_series[seq_negativa[k]] - media_historico[seq_negativa[k]])
            intensidade_series[k] = soma_series[k] / comprimento_series[k]

        # Preparação dos dados para o teste Qui^2 (aplicado ao comprimento de sequencia negativa)
        max_comp = np.maximum(np.max(comprimento_series), np.max(comprimento_historico))
        min_comp = np.minimum(np.min(comprimento_series), np.min(comprimento_historico))
        num_classes = int((max_comp - min_comp) / 3)
        data = np.zeros((2, int(num_classes)))
        classes = np.zeros((num_classes, 2))
        aux = min_comp - 1
        for icl in np.arange(1, num_classes + 1):
            if (icl / num_classes) <= 0.6:
                classes[icl - 1, :] = [aux, aux + 1]
                aux += 1
            elif (icl / num_classes > 0.6) and (icl / num_classes <= 0.9):
                classes[icl - 1, :] = [aux, aux + 2]
                aux += 2
            if icl == num_classes:
                classes[icl - 1, :] = [aux, max_comp]

        for k in range(num_classes):
            quant_historico = np.size(
                np.where(np.logical_and(comprimento_historico > classes[k, 0], comprimento_historico <= classes[k, 1])))
            quant_series = np.size(
                np.where(np.logical_and(comprimento_series > classes[k, 0], comprimento_series <= classes[k, 1])))
            data[:, k] = [quant_historico, quant_series]
        # data[:, -1] = np.sum(data[:, :-1], axis=1)
        # Deletar colunas com zeros em ambas distribuições
        ind_del = [i for i in range(data.shape[1]) if ((data[0, i] == 0) and (data[1, i] == 0))]
        data = np.delete(data, ind_del, axis=1)

        # Aplicação do teste de Qui^2
        qui2, p, dof, ex = stats.chi2_contingency(data, correction=False)
        # Valor crítico
        valor_critico = chi2.ppf(0.95, dof)
        print('Teste de sequência negativa - Comprimento (Chi Quadrado)')
        if qui2 <= valor_critico:
            print('Aprovado no teste!!!!')
            print('chi2 = %4.3f <= %4.3f = valor crítico' % (qui2, valor_critico))
        else:
            print('Reprovado no teste!!!!')
            print('chi2 = %4.3f > %4.3f = valor crítico' % (qui2, valor_critico))
        print('-------------------------------------------------------------')

        # Aplicação do teste de Kolmogorov-Smirnov (Soma)
        ks, p = stats.ks_2samp(soma_historico, soma_series)
        # Valor crítico
        valor_critico = 1.36 * np.sqrt(
            (soma_historico.size + soma_series.size) / (soma_historico.size * soma_series.size))
        print('Teste de sequência negativa - Soma (Kolmogorov-Smirnov)')
        if ks <= valor_critico:
            print('Aprovado no teste!!!!')
            print('ks = %4.3f <= %4.3f = valor crítico' % (ks, valor_critico))
        else:
            print('Reprovado no teste!!!!')
            print('ks = %4.3f > %4.3f = valor crítico' % (ks, valor_critico))
        print('-------------------------------------------------------------')

        # Aplicação do teste de Kolmogorov-Smirnov (Soma)
        ks, p = stats.ks_2samp(intensidade_historico, intensidade_series)
        # Valor crítico
        valor_critico = 1.36 * np.sqrt((intensidade_historico.size + intensidade_series.size) / (
                intensidade_historico.size * intensidade_series.size))
        print('Teste de sequência negativa - Intensidade (Kolmogorov-Smirnov)')
        if ks <= valor_critico:
            print('Aprovado no teste!!!!')
            print('ks = %4.3f <= %4.3f = valor crítico' % (ks, valor_critico))
        else:
            print('Reprovado no teste!!!!')
            print('ks = %4.3f > %4.3f = valor crítico' % (ks, valor_critico))
        print('-------------------------------------------------------------')

        galo = 13

        #####################################################################
        # TESTES ESTATÍSTICOS DOS RESIDUOS
        #####################################################################

        # Teste de média

    def Teste_Residuo_Media(self, tipo_residuo, residuos):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = residuos[:, cont]
            if tipo_residuo == "aditivo":
                t_valor, p_valor = stats.ttest_1samp(a, 0.0)
            elif tipo_residuo == "multiplicativo":
                t_valor, p_valor = stats.ttest_1samp(a, 1.0)
            Teste[1, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Média dos Resíduos do Modelo: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[1, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\n ANÁLISE DOS RESÍDUOS - TESTE DE MÉDIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Teste de Ljung-Box

    def Teste_Residuo_Dependencia_Linear(self, residuos):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = np.array(residuos[:, cont])
            t_valor, p_valor = diagnostic.acorr_ljungbox(a, lags=1)
            Teste[1, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Dependência Linear dos Resíduos do Modelo: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[1, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\n ANÁLISE DOS RESÍDUOS - TESTE DE DEPENDÊNCIA LINEAR"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Teste ARCH

    def Teste_Residuo_ARCH(self, residuos):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = residuos[:, cont]
            t_valor, p_valor, p1, p2 = diagnostic.het_arch(a, maxlag=20, autolag=None, store=False, regresults=False,
                                                           ddof=0)
            Teste[1, iteste] = p_valor * 100

            # Verificacao da quantidade de valores aprovados
            if p_valor >= float(0.05):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste ARCH dos Resíduos do Modelo: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[1, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(5)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\n ANÁLISE DOS RESÍDUOS - TESTE ARCH"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

    #############################################################################
    ########################### Graficos Diversos ###############################
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
                    if iusina.TipoReg == b'M' and iusina.Sist == self.Codigo and iusina.StatusVolMorto[iano][imes] == 2:
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

    def PlotaHistENA(self):

        nanos = self.ENA.shape[0]
        nmeses = self.ENA.shape[1]

        f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        eixo_x = np.arange(1, nmeses + 1)

        ENAS = self.ENA
        ECS = self.EC
        EFIOBS = self.EFIOB

        for iano in range(nanos):
            ax1.plot(eixo_x, ENAS[iano, :], 'c-')
            ax2.plot(eixo_x, ECS[iano, :], 'c-')
            ax3.plot(eixo_x, EFIOBS[iano, :], 'c-')

        mediaENA = np.mean(ENAS, axis=0)
        mediaEC = np.mean(ECS, axis=0)
        mediaEFIOB = np.mean(EFIOBS, axis=0)

        ax1.plot(eixo_x, mediaENA, 'r-', lw=3)
        ax2.plot(eixo_x, mediaEC, 'r-', lw=3)
        ax3.plot(eixo_x, mediaEFIOB, 'r-', lw=3)

        desvioENA = np.nanstd(ENAS, axis=0)
        desvioEC = np.nanstd(ECS, axis=0)
        desvioEFIOB = np.nanstd(EFIOBS, axis=0)

        ax1.plot(eixo_x, mediaENA + desvioENA, 'r-.', lw=2)
        ax1.plot(eixo_x, mediaENA - desvioENA, 'r-.', lw=2)
        ax2.plot(eixo_x, mediaEC + desvioEC, 'r-.', lw=2)
        ax2.plot(eixo_x, mediaEC - desvioEC, 'r-.', lw=2)
        ax3.plot(eixo_x, mediaEFIOB + desvioEFIOB, 'r-.', lw=2)
        ax3.plot(eixo_x, mediaEFIOB - desvioEFIOB, 'r-.', lw=2)

        ax1.set_xticks(np.arange(1, 12))
        ax1.set_ylabel('ENA (MWmes)')
        ax2.set_ylabel('EC (MWmes)')
        ax3.set_ylabel('EFIOB (MWMes)')
        tituloENA = 'ENA do Submercado ' + self.Nome
        tituloEC = 'EC do Submercado ' + self.Nome
        tituloEFIOB = 'EFIOB do Submercado ' + self.Nome
        ax1.set_title(tituloENA, fontsize=13)
        ax2.set_title(tituloEC, fontsize=13)
        ax3.set_title(tituloEFIOB, fontsize=13)

        plt.show()
