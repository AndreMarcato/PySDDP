import numpy as np

class interc(object):

    # Classe contendo informacoes sobre os arquivos de entrada e saida
    De = None
    Para = None
    LimiteMaximo = None
    LimiteMinimo = None
    Flag = None     # Flag 0: Limite de intercambio; 1: Limite de intercambio minimo obrigatorio

    def __init__(self, nanos):
        self.LimiteMaximo = np.zeros((nanos,12), 'd')
        self.LimiteMinimo = np.zeros((nanos,12), 'd')
