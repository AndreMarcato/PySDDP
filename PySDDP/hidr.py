import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from random import randint
from scipy.optimize import minimize
from pyswarm import pso


class hidr(object):

    # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)
    Codigo = None           # Codigo da UHE
    Nome = None             # Nome da UHE
    Posto = None            # Numero do Posto
    Bdh = None              # Desvio - Nao sei qual e esta informacao ??????
    Sist = None             # Submercado
    Empr = None             # Codigo da empresa
    Jusante = None          # Codigo de Jusante
    Desvio = None           # Desvio - Nao sei qual e esta informacao ??????
    VolMin = None           # Volume Minimo
    VolMax = None           # Volume Maximo
    VolVert = None          # Volume Vertimento
    VolMinDesv = None       # Volume Minimo para Desvio
    CotaMin = None          # Cota Minima
    CotaMax = None          # Cota Maxima
    PolCotaVol = None       # Polinomio Cota-Volume
    PolCotaArea = None      # Polinomio Cata-Area
    CoefEvap = None         # Coeficientes de Evaporacao
    NumConjMaq = None       # Numero de Conjuntos de Maquinas
    MaqporConj = None       # Numero de Maquinas por Conjunto
    PEfporConj = None       # POtencia Efetiva por Maquina do Conjunto

    CF_HBQT = None          # Nao sei qual e esta informacao ??????
    CF_HBQG = None          # Nao sei qual e esta informacao ??????
    CF_HBPT = None          # Nao sei qual e esta informacao ??????

    AltEfetConj = None      # Altura de Queda Efetiva do Conjunto
    VazEfetConj = None      # Vazao Efetiva do Conjunto
    ProdEsp = None          # Produtibilidade Especifica
    PerdaHid = None         # Perda Hidraulica
    NumPolVNJ = None        # Numero de Polinomios Vazao Nivel Jusante

    PolVazNivJus = None     # Polinomios Vazao Nivel Jusante

    CotaRefNivelJus = None  # Cota Referencia Nivel de Jusante
    CFMed = None            # Cota Media do Canal de Fuga
    InfCanalFuga = None     # Informacao Canal de Fuga - Nao sei qual e esta informacao ??????
    FatorCargaMax = None    # Fator de Caga Maximo - Nao sei qual e esta informacao ?????????
    FatorCargaMin = None    # Fator de Caga Minimo - Nao sei qual e esta informacao ?????????
    VazMin = None           # Vazao Minima Obrigatoria
    UnidBase = None         # Numero de Unidades de Base
    TipoTurb = None         # Tipo de Turbina Hidraulica
    Repres_Conj = None      # Representacao Conjunto de Maquina - Nao sei qual e esta informacao ?????
    TEIFH = None            # Taxa Equivalente de Indisponibilidade Forcada Hidraulica
    IP = None               # Indisponibilidade Programada
    TipoPerda = None        # Tipo Perda Hidraulica
    Data = None             # Nao sei qual e esta informacao ??????
    Observ = None           # Observacao
    VolRef = None           # Volume de Referencia
    TipoReg = None          # Tipo de Regulacao

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
    Ro65 = None             # PDTMED (NEWAVE) - PROD. ASSOCIADA A ALTURA CORRESPONDENTE A 65% DO V.U.
    Ro50 = None
    RoMax = None            # PDTMAX (NEWAVE) - PROD. ASSOCIADA A ALTURA MAXIMA
    RoMin = None            # PDTMIN (NEWAVE) - PROD. ASSOCIADA A ALTURA MINIMA
    RoEquiv = None          # PRODT (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO AO VOL. MAXIMO )
    RoEquiv65 = None        # PRODTM (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO A 65% DO V.U. )
    Engolimento = None
    RoAcum = None           # PDTARM (NEWAVE) - PROD. ACUM. PARA CALCULO DA ENERGIA ARMAZENADA
    RoAcum65 = None         # PDAMED (NEWAVE) - PROD. ACUM. PARA CALCULO DA ENERGIA ARMAZENADA CORRESPONDENTE A 65% DO V.U.
    RoAcumMax = None        # PDCMAX e PDVMAX (NEWAVE) - PROD. ACUM.
    RoAcumMed = None        # PDTCON, PDCMED e PDVMED (NEWAVE) - PROD. ACUM.
    RoAcumMin = None        # PDCMIN e PDVMIN (NEWAVE) - PROD. ACUM.

    RoAcum_A_Ree = None
    RoAcum_B_Ree = None
    RoAcum_C_Ree = None
    RoAcum_A_Sist = None
    RoAcum_B_Sist = None
    RoAcum_C_Sist = None

    RoAcumEntreResRee = None
    RoAcumEntreResSist = None

    # Vazoes Naturais, Incrementais e Par(p)
    Vazoes = None       # Historico de Vazoes naturais (imes, ilag)
    FAC = None          # Funcao de Autocorrelacao (imes, ilag)
    FACP = None         # Funcao de Autocorrelacao Parcial (imes, ilag)
    CoefParp = None     # Coeficientes do Modelo par(p) (imes,ilag)
    CoefIndParp  = None     # Coeficientes independentes do Modelo par(p) (imes) - Aditivo = 0 - Multiplicativo > 0
    Ordem = None        # Ordem do modelo par(p) para todos os meses (mes)

    # Parametros da usina Dependentes do Tempo - Especificados (MODIF.DAT)
    VolMinT = None     # Volume Mínimo Operativo (pode variar mes a mes)
    VolMaxT = None     # Volume Maximo Operativo (pode variar mes a mes)
    VolMinP = None     # Volume Mínimo com adocao de penalidade (pode variar mes a mes)
    VazMinT = None     # Vazao Minima pode variar mes a mes
    CFugaT  = None     # Cota do Canal de Fuga (pode varia mes a mes)

    # Parametros relativos a expansao hidrica que variam no tempo para usinas 'EE' e 'NE' (EXPH)
    StatusVolMorto = None       # Status do Volume Morto - 0: Nao Comecou Encher - 1: Enchendo - 2: Cheio
    VolMortoTempo = None        # Evolucao do Volume Minimo da Usina
    StatusMotoriz  = None       # Status da Motorizacao  - 0: Nao Comecou Motorizar - 1: Motorizando - 3: Motorizada
    UnidadesTempo = None        # Numero de Unidades em cada mes
    EngolTempo = None           # Evolucao do Engolimento Maximo da Usina
    PotenciaTempo = None        # Evolucao da Potencia Instalada da Usina

    ##########################################################################################################
    # Graficos Diversos
    ##########################################################################################################

    # Plota Polinomio Cota-Volume
    def PlotaPCV(self):
        if self.VolMin == 0:
            return

        if (self.VolMin == self.VolMax):
            volumes = np.linspace(self.VolMin - 1,self.VolMax + 1, 100)
        else:
            volumes = np.linspace(self.VolMin,self.VolMax,100)
        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]
        cota = a + b*volumes + c*volumes**2 + d*volumes**3 + e*volumes**4
        cota.shape = volumes.shape
        plt.plot(volumes, cota, 'b-', lw=3)

        plt.xlabel('Volume do Reservatorio (hm^3)', fontsize=16)
        titulo = 'Polinomio Cota-Volume da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Cota em Metros', fontsize=16)
        plt.xlim(volumes[0], volumes[99])
        if ( cota[0] == cota[99]):
            plt.ylim(cota[0]-1, cota[99]+1)
        else:
            plt.ylim(cota[0], cota[99])
        plt.show()

    # Plota Polinomio Cota-Area
    def PlotaPCA(self):
        if self.VolMin == 0:
            return

        if (self.CotaMax == self.CotaMin):
            cotas = np.linspace(self.CotaMin - 1,self.CotaMax + 1, 100)
        else:
            cotas = np.linspace(self.CotaMin,self.CotaMax,100)
        a = self.PolCotaArea[0]
        b = self.PolCotaArea[1]
        c = self.PolCotaArea[2]
        d = self.PolCotaArea[3]
        e = self.PolCotaArea[4]
        areas = a + b*cotas + c*cotas**2 + d*cotas**3 + e*cotas**4
        areas.shape = cotas.shape
        plt.plot(cotas, areas, 'b-', lw=3)

        plt.xlabel('Cota do Reservatorio (em metros)', fontsize=16)
        titulo = 'Polinomio Cota-Area da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Area Superficia em km^2', fontsize=16)
        plt.xlim(cotas[0], cotas[99])
        if ( areas[0] == areas[99]):
            plt.ylim(areas[0]-1, areas[99]+1)
        else:
            plt.ylim(areas[0], areas[99])
        plt.show()

    # Plota Curva Colina
    def PlotaColina(self):
        if self.VolMin == 0:
            return

        if (self.VolMin == self.VolMax):
            volumes = np.linspace(self.VolMin - 1,self.VolMax + 1, 100)
        else:
            volumes = np.linspace(self.VolMin,self.VolMax,100)

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        cotamont = a + b*volumes + c*volumes**2 + d*volumes**3 + e*volumes**4
        cotamont.shape = volumes.shape

        qdef = np.linspace(self.VazMin, 5*self.Engolimento, 100)

        a = self.PolVazNivJus[0][0]
        b = self.PolVazNivJus[0][1]
        c = self.PolVazNivJus[0][2]
        d = self.PolVazNivJus[0][3]
        e = self.PolVazNivJus[0][4]

        cotajus = a + b*qdef + c*qdef**2 + d*qdef**3 + e*qdef**4
        cotajus.shape = qdef.shape

        xGrid, yGrid = np.meshgrid(cotamont, cotajus)

        z = self.ProdEsp * ( xGrid - yGrid )

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surf = ax.plot_surface(qdef, volumes,z, rcount=100, ccount = 100, cmap=plt.cm.coolwarm,
                       linewidth=0, antialiased=False)

        plt.xlabel('Vazão Defluente em m^3/s', fontsize=12)
        titulo = 'Produtibilidade da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.ylabel('Volume Armazenado em hm^3', fontsize=12)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()


    def PlotaProdutibs(self, iano, imes):
        x_axis = np.arange(1,6)
        y_axis = [ self.RoEquiv[iano][imes], self.RoMin[iano][imes], self.Ro50[iano][imes], self.Ro65[iano][imes], self.RoMax[iano][imes] ]
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
        x_axis = np.arange(1,13)
        plt.plot(x_axis,self.Vazoes.transpose(),'c-')
        media = np.mean(self.Vazoes, axis=0)
        plt.plot(x_axis,media,'r-',lw=3)
        desvio = np.nanstd(self.Vazoes, axis=0)
        plt.plot(x_axis,media+desvio,'r-.',lw=2)
        plt.plot(x_axis,media-desvio,'r-.',lw=2)
        ultimo = len(self.Vazoes)-1
        plt.plot(x_axis,self.Vazoes[:][ultimo],'b-')
        titulo = 'Historico de Vazoes da Usina ' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes do Ano', fontsize=16)
        plt.ylabel('Vazao', fontsize=16)
        plt.show()

    def PlotaVolume(self):
        nanos = len(self.VolMinT)

        fig = plt.figure()
        ax = plt.subplot(111)


        x_axis = np.arange(1,nanos*12+1)
        ax.plot(x_axis,self.VolMinT.reshape(nanos*12),'g-.',lw=2, label = 'Vol.Min.Operat.')
        ax.plot(x_axis,self.VolMaxT.reshape(nanos*12),'g-.',lw=2, label = 'Vol.Max.Operat.')
        ax.plot(x_axis,self.VolMax*np.ones(nanos*12),'b-',lw=3,   label = 'Vol.Minimo Real')
        ax.plot(x_axis,self.VolMin*np.ones(nanos*12),'b-',lw=3,   label = 'Vol.Maximo Real')
        ax.plot(x_axis,self.VolMinP.reshape(nanos*12),'b-.',lw=2, label = 'Vol.Min.com Pen.')

        plt.fill_between(x_axis,self.VolMinT.reshape(nanos*12), self.VolMaxT.reshape(nanos*12), facecolor='g', alpha=0.1)

        titulo = 'Evolucao dos Volumes da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Volume em hm^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([ box.x0, box.y0, box.width*0.7, box.height] )

        ax.legend(loc='center left', shadow=True, fontsize=12, bbox_to_anchor=(1, 0.5))

        plt.show()

    def PlotaVazMin(self):
        nanos = len(self.VazMinT)

        fig = plt.figure()
        ax = plt.subplot(111)

        x_axis = np.arange(1,nanos*12+1)
        ax.plot(x_axis,self.VazMinT.reshape(nanos*12),'g-.',lw=2, label='Vaz.Min.Operat.')
        ax.plot(x_axis,self.VazMin*np.ones(nanos*12),'b-',lw=3,   label='Vaz.Min.Cadastro')

        titulo = 'Evolucao da Vazao Minima da Usina \n' + self.Nome
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Vazao Minima em m^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([ box.x0, box.y0, box.width*0.7, box.height] )

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

        x_axis = np.arange(1,nanos*12+1)
        p1 = ax.plot(x_axis,self.VolMortoTempo.reshape(nanos*12),'g-.',lw=2, label = legenda )

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

        IC = 1.96/sqrt(nanos-1)

        cores = []
        limitesup = []
        limiteinf = []
        for elemento in self.FACP[mes][1:ordmax+1]:
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

        ax1.bar(np.arange(1,ordmax+1), self.FAC[mes][1:ordmax+1], barWidth, align='center')
        ax2.bar(np.arange(1,ordmax+1), self.FACP[mes][1:ordmax+1], barWidth, align='center', color = cores)
        ax2.plot(np.arange(1,ordmax+1), limitesup, 'm--', lw=1)
        ax2.plot(np.arange(1,ordmax+1), limiteinf, 'm--', lw=1)

        ax1.set_xticks(np.arange(1,ordmax+1))
        ax2.set_xticks(np.arange(1,ordmax+1))
        tituloFAC =  'FAC - Month: ' + str_mes + '\n of UHE ' + self.Nome
        tituloFACP = 'FACP - Month ' + str_mes +  '\n of UHE ' + self.Nome
        ax1.set_title(tituloFAC,  fontsize = 13)
        ax2.set_title(tituloFACP, fontsize =13)
        #ax1.xlabel('Lag')
        #ax2.xlabel('Lag')
        #ax1.ylabel('Autocorrelacao e Autocorrelacao Parcial')

        plt.show()


    ##########################################################################################################
    # Calcula Parametros das Usinas
    ##########################################################################################################

    def CalcVolUtil(self):     # Calcula Volume Util da Usina
        if self.TipoReg == b'M':
            self.VolUtil = self.VolMax - self.VolMin
        else:
            self.VolUtil = float(0)
            self.VolMin = self.VolMax

    def CalcPotEfetiva(self):     # Calcula Potencia Efetiva da Usina
        a = np.array(self.MaqporConj)
        b = np.array(self.PEfporConj)
        self.PotEfet = np.vdot(a, b)

    def CalcVazEfetiva(self):      # Calcula Vazao Efetiva da Usina
        a = np.array(self.MaqporConj)
        b = np.array(self.VazEfetConj)
        self.VazEfet = np.vdot(a, b)

    def CalcEngolMaximo(self):    # Estima Engolimento Maximo da Usina

        def CalcEngol(self, ql):
            engol = 0.
            for i in range(5):   # Varre Conjuntos de Maquinas
                if self.MaqporConj[i] > 0:
                    if ql < self.AltEfetConj[i]:
                        if self.TipoTurb == 1 or self.TipoTurb == 3:
                            alpha = 0.5
                        else:
                            alpha = 0.2
                    else:
                        alpha = -1
                    if self.AltEfetConj[i] != 0:
                        engol = engol + self.MaqporConj[i]*self.VazEfetConj[i]*((ql/self.AltEfetConj[i])**alpha)
            return engol

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        # Calcula Engolimento a 65% do Volume Util
        volume = self.VolMin + 0.65*self.VolUtil
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda65 = cota - self.CFMed
        engol65 = CalcEngol(self, queda65)

        # Calcula Engolimento a 50% do Volume Util
        volume = self.VolMin + 0.50*self.VolUtil
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda50 = cota - self.CFMed
        engol50 = CalcEngol(self, queda50)

        # Calcula Engolimento Associada ao Volume Maximo
        volume = self.VolMax
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMax = cota - self.CFMed
        engolMax = CalcEngol(self, quedaMax)

        # Calcula Engolimento Associada ao Volume Minimo
        volume = self.VolMin
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMin = cota - self.CFMed
        engolMin = CalcEngol(self, quedaMin)

        # Calcula Engolimento Associado a Altura Equivalente
        if ( self.VolUtil > 0):
            cota = 0
            for i in range(5):
                cota = cota + self.PolCotaVol[i] * (self.VolMax**(i+1)) / (i+1)
                cota = cota - self.PolCotaVol[i] * (self.VolMin**(i+1)) / (i+1)
            cota = cota / self.VolUtil
        quedaEquiv = cota - self.CFMed
        engolEquiv = CalcEngol(self, quedaEquiv)

        self.Engolimento = (engol50+engol65+engolEquiv+engolMax+engolMin)/5

        return

    def CalcProdutibs(self, nanos):       # Calcula Produtibilidades Associadas aa diversos volumes

        self.Ro65       = np.zeros( (nanos,12), 'd' )
        self.Ro50       = np.zeros( (nanos,12), 'd' )
        self.RoEquiv    = np.zeros( (nanos,12), 'd' )
        self.RoEquiv65  = np.zeros( (nanos,12), 'd' )
        self.RoMin      = np.zeros( (nanos,12), 'd' )
        self.RoMax      = np.zeros( (nanos,12), 'd' )

        a = self.PolCotaVol[0]
        b = self.PolCotaVol[1]
        c = self.PolCotaVol[2]
        d = self.PolCotaVol[3]
        e = self.PolCotaVol[4]

        # Calcula Produtibilidade Associada a 65% do Volume Util
        volume = self.VolMin + 0.65*self.VolUtil
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.Ro65[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.Ro65[iano][imes] = self.ProdEsp * (cota - cfuga)*(1. - self.PerdaHid/100)

        # Calcula Produtibilidade Associada a 50% do Volume Util
        volume = self.VolMin + 0.50*self.VolUtil
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.Ro50[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.Ro50[iano][imes] = self.ProdEsp * (cota - cfuga)*(1. - self.PerdaHid/100)

        # Calcula Produtibilidade Associada ao Volume Maximo
        volume = self.VolMax
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoMax[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.RoMax[iano][imes] = self.ProdEsp * (cota - cfuga)*(1. - self.PerdaHid/100)

        # Calcula Produtibilidade Associada ao Volume Minimo
        volume = self.VolMin
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoMin[iano][imes] = self.ProdEsp * (cota - cfuga - self.PerdaHid)
                else:
                    self.RoMin[iano][imes] = self.ProdEsp * (cota - cfuga)*(1. - self.PerdaHid/100)

        # Calcula Produtibilidade Equivalente
        if ( self.VolUtil > 0):
            cota = 0
            cota65 = 0
            Vol65 = self.VolMin + 0.65*self.VolUtil
            for i in range(5):
                cota = cota + self.PolCotaVol[i] * (self.VolMax**(i+1)) / (i+1)
                cota = cota - self.PolCotaVol[i] * (self.VolMin**(i+1)) / (i+1)
                cota65 = cota65 + self.PolCotaVol[i] * (Vol65**(i+1)) / (i+1)
                cota65 = cota65 - self.PolCotaVol[i] * (self.VolMin**(i+1)) / (i+1)
            cota = cota / self.VolUtil
            cota65 = cota65 / (Vol65 - self.VolMin)
        else:
            cota65 = cota
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self.CFugaT[iano][imes]
                if self.TipoPerda == 2:
                    self.RoEquiv[iano][imes]   = self.ProdEsp * (cota   - cfuga - self.PerdaHid)
                    self.RoEquiv65[iano][imes] = self.ProdEsp * (cota65 - cfuga - self.PerdaHid)
                else:
                    self.RoEquiv[iano][imes]   = self.ProdEsp * (cota   - cfuga)*(1. - self.PerdaHid/100)
                    self.RoEquiv65[iano][imes] = self.ProdEsp * (cota65 - cfuga)*(1. - self.PerdaHid/100)
        return

    # Calcula Vazao Incremental
    def QInc(self, usinas, iano, imes):

        nanos_hist = len(self.Vazoes)

        def Montante(usinas, usina, iano, imes):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.StatusVolMorto[iano][imes] == 2:
                        yield iusi
                    else:
                        yield from Montante(usinas, iusi, iano, imes)

        if self.StatusVolMorto[iano][imes] != 2:
            print ('Erro: Tentativa de calculo de Incremental para usina (', self.Nome, ') fora de operacao no mes ', imes, ' e ano ', iano)
            return 0
        else:
            Incremental = self.Vazoes[0:nanos_hist,imes]
            for iusina in Montante(usinas, self, iano, imes):
                Incremental = Incremental - iusina.Vazoes[0:nanos_hist,imes]

        if np.min(Incremental) < 0:
            contador = 0
            for i in range(nanos_hist):
                if Incremental[i] < 0:
                    Incremental[i] = 0
                    contador = contador + 1
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
            print ('Erro: Tentativa de calculo de Incremental para usina (', self.Nome, ') fora de operacao no mes ', imesconf, ' e ano ', ianoconf)
            return 0
        else:
            Incremental = np.zeros( (nanos_hist,1) , 'd')
            Incremental = self.Vazoes[0:nanos_hist,imesconf]
            for iusina in Montante(usinas, self, ianoconf, imesconf):
                Incremental = Incremental - iusina.Vazoes[0:nanos_hist,imesconf]

        if np.min(Incremental) < 0:
            contador = 0
            for i in range(nanos_hist):
                if Incremental[i] < 0:
                    #Incremental[i] = 0
                    contador = contador + 1
            #print ('Vazao Incremental da Usina ', self.Nome, 'menor que zero no mes ', imesconf, ' e ano ', ianoconf, 'Quantidade:', contador )
            return Incremental
        else:
            return Incremental

    def ProdAcum(self, usinas):

        def Cascata(usinas,iano,imes):
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

        self.RoAcum_A_Ree = np.zeros( (nanos,12), 'd')
        self.RoAcum_B_Ree = np.zeros( (nanos,12), 'd')
        self.RoAcum_C_Ree = np.zeros( (nanos,12), 'd')

        self.RoAcum_A_Sist = np.zeros( (nanos,12), 'd')
        self.RoAcum_B_Sist = np.zeros( (nanos,12), 'd')
        self.RoAcum_C_Sist = np.zeros( (nanos,12), 'd')

        self.RoAcum    = np.zeros( (nanos,12), 'd')
        self.RoAcum65  = np.zeros( (nanos,12), 'd' )
        self.RoAcumMax = np.zeros( (nanos,12), 'd' )
        self.RoAcumMed = np.zeros( (nanos,12), 'd' )
        self.RoAcumMin = np.zeros( (nanos,12), 'd' )

        for iano in range(nanos):
            for imes in range(12):
                trocouRee = 0
                trocouSist = 0
                FioRee = True
                FioSist = True

                for iusina in Cascata(usinas, iano, imes):
                    produtib    = iusina.RoEquiv[iano][imes]
                    produtib65  = iusina.RoEquiv65[iano][imes]
                    produtibMax = iusina.RoMax[iano][imes]
                    produtibMed = iusina.Ro65[iano][imes]
                    produtibMin = iusina.RoMin[iano][imes]
                    if iusina.StatusMotoriz[iano][imes] == 2:
                        self.RoAcum[iano][imes]    = self.RoAcum[iano][imes]    + produtib
                        self.RoAcum65[iano][imes]  = self.RoAcum65[iano][imes]  + produtib65
                        self.RoAcumMax[iano][imes] = self.RoAcumMax[iano][imes] + produtibMax
                        self.RoAcumMed[iano][imes] = self.RoAcumMed[iano][imes] + produtibMed
                        self.RoAcumMin[iano][imes] = self.RoAcumMin[iano][imes] + produtibMin
                    if iusina.Sist != self.Sist:
                        trocouSist = trocouSist+ 1
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
    #
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

        media = np.mean(self.Vazoes[1:nanos], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(self.Vazoes[1:nanos], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)

        # Calcula vazao normalizada (nao precisa)
        #vaznorm = np.zeros((nanos,12),'d')
        #for iano in range(nanos):
        #    for imes in range(12):
        #        vaznorm[iano][imes] = (self.Vazoes[iano][imes] - media[imes])/desvio[imes]

        # Calcula funcao de auto-correlacao (uma para cada mes)
        self.FAC = np.zeros( (12, ord_max+1), 'd')
        for ilag in range(ord_max+1):
            for imes in range(12):
                for iano in np.arange(1,nanos):
                     ano_ant = iano
                     mes_ant = imes - ilag
                     if mes_ant < 0:
                         ano_ant -= 1
                         mes_ant += 12
                     self.FAC[imes][ilag] += (self.Vazoes[iano][imes] - media[imes])* (self.Vazoes[ano_ant][mes_ant] - media[mes_ant])
                self.FAC[imes][ilag] /= (nanos-1)
                self.FAC[imes][ilag] /= (desvio[imes]*desvio[mes_ant])

        # Calcula funcao de auto-correlacao parcial (uma para cada mes)
        self.FACP = np.zeros((12, ord_max+1), 'd')
        for ilag in np.arange(1,ord_max+1):
            for imes in range(12):
                A = np.eye(ilag)
                B = np.zeros(ilag)
                # Preenche matriz triangular superior
                for ilin in range(len(A)):
                    for icol in range( len(A) ):           # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                        if icol > ilin:
                            mes = imes - ilin - 1
                            if mes < 0:
                               mes = mes + 12
                            A[ilin][icol] = self.FAC[mes][icol-ilin]
                    B[ilin] = self.FAC[imes][ilin+1]
                # Preenche matriz triangular inferior
                for ilin in range(len(A)):
                    for icol in range( len(A) ):          # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                        if icol < ilin:
                            A[ilin][icol] = A[icol][ilin]
                phi = np.linalg.solve(A,B)
                self.FACP[imes][ilag] = phi[ len(phi)-1 ]

        # Identificacao da ordem
        IC = 1.96/sqrt(nanos-1)
        self.Ordem = np.zeros(12, 'i')
        for imes in range(12):
            self.Ordem[imes] = 0
            for ilag in range(ord_max+1):
                if self.FACP[imes][ilag] > IC or self.FACP[imes][ilag] < -IC:
                    self.Ordem[imes] = ilag

        # Calculo dos coeficientes
        self.CoefParp = np.zeros( (12,ord_max), 'd')
        for imes in range(12):
            ilag = self.Ordem[imes]
            A = np.eye(ilag)
            B = np.zeros(ilag)
            # Preenche matriz triangular superior
            for ilin in range(len(A)):
                for icol in range( len(A) ):             # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                    if icol > ilin:
                        mes = imes - ilin - 1
                        if mes < 0:
                           mes = mes + 12
                        A[ilin][icol] = self.FAC[mes][icol-ilin]
                B[ilin] = self.FAC[imes][ilin+1]
            # Preenche matriz triangular inferior
            for ilin in range(len(A)):
                for icol in range( len(A) ):             # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                    if icol < ilin:
                        A[ilin][icol] = A[icol][ilin]
            phi = np.linalg.solve(A,B)
            for iord in range ( len(phi) ):
                self.CoefParp[imes][iord ] = phi[ iord ]

    def gera_series_aditivo(self):

        nanos = len(self.Vazoes) - 1
        ord_max = len(self.CoefParp[0])

        media = np.mean(self.Vazoes[1:nanos], 0)
        desvio = np.std(self.Vazoes[1:nanos], 0)

        # Calculo dos residuos
        residuos = np.zeros( (nanos, 12) )
        for iano in np.arange(1,nanos):
            for imes in range(12):
                residuos[iano][imes]= ( self.Vazoes[iano][imes]-media[imes] ) / desvio[imes]
                for ilag in range(ord_max):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    residuos[iano][imes] -= self.CoefParp[imes][ilag]*( self.Vazoes[ano_ant][mes_ant]-media[mes_ant] ) / desvio[mes_ant]

        # Gera series sinteticas
        sintetica_adit = np.zeros((1000,60),'d')
        for iser in range(1000):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(1,nanos-1)
                    valor = media[imes] + desvio[imes]*residuos[serie][imes]
                    for ilag in range(ord_max):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_adit[iser][contador-1-ilag]
                        valor += desvio[imes]*self.CoefParp[imes][ilag]*(vazant-media[mes_ant])/desvio[mes_ant]
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_adit.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_adit,0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit,0) + np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2, label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit,0) - np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2)
        m = np.concatenate([ media, media, media, media, media])
        d = np.concatenate([ desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Aditive Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflow (m^3/s', fontsize=16)
        plt.legend(fontsize=12)
        plt.show()


    def gera_series_multiplicativo(self):

        nanos = len(self.Vazoes) - 1
        ord_max = len(self.CoefParp[0])

        media = np.mean(self.Vazoes[1:nanos], 0)
        desvio = np.std(self.Vazoes[1:nanos], 0)

        # Calculo dos residuos
        residuosmult = np.zeros( (nanos, 12) )
        termoind = np.zeros(12, 'd')
        for iano in np.arange(1,nanos):
            for imes in range(12):
                residuosmult[iano][imes]= self.Vazoes[iano][imes]
                somatorio = 0
                termoind[imes] = media[imes]  # Versao centrada: ver pagina 20 dissertacao Filipe Goulart Cabral (COPPE 2016)
                                              # O ideal portanto, seria utilizar este metodo com formulacao de otimzicao ao
                                              # inves de yule-walker. Restringindo que o termo-ind e os phis sejam todos positivos
                for ilag in range(ord_max):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    somatorio += self.CoefParp[imes][ilag]*self.Vazoes[ano_ant][mes_ant]
                    termoind[imes] -= self.CoefParp[imes][ilag]*media[mes_ant]
                residuosmult[iano][imes] = residuosmult[iano][imes]/(termoind[imes]+somatorio)

        # Gera series sinteticas
        sintetica_mult = np.zeros((1000,60),'d')
        for iser in range(1000):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(1,nanos-1)
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
                            vazant = sintetica_mult[iser][contador-1-ilag]
                        valor += self.CoefParp[imes][ilag]*vazant
                    sintetica_mult[iser][contador] = valor*residuosmult[serie][imes]

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_mult.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_mult,0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult,0) + np.std(sintetica_mult, axis=0), 'r-.', lw=2, label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult,0) - np.std(sintetica_mult, axis=0), 'r-.', lw=2)
        m = np.concatenate([ media, media, media, media, media])
        d = np.concatenate([ desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Multiplicative Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflows (m3/s)', fontsize=16)
        #plt.ylim(-100, 30000)
        plt.legend(fontsize=12)
        plt.show()

        vasco = 1000

    def pso(self, ord_max):

        def objetivo(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros( ord_max+1, 'd')
            for icoef in range(ord_max+1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            residuos = np.zeros(nanos-1)

            for iano in np.arange(1,nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                residuos[iano-1]=(self.Vazoes[iano][imes] / somatorio)
                objetivo += ((self.Vazoes[iano][imes] / somatorio) ** 2)

            total = np.sum(residuos) - nanos + 1
            total = total ** 2
            total = 10000*total

            return ( objetivo/(nanos-1) + total )

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.CoefIndParp = np.zeros(12, 'd')
        self.Ordem = np.zeros(12,'d')
        for imes in range(12):
            print( '*******', imes+1)

            best = 999999
            best_ordem = 0
            for iord in np.arange(1,(ord_max+1)):
                # Define limites e condicao inicial
                lb = np.zeros(iord + 1)
                ub = np.zeros(iord + 1)
                for i in range(iord + 1):
                    lb[i] = 0.00001
                    ub[i] = 10000

                print('**', iord)
                solution, fopt = pso(objetivo, lb, ub, args=(iord, imes), maxiter = 500)

                #solution = minimize(objetivo, x0, method= 'SLSQP', bounds=limites, constraints=cons, args=( iord, imes), options={ 'disp': False, 'maxiter': 10000 }  )
                if fopt < best:
                    best = fopt
                    best_ordem = iord

            self.Ordem[imes] = best_ordem

            solution, fopt = pso(objetivo, lb, ub, args=(iord, imes), maxiter=5000)

            for icoef in range(ord_max):
                self.CoefParp[imes][icoef] = solution[icoef+1]
            self.CoefIndParp[imes] = solution[0]


    def parp_otimo(self, ord_max):


        # Funcao objetivo minimizar erro quatratico medio (o residuo eh o erro)
        def objetivo(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros( ord_max+1, 'd')
            for icoef in range(ord_max+1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            for iano in np.arange(1,nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                objetivo += ((self.Vazoes[iano][imes] / somatorio) ** 2)

            return objetivo/(nanos-1)

        # Restricoes a media dos residuos devem ser igual a unidade ou somatorio dos residuos devem ser igual a nanos
        def restricao(x, ord_max, imes):

            nanos = len(self.Vazoes) - 1  # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

            coef = np.zeros( ord_max+1, 'd')
            for icoef in range(ord_max+1):
                coef[icoef] = x[icoef]

            objetivo = 0.
            residuos = np.zeros(nanos-1)
            for iano in np.arange(1,nanos):
                somatorio = coef[0]
                for ilag in range(ord_max):
                    mes_ant = imes - 1 - ilag
                    ano_ant = iano
                    if mes_ant < 0:
                        mes_ant += 12
                        ano_ant -= 1
                    somatorio += coef[ilag + 1] * self.Vazoes[ano_ant][mes_ant]
                objetivo += (self.Vazoes[iano][imes] / somatorio)
                residuos[iano-1]=(self.Vazoes[iano][imes] / somatorio)
                desvio = np.std(residuos)
                #curtose = kurtosis(residuos) - 3
            # return ([ objetivo - nanos + 1 , desvio - 0.2])
            return ([ objetivo - nanos + 1 ])

        # Define limites e condicao inicial
        x0 = np.zeros(ord_max+1)
        limites = []
        for i in range(ord_max + 1):
            x0[i] = 0.1
            limites.append((0, 10000))

        self.CoefParp = np.zeros((12, ord_max), 'd')
        self.CoefIndParp = np.zeros(12, 'd')
        self.Ordem = np.zeros(12,'d')
        for imes in range(12):
            print( '*******', imes+1)
            conl = {'type': 'eq', 'fun': restricao, 'args': (ord_max, imes)}
            cons = ([conl])
            best = 999999
            best_ordem = 0
            #for iord in np.arange(1,(ord_max+1)):
            for iord in np.arange(6, 7):
                solution = minimize(objetivo, x0, method= 'SLSQP', bounds=limites, constraints=cons, args=( iord, imes), options={ 'disp': False, 'maxiter': 10000 }  )
                if solution.fun < best:
                    best = solution.fun
                    best_ordem = iord

            self.Ordem[imes] = best_ordem
            solution = minimize(objetivo, x0, method= 'SLSQP', bounds=limites, constraints=cons, args=( best_ordem, imes), options={ 'disp': True, 'maxiter': 10000 }  )


            for icoef in range(ord_max):
                self.CoefParp[imes][icoef] = solution.x[icoef+1]
            self.CoefIndParp[imes] = solution.x[0]


    def gera_series_multiplicativo_parp_otimo(self):

        nanos = len(self.Vazoes) - 1
        ord_max = len(self.CoefParp[0])

        media = np.mean(self.Vazoes[1:nanos], 0)
        desvio = np.std(self.Vazoes[1:nanos], 0)

        # Calculo dos residuos
        residuosmult = np.zeros( (nanos, 12) )
        for iano in np.arange(1,nanos):
            for imes in range(12):
                residuosmult[iano][imes]= self.Vazoes[iano][imes]
                somatorio = 0
                for ilag in range(ord_max):
                    ano_ant = iano
                    mes_ant = imes - ilag - 1
                    if mes_ant < 0:
                        ano_ant -= 1
                        mes_ant += 12
                    somatorio += self.CoefParp[imes][ilag]*self.Vazoes[ano_ant][mes_ant]
                residuosmult[iano][imes] = residuosmult[iano][imes]/(self.CoefIndParp[imes]+somatorio)

        # Gera series sinteticas
        sintetica_mult = np.zeros((1000,60),'d')
        for iser in range(1000):
            contador = -1
            for iano in range(5):
                for imes in range(12):
                    contador += 1
                    serie = randint(1,nanos-1)
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
                            vazant = sintetica_mult[iser][contador-1-ilag]
                        valor += self.CoefParp[imes][ilag]*vazant
                    sintetica_mult[iser][contador] = valor*residuosmult[serie][imes]

        x_axis = np.arange(1, 61)
        plt.plot(x_axis, sintetica_mult.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_mult,0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult,0) + np.std(sintetica_mult, axis=0), 'r-.', lw=2, label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_mult,0) - np.std(sintetica_mult, axis=0), 'r-.', lw=2)
        m = np.concatenate([ media, media, media, media, media])
        d = np.concatenate([ desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = self.Nome.strip() + "'s Synthetic Series of Natural \n" " Inflows - Multiplicative Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflows (m3/s)', fontsize=16)
        #plt.ylim(-100, 30000)
        plt.legend(fontsize=12)
        plt.show()