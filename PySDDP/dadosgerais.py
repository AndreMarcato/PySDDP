class dadosgerais(object):

    # Dados de cadastro das usinas termeletrica (presentes no TERM.DAT)
    NomedoCaso = None
    NAnosEstudo = None
    MesInicioEstudo = None
    MesInicioPreEstudo = None
    AnoInicioEstudo = None
    NAnosPreEstudo = None
    NAnosPosEstudo = None
    NAnosPosSimulacao = None
    NumMaxIter = None
    NumSimForward = None
    NumAberturas = None
    NumSeriesSinteticas = None
    OrdemMaxParP = None
    AnoInicHistorico = None

    def __init__(self, nanos):
        self.NAnosEstudo = nanos