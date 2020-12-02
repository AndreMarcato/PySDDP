import os
from pprint import pprint
from PySDDP.dessem.script.arquivos import Arquivos
#from script.dadvaz import DadVaz
#from script.deflant import DeflAnt
#from script.operut import Operut
#from script.rampas import Rampas
#from script.rstlpp import Rstlpp
#from script.eolica import Eolica
#from script.ilstri import Ilstri
#from script.areacont import Areacont
#from script.respotele import Respotele


class Dessem(object):

    path_ = "/Users/andremarcato/Dropbox/Projeto ReadDessem/DS_CCEE_082020_SEMREDE_RV0D01"
    file_ = "dessem.arq"
    arquivos = None

    def __init__(self, caminho, nome):
        self.path_ = caminho
        self.file_ = nome
        self.arquivos = Arquivos()
        self.arquivos.ler(os.path.join(self.path_, self.file_))
