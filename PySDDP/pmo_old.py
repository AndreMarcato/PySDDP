# coding=utf-8

import struct
from PySDDP.hidr import hidr
from PySDDP.term import term
from PySDDP.resequiv import resequiv
from PySDDP.submercado import submercado as subsist
from PySDDP.interc import interc
import numpy as np
import PySDDP.mixins as mixins


class pmo(object):
    diretorio = None
    nome_arquivo = None
    nome_dger = None
    nome_sistema = None
    nome_confhd = None
    nome_modif = None
    nome_conft = None
    nome_term = None
    nome_clast = None
    nome_exph = None
    nome_expt = None
    nome_patamar = None
    nome_cortes = None
    nome_corteh = None
    nome_pmo = None
    nome_parp = None
    nome_forward = None
    nome_fowardh = None
    nome_shist = None
    nome_manutt = None
    nome_newdesp = None
    nome_vazpast = None
    nome_itaipu = None
    nome_bid = None
    nome_c_adic = None
    nome_loss = None
    nome_gtminpat = None
    nome_elnino = None
    nome_ensoaux = None
    nome_dsvagua = None
    nome_penalid = None
    nome_curva = None
    nome_agrint = None
    nome_adterm = None
    nome_ghmin = None
    nome_sar = None
    nome_cvar = None
    nome_ree = None
    nome_re = None
    nome_hidr = 'HIDR.DAT'
    nome_vazoes = 'VAZOES.DAT'

    def __init__(self, diretorio):
        self.diretorio = diretorio

    def le_caso(self):

        # Le nome de arquivo com lista de arquivos de entrada
        file = mixins.read_file(self.diretorio, 'CASO.DAT')
        arquivo = file.readlines()
        file.close()
        self.nome_arquivo = arquivo[0][0:len(arquivo[0]) - 1]

        # Le nomes de todos os arquivos de entrada e saida do modelo NEWAVE
        file = mixins.read_file(self.diretorio, self.nome_arquivo)
        arquivo = file.readlines()
        file.close()

        self.nome_dger = arquivo[0][30:len(arquivo[0]) - 1]
        self.nome_sistema = arquivo[1][30:len(arquivo[1]) - 1]
        self.nome_confhd = arquivo[2][30:len(arquivo[2]) - 1]
        self.nome_modif = arquivo[3][30:len(arquivo[3]) - 1]
        self.nome_conft = arquivo[4][30:len(arquivo[4]) - 1]
        self.nome_term = arquivo[5][30:len(arquivo[5]) - 1]
        self.nome_clast = arquivo[6][30:len(arquivo[6]) - 1]
        self.nome_exph = arquivo[7][30:len(arquivo[7]) - 1]
        self.nome_expt = arquivo[8][30:len(arquivo[8]) - 1]
        self.nome_patamar = arquivo[9][30:len(arquivo[9]) - 1]
        self.nome_cortes = arquivo[10][30:len(arquivo[10]) - 1]
        self.nome_corteh = arquivo[11][30:len(arquivo[11]) - 1]
        self.nome_pmo = arquivo[12][30:len(arquivo[12]) - 1]
        self.nome_parp = arquivo[13][30:len(arquivo[13]) - 1]
        self.nome_forward = arquivo[14][30:len(arquivo[14]) - 1]
        self.nome_fowardh = arquivo[15][30:len(arquivo[15]) - 1]
        self.nome_shist = arquivo[16][30:len(arquivo[16]) - 1]
        self.nome_manutt = arquivo[17][30:len(arquivo[17]) - 1]
        self.nome_newdesp = arquivo[18][30:len(arquivo[18]) - 1]
        self.nome_vazpast = arquivo[19][30:len(arquivo[19]) - 1]
        self.nome_itaipu = arquivo[20][30:len(arquivo[20]) - 1]
        self.nome_bid = arquivo[21][30:len(arquivo[21]) - 1]
        self.nome_c_adic = arquivo[22][30:len(arquivo[22]) - 1]
        self.nome_loss = arquivo[23][30:len(arquivo[23]) - 1]
        self.nome_gtminpat = arquivo[24][30:len(arquivo[24]) - 1]
        self.nome_elnino = arquivo[25][30:len(arquivo[25]) - 1]
        self.nome_ensoaux = arquivo[26][30:len(arquivo[26]) - 1]
        self.nome_dsvagua = arquivo[27][30:len(arquivo[27]) - 1]
        self.nome_penalid = arquivo[28][30:len(arquivo[28]) - 1]
        self.nome_curva = arquivo[29][30:len(arquivo[29]) - 1]
        self.nome_agrint = arquivo[30][30:len(arquivo[30]) - 1]
        self.nome_adterm = arquivo[31][30:len(arquivo[31]) - 1]
        self.nome_ghmin = arquivo[32][30:len(arquivo[32]) - 1]
        self.nome_sar = arquivo[33][30:len(arquivo[33]) - 1]
        self.nome_cvar = arquivo[35][30:len(arquivo[34]) - 1]
        self.nome_ree = arquivo[35][30:len(arquivo[35]) - 1]
        self.nome_re = arquivo[36][30:len(arquivo[36]) - 1]
        print('OK! Leitura do CASO.DAT e ARQUIVOS.DAT realizada com sucesso.')

    def le_hidr(self, cadastro):

        file = mixins.read_file(self.diretorio, self.nome_hidr, mode='rb')
        nreg = 320

        i = 0
        while i < nreg:
            cadastro.append(hidr())
            iusi = len(cadastro) - 1
            cadastro[iusi].Codigo = i + 1
            cadastro[iusi].Nome = struct.unpack('12s', file.read(12))[0]
            cadastro[iusi].Posto = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].Bdh = struct.unpack('8s', file.read(8))[0]
            cadastro[iusi].Sist = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].Empr = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].Jusante = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].Desvio = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].VolMin = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].VolMax = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].VolVert = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].VolMinDesv = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].CotaMin = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].CotaMax = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].PolCotaVol = list(struct.unpack('5f', bytearray(file.read(20))))
            cadastro[iusi].PolCotaArea = list(struct.unpack('5f', bytearray(file.read(20))))
            cadastro[iusi].CoefEvap = list(struct.unpack('12i', bytearray(file.read(48))))
            cadastro[iusi].NumConjMaq = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].MaqporConj = list(struct.unpack('5i', bytearray(file.read(20))))
            cadastro[iusi].PEfporConj = list(struct.unpack('5f', bytearray(file.read(20))))

            cadastro[iusi].CF_HBQT = []
            cadastro[iusi].CF_HBQG = []
            cadastro[iusi].CF_HBPT = []
            for j in range(5):
                cadastro[iusi].CF_HBQT.append(list(struct.unpack('5f', bytearray(file.read(20)))))
            for j in range(5):
                cadastro[iusi].CF_HBQG.append(list(struct.unpack('5f', bytearray(file.read(20)))))
            for j in range(5):
                cadastro[iusi].CF_HBPT.append(list(struct.unpack('5f', bytearray(file.read(20)))))

            cadastro[iusi].AltEfetConj = list(struct.unpack('5f', bytearray(file.read(20))))
            cadastro[iusi].VazEfetConj = list(struct.unpack('5i', bytearray(file.read(20))))
            cadastro[iusi].ProdEsp = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].PerdaHid = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].NumPolVNJ = struct.unpack('i', file.read(4))[0]

            cadastro[iusi].PolVazNivJus = []
            for j in range(5):
                cadastro[iusi].PolVazNivJus.append(list(struct.unpack('6f', bytearray(file.read(24)))))

            cadastro[iusi].CotaRefNivelJus = list(struct.unpack('6f', bytearray(file.read(24))))
            cadastro[iusi].CFMed = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].InfCanalFuga = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].FatorCargaMax = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].FatorCargaMin = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].VazMin = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].UnidBase = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].TipoTurb = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].RepresConj = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].TEIF = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].IP = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].TipoPerda = struct.unpack('i', file.read(4))[0]
            cadastro[iusi].Data = struct.unpack('8s', file.read(8))[0]
            cadastro[iusi].Observ = struct.unpack('43s', file.read(43))[0]
            cadastro[iusi].VolRef = struct.unpack('f', file.read(4))[0]
            cadastro[iusi].TipoReg = struct.unpack('c', file.read(1))[0]

            i = i + 1

        file.close()
        print('OK! Leitura do HIDR.DAT realizada com sucesso. (', nreg, 'Usinas Hidraulicas )')

        return cadastro

    def le_confh(self, conf, cadastro, nanos):

        file = mixins.read_file(self.diretorio, self.nome_confhd)
        arquivo = file.readlines()
        file.close()

        file_vazoes = mixins.read_file(self.diretorio, self.nome_vazoes, mode='rb')
        vazoes = np.fromfile(file_vazoes, dtype=np.int32)
        file_vazoes.close()
        # A principio o numero de anos seria ano corrente - 2, mas
        # o ons tem usado complementar o arquivo de vazoes com os
        # dados ate o mes anterior do ano corrente
        # Calcular o numero de anos dividindo o tamanho da variavel data / nreg / nmeses

        num_anos = int(vazoes.shape[0] / 320 / 12)
        vaz_nat = vazoes.reshape(num_anos * 12, 320)

        for i in range(2, len(arquivo)):
            if len(arquivo[i]) > 5:
                codigo = int(arquivo[i][1:5])
            else:
                break
            for iusi, usina in enumerate(cadastro):
                if usina.Codigo == codigo:
                    conf.append(usina)
                    indice = len(conf) - 1
                    conf[indice].Nome = arquivo[i][6:18]
                    conf[indice].Posto = int(arquivo[i][19:23])
                    conf[indice].Jusante = int(arquivo[i][25:29])
                    conf[indice].Ree = int(arquivo[i][30:34])
                    conf[indice].VolIni = float(arquivo[i][35:41])
                    conf[indice].Status = arquivo[i][44:46]
                    conf[indice].Modif = int(arquivo[i][49:53])
                    conf[indice].AnoI = int(arquivo[i][58:62])
                    conf[indice].AnoF = int(arquivo[i][67:71])

                    # Se a usina for 'NE' ou 'EE' nao deve possuir maquinas
                    if conf[indice].Status == 'NE' or conf[indice].Status == 'EE':
                        for iconj in range(5):
                            conf[indice].MaqporConj[iconj] = 0

                    # Parametros Temporais controlados pelo MODIF.DAT
                    conf[indice].VolMinT = conf[indice].VolMin * np.ones((nanos, 12), 'f')
                    conf[indice].VolMaxT = conf[indice].VolMax * np.ones((nanos, 12), 'f')
                    conf[indice].VolMinP = conf[indice].VolMin * np.ones((nanos, 12), 'f')
                    conf[indice].VazMinT = conf[indice].VazMin * np.ones((nanos, 12), 'f')
                    conf[indice].CFugaT = conf[indice].CFMed * np.ones((nanos, 12), 'f')

                    # Calcula Parametros
                    conf[indice].CalcVolUtil()
                    conf[indice].CalcVazEfetiva()
                    conf[indice].CalcPotEfetiva()
                    conf[indice].CalcProdutibs(nanos)
                    conf[indice].CalcEngolMaximo()

                    # Parametros Temporais calculados pelo EXPH.DAT
                    if conf[indice].Status == 'EX':
                        conf[indice].StatusVolMorto = 2 * np.ones((nanos, 12), 'i')
                        conf[indice].StatusMotoriz = 2 * np.ones((nanos, 12), 'i')
                        conf[indice].VolMortoTempo = np.zeros((nanos, 12), 'f')
                        conf[indice].EngolTempo = conf[indice].Engolimento * np.ones((nanos, 12), 'f')
                        conf[indice].PotenciaTempo = conf[indice].PotEfet * np.ones((nanos, 12), 'f')
                        conf[indice].UnidadesTempo = sum(conf[indice].MaqporConj) * np.ones((nanos, 12), 'f')
                    else:
                        conf[indice].StatusVolMorto = np.zeros((nanos, 12), 'i')
                        conf[indice].StatusMotoriz = np.zeros((nanos, 12), 'i')
                        conf[indice].VolMortoTempo = np.zeros((nanos, 12), 'f')
                        conf[indice].UnidadesTempo = np.zeros((nanos, 12), 'i')
                        if conf[indice].Status == 'EE':
                            conf[indice].EngolTempo = conf[indice].Engolimento * np.ones((nanos, 12), 'f')
                            conf[indice].PotenciaTempo = conf[indice].PotEfet * np.ones((nanos, 12), 'f')
                        else:
                            conf[indice].EngolTempo = np.zeros((nanos, 12), 'f')
                            conf[indice].PotenciaTempo = np.zeros((nanos, 12), 'f')

                    # Le Historico de Vazoes Naturais da Usina
                    posto = conf[indice].Posto - 1
                    vaz_nat_usina = np.zeros(num_anos * 12, int)
                    for i in range(num_anos * 12):
                        vaz_nat_usina[i] = vaz_nat[i][posto]
                    conf[indice].Vazoes = vaz_nat_usina
                    conf[indice].Vazoes.shape = (num_anos, 12)

                    break

        print('OK! Leitura do CONFHD e VAZOES realizada com sucesso. (', indice + 1, 'Usinas Hidraulicas )')
        return conf

    def le_term(self, cadastro):

        file = mixins.read_file(self.diretorio, self.nome_term)
        arquivo = file.readlines()
        file.close()

        for i in range(2, len(arquivo)):
            if len(arquivo[i]) > 134:
                cadastro.append(term())
                indice = len(cadastro) - 1
                cadastro[indice].Codigo = int(arquivo[i][1:4])
                cadastro[indice].Nome = arquivo[i][5:17]
                cadastro[indice].Potencia = float(arquivo[i][19:24])
                cadastro[indice].FCMax = float(arquivo[i][25:29])
                cadastro[indice].TEIF = float(arquivo[i][31:37])
                cadastro[indice].IP = float(arquivo[i][38:44])
                gtmin = np.zeros(13, float)
                for j in range(13):
                    gtmin[j] = float(arquivo[i][(45 + j * 7):(51 + j * 7)])
                cadastro[indice].GTMin = gtmin
            else:
                break

        print('OK! Leitura do TERM realizada com sucesso. (', indice + 1, 'Usinas Termicas )')
        return cadastro

    def le_conft(self, conf, cadastro):

        file = mixins.read_file(self.diretorio, self.nome_conft)
        arquivo = file.readlines()
        file.close()

        for i in range(2, len(arquivo)):
            if len(arquivo[i]) > 5:
                codigo = int(arquivo[i][2:5])
            else:
                break
            encontrei = False
            for iusi, usina in enumerate(cadastro):
                if usina.Codigo == codigo:
                    encontrei = True
                    conf.append(usina)
                    indice = len(conf) - 1
                    conf[indice].Nome = arquivo[i][6:18]
                    conf[indice].Sist = int(arquivo[i][21:25])
                    conf[indice].Status = arquivo[i][30:32]
                    conf[indice].Classe = int(arquivo[i][35:39])
                    break
            if not encontrei:
                print('Ops.... Usina', codigo, 'do CONFT nao encontrada no TERM')

        print('OK! Leitura do CONFT realizada com sucesso. (', indice + 1, 'Usinas Termicas )')

        return conf

    def le_clast(self, conf):

        file = mixins.read_file(self.diretorio, self.nome_clast)
        arquivo = file.readlines()
        file.close()

        contador = 0
        for i in range(2, len(arquivo)):
            if len(arquivo[i]) > 5:
                codigo = int(arquivo[i][1:5])
                if codigo == 9999:
                    break
            else:
                break
            for iusi, usina in enumerate(conf):
                if usina.Classe == codigo:
                    contador += 1
                    usina.NomeClasse = arquivo[i][6:18]
                    usina.TipoComb = arquivo[i][19:29]
                    custo = np.zeros(5, float)
                    for j in range(5):
                        custo[j] = float(arquivo[i][(30 + j * 8):(37 + j * 8)])
                    usina.Custo = custo
                    break

        print('OK! Leitura do CLAST realizada com sucesso. (', contador, 'Usinas Termicas )')

        return conf

    def le_modif(self, conf, anoinicial, nanos):
        file = mixins.read_file(self.diretorio, self.nome_modif)
        arquivo = file.readlines()
        file.close()

        i = 2
        nr_modificacoes = 0
        while i < len(arquivo) - 1:
            codigo = int(arquivo[i][6:13])
            encontrou = False
            for iusi, usina in enumerate(conf):
                if usina.Codigo == codigo:
                    nr_modificacoes += 1
                    encontrou = True
                    break
            i = i + 1
            if not encontrou:
                print('Usina com codigo', codigo, 'listada no modif nao encontrada.')
                while arquivo[i][1:6] != 'USINA' and i < len(arquivo) - 2:
                    i = i + 1
            while arquivo[i][1:6] != 'USINA' and encontrou:
                if arquivo[i][1:7] == 'VOLMIN' or arquivo[i][1:7] == 'volmin':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    if texto[1] == "'%'":
                        usina.VolMin = usina.VolMin + float(texto[0]) * usina.VolUtil / 100
                    else:
                        usina.VolMin = float(texto[0])
                    usina.CalcVolUtil()
                    usina.CalcProdutibs(nanos)
                    usina.CalcEngolMaximo()
                    usina.VolMinT = usina.VolMin * np.ones((nanos, 12), 'f')
                    usina.VolMinP = usina.VolMin * np.ones((nanos, 12), 'f')
                elif arquivo[i][1:7] == 'VOLMAX' or arquivo[i][1:7] == 'volmax':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    if texto[1] == "'%'":
                        usina.VolMax = usina.VolMin + float(texto[0]) * usina.VolUtil / 100
                    else:
                        usina.VolMax = float(texto[0])
                    usina.CalcVolUtil()
                    usina.CalcProdutibs(nanos)
                    usina.CalcEngolMaximo()
                    usina.VolMaxT = usina.VolMax * np.ones((nanos, 12), 'f')
                elif arquivo[i][1:7] == 'NUMCNJ' or arquivo[i][1:7] == 'numcnj':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.NumConjMaq = int(texto[0])
                    usina.CalcVazEfetiva()
                    usina.CalcPotEfetiva()
                    usina.CalcEngolMaximo()
                    usina.UnidadesTempo = sum(usina.MaqporConj) * np.ones((nanos, 12), 'f')
                    if usina.Status == 'EE' or usina.Status == 'EX':
                        usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                        usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    else:
                        usina.EngolTempo = np.zeros((nanos, 12), 'f')
                        usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:7] == 'NUMMAQ' or arquivo[i][1:7] == 'nummaq':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    numero = int(texto[1])
                    usina.MaqporConj[numero - 1] = int(texto[0])
                    usina.CalcVazEfetiva()
                    usina.CalcPotEfetiva()
                    usina.CalcEngolMaximo()
                    usina.UnidadesTempo = sum(usina.MaqporConj) * np.ones((nanos, 12), 'f')
                    if usina.Status == 'EE' or usina.Status == 'EX':
                        usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                        usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    else:
                        usina.EngolTempo = np.zeros((nanos, 12), 'f')
                        usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:7] == 'POTEFE' or arquivo[i][1:7] == 'potefe':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    numero = int(texto[1])
                    usina.PEfporConj[numero - 1] = float(texto[0])
                    usina.CalcPotEfetiva()
                    usina.CalcEngolMaximo()
                    if usina.Status == 'EE' or usina.Status == 'EX':
                        usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                        usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    else:
                        usina.EngolTempo = np.zeros((nanos, 12), 'f')
                        usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:8] == 'PRODESP' or arquivo[i][1:8] == 'prodesp':
                    j = 8
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.ProdEsp = float(texto[0])
                    usina.CalcProdutibs(nanos)
                    usina.CalcEngolMaximo()
                    if usina.Status == 'EE' or usina.Status == 'EX':
                        usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                        usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    else:
                        usina.EngolTempo = np.zeros((nanos, 12), 'f')
                        usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:5] == 'TEIF' or arquivo[i][1:5] == 'teif':
                    j = 5
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.TEIF = float(texto[0])
                elif arquivo[i][1:3] == 'IP' or arquivo[i][1:3] == 'ip':
                    j = 3
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.IP = float(texto[0])
                elif arquivo[i][1:9] == 'PERDHIDR' or arquivo[i][1:9] == 'perdhidr':
                    j = 9
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.PerdaHid = float(texto[0])
                elif arquivo[i][1:8] == 'VAZMIN ' or arquivo[i][1:8] == 'vazmin ':
                    j = 8
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.VazMin = float(texto[0])
                    usina.VazMinT = usina.VazMin * np.ones((nanos, 12), 'f')
                elif arquivo[i][1:9] == 'COEFEVAP' or arquivo[i][1:9] == 'coefevap':
                    j = 9
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    numero = int(texto[1])
                    usina.CoefEvap[numero] = int(texto[0])
                elif arquivo[i][1:8] == 'COTAREA' or arquivo[i][1:8] == 'cotarea':
                    j = 8
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    for i in range(5):
                        usina.PolCotaArea[i] = float(texto[i])
                elif arquivo[i][1:8] == 'VOLCOTA' or arquivo[i][1:8] == 'volcota':
                    j = 8
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    for i in range(5):
                        usina.PolCotaVol[i] = float(texto[i])
                    usina.CalcProdutibs(nanos)
                    usina.CalcEngolMaximo()
                    if usina.Status == 'EE' or usina.Status == 'EX':
                        usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                        usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    else:
                        usina.EngolTempo = np.zeros((nanos, 12), 'f')
                        usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:6] == 'CFUGA' or arquivo[i][1:6] == 'cfuga':
                    j = 6
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    valor = float(texto[2])
                    mesinicial = int(texto[0])
                    for iano in range(int(texto[1]) - anoinicial, nanos):
                        for imes in range(mesinicial - 1, 12):
                            usina.CFugaT[iano][imes] = valor
                        mesinicial = 0
                    usina.CalcProdutibs(nanos)
                    # usina.CFMed = float(texto[0])
                    #
                    # usina.CalcEngolMaximo()
                    # if usina.Status == 'EE' or usina.Status == 'EX':
                    #    usina.EngolTempo = usina.Engolimento * np.ones((nanos, 12), 'f')
                    #    usina.PotenciaTempo = usina.PotEfet * np.ones((nanos, 12), 'f')
                    # else:
                    #    usina.EngolTempo = np.zeros((nanos, 12), 'f')
                    #    usina.PotenciaTempo = np.zeros((nanos, 12), 'f')
                elif arquivo[i][1:6] == 'VMAXT' or arquivo[i][1:6] == 'vmaxt':
                    j = 6
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    valor = float(texto[2])
                    if (texto[3] == "'%'"):
                        valor = usina.VolMin + usina.VolUtil * float(texto[2]) / 100
                    mesinicial = int(texto[0])
                    for iano in range(int(texto[1]) - anoinicial, nanos):
                        for imes in range(mesinicial - 1, 12):
                            usina.VolMaxT[iano][imes] = valor
                        mesinicial = 0
                elif arquivo[i][1:6] == 'VMINT' or arquivo[i][1:6] == 'vmint':
                    j = 6
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    valor = float(texto[2])
                    if (texto[3] == "'%'"):
                        valor = usina.VolMin + usina.VolUtil * float(texto[2]) / 100
                    mesinicial = int(texto[0])
                    for iano in range(int(texto[1]) - anoinicial, nanos):
                        for imes in range(mesinicial - 1, 12):
                            usina.VolMinT[iano][imes] = valor
                        mesinicial = 0
                elif arquivo[i][1:7] == 'NUMBAS' or arquivo[i][1:7] == 'numbas':
                    j = 7
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    usina.UnidBase = int(texto[0])
                elif arquivo[i][1:6] == 'VMINP' or arquivo[i][1:6] == 'vminp':
                    j = 6
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    valor = float(texto[2])
                    if (texto[3] == "'%'"):
                        valor = usina.VolMin + usina.VolUtil * float(texto[2]) / 100
                    mesinicial = int(texto[0])
                    for iano in range(int(texto[1]) - anoinicial, nanos):
                        for imes in range(mesinicial - 1, 12):
                            usina.VolMinP[iano][imes] = valor
                        mesinicial = 0
                elif arquivo[i][1:8] == 'VAZMINT' or arquivo[i][1:8] == 'vazmint':
                    j = 8
                    texto = arquivo[i][j:len(arquivo[i]) - 1]
                    texto = texto.split(" ")
                    while '' in texto:
                        texto.remove('')
                    valor = float(texto[2])
                    mesinicial = int(texto[0])
                    for iano in range(int(texto[1]) - anoinicial, nanos):
                        for imes in range(mesinicial - 1, 12):
                            usina.VazMinT[iano][imes] = valor
                        mesinicial = 0
                else:
                    print('Oooopppppsssss: Erro Leitura MODIF.DAT -  Linha', i + 1)
                i = i + 1
                if i == len(arquivo):
                    break
        print('OK! Leitura do MODIF realizada com sucesso. (', nr_modificacoes, 'Usinas Hidraulicas Modificadas - ', i,
              'linhas lidas )')
        return conf

    def le_exph(self, conf, anoinicial, nanos):
        file = mixins.read_file(self.diretorio, self.nome_exph)
        arquivo = file.readlines()
        file.close()

        i = 3
        nr_expansoes = 0
        while i < len(arquivo) and len(arquivo[i]) > 3:
            codigo = int(arquivo[i][0:4])
            for iusi, usina in enumerate(conf):
                if usina.Codigo == codigo:
                    if arquivo[i][18:20] != '  ':
                        mes_vm = int(arquivo[i][18:20])
                    else:
                        mes_vm = 0
                    if arquivo[i][21:25] != '    ':
                        ano_vm = int(arquivo[i][21:25])
                    else:
                        ano_vm = 0
                    if arquivo[i][31:33] != '  ':
                        dur_vm = int(arquivo[i][31:33])
                    else:
                        dur_vm = 0
                    if arquivo[i][38:42] != '    ':
                        per_vm = float(arquivo[i][38:42])
                    else:
                        per_vm = 0.

                    if len(arquivo[i]) > 64:
                        mes_ent = int(arquivo[i][44:46])
                        ano_ent = int(arquivo[i][47:51])
                        pot_ent = float(arquivo[i][52:58])
                        unidade = int(arquivo[i][60:62])
                        conjunto = int(arquivo[i][63:65])
                    else:
                        mes_ent = 0
                        ano_ent = 0
                        pot_ent = 0.
                        unidade = 0
                        conjunto = 0

                    nr_expansoes += 1

                    # Trata Volume Morto
                    if mes_vm > 0:
                        volume = usina.VolMin * per_vm / 100
                        volume = (usina.VolMin - volume) / dur_vm
                        mesinicial = mes_vm
                        for iano in range(ano_vm - anoinicial, nanos):
                            for imes in range(mesinicial - 1, 12):
                                if dur_vm > 0:
                                    usina.StatusVolMorto[iano][imes] = 1
                                    usina.VolMortoTempo[iano][imes] = volume
                                    dur_vm -= 1
                                else:
                                    usina.StatusVolMorto[iano][imes] = 2
                                    usina.VolMortoTempo[iano][imes] = 0.
                            mesinicial = 1
                    else:
                        usina.StatusVolMorto = 2 * np.ones((nanos, 12), 'i')

                    if mes_ent > 0:
                        mesinicial = mes_ent
                        usina.MaqporConj[conjunto - 1] = unidade
                        usina.PEfporConj[conjunto - 1] = pot_ent
                        usina.CalcPotEfetiva()
                        usina.CalcEngolMaximo()
                        for iano in range(ano_ent - anoinicial, nanos):
                            for imes in range(mesinicial - 1, 12):
                                usina.UnidadesTempo[iano][imes] += 1
                                usina.EngolTempo[iano][imes] = usina.Engolimento
                                usina.PotenciaTempo[iano][imes] = usina.PotEfet
                            mesinicial = 1

                    i += 1
                    while arquivo[i][0:4] != '9999':
                        mes_ent = int(arquivo[i][44:46])
                        ano_ent = int(arquivo[i][47:51])
                        pot_ent = float(arquivo[i][52:58])
                        unidade = int(arquivo[i][60:62])
                        conjunto = int(arquivo[i][63:65])
                        if mes_ent > 0:
                            mesinicial = mes_ent
                            usina.MaqporConj[conjunto - 1] = unidade
                            usina.PEfporConj[conjunto - 1] = pot_ent
                            usina.CalcPotEfetiva()
                            usina.CalcEngolMaximo()
                            for iano in range(ano_ent - anoinicial, nanos):
                                for imes in range(mesinicial - 1, 12):
                                    usina.UnidadesTempo[iano][imes] += 1
                                    usina.EngolTempo[iano][imes] = usina.Engolimento
                                    usina.PotenciaTempo[iano][imes] = usina.PotEfet
                                mesinicial = 1
                        i += 1

                    for iano in range(nanos):
                        for imes in range(12):
                            if usina.UnidadesTempo[iano][imes] >= usina.UnidBase:
                                usina.StatusMotoriz[iano][imes] = 2
                            elif usina.UnidadesTempo[iano][imes] > 0:
                                usina.StatusMotoriz[iano][imes] = 1
                            else:
                                if usina.StatusVolMorto[iano][imes] == 2:
                                    usina.StatusMotoriz[iano][imes] = 1
                                else:
                                    usina.StatusMotoriz[iano][imes] = 0
                    break
            i += 1

        print('OK! Leitura do EXPH realizada com sucesso. (', nr_expansoes, 'Usinas Hidraulicas Expandidas - ', i,
              'linhas lidas )')
        return (conf)

    def le_ree(self, ree):

        file = mixins.read_file(self.diretorio, self.nome_ree)
        arquivo = file.readlines()
        file.close()

        for i in range(3, len(arquivo)):
            if len(arquivo[i]) > 20:
                ree.append(resequiv())
                indice = len(ree) - 1
                ree[indice].Codigo = int(arquivo[i][1:4])
                ree[indice].Nome = arquivo[i][5:15]
                ree[indice].Submercado = int(arquivo[i][18:21])
            else:
                break

        print('OK! Leitura do REE realizada com sucesso. (', indice + 1, 'Reservatorios Equivalentes de Energia )')
        return ree

    def le_sistema(self, submercado, intercambio, nanos, npmc):

        file = mixins.read_file(self.diretorio, self.nome_sistema)
        arquivo = file.readlines()
        file.close()

        npmc = int(arquivo[3][1:4])

        i = 7

        while arquivo[i][1:4] != '999':
            submercado.append(subsist(nanos))
            isis = len(submercado) - 1
            submercado[isis].Codigo = int(arquivo[i][1:4])
            submercado[isis].Nome = arquivo[i][5:15]
            submercado[isis].Ficticio = int(arquivo[i][17:18])
            if not submercado[isis].Ficticio:
                for idef in range(4):
                    submercado[isis].CustoDeficit[idef] = float(arquivo[i][19 + 8 * idef:26 + 8 * idef])
                    submercado[isis].ProfundidadeDeficit[idef] = float(arquivo[i][51 + 6 * idef:56 + 6 * idef])
            i = i + 1

        i = i + 4

        while arquivo[i][1:4] != '999':
            intercambio.append(interc(nanos))
            iinter = len(intercambio) - 1
            intercambio[iinter].De = int(arquivo[i][1:4])
            intercambio[iinter].Para = int(arquivo[i][5:8])
            intercambio[iinter].Flag = int(arquivo[i][23:24])

            i = i + 1

            for iano in range(nanos):
                for imes in range(12):
                    valor = arquivo[i + iano][7 + 8 * imes:14 + 8 * imes]
                    valor = valor.strip()
                    if valor != '':
                        if intercambio[iinter].Flag == 0:
                            intercambio[iinter].LimiteMaximo[iano][imes] = float(valor)
                        else:
                            intercambio[iinter].LimiteMinimo[iano][imes] = float(valor)

            intercambio.append(interc(nanos))
            iinter = len(intercambio) - 1
            intercambio[iinter].De = intercambio[iinter - 1].Para
            intercambio[iinter].Para = intercambio[iinter - 1].De
            intercambio[iinter].Flag = intercambio[iinter - 1].Flag

            i = i + nanos + 1

            for iano in range(nanos):
                for imes in range(12):
                    valor = arquivo[i + iano][7 + 8 * imes:14 + 8 * imes]
                    valor = valor.strip()
                    if valor != '':
                        if intercambio[iinter].Flag == 0:
                            intercambio[iinter].LimiteMaximo[iano][imes] = float(valor)
                        else:
                            intercambio[iinter].LimiteMinimo[iano][imes] = float(valor)

            i = i + nanos

        i = i + 4
        while arquivo[i][1:4] != '999':
            codigo = int(arquivo[i][1:4])
            i = i + 1
            for isub in submercado:
                if isub.Codigo == codigo:
                    for iano in range(nanos + 1):
                        for imes in range(12):
                            valor = arquivo[i + iano][7 + 8 * imes:14 + 8 * imes]
                            valor = valor.strip()
                            if valor != '':
                                isub.Mercado[iano][imes] = float(valor)
                    break
            i = i + nanos + 1

        i = i + 4
        while arquivo[i][1:4] != '999':
            codigo = int(arquivo[i][1:4])
            i = i + 1
            for isub in submercado:
                if isub.Codigo == codigo:
                    for iano in range(nanos):
                        for imes in range(12):
                            valor = arquivo[i + iano][7 + 8 * imes:14 + 8 * imes]
                            valor = valor.strip()
                            if valor != '':
                                isub.NaoSimuladas[iano][imes] = float(valor)
                    break
            i = i + nanos

        print('OK! Leitura do arquivo SISTEMA realizada com sucesso.')
        return submercado, intercambio, npmc
