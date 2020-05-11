import re


class dadosgerais(object):
    NAnosEstudo = None
    MesInicioEstudo = None
    AnoInicioEstudo = None
    # MesInicioPreEstudo = None
    # NAnosPreEstudo = None
    # NAnosPosEstudo = None
    # NAnosPosSimulacao = None
    NumMaxIter = None
    NumMinInter = None
    NumSimForward = None
    NumAberturas = None
    NumSeriesSinteticas = None
    OrdemMaxParP = None
    AnoInicioHistorico = None
    TaxaDesconto = None
    DeltaZSUP = None
    DeltaZINF = None

    def __init__(self, diretorio):
        # Le parâmetros de configuração do deck de entrada do NEWAVE
        file_name = diretorio + 'DGER.DAT'
        file = open(file_name, "r")
        arquivo = file.readlines()
        file.close()
        self.NAnosEstudo = int(re.findall("\d+[.]\d+|\d+", arquivo[3])[0])
        self.MesInicioEstudo = int(re.findall("\d+[.]\d+|\d+", arquivo[5])[0])
        self.AnoInicioEstudo = int(re.findall("\d+[.]\d+|\d+", arquivo[6])[0])
        self.NumMaxIter = int(re.findall("\d+[.]\d+|\d+", arquivo[15])[0])
        self.NumSimForward = int(re.findall("\d+[.]\d+|\d+", arquivo[16])[0])
        self.NumAberturas = int(re.findall("\d+[.]\d+|\d+", arquivo[17])[0])
        self.NumSeriesSinteticas = int(re.findall("\d+[.]\d+|\d+", arquivo[18])[0])
        self.OrdemMaxParP = int(re.findall("\d+[.]\d+|\d+", arquivo[19])[0])
        self.AnoInicioHistorico = int(re.findall("\d+[.]\d+|\d+", arquivo[20])[0])
        self.TaxaDesconto = float(re.findall("\d+[.]\d+|\d+", arquivo[25])[0]) / 100
        self.NumMinInter = int(re.findall("\d+[.]\d+|\d+", arquivo[30])[0])
        self.DeltaZSUP = float(re.findall("\d+[.]\d+|\d+", arquivo[51])[0]) / 100
        self.DeltaZINF = float(re.findall("\d+[.]\d+|\d+", arquivo[52])[0]) / 100
