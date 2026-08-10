import os
from PySDDP.newave.script.caso import Caso
from PySDDP.newave.script.arquivos import Arquivos
from PySDDP.newave.script.hidr import Hidr
from PySDDP.newave.script.vazoes import Vazoes
from PySDDP.newave.script.confhd import Confhd
from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.modif import Modif
from PySDDP.newave.script.exph import Exph
from PySDDP.newave.script.conft import Conft
from PySDDP.newave.script.clast import Clast
from PySDDP.newave.script.ree import Ree
from PySDDP.newave.script.term import Term
from PySDDP.newave.script.sistema import Sistema
from PySDDP.newave.script.manutt import Manutt
from PySDDP.newave.script.expt import Expt


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
        self.vazoes.ler(os.path.join(self.path_, 'VAZOES.DAT'), self.hidr.nr_usinas)
        # Realiza a Leitura do MODIF.DAT
        self.modif = Modif()
        self.modif.ler(os.path.join(self.path_, self.arquivos.modif))
        # Realiza a Leitura do EXPH.DAT
        self.exph = Exph()
        self.exph.ler(os.path.join(self.path_, self.arquivos.exph))
        # Realiza a Leitura do CONFHD.DAT
        self.confhd = Confhd()
        self.confhd.ler(os.path.join(self.path_, self.arquivos.confhd), self.hidr, self.vazoes, self.dger,
                        self.modif, self.exph)
        # Realiza a Leitura do CONFT.DAT
        self.conft = Conft()
        self.conft.ler(os.path.join(self.path_, self.arquivos.conft))
        # Realiza a Leitura do CLAST.DAT
        self.clast = Clast()
        self.clast.ler(os.path.join(self.path_, self.arquivos.clast), self.dger)
        # Realiza a Leitura do REE.DAT
        self.ree = Ree()
        self.ree.ler(os.path.join(self.path_, self.arquivos.ree), self.confhd)
        # Realiza a Leitura do SISTEMA.DAT
        self.sistema = Sistema()
        self.sistema.ler(os.path.join(self.path_, self.arquivos.sistema), self.dger)
        self.term = Term()
        self.term.ler(os.path.join(self.path_, self.arquivos.term))
        # Realiza a Leitura do MANUTT.DAT
        self.manutt = Manutt()
        self.manutt.ler(os.path.join(self.path_, self.arquivos.manutt))
        # Realiza a Leitura do EXPT.DAT
        self.expt = Expt()
        self.expt.ler(os.path.join(self.path_, self.arquivos.expt))
    def escrever(self, caminho):
        self.caso.escrever(os.path.join(caminho, 'CASO.DAT'))
        self.arquivos.escrever(os.path.join(caminho, self.caso.nome_arquivos))
        self.dger.escrever(os.path.join(caminho, self.arquivos.dger))
        self.hidr.escrever(os.path.join(caminho, 'HIDR.DAT'))
        self.vazoes.escrever(os.path.join(caminho, 'VAZOES.DAT'))
        self.modif.escrever(os.path.join(caminho, self.arquivos.modif))
        self.exph.escrever(os.path.join(caminho, self.arquivos.exph))
        self.confhd.escrever(os.path.join(caminho, self.arquivos.confhd))
        self.conft.escrever(os.path.join(caminho, self.arquivos.conft))
        self.clast.escrever(os.path.join(caminho, self.arquivos.clast))
        self.ree.escrever(os.path.join(caminho, self.arquivos.ree))
        self.sistema.escrever((os.path.join(caminho, self.arquivos.sistema)),self.dger)
        self.manutt.escrever(os.path.join(caminho, self.arquivos.manutt))
        self.expt.escrever(os.path.join(caminho, self.arquivos.expt))
