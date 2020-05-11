# coding=utf-8
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from math import sqrt
from random import randint
from scipy.optimize import minimize
from scipy import stats
from typing import List
import pandas as pd
from scipy.spatial.distance import cdist
from functools import partial
from scipy.stats import kurtosis


class hidr(object):
    # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)
    Codigo = None  # Codigo da UHE
    Nome = None  # Nome da UHE
    Posto = None  # Numero do Posto
    Bdh = None  # Desvio - Nao sei qual e esta informacao ??????
    Sist = None  # Submercado
    Empr = None  # Codigo da empresa
    Jusante = None  # Codigo de Jusante
    Desvio = None  # Desvio - Nao sei qual e esta informacao ??????
    VolMin = None  # Volume Minimo
    VolMax = None  # Volume Maximo
    VolVert = None  # Volume Vertimento
    VolMinDesv = None  # Volume Minimo para Desvio
    CotaMin = None  # Cota Minima
    CotaMax = None  # Cota Maxima
    CotaMed = None  # Cota Média
    PolCotaVol = None  # Polinomio Cota-Volume
    PolCotaArea = None  # Polinomio Cota-Area
    CoefEvap = None  # Coeficientes de Evaporacao
    NumConjMaq = None  # Numero de Conjuntos de Maquinas
    MaqporConj = None  # Numero de Maquinas por Conjunto
    PEfporConj = None  # POtencia Efetiva por Maquina do Conjunto

    CF_HBQT = None  # Nao sei qual e esta informacao ??????
    CF_HBQG = None  # Nao sei qual e esta informacao ??????
    CF_HBPT = None  # Nao sei qual e esta informacao ??????

    AltEfetConj = None  # Altura de Queda Efetiva do Conjunto
    VazEfetConj = None  # Vazao Efetiva do Conjunto
    ProdEsp = None  # Produtibilidade Especifica
    PerdaHid = None  # Perda Hidraulica
    NumPolVNJ = None  # Numero de Polinomios Vazao Nivel Jusante

    PolVazNivJus = None  # Polinomios Vazao Nivel Jusante

    CotaRefNivelJus = None  # Cota Referencia Nivel de Jusante
    CFMed = None  # Cota Media do Canal de Fuga
    InfCanalFuga = None  # Informacao Canal de Fuga - Nao sei qual e esta informacao ??????
    FatorCargaMax = None  # Fator de Caga Maximo - Nao sei qual e esta informacao ?????????
    FatorCargaMin = None  # Fator de Caga Minimo - Nao sei qual e esta informacao ?????????
    VazMin = None  # Vazao Minima Obrigatoria
    UnidBase = None  # Numero de Unidades de Base
    TipoTurb = None  # Tipo de Turbina Hidraulica
    Repres_Conj = None  # Representacao Conjunto de Maquina - Nao sei qual e esta informacao ?????
    TEIF = None
    TEIFH = None  # Taxa Equivalente de Indisponibilidade Forcada Hidraulica
    IP = None  # Indisponibilidade Programada
    TipoPerda = None  # Tipo Perda Hidraulica
    Data = None  # Nao sei qual e esta informacao ??????
    Observ = None  # Observacao
    VolRef = None  # Volume de Referencia
    TipoReg = None  # Tipo de Regulacao

    # Dados Adicionais Especificados no arquivo de configuracao hidraulica (CONFHD)
    Ree = None
    Status = None
    VolIni = None
    Modif = None
    AnoI = None
    AnoF = None

    # Dados Adicinais Calculados para as Usinas pertecentes a configuracao hidraulica (CONFHD)
    VolUtil = None
    VazEfet = None
    PotEfet = None
    # PotNom = None
    Ro65 = None  # PDTMED (NEWAVE) - PROD. ASSOCIADA A ALTURA CORRESPONDENTE A 65% DO V.U.
    Ro50 = None
    RoMax = None  # PDTMAX (NEWAVE) - PROD. ASSOCIADA A ALTURA MAXIMA
    RoMin = None  # PDTMIN (NEWAVE) - PROD. ASSOCIADA A ALTURA MINIMA
    RoEquiv = None  # PRODT (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO AO VOL. MAXIMO )
    RoEquiv65 = None  # PRODTM (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO A 65% DO V.U. )
    Engolimento = None
    RoAcum = None  # PDTARM (NEWAVE) - PROD. ACUM. PARA CALCULO DA ENERGIA ARMAZENADA
    RoAcum65 = None  # PDAMED (NEWAVE) - PROD. ACUM. PARA CALCULO DA ENERGIA ARMAZENADA CORRESPONDENTE A 65% DO V.U.
    RoAcumMax = None  # PDCMAX e PDVMAX (NEWAVE) - PROD. ACUM.
    RoAcumMed = None  # PDTCON, PDCMED e PDVMED (NEWAVE) - PROD. ACUM.
    RoAcumMin = None  # PDCMIN e PDVMIN (NEWAVE) - PROD. ACUM.
    RoAcumOperEquiv = None

    RoAcum_A_Ree = None
    RoAcum_B_Ree = None
    RoAcum_C_Ree = None
    RoAcum_A_Sist = None
    RoAcum_B_Sist = None
    RoAcum_C_Sist = None

    RoAcumEntreResRee = None
    RoAcumEntreResSist = None

    RoAcumDesvAguaEquiv = None

    # Vazoes Naturais, Incrementais e Par(p)
    Vazoes = None  # Historico de Vazoes naturais (imes, ilag)
    FAC = None  # Funcao de Autocorrelacao (imes, ilag)
    FACP = None  # Funcao de Autocorrelacao Parcial (imes, ilag)
    CoefParp = None  # Coeficientes do Modelo par(p) (imes,ilag)
    CoefIndParp = None  # Coeficientes independentes do Modelo par(p) (imes) - Aditivo = 0 - Multiplicativo > 0
    Ordem = None  # Ordem do modelo par(p) para todos os meses (mes)

    # Parametros da usina Dependentes do Tempo - Especificados (MODIF.DAT)
    VolMinT = None  # Volume Mínimo Operativo (pode variar mes a mes)
    VolMaxT = None  # Volume Maximo Operativo (pode variar mes a mes)
    VolUtilT = None
    VolMinP = None  # Volume Mínimo com adocao de penalidade (pode variar mes a mes)
    VazMinT = None  # Vazao Minima pode variar mes a mes
    CFugaT = None  # Cota do Canal de Fuga (pode varia mes a mes)

    # Parametros relativos a expansao hidrica que variam no tempo para usinas 'EE' e 'NE' (EXPH)
    StatusVolMorto = None  # Status do Volume Morto - 0: Nao Comecou Encher - 1: Enchendo - 2: Cheio
    VolMortoTempo = None  # Evolucao do Volume Minimo da Usina
    StatusMotoriz = None  # Status da Motorizacao  - 0: Nao Comecou Motorizar - 1: Motorizando - 3: Motorizada
    UnidadesTempo = None  # Numero de Unidades em cada mes
    EngolTempo = None  # Evolucao do Engolimento Maximo da Usina
    PotenciaTempo = None  # Evolucao da Potencia Instalada da Usina

    VazDesv = None

    ##########################################################################################################
    # Graficos Diversos
    ##########################################################################################################

    # Plota Polinomio Cota-Volume
    def PlotaPCV(self):
        if self.VolMin == 0:
            return

        if (self.VolMin == self.VolMax):
            volumes = np.linspace(self.VolMin - 1, self.VolMax + 1, 100)
        else:
            volumes = np.linspace(self.VolMin, self.VolMax, 100)
        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]
        cota = a + b * volumes + c * volumes ** 2 + d * volumes ** 3 + e * volumes ** 4
        cota.shape = volumes.shape
        plt.plot(volumes, cota, 'b-', lw=3)

        plt.xlabel('Volume do Reservatorio (hm^3)', fontsize=16)
        titulo = 'Polinomio Cota-Volume da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Cota em Metros', fontsize=16)
        plt.xlim(volumes[0], volumes[99])
        if (cota[0] == cota[99]):
            plt.ylim(cota[0] - 1, cota[99] + 1)
        else:
            plt.ylim(cota[0], cota[99])
        plt.show()

    # Plota Polinomio Cota-Area
    def PlotaPCA(self):
        if self.VolMin == 0:
            return

        if (self.CotaMax == self.CotaMin):
            cotas = np.linspace(self.CotaMin - 1, self.CotaMax + 1, 100)
        else:
            cotas = np.linspace(self.CotaMin, self.CotaMax, 100)
        a = self.PolCotaArea[0]
        b = self.PolCotaArea[1]
        c = self.PolCotaArea[2]
        d = self.PolCotaArea[3]
        e = self.PolCotaArea[4]
        areas = a + b * cotas + c * cotas ** 2 + d * cotas ** 3 + e * cotas ** 4
        areas.shape = cotas.shape
        plt.plot(cotas, areas, 'b-', lw=3)

        plt.xlabel('Cota do Reservatorio (em metros)', fontsize=16)
        titulo = 'Polinomio Cota-Area da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Area Superficia em km^2', fontsize=16)
        plt.xlim(cotas[0], cotas[99])
        if (areas[0] == areas[99]):
            plt.ylim(areas[0] - 1, areas[99] + 1)
        else:
            plt.ylim(areas[0], areas[99])
        plt.show()

    # Plota Curva Colina
    def PlotaColina(self):
        if self.VolMin == 0:
            return

        if (self.VolMin == self.VolMax):
            volumes = np.linspace(self.VolMin - 1, self.VolMax + 1, 100)
        else:
            volumes = np.linspace(self.VolMin, self.VolMax, 100)

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        cotamont = a + b * volumes + c * volumes ** 2 + d * volumes ** 3 + e * volumes ** 4
        cotamont.shape = volumes.shape

        qdef = np.linspace(self.VazMin, 5 * self.Engolimento, 100)

        a = self.PolVazNivJus[0][0]
        b = self.PolVazNivJus[0][1]
        c = self.PolVazNivJus[0][2]
        d = self.PolVazNivJus[0][3]
        e = self.PolVazNivJus[0][4]

        cotajus = a + b * qdef + c * qdef ** 2 + d * qdef ** 3 + e * qdef ** 4
        cotajus.shape = qdef.shape

        xGrid, yGrid = np.meshgrid(cotamont, cotajus)

        z = self.ProdEsp * (xGrid - yGrid)

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surf = ax.plot_surface(qdef, volumes, z, rcount=100, ccount=100, cmap=plt.cm.coolwarm,
                               linewidth=0, antialiased=False)

        plt.xlabel('Vazão Defluente em m^3/s', fontsize=12)
        titulo = 'Produtibilidade da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Volume Armazenado em hm^3', fontsize=12)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()

    def PlotaProdutibs(self, iano, imes):
        x_axis = np.arange(1, 6)
        y_axis = [self.RoEquiv[iano][imes], self.RoMin[iano][imes], self.Ro50[iano][imes], self.Ro65[iano][imes],
                  self.RoMax[iano][imes]]
        fig, ax = plt.subplots()
        a, b, c, d, e = plt.bar(x_axis, y_axis)
        a.set_facecolor('r')
        b.set_facecolor('g')
        c.set_facecolor('b')
        d.set_facecolor('y')
        e.set_facecolor('m')
        ax.set_xticks(x_axis)
        ax.set_xticklabels(['Equiv', 'Min', '50%', '65%', 'Max'])
        titulo = 'Produtibilidades da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Tipo de Produtibilidade', fontsize=16)
        plt.ylabel('Produtibilidade', fontsize=16)
        plt.show()

    def PlotaVazoes(self):
        x_axis = np.arange(1, 13)
        plt.plot(x_axis, self.Vazoes.transpose(), 'c-')
        media = np.mean(self.Vazoes, axis=0)
        plt.plot(x_axis, media, 'r-', lw=3)
        desvio = np.nanstd(self.Vazoes, axis=0)
        plt.plot(x_axis, media + desvio, 'r-.', lw=2)
        plt.plot(x_axis, media - desvio, 'r-.', lw=2)
        ultimo = len(self.Vazoes) - 1
        plt.plot(x_axis, self.Vazoes[:][ultimo], 'b-')
        titulo = 'Historico de Vazoes da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes do Ano', fontsize=16)
        plt.ylabel('Vazao', fontsize=16)
        plt.show()

    def PlotaVolume(self):
        nanos = len(self.VolMinT)

        fig = plt.figure()
        ax = plt.subplot(111)

        x_axis = np.arange(1, nanos * 12 + 1)
        ax.plot(x_axis, self.VolMinT.reshape(nanos * 12), 'g-.', lw=2, label='Vol.Min.Operat.')
        ax.plot(x_axis, self.VolMaxT.reshape(nanos * 12), 'g-.', lw=2, label='Vol.Max.Operat.')
        ax.plot(x_axis, self.VolMax * np.ones(nanos * 12), 'b-', lw=3, label='Vol.Minimo Real')
        ax.plot(x_axis, self.VolMin * np.ones(nanos * 12), 'b-', lw=3, label='Vol.Maximo Real')
        ax.plot(x_axis, self.VolMinP.reshape(nanos * 12), 'b-.', lw=2, label='Vol.Min.com Pen.')

        plt.fill_between(x_axis, self.VolMinT.reshape(nanos * 12), self.VolMaxT.reshape(nanos * 12), facecolor='g',
                         alpha=0.1)

        titulo = 'Evolucao dos Volumes da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Volume em hm^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        ax.legend(loc='center left', shadow=True, fontsize=12, bbox_to_anchor=(1, 0.5))

        plt.show()

    def PlotaVazMin(self):
        nanos = len(self.VazMinT)

        fig = plt.figure()
        ax = plt.subplot(111)

        x_axis = np.arange(1, nanos * 12 + 1)
        ax.plot(x_axis, self.VazMinT.reshape(nanos * 12), 'g-.', lw=2, label='Vaz.Min.Operat.')
        ax.plot(x_axis, self.VazMin * np.ones(nanos * 12), 'b-', lw=3, label='Vaz.Min.Cadastro')

        titulo = 'Evolucao da Vazao Minima da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Vazao Minima em m^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        ax.legend(loc='center left', shadow=True, fontsize=12, bbox_to_anchor=(1, 0.5))

        plt.show()

    def PlotaVolMorto(self):

        if self.Status == 'EX':
            print('Grafico de Volume Morto nao impresso, pois ', self.Nome, 'e uma usina existente')
            return

        nanos = len(self.VolMortoTempo)

        nmeses = np.count_nonzero(self.VolMortoTempo)

        legenda = str(nmeses) + ' Meses'

        ax = plt.subplot(111)

        x_axis = np.arange(1, nanos * 12 + 1)
        p1 = ax.plot(x_axis, self.VolMortoTempo.reshape(nanos * 12), 'g-.', lw=2, label=legenda)

        titulo = 'Enchimento do Volume Morto da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Volume Morto em hm^3', fontsize=16)

        plt.legend(fontsize=12)

        np.count_nonzero(self.VolMortoTempo)

        plt.show()

    def PlotaPotencia(self):

        nanos = len(self.PotenciaTempo)

        ax = plt.subplot(111)

        x_axis = np.arange(1, nanos * 12 + 1)
        p1 = ax.plot(x_axis, self.PotenciaTempo.reshape(nanos * 12), 'g-.', lw=2)

        titulo = 'Evolucao da Potencia Efetiva da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Potencia Efetiva em MW', fontsize=16)

        plt.show()

    def PlotaParp(self, mes):

        ordmax = len(self.CoefParp[0])
        nanos = len(self.Vazoes) - 1

        if mes == 0:
            str_mes = 'January'
        elif mes == 1:
            str_mes = 'Fevereiro'
        elif mes == 2:
            str_mes = 'Marco'
        elif mes == 3:
            str_mes = 'Abril'
        elif mes == 4:
            str_mes = 'Maio'
        elif mes == 5:
            str_mes = 'Junho'
        elif mes == 6:
            str_mes = 'Julho'
        elif mes == 7:
            str_mes = 'Agosto'
        elif mes == 8:
            str_mes = 'Setembro'
        elif mes == 9:
            str_mes = 'Outubro'
        elif mes == 10:
            str_mes = 'Novembro'
        else:
            str_mes = 'Dezembro'

        IC = 1.96 / sqrt(nanos - 1)

        cores = []
        limitesup = []
        limiteinf = []
        for elemento in self.FACP[mes][1:ordmax + 1]:
            limitesup.append(IC)
            limiteinf.append(-IC)
            if elemento > IC or elemento < -IC:
                cores.append('r')
            else:
                cores.append('b')

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        barWidth = 0.40

        titulo = 'FAC e FACP of ' + str_mes + ' - UHE ' + self.Nome
        f.canvas.set_window_title(titulo)

        ax1.bar(np.arange(1, ordmax + 1), self.FAC[mes][1:ordmax + 1], barWidth, align='center')
        ax2.bar(np.arange(1, ordmax + 1), self.FACP[mes][1:ordmax + 1], barWidth, align='center', color=cores)
        ax2.plot(np.arange(1, ordmax + 1), limitesup, 'm--', lw=1)
        ax2.plot(np.arange(1, ordmax + 1), limiteinf, 'm--', lw=1)

        ax1.set_xticks(np.arange(1, ordmax + 1))
        ax2.set_xticks(np.arange(1, ordmax + 1))
        tituloFAC = 'FAC - Month: ' + str_mes + '\n of UHE ' + self.Nome
        tituloFACP = 'FACP - Month ' + str_mes + '\n of UHE ' + self.Nome
        ax1.set_title(tituloFAC, fontsize=13)
        ax2.set_title(tituloFACP, fontsize=13)
        # ax1.xlabel('Lag')
        # ax2.xlabel('Lag')
        # ax1.ylabel('Autocorrelacao e Autocorrelacao Parcial')

        plt.show()

    ##########################################################################################################
    # Calcula Parametros das Usinas
    ##########################################################################################################

    def CalcVolUtil(self):  # Calcula Volume Util da Usina
        if self.TipoReg == b'M':
            self.VolUtil = self.VolMax - self.VolMin
        else:
            self.VolUtil = float(0)
            self.VolMin = self.VolMax

    def CalcVolUtilT(self):
        if self.TipoReg == b'M':
            self.VolUtilT = self.VolMaxT - self.VolMinT
        else:
            self.VolUtilT = np.zeros(self.VolMaxT.shape)
            self.VolMinT = self.VolMaxT

    def CalcPotEfetiva(self):  # Calcula Potencia Efetiva da Usina
        a = np.array(self.MaqporConj)
        b = np.array(self.PEfporConj)
        self.PotEfet = np.vdot(a, b)

    def CalcVazEfetiva(self):  # Calcula Vazao Efetiva da Usina
        a = np.array(self.MaqporConj)
        b = np.array(self.VazEfetConj)
        self.VazEfet = np.vdot(a, b)

    def CalcEngolMaximo(self):  # Estima Engolimento Maximo da Usina

        def CalcEngol(self, ql):
            engol = 0.
            for i in range(5):  # Varre Conjuntos de Maquinas
                if self.MaqporConj[i] > 0:
                    if ql < self.AltEfetConj[i]:
                        if self.TipoTurb == 1 or self.TipoTurb == 3:
                            alpha = 0.5
                        else:
                            alpha = 0.2
                    else:
                        alpha = -1
                    if self.AltEfetConj[i] != 0:
                        engol = engol + self.MaqporConj[i] * self.VazEfetConj[i] * ((ql / self.AltEfetConj[i]) ** alpha)
            return engol

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        # Calcula Engolimento a 65% do Volume Util
        volume = self.VolMin + 0.65 * self.VolUtil
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        queda65 = cota - self.CFMed
        engol65 = CalcEngol(self, queda65)

        # Calcula Engolimento a 50% do Volume Util
        volume = self.VolMin + 0.50 * self.VolUtil
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        queda50 = cota - self.CFMed
        engol50 = CalcEngol(self, queda50)

        # Calcula Engolimento Associada ao Volume Maximo
        volume = self.VolMax
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        quedaMax = cota - self.CFMed
        engolMax = CalcEngol(self, quedaMax)

        # Calcula Engolimento Associada ao Volume Minimo
        volume = self.VolMin
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        quedaMin = cota - self.CFMed
        engolMin = CalcEngol(self, quedaMin)

        # Calcula Engolimento Associado a Altura Equivalente
        if (self.VolUtil > 0):
            cota = 0
            for i in range(5):
                cota = cota + self.PolCotaVol[i] * (self.VolMax ** (i + 1)) / (i + 1)
                cota = cota - self.PolCotaVol[i] * (self.VolMin ** (i + 1)) / (i + 1)
            cota = cota / self.VolUtil
        quedaEquiv = cota - self.CFMed
        engolEquiv = CalcEngol(self, quedaEquiv)

        self.Engolimento = (engol50 + engol65 + engolEquiv + engolMax + engolMin) / 5
        # self.Engolimento = engol65

        return

    def CalcProdutibs(self, nanos):  # Calcula Produtibilidades Associadas aa diversos volumes

        self.Ro65 = np.zeros((nanos, 12), 'd')
        self.Ro50 = np.zeros((nanos, 12), 'd')
        self.RoEquiv = np.zeros((nanos, 12), 'd')
        self.RoEquiv65 = np.zeros((nanos, 12), 'd')
        self.RoEquiv50 = np.zeros((nanos, 12), 'd')
        self.RoMin = np.zeros((nanos, 12), 'd')
        self.RoMax = np.zeros((nanos, 12), 'd')
        self.RoEquivMinOp = np.zeros((nanos, 12), 'd')

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        # Calcula Produtibilidade Associada a 65% do Volume Util
        volume = self.VolMin + 0.65 * self.VolUtil
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.Ro65[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.Ro65[iano][imes] = self.ProdEsp * (cota - cfuga) * (1. - self.PerdaHid / 100)

        # Calcula Produtibilidade Associada a 50% do Volume Util
        volume = self.VolMin + 0.50 * self.VolUtil
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.Ro50[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.Ro50[iano][imes] = self.ProdEsp * (cota - cfuga) * (1. - self.PerdaHid / 100)

        # Calcula Produtibilidade Associada ao Volume Maximo
        volume = self.VolMax
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoMax[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.RoMax[iano][imes] = self.ProdEsp * (cota - cfuga) * (1. - self.PerdaHid / 100)

        # Calcula Produtibilidade Associada ao Volume Minimo
        volume = self.VolMin
        cota = a + b * volume + c * volume ** 2 + d * volume ** 3 + e * volume ** 4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoMin[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.RoMin[iano][imes] = self.ProdEsp * (cota - cfuga) * (1. - self.PerdaHid / 100)

        # Calcula Produtibilidade Equivalente
        if (self.VolUtil > 0):
            cota, cota50, cota65, cota_minop = 0, 0, 0, 0
            Vol65 = self.VolMin + 0.65 * self.VolUtil
            Vol50 = self.VolMin + 0.5 * self.VolUtil
            for i in range(5):
                cota = cota + self.PolCotaVol[i] * (self.VolMax ** (i + 1)) / (i + 1) - self.PolCotaVol[i] * (
                            self.VolMin ** (i + 1)) / (i + 1)
                cota65 = cota65 + self.PolCotaVol[i] * (Vol65 ** (i + 1)) / (i + 1) - self.PolCotaVol[i] * (
                            self.VolMin ** (i + 1)) / (i + 1)
                cota50 = cota50 + self.PolCotaVol[i] * (Vol50 ** (i + 1)) / (i + 1) - self.PolCotaVol[i] * (
                            self.VolMin ** (i + 1)) / (i + 1)
                cota_minop = cota_minop + self.PolCotaVol[i] * (self.VolMinP[1, 0] ** (i + 1)) / (i + 1) - \
                             self.PolCotaVol[i] * (self.VolMin ** (i + 1)) / (i + 1)
            cota = cota / self.VolUtil
            cota65 = cota65 / (Vol65 - self.VolMin)
            cota50 = cota50 / (Vol50 - self.VolMin)
            if self.VolMinP[1, 0] == self.VolMin:
                cota_minop = self.CotaMin
            else:
                cota_minop = cota_minop / (self.VolMinP[1, 0] - self.VolMin)
            self.CotaMed = cota65
        else:
            cota65 = cota
            cota50 = cota
            cota_minop = self.CotaMin
            self.CotaMed = self.CotaMax
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoEquiv[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                    self.RoEquiv65[iano][imes] = self.ProdEsp * (cota65 - cfuga - self.PerdaHid)
                    self.RoEquiv50[iano][imes] = self.ProdEsp * (cota50 - cfuga - self.PerdaHid)
                    self.RoEquivMinOp[iano][imes] = self.ProdEsp * (cota_minop - cfuga - self.PerdaHid)
                else:
                    self.RoEquiv[iano][imes] = self.ProdEsp * (cota - cfuga) * (1. - self.PerdaHid / 100)
                    self.RoEquiv65[iano][imes] = self.ProdEsp * (cota65 - cfuga) * (1. - self.PerdaHid / 100)
                    self.RoEquiv50[iano][imes] = self.ProdEsp * (cota50 - cfuga) * (1. - self.PerdaHid / 100)
                    self.RoEquivMinOp[iano][imes] = self.ProdEsp * (cota_minop - cfuga) * (1. - self.PerdaHid / 100)

        return

    # Calcula Soma das Vazões Mínima Montante
    def QMin(self, usinas, iano, imes):

        def Montante(usinas, usina):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.VolUtil > 0:
                        yield iusi
                    else:
                        yield from Montante(usinas, iusi)

        # def Montante(usinas, usina, iano, imes):
        #     for iusi in usinas:
        #         if iusi.Jusante == usina.Codigo:
        #             yield iusi

        VazMin = 0
        montantes = Montante(usinas, self)
        for iusina in montantes:
            VazMin = VazMin + iusina.VazMin

        return VazMin

    # Calcula Soma Vazao Montante
    def QMontante(self, usinas, iano, imes):

        def Montante(usinas, usina):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.VolUtil > 0:
                        yield iusi
                    else:
                        yield from Montante(usinas, iusi)

        # def Montante(usinas, usina, iano, imes):
        #     for iusi in usinas:
        #         if iusi.Jusante == usina.Codigo:
        #             yield iusi

        SomaVazao = 0
        montantes = Montante(usinas, self)
        for iusina in montantes:
            SomaVazao = SomaVazao + iusina.Vazoes[iano, imes]

        return SomaVazao

    def QInc(self, usinas, iano, imes):

        nanos_hist = len(self.Vazoes)

        def Montante(usinas, usina, iano, imes):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    yield iusi

        # if self.StatusVolMorto[iano][imes] != 2:
        #     print('Erro: Tentativa de calculo de Incremental para usina (', self.Nome, ') fora de operacao no mes ', imes, ' e ano ', iano)
        #     return 0
        # else:
        Incremental = self.Vazoes[iano, imes]
        for iusina in Montante(usinas, self, iano, imes):
            Incremental = Incremental - iusina.Vazoes[iano, imes]

        if Incremental < 0:
            Incremental = 0
            return Incremental
        else:
            return Incremental

    # Calcula vazao incremental entre a usina e todos os reservatorios a montante
    def QIncEntreRes(self, usinas, ianoconf, imesconf):

        nanos_hist = len(self.Vazoes)

        def Montante(usinas, usina, iano, imes):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.StatusVolMorto[iano][imes] == 2:
                        if iusi.VolUtil > 0:
                            yield iusi
                        else:
                            yield from Montante(usinas, iusi, iano, imes)
                    else:
                        yield from Montante(usinas, iusi, iano, imes)

        if self.StatusVolMorto[ianoconf][imesconf] != 2:
            print('Erro: Tentativa de calculo de Incremental para usina (', self.Nome, ') fora de operacao no mes ',
                  imesconf, ' e ano ', ianoconf)
            return 0
        else:
            Incremental = np.zeros((nanos_hist, 1), 'd')
            Incremental = self.Vazoes[0:nanos_hist, imesconf]
            for iusina in Montante(usinas, self, ianoconf, imesconf):
                Incremental = Incremental - iusina.Vazoes[0:nanos_hist, imesconf]

        if np.min(Incremental) < 0:
            contador = 0
            for i in range(nanos_hist):
                if Incremental[i] < 0:
                    # Incremental[i] = 0
                    contador = contador + 1
            # print ('Vazao Incremental da Usina ', self.Nome, 'menor que zero no mes ', imesconf, ' e ano ', ianoconf, 'Quantidade:', contador )
            return Incremental
        else:
            return Incremental

    def QIncHistEntreRes(self, usinas, ianoconf, imesconf):

        nanos_hist = len(self.Vazoes)

        def Montante(usinas, usina):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.TipoReg == b'M':
                        yield iusi
                    else:
                        yield from Montante(usinas, iusi)

        Incremental = self.Vazoes[ianoconf, imesconf]
        montante = Montante(usinas, self)
        for iusina in montante:
            Incremental -= iusina.Vazoes[ianoconf, imesconf]

        if Incremental <= 0:
            Incremental = 0

        return Incremental

        # if np.min(Incremental) < 0:
        #     contador = 0
        #     for i in range(nanos_hist):
        #         if Incremental[i] < 0:
        #             #Incremental[i] = 0
        #             contador = contador + 1
        #     #print ('Vazao Incremental da Usina ', self.Nome, 'menor que zero no mes ', imesconf, ' e ano ', ianoconf, 'Quantidade:', contador )
        #     return Incremental
        # else:
        #     return Incremental

    def ProdAcum(self, usinas):

        def CascataDesvAgua(usinas, iano, imes):
            current = self
            if current.StatusVolMorto[iano][imes] == 2 and current.VolUtil > 0:
                yield current
                while current.Jusante != 0:
                    for iusi in usinas:
                        if iusi.Codigo == current.Jusante:
                            if iusi.StatusVolMorto[iano][imes] == 2:
                                yield iusi
                            current = iusi
                            break
            else:
                condition = False
                for iusi in usinas:
                    if iusi.Codigo == current.Jusante and iusi.StatusVolMorto[iano][imes] == 2 and iusi.VolUtil > 0:
                        yield iusi
                        current = iusi
                        condition = True
                        break
                while current.Jusante != 0 and condition:
                    for iusi in usinas:
                        if iusi.Codigo == current.Jusante:
                            if iusi.StatusVolMorto[iano][imes] == 2:
                                yield iusi
                            current = iusi
                            break

        def CascataFiodAgua(usinas, iano, imes):
            current = self
            if current.StatusVolMorto[iano][imes] == 2:
                yield current
            condition = True
            while condition and current.Jusante != 0:
                jusante = [x for x in usinas if x.Codigo == current.Jusante]
                if jusante[0].VolIni > 0:
                    break
                for iusi in usinas:
                    if iusi.Codigo == current.Jusante:
                        if iusi.StatusVolMorto[iano][imes] == 2 and iusi.VolUtil == 0.:
                            yield iusi
                        else:
                            condition = False
                            break
                        current = iusi
                        break

        def Cascata(usinas, iano, imes):
            current = self
            if current.StatusVolMorto[iano][imes] == 2:
                yield current
            while current.Jusante != 0:
                for iusi in usinas:
                    if iusi.Codigo == current.Jusante:
                        if iusi.StatusVolMorto[iano][imes] == 2:
                            yield iusi
                        current = iusi
                        break

        nanos = len(self.StatusVolMorto)

        self.RoAcum_A_Ree = np.zeros((nanos, 12), 'd')
        self.RoAcum_B_Ree = np.zeros((nanos, 12), 'd')
        self.RoAcum_C_Ree = np.zeros((nanos, 12), 'd')

        self.RoAcum_A_Sist = np.zeros((nanos, 12), 'd')
        self.RoAcum_B_Sist = np.zeros((nanos, 12), 'd')
        self.RoAcum_C_Sist = np.zeros((nanos, 12), 'd')

        self.RoAcum = np.zeros((nanos, 12), 'd')
        self.RoAcum65 = np.zeros((nanos, 12), 'd')
        self.RoAcum50 = np.zeros((nanos, 12), 'd')
        self.RoAcumMax = np.zeros((nanos, 12), 'd')
        self.RoAcumMed = np.zeros((nanos, 12), 'd')
        self.RoAcumMin = np.zeros((nanos, 12), 'd')
        self.RoAcumOperEquiv = np.zeros((nanos, 12), 'd')
        self.RoAcumFiodAguaMax = np.zeros((nanos, 12), 'd')
        self.RoAcumFiodAguaMin = np.zeros((nanos, 12), 'd')
        self.RoAcumFiodAguaMed = np.zeros((nanos, 12), 'd')
        self.RoAcumFiodAguaEquiv = np.zeros((nanos, 12), 'd')

        self.RoAcumDesvAguaEquiv = np.zeros((nanos, 12), 'd')

        # for iusina in CascataFiodAgua(usinas, 0, 0):
        #     print(f'Justantes da usina {self.Nome}: {iusina.Nome}')

        for iano in range(nanos):
            for imes in range(12):
                trocouRee = 0
                trocouSist = 0
                FioRee = True
                FioSist = True

                for iusina in CascataDesvAgua(usinas, iano, imes):
                    produtibEquiv = iusina.RoEquiv[iano][imes]
                    if iusina.StatusMotoriz[iano][imes] == 2:
                        self.RoAcumDesvAguaEquiv[iano, imes] = self.RoAcumDesvAguaEquiv[iano, imes] + produtibEquiv

                for iusina in CascataFiodAgua(usinas, iano, imes):
                    produtibMax = iusina.RoMax[iano][imes]
                    produtibMed = iusina.RoEquiv50[iano][imes]
                    produtibEquiv = iusina.RoEquiv[iano][imes]
                    produtibMin = iusina.RoMin[iano][imes]
                    if iusina.StatusMotoriz[iano][imes] == 2:
                        self.RoAcumFiodAguaMax[iano, imes] = self.RoAcumFiodAguaMax[iano, imes] + produtibMax
                        self.RoAcumFiodAguaMin[iano, imes] = self.RoAcumFiodAguaMin[iano, imes] + produtibMin
                        self.RoAcumFiodAguaMed[iano, imes] = self.RoAcumFiodAguaMed[iano, imes] + produtibMed
                        self.RoAcumFiodAguaEquiv[iano, imes] = self.RoAcumFiodAguaEquiv[iano, imes] + produtibEquiv

                for iusina in Cascata(usinas, iano, imes):
                    produtib_minop = iusina.RoEquivMinOp[iano][imes]
                    produtib = iusina.RoEquiv[iano][imes]
                    produtib65 = iusina.RoEquiv65[iano][imes]
                    produtib50 = iusina.RoEquiv50[iano][imes]
                    produtibMax = iusina.RoMax[iano][imes]
                    produtibMed = iusina.RoEquiv50[iano][imes]
                    produtibMin = iusina.RoMin[iano][imes]
                    if iusina.StatusMotoriz[iano][imes] == 2:
                        self.RoAcum[iano][imes] = self.RoAcum[iano][imes] + produtib
                        self.RoAcum65[iano][imes] = self.RoAcum65[iano][imes] + produtib65
                        self.RoAcum50[iano][imes] = self.RoAcum50[iano][imes] + produtib50
                        self.RoAcumMax[iano][imes] = self.RoAcumMax[iano][imes] + produtibMax
                        self.RoAcumMed[iano][imes] = self.RoAcumMed[iano][imes] + produtibMed
                        self.RoAcumMin[iano][imes] = self.RoAcumMin[iano][imes] + produtibMin
                        self.RoAcumOperEquiv[iano, imes] = self.RoAcumOperEquiv[iano, imes] + produtib_minop

                    if iusina.Sist != self.Sist:
                        trocouSist = trocouSist + 1
                    if iusina.Ree != self.Ree:
                        trocouRee = trocouRee + 1

                    if trocouRee == 0:
                        if iusina.StatusMotoriz[iano][imes] == 2:
                            self.RoAcum_A_Ree[iano][imes] = self.RoAcum_A_Ree[iano][imes] + produtib
                    else:
                        if iusina.VolUtil > 0:
                            FioRee = False
                        if FioRee:
                            if iusina.StatusMotoriz[iano][imes] == 2:
                                self.RoAcum_B_Ree[iano][imes] = self.RoAcum_B_Ree[iano][imes] + produtib
                        else:
                            if iusina.StatusMotoriz[iano][imes] == 2:
                                self.RoAcum_C_Ree[iano][imes] = self.RoAcum_C_Ree[iano][imes] + produtib

                    if trocouSist == 0:
                        if iusina.StatusMotoriz[iano][imes] == 2:
                            self.RoAcum_A_Sist[iano][imes] = self.RoAcum_A_Sist[iano][imes] + produtib
                    else:
                        if iusina.VolUtil > 0:
                            FioSist = False
                        if FioSist:
                            if iusina.StatusMotoriz[iano][imes] == 2:
                                self.RoAcum_B_Sist[iano][imes] = self.RoAcum_B_Sist[iano][imes] + produtib
                        else:
                            if iusina.StatusMotoriz[iano][imes] == 2:
                                self.RoAcum_C_Sist[iano][imes] = self.RoAcum_C_Sist[iano][imes] + produtib

    def ProdAcumEntreResRee(self, iano, imes, usinas):
        if self.Jusante == 0:
            return 0
        for iusina in usinas:
            if iusina.Codigo == self.Jusante:
                if iusina.VolUtil != 0:
                    return 0.
                elif self.Ree != iusina.Ree:
                    return 0.
                elif iusina.StatusMotoriz[iano][imes] == 2:
                    return iusina.RoEquiv[iano][imes] + iusina.ProdAcumEntreResRee(iano, imes, usinas)
                else:
                    return iusina.ProdAcumEntreResRee(iano, imes, usinas)
                break

    # def ProdAcumEntreResSist(self, iano, imes, usinas):
    #     if self.Jusante == 0:
    #         return 0
    #     for iusina in usinas:
    #         if iusina.Codigo == self.Jusante:
    #             if iusina.VolUtil != 0:
    #                 return 0.
    #             elif self.Sist != iusina.Sist:
    #                 return 0.
    #             elif iusina.StatusMotoriz[iano][imes] == 2:
    #                 return iusina.RoEquiv + iusina.ProdAcumEntreResSist(iano, imes, usinas)
    #             else:
    #                 return iusina.ProdAcumEntreResSist(iano, imes, usinas)
    #             break

    #########################################################
    # Calcula Modelo PAR(p)
    #########################################################

    def parp(self, ord_max):

        nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

        media = np.mean(self.Vazoes[:, :], 0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(self.Vazoes[:, :], 0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)

        # Calcula vazao normalizada (nao precisa)
        # vaznorm = np.zeros((nanos,12),'d')
        # for iano in range(nanos):
        #    for imes in range(12):
        #        vaznorm[iano][imes] = (self.Vazoes[iano][imes] - media[imes])/desvio[imes]

        ################ TESTE ALEXANDRE #############################

        # # Calcula funcao de auto-correlacao (uma para cada mes)
        # FAC = np.zeros((12, ord_max), 'd')
        # for ilag in range(ord_max):
        #     for imes in range(12):
        #         for iano in np.arange(1, nanos + 1):
        #             ano_ant = iano
        #             mes_ant = imes - ilag - 1
        #             if mes_ant < 0:
        #                 ano_ant -= 1
        #                 mes_ant += 12
        #             FAC[imes][ilag] += (self.Vazoes[iano][imes] - media[imes]) * (
        #                         self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
        #         FAC[imes][ilag] /= (nanos * desvio[imes] * desvio[mes_ant])
        #
        # FACP = np.zeros((12, ord_max), 'd')
        # for ilag in np.arange(1, ord_max + 1):
        #     for imes in range(12):
        #         A = np.eye(ilag)
        #         B = np.zeros(ilag)
        #         # Preenche matriz triangular superior
        #         for ilin in range(len(A)):
        #             for icol in range(
        #                     len(A)):  # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
        #                 if icol > ilin:
        #                     mes = imes - ilin - 1
        #                     if mes < 0:
        #                         mes = mes + 12
        #                     A[ilin][icol] = FAC[mes][icol - ilin - 1]
        #             B[ilin] = FAC[imes][ilin]
        #         # Preenche matriz triangular inferior
        #         for ilin in range(len(A)):
        #             for icol in range(
        #                     len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
        #                 if icol < ilin:
        #                     A[ilin][icol] = A[icol][ilin]
        #         phi = np.linalg.solve(A, B)
        #         FACP[imes][ilag - 1] = phi[-1]

        ################ TESTE ALEXANDRE #############################

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros((12, ord_max + 1), 'd')
        for ilag in range(ord_max + 1):
            for imes in range(12):
                for iano in np.arange(1, nanos + 1):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    self.FAC[imes][ilag] += (self.Vazoes[iano][imes] - media[imes]) * (
                                self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= (nanos * desvio[imes] * desvio[mes_ant])

        # Calcula funcao de auto-correlacao parcial (uma para cada mes)
        self.FACP = np.zeros((12, ord_max + 1), 'd')
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
                            A[ilin][icol] = self.FAC[mes][icol - ilin]
                    B[ilin] = self.FAC[imes][ilin + 1]
                # Preenche matriz triangular inferior
                for ilin in range(len(A)):
                    for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                        if icol < ilin:
                            A[ilin][icol] = A[icol][ilin]

                phi = np.linalg.solve(A, B)
                self.FACP[imes][ilag] = phi[len(phi) - 1]

            galo = 13

        # Identificacao da ordem
        IC = 1.96 / sqrt(nanos - 1)
        self.Ordem = np.zeros(12, 'i')
        for imes in range(12):
            self.Ordem[imes] = 0
            for ilag in range(ord_max + 1):
                if self.FACP[imes][ilag] > IC or self.FACP[imes][ilag] < -IC:
                    self.Ordem[imes] = ilag

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
                        A[ilin][icol] = self.FAC[mes][icol - ilin]
                B[ilin] = self.FAC[imes][ilin + 1]
            # Preenche matriz triangular inferior
            for ilin in range(len(A)):
                for icol in range(len(A)):  # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                    if icol < ilin:
                        A[ilin][icol] = A[icol][ilin]
            phi = np.linalg.solve(A, B)
            for iord in range(len(phi)):
                self.CoefParp[imes][iord] = phi[iord]

    def gera_series_aditivo(self, nr_ser):

        nanos = len(self.Vazoes) - 1
        media = np.mean(self.Vazoes[:nanos], 0)
        desvio = np.std(self.Vazoes[:nanos], 0)

        # Calculo dos residuos
        residuos = np.zeros((nanos - 1, 12))
        for iano in np.arange(1, nanos):
            for imes in range(12):
                residuos[iano - 1][imes] = (self.Vazoes[iano][imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    residuos[iano - 1][imes] -= self.CoefParp[imes][ilag] * (
                                self.Vazoes[ano_ant][mes_ant] - media[mes_ant]) / desvio[mes_ant]

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_ser, 60), 'd')
        for iser in range(nr_ser):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(0, nanos - 1)
                    valor = media[imes] + desvio[imes] * residuos[serie][imes]
                    for ilag in range(int(self.Ordem[imes])):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_adit[iser][contador - 1 - ilag]
                        valor += desvio[imes] * self.CoefParp[imes][ilag] * (vazant - media[mes_ant]) / desvio[mes_ant]
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_adit.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2,
                 label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Aditive Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflow (m^3/s', fontsize=16)
        plt.legend(fontsize=12)
        plt.show()

        return sintetica_adit

    def gera_series_multiplicativo(self):

        nanos = len(self.Vazoes) - 1
        ord_max = len(self.CoefParp[0])

        media = np.mean(self.Vazoes[1:nanos], 0)
        desvio = np.std(self.Vazoes[1:nanos], 0)

        # Calculo dos residuos
        residuosmult = np.zeros((nanos, 12))
        termoind = np.zeros(12, 'd')
        for iano in np.arange(1, nanos):
            for imes in range(12):
                residuosmult[iano][imes] = self.Vazoes[iano][imes]
                somatorio = 0
                termoind[imes] = media[
                    imes]  # Versao centrada: ver pagina 20 dissertacao Filipe Goulart Cabral (COPPE 2016)
                # O ideal portanto, seria utilizar este metodo com formulacao de otimzicao ao
                # inves de yule-walker. Restringindo que o termo-ind e os phis sejam todos positivos
                for ilag in range(ord_max):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    somatorio += self.CoefParp[imes][ilag] * self.Vazoes[ano_ant][mes_ant]
                    termoind[imes] -= self.CoefParp[imes][ilag] * media[mes_ant]
                residuosmult[iano][imes] = residuosmult[iano][imes] / (termoind[imes] + somatorio)

        # Gera series sinteticas
        sintetica_mult = np.zeros((1000, 60), 'd')
        for iser in range(1000):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(1, nanos - 1)
                    valor = termoind[imes]
                    for ilag in range(ord_max):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_mult[iser][contador - 1 - ilag]
                        valor += self.CoefParp[imes][ilag] * vazant
                    sintetica_mult[iser][contador] = valor * residuosmult[serie][imes]

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_mult.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_mult, 0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult, 0) + np.std(sintetica_mult, axis=0), 'r-.', lw=2,
                 label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult, 0) - np.std(sintetica_mult, axis=0), 'r-.', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Multiplicative Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflows (m3/s)', fontsize=16)
        # plt.ylim(-100, 30000)
        plt.legend(fontsize=12)
        plt.show()

        vasco = 1000

    def pso(self, ord_max):

        def objetivo(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros(ord_max + 1, 'd')
            for icoef in range(ord_max + 1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            residuos = np.zeros(nanos - 1)

            for iano in np.arange(1, nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                residuos[iano - 1] = (self.Vazoes[iano][imes] / somatorio)
                objetivo += ((self.Vazoes[iano][imes] / somatorio) ** 2)

            total = np.sum(residuos) - nanos + 1
            total = total ** 2
            total = 10000 * total

            return (objetivo / (nanos - 1) + total)

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.CoefIndParp = np.zeros(12, 'd')
        self.Ordem = np.zeros(12, 'd')
        for imes in range(12):
            print('*******', imes + 1)

            best = 999999
            best_ordem = 0
            for iord in np.arange(1, (ord_max + 1)):
                # Define limites e condicao inicial
                lb = np.zeros(iord + 1)
                ub = np.zeros(iord + 1)
                for i in range(iord + 1):
                    lb[i] = 0.00001
                    ub[i] = 10000

                print('**', iord)
                solution, fopt = pso(objetivo, lb, ub, args=(iord, imes), maxiter=500)

                # solution = minimize(objetivo, x0, method= 'SLSQP', bounds=limites, constraints=cons, args=( iord, imes), options={ 'disp': False, 'maxiter': 10000 }  )
                if fopt < best:
                    best = fopt
                    best_ordem = iord

            self.Ordem[imes] = best_ordem

            solution, fopt = pso(objetivo, lb, ub, args=(iord, imes), maxiter=5000)

            for icoef in range(ord_max):
                self.CoefParp[imes][icoef] = solution[icoef + 1]
            self.CoefIndParp[imes] = solution[0]

    def parp_otimo(self, ord_max):

        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def objetivo(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros(ord_max + 1, 'd')
            for icoef in range(ord_max + 1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            for iano in np.arange(1, nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                objetivo += ((self.Vazoes[iano][imes] / somatorio) ** 2)

            return objetivo / (nanos - 1)

        # Restricoes a media dos residuos devem ser igual a unidade ou somatorio dos residuos devem ser igual a nanos
        def restricao(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros(ord_max + 1, 'd')
            for icoef in range(ord_max + 1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                objetivo += (self.Vazoes[iano][imes] / somatorio)
                residuos[iano - 1] = (self.Vazoes[iano][imes] / somatorio)
                desvio = np.std(residuos)
                # curtose = kurtosis(residuos) - 3
            # return ([ objetivo - nanos + 1 , desvio - 0.2])
            return ([objetivo - nanos + 1])

        # Define limites e condicao inicial
        x0 = np.zeros(ord_max + 1)
        limites = []
        for i in range(ord_max + 1):
            x0[i] = 0.1
            limites.append((-10000, 10000))

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.CoefIndParp = np.zeros(12, 'd')
        self.Ordem = np.zeros(12, 'd')
        for imes in range(12):
            print('*******', imes + 1)
            conl = {'type': 'eq', 'fun': restricao, 'args': (ord_max, imes)}
            cons = ([conl])
            best = 999999
            best_ordem = 0
            # for iord in np.arange(1,(ord_max+1)):
            for iord in np.arange(6, 7):
                solution = minimize(objetivo, x0, method='SLSQP', bounds=limites, constraints=cons, args=(iord, imes),
                                    options={'disp': False, 'maxiter': 10000})
                if solution.fun < best:
                    best = solution.fun
                    best_ordem = iord

            self.Ordem[imes] = best_ordem
            solution = minimize(objetivo, x0, method='SLSQP', bounds=limites, constraints=cons, args=(best_ordem, imes),
                                options={'disp': True, 'maxiter': 10000})

            for icoef in range(ord_max):
                self.CoefParp[imes][icoef] = solution.x[icoef + 1]
            self.CoefIndParp[imes] = solution.x[0]

    def gera_series_multiplicativo_parp_otimo(self):

        nanos = len(self.Vazoes) - 1
        ord_max = len(self.CoefParp[0])

        media = np.mean(self.Vazoes[1:nanos], 0)
        desvio = np.std(self.Vazoes[1:nanos], 0)

        # Calculo dos residuos
        residuosmult = np.zeros((nanos, 12))
        for iano in np.arange(1, nanos):
            for imes in range(12):
                residuosmult[iano][imes] = self.Vazoes[iano][imes]
                somatorio = 0
                for ilag in range(ord_max):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    somatorio += self.CoefParp[imes][ilag] * self.Vazoes[ano_ant][mes_ant]
                residuosmult[iano][imes] = residuosmult[iano][imes] / (self.CoefIndParp[imes] + somatorio)

        # Gera series sinteticas
        sintetica_mult = np.zeros((1000, 60), 'd')
        for iser in range(1000):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(1, nanos - 1)
                    valor = self.CoefIndParp[imes]
                    for ilag in range(ord_max):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_mult[iser][contador - 1 - ilag]
                        valor += self.CoefParp[imes][ilag] * vazant
                    sintetica_mult[iser][contador] = valor * residuosmult[serie][imes]

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_mult.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_mult, 0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult, 0) + np.std(sintetica_mult, axis=0), 'r-.', lw=2,
                 label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult, 0) - np.std(sintetica_mult, axis=0), 'r-.', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Multiplicative Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflows (m3/s)', fontsize=16)
        # plt.ylim(-100, 30000)
        plt.legend(fontsize=12)
        plt.show()

    def parp_alexandre(self, ord_max):

        nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

        media = np.mean(self.Vazoes[:nanos, :],
                        axis=0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(self.Vazoes[:nanos, :],
                        axis=0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)

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
                    self.FAC[imes][ilag] += (self.Vazoes[iano][imes] - media[imes]) * (
                                self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
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

    def parp_otimo_alexandre(self, ord_max):

        nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)
        media = np.mean(self.Vazoes[:nanos, :],
                        axis=0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(self.Vazoes[:nanos, :],
                        axis=0)  # A primeira serie historica eh utilizada como tendencia (despreze-a)

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
                    self.FAC[imes][ilag] += (self.Vazoes[iano][imes] - media[imes]) * (
                            self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= ((nanos - 1) * desvio[imes] * desvio[mes_ant])

        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def objetivo(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # último ano está incompleto
            media = np.mean(self.Vazoes[:nanos], axis=0)
            desv_pad = np.std(self.Vazoes[:nanos], axis=0)

            # Calcula funcao de auto-correlacao
            FAC = np.zeros(ord_max, 'd')
            for ilag in range(ord_max):
                for iano in np.arange(1, nanos):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    FAC[ilag] += (self.Vazoes[iano][imes] - media[imes]) * (
                                self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
                FAC[ilag] /= ((nanos - 1) * desv_pad[imes] * desv_pad[mes_ant])

            # TODO: Montagem da FOB
            coef = np.zeros(ord_max, 'd')
            for icoef in range(ord_max):
                coef[icoef] = x[icoef]

            # Calcula o desvio padrão do ruido
            variancia_ruido = 1
            for icoef in range(len(coef)):
                variancia_ruido -= coef[icoef] * FAC[icoef]
            # variancia_ruido = (desv_pad[imes] ** 2) * (1 + somatorio)  # outra fórmula

            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = (self.Vazoes[iano, imes] - media[imes]) / desv_pad[imes]
                for ilag in range(ord_max):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= coef[ilag] * ((self.Vazoes[ano_ant, mes_ant] - media[mes_ant]) / desv_pad[mes_ant])
                residuos[iano - 1] = somatorio

            variancia = np.std(residuos) ** 2

            return np.abs(np.mean(residuos)) + (variancia - variancia_ruido)

        # Restricoes a media dos residuos devem ser igual a unidade ou somatorio dos residuos devem ser igual a nanos
        def restricao(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # último ano está incompleto

            media = np.mean(self.Vazoes[:nanos], axis=0)
            desv_pad = np.std(self.Vazoes[:nanos], axis=0)

            # Cálculo da variância do ruido
            somatorio = 0.
            for ilag in range(ord_max):
                autocorr = 0
                for iano in np.arange(1, nanos):  # começa a partir do segundo ano
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    aux1 = (self.Vazoes[iano][imes] - media[imes]) / desv_pad[imes]
                    aux2 = (self.Vazoes[ano_ant][mes_ant] - media[mes_ant]) / desv_pad[mes_ant]
                    autocorr += aux1 * aux2
                autocorr = autocorr / (nanos - 1)
                somatorio += autocorr

            variancia_ruido = (desv_pad[imes] ** 2) * (1 + somatorio)

            # Montagem da restrição de variância do ruido
            coef = np.zeros(ord_max, 'd')
            for icoef in range(ord_max):
                coef[icoef] = x[icoef]

            residuos = np.zeros(nanos - 1)
            for iano in np.arange(1, nanos):
                somatorio = (self.Vazoes[iano][imes] - media[imes]) / desv_pad[imes]
                for ilag in range(ord_max):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= coef[ilag] * ((self.Vazoes[ano_ant][mes_ant] - media[mes_ant]) / desv_pad[mes_ant])
                residuos[iano - 1] = somatorio

            variancia = np.std(residuos) ** 2

            # variancia_ruido = desv_pad[imes] ** 2
            return ([variancia - variancia_ruido])

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.Ordem = np.zeros(12, 'd')
        for imes in range(12):
            print('*******', imes + 1)
            best = 999999
            for iord in np.arange(1, (ord_max + 1)):

                conl = {'type': 'eq', 'fun': restricao, 'args': (iord, imes)}
                cons = ([conl])
                cons_new = ([])

                # Define limites e condicao inicial
                x0 = np.zeros(iord)
                limites = []
                for i in range(iord):
                    x0[i] = 0.1
                    limites.append((-1, 1))

                solution = minimize(objetivo, x0, method='SLSQP', bounds=limites, constraints=cons_new,
                                    args=(iord, imes), options={'disp': False, 'maxiter': 10000})

                if solution.fun < best:
                    best = solution.fun
                    self.Ordem[imes] = iord
                    COEF = solution.x

            for iord in range(len(COEF)):
                self.CoefParp[imes, iord] = COEF[iord]

    def gera_series_aditivo_alexandre(self, nr_ser, nr_meses):

        nanos = len(self.Vazoes) - 1

        media = np.mean(self.Vazoes[:nanos, :], axis=0)  # média
        desvio = np.std(self.Vazoes[:nanos, :], axis=0)  # desvio padrão
        assim = stats.skew(self.Vazoes[:nanos, :], axis=0)  # coeficiente de assimetria

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
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_adit[iser][contador - ilag - 1]
                        delta -= self.CoefParp[imes][ilag] * (vazant - media[mes_ant]) / desvio[mes_ant]
                        valor += desvio[imes] * self.CoefParp[imes][ilag] * (vazant - media[mes_ant]) / desvio[mes_ant]
                    teta = 1 + ((desvio_ruido[imes] ** 2) / ((-delta) ** 2))
                    # aux1 = 1 + ((assim[imes] ** 2) / 2)
                    # aux2 = ((assim[imes] ** 2) + ((assim[imes] ** 4) / 4)) ** (1/2)
                    # teta = ((aux1 + aux2) ** (1/3)) + ((aux1 - aux2) ** (1/3)) - 1
                    mu = (1 / 2) * np.log((desvio_ruido[imes] ** 2) / (teta * (teta - 1)))
                    sigma = np.sqrt(np.log(teta))
                    epsilon = np.random.normal(mu, sigma, 1)
                    ruido = np.exp(epsilon) + delta  # desvio_ruido[imes] * np.random.normal(0, 1, 1)
                    valor += desvio[imes] * ruido
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2,
                 label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Aditive Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflow (m^3)/s', fontsize=16)
        plt.legend(fontsize=12)
        # plt.show()

        self.series_sinteticas = sintetica_adit

    def gera_series_aditivo_ricardo(self, nr_ser, nr_meses):

        nanos = len(self.Vazoes) - 1

        media = np.mean(self.Vazoes[:nanos, :], axis=0)  # média
        desvio = np.std(self.Vazoes[:nanos, :], axis=0)  # desvio padrão

        # PASSO 1: Ruídos
        ruidos = np.zeros((nanos - 1, 12))
        for imes in range(12):
            for iano in np.arange(1, nanos):
                somatorio = (self.Vazoes[iano, imes] - media[imes]) / desvio[imes]
                for ilag in range(int(self.Ordem[imes])):
                    mes_ant = imes - ilag - 1
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio -= self.CoefParp[imes, ilag] * (
                                (self.Vazoes[ano_ant, mes_ant] - media[mes_ant]) / desvio[mes_ant])
                ruidos[iano - 1, imes] = somatorio

        # PASSO 2: Média e variância do ruído
        media_ruido = np.mean(ruidos, axis=0)
        variancia_ruido = np.var(ruidos, axis=0)

        # PASSO 3: for para geração das séries
        sintetica_adit = np.zeros((nr_ser, nr_meses), 'd')
        x0 = np.min(self.Vazoes[:nanos, :], axis=0)
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
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_adit[iser][contador - ilag - 1]
                        valor += self.CoefParp[imes, ilag] * ((vazant - media[mes_ant]) / desvio[mes_ant])

                    # PASSO 4: Estimativas dos parâmetros (teta, média e variância)
                    teta = 1 + (variancia_ruido[imes] / ((media_ruido[imes] - valor) ** 2))
                    var = np.log(teta)
                    med = 0.5 * np.log(variancia_ruido[imes] / ((teta ** 2) - teta))

                    # PASSO 6: Geração de números randômicos
                    num_rand = np.random.normal(med, np.sqrt(var), 1)

                    # PASSO 7: Geração da vazão sintética
                    sintetica_adit[iser, contador] = x0[imes] + desvio[imes] * np.exp(num_rand)

        x_axis = np.arange(1, nr_meses + 1)
        plt.plot(x_axis, sintetica_adit.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_adit, 0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) + np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2,
                 label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit, 0) - np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2)
        m = np.concatenate([media, media, media, media, media])
        d = np.concatenate([desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Aditive Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflow (m^3)/s', fontsize=16)
        plt.legend(fontsize=12)
        # plt.show()

        self.series_sinteticas = sintetica_adit

    def Teste_de_Media(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = self.Vazoes[1:nanos, cont]
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ttest_ind(a, b, equal_var=True)
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
        print("Resultado do Teste de Média das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

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
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\nTESTE DE MÉDIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        # plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Media

    def Teste_de_Variancia(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste de Levene
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = self.Vazoes[1:nanos, cont]
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.levene(a, b)
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
        print("Resultado do Teste de Variância das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

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
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\nTESTE DE VARIÂNCIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        # plt.show()

    def Teste_de_Aderencia(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        aprovados = 0

        # Realizacao do Teste T
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = self.Vazoes[1:nanos, cont]
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ks_2samp(a, b)
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
        print("Resultado do Teste de Aderência das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

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
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\nTESTE DE ADERÊNCIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        # plt.show()

    def Teste_de_Mediana(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]

        # Realizacao do Teste de Wilcoxon
        aprovados = 0
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = self.Vazoes[1:nanos, cont]
            b = self.series_sinteticas[:, iteste]
            t_valor, p_valor = stats.ranksums(a, b)
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
        print("Resultado do Teste de Mediana das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

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
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\nTESTE DE MEDIANA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Mediana

    def Teste_de_Assimetria(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]

        # Realizacao do Teste de Assimetria
        aprovados = 0
        Teste = np.zeros((2, nestagios))
        cont = 0
        for iteste in range(nestagios):
            a = self.Vazoes[1:nanos, cont]
            b = self.series_sinteticas[:, iteste]
            z_valor1, p_valor1 = stats.skewtest(a)
            z_valor2, p_valor2 = stats.skewtest(b)
            aux = p_valor1 - p_valor2
            max_v = max(p_valor1, p_valor2)
            Teste[1, iteste] = abs(aux / max_v) * 100

            # Verificacao da quantidade de valores aprovados
            if Teste[1, iteste] >= float(40):
                aprovados += 1

            if (cont < 11):
                cont = cont + 1
            else:
                cont = 0

        # Aprovação total da serie
        porcentagem = int((aprovados / nestagios) * 100)
        print("Resultado do Teste de Assimetria das Séries Sintéticas Geradas: ", porcentagem, "% aprovados.")

        # Grafico analitico
        y_axis = Teste[1, :]
        x_axis = np.arange(1, 61)
        k_axis = np.zeros((nestagios, 1))
        for iplot in range(nestagios):
            k_axis[iplot, 0] = int(40)
        width_n = 0.9
        bar_color = 'gray'
        plt_color = 'red'
        plt.bar(x_axis, y_axis, width=width_n, color=bar_color, label=str(porcentagem) + "% Aprovados")
        plt.plot(x_axis, k_axis, color=plt_color)
        titulo = "Caso da Usina Hidrelétrica de " + self.Nome.strip() + "\nTESTE DE ASSIMETRIA"
        plt.title(titulo, fontsize=16)
        plt.xlabel('Meses', fontsize=16)
        plt.ylabel('p-valor (%)', fontsize=16)
        plt.ylim(0, 100)
        plt.xlim(0, 61)
        plt.legend(fontsize=12)
        plt.show()

        # Retorno dos resultados obtidos pelo teste
        # return Teste_Assimetria

    def consecutive(self, data, stepsize=1):
        return np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)

    def Teste_de_Sequencia_Negativa(self):

        # Vetorizacao da media mensal historica de vazoes, tendo em vista o numero de estagios de analise
        nanos = len(self.Vazoes) - 1
        nestagios = self.series_sinteticas.shape[1]
        nseries = self.series_sinteticas.shape[0]

        # Determinação do periodo da serie historica com menor vazao acumulada
        total_periodo_ant = []
        periodo_seco = []
        fim_periodo = 5
        for iperiodo in range(nestagios - 5):
            serie_analisada = self.Vazoes[iperiodo:fim_periodo, :]
            total_meses = sum(serie_analisada)
            total_periodo = sum(total_meses)
            print(total_periodo)

            if iperiodo == 0:
                total_periodo_ant = total_periodo
                periodo_seco = serie_analisada
            else:
                if total_periodo <= total_periodo_ant:
                    total_periodo_ant = total_periodo
                    periodo_seco = serie_analisada

            fim_periodo = fim_periodo + 1
        print(total_periodo_ant)

        # Comparacao entre a serie historica e o periodo historico com menor vazao acumulada
        aprovados = 0
        Comprimento = np.zeros((nseries, nestagios))
        Soma = np.zeros((nseries, nestagios))
        Intensidade = np.zeros((nseries, nestagios))
        cont = 0
        for iserie in range(nseries):
            a = np.reshape(periodo_seco, (1, 60))
            b = self.series_sinteticas[iserie, :]
            c = b - a
            d = np.nonzero(c > 0)
            data = d[1]
            grupos = self.consecutive(data)
            print(grupos)
            for igrupo in range(len(grupos)):
                pos = grupos[igrupo]
                print(pos)
                valores = c[pos]
                Comprimento[iserie, igrupo] = pos.shape[1]
                Soma[iserie, igrupo] = sum(valores)
                Intensidade[iserie, igrupo] = sum(valores) / (pos.shape[1])
                print(Intensidade[iserie, igrupo])
        # Retorno dos resultados obtidos pelo teste
        # return Teste_Assimetria

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
