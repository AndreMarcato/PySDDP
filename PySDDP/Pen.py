import os
from PySDDP.newave.script.caso import Caso
from PySDDP.newave.script.arquivos import Arquivos
from PySDDP.newave.script.hidr import Hidr
from PySDDP.newave.script.vazoes import Vazoes


class Newave(object):

    path_ = "/Users/andremarcato/Dropbox/Projeto ReadDessem/Deck_Newave"
    file_ = "CASO.DAT"
    caso = None
    arquivos = None
    hidr = None

    def __init__(self, caminho):
        self.path_ = caminho
        # Realiza Leitura do CASO.DAT
        self.caso = Caso()
        self.caso.ler(os.path.join(self.path_, self.file_))
        # Realiza a Leitura dos Nomes dos Arquivos de Entrada
        self.arquivos = Arquivos()
        self.arquivos.ler(os.path.join(self.path_, self.caso.nome_arquivos))
        # Realiza a Leitura do HIDR.DAT
        self.hidr = Hidr()
        self.hidr.ler(os.path.join(self.path_, 'HIDR.DAT'))
        # Realiza a Leitura do VAZOES.DAT
        self.vazoes = Vazoes()
        self.vazoes.ler(os.path.join(self.path_, 'VAZOES.DAT'),self.hidr.numero_postos)
