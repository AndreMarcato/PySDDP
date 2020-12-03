import os
from pprint import pprint
from PySDDP.dessem.script.arquivos import Arquivos
from PySDDP.dessem.script.areacont import Areacont
from PySDDP.dessem.script.bateria import Bateria
from PySDDP.dessem.script.cadterm import CadTerm
from PySDDP.dessem.script.hidr import Hidr
from PySDDP.dessem.script.cotasr11 import Cotasr11
from PySDDP.dessem.script.curvtviag import Curvtviag
from PySDDP.dessem.script.dadvaz import DadVaz
from PySDDP.dessem.script.deflant import DeflAnt
from PySDDP.dessem.script.eolica import Eolica
from PySDDP.dessem.script.ilstri import Ilstri
from PySDDP.dessem.script.indelet import Indelet
from PySDDP.dessem.script.infofcf import Infofcf
from PySDDP.dessem.script.operuh import Operuh
from PySDDP.dessem.script.operut import Operut
from PySDDP.dessem.script.ptoper import Ptoper
from PySDDP.dessem.script.rampas import Rampas
from PySDDP.dessem.script.respot import Respot
from PySDDP.dessem.script.respotele import Respotele
from PySDDP.dessem.script.restseg import Restseg
from PySDDP.dessem.script.rmpflx import Rmpflx
from PySDDP.dessem.script.rstlpp import Rstlpp   # Não está lendo o nome deste arquivo
from PySDDP.dessem.script.simul import Simul
from PySDDP.dessem.script.solar import Solar     # Não está lendo o nome deste arquivo
from PySDDP.dessem.script.tolperd import Tolperd


class Dessem(object):

    path_ = "/Users/andremarcato/Dropbox/Projeto ReadDessem/DS_CCEE_082020_SEMREDE_RV0D01"
    file_ = "dessem.arq"
    arquivos = None

    def __init__(self, caminho, nome):
        self.path_ = caminho
        self.file_ = nome
        self.arquivos = Arquivos()
        self.arquivos.ler(os.path.join(self.path_, self.file_))

        #file_areacont = self.arquivos.areacont
        #self.areacont = Areacont()
        #self.areacont.ler(os.path.join(self.path_, file_areacont))

        #file_bateria = self.arquivos.bateria
        #self.bateria = Bateria()
        #self.bateria.ler(os.path.join(self.path_, file_bateria))

        file_cadterm = self.arquivos.cadterm
        self.cadterm = CadTerm()
        self.cadterm.ler(os.path.join(self.path_, file_cadterm))

        file_hidr = self.arquivos.cadusih
        self.hidr = Hidr()
        self.hidr.ler(os.path.join(self.path_, file_hidr))

        #file_cotasr11 = self.arquivos.cotasr11
        #self.cotasr11 = Cotasr11()
        #self.cotasr11.ler(os.path.join(self.path_, file_cotasr11))

        #file_curvatviag = self.arquivos.curvtviag
        #self.curvatviag = Curvtviag()
        #self.curvatviag.ler(os.path.join(self.path_, file_curvatviag))

        file_dadvaz = self.arquivos.vazoes
        self.dadvaz = DadVaz()
        self.dadvaz.ler(os.path.join(self.path_, file_dadvaz))

        file_deflant = self.arquivos.deflant
        self.deflant = DeflAnt()
        self.deflant.ler(os.path.join(self.path_, file_deflant))

        file_eolica = self.arquivos.eolica
        self.eolica = Eolica()
        self.eolica.ler(os.path.join(self.path_, file_eolica))

        file_ilstri = self.arquivos.ilstri
        self.ilstri = Ilstri()
        self.ilstri.ler(os.path.join(self.path_, file_ilstri))

        file_indelet = self.arquivos.indelet
        self.indelet = Indelet()
        self.indelet.ler(os.path.join(self.path_, file_indelet))

        file_infofcf = self.arquivos.infofcf
        self.infofcf = Infofcf()
        self.infofcf.ler(os.path.join(self.path_, file_infofcf))

        file_operuh = self.arquivos.operuh
        self.operuh = Operuh()
        self.operuh.ler(os.path.join(self.path_, file_operuh))

        file_operut = self.arquivos.operut
        self.operut = Operut()
        self.operut.ler(os.path.join(self.path_, file_operut))

        file_ptoper = self.arquivos.ptoper
        self.ptoper = Ptoper()
        self.ptoper.ler(os.path.join(self.path_, file_ptoper))

        file_rampas = self.arquivos.rampas
        self.rampas = Rampas()
        self.rampas.ler(os.path.join(self.path_, file_rampas))

        file_respot = self.arquivos.respot
        self.respot = Respot()
        self.respot.ler(os.path.join(self.path_, file_respot))

        file_respotele = self.arquivos.respotele
        self.respotele = Respotele()
        self.respotele.ler(os.path.join(self.path_, file_respotele))

        file_restseg = self.arquivos.restseg
        self.restseg = Restseg()
        self.restseg.ler(os.path.join(self.path_, file_restseg))

        #file_rmpflx = self.arquivos.rmpflx
        #self.rmpflx = Rmpflx()
        #self.rmpflx.ler(os.path.join(self.path_, file_rmpflx))

        #file_simul = self.arquivos.simul
        #self.simul = Simul()
        #self.simul.ler(os.path.join(self.path_, file_simul))

        #file_tolperd = self.arquivos.tolperd
        #self.tolperd = Tolperd()
        #self.tolperd.ler(os.path.join(self.path_, file_tolperd))









