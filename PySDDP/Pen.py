import os
from PySDDP.newave.script.caso import Caso
from PySDDP.newave.script.arquivos import Arquivos
from PySDDP.newave.script.hidr import Hidr
from PySDDP.newave.script.vazoes import Vazoes
from PySDDP.newave.script.confhd import Confhd
from PySDDP.newave.script.dger import Dger


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
        # Realiza a Leitura do DGER.DAT
        self.dger = Dger()
        self.dger.ler(os.path.join(self.path_, self.arquivos.dger))
        # Realiza a Leitura do HIDR.DAT
        self.hidr = Hidr()
        self.hidr.ler(os.path.join(self.path_, 'HIDR.DAT'))
        # Realiza a Leitura do VAZOES.DAT
        self.vazoes = Vazoes()
        self.vazoes.ler(os.path.join(self.path_, 'VAZOES.DAT'), self.hidr.numero_postos)
        # Realiza a Leitura do CONFHD.DAT
        self.confhd = Confhd()
        self.confhd.ler(os.path.join(self.path_, self.arquivos.confhd), self.hidr, self.vazoes)

    def escrever(self, caminho):
        self.caso.escrever(os.path.join(caminho, 'CASO.DAT'))
        self.arquivos.escrever(os.path.join(caminho, self.caso.nome_arquivos))
        self.dger.escrever(os.path.join(caminho, self.arquivos.dger))
        self.hidr.escrever(os.path.join(caminho, 'HIDR.DAT'))
        self.vazoes.escrever(os.path.join(caminho, 'VAZOES.DAT'))
        self.confhd.escrever(os.path.join(caminho, self.arquivos.confhd))
