import os
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
from PySDDP.dessem.script.dadger import Dadger
from PySDDP.dessem.script.dados_eletricos import DadosEletricos
from PySDDP.dessem.script.dessopc import Dessopc
from PySDDP.dessem.script.ilibs import ILibs
from PySDDP.dessem.script.vazao_lateral import VazaoLateral

class Dessem(object):

    path_ = "/Users/andremarcato/Dropbox/Projeto ReadDessem/DS_CCEE_082020_SEMREDE_RV0D01"
    file_ = "dessem.arq"
    arquivos = None

    def __init__(self, caminho, nome):

        nao_lidos = list()

        self.path_ = caminho
        self.file_ = nome
        self.arquivos = Arquivos()
        self.arquivos.ler(os.path.join(self.path_, self.file_))

        try:
            file_areacont = self.arquivos.areacont
            self.areacont = Areacont()
            self.areacont.ler(os.path.join(self.path_, file_areacont))
        except Exception as err:
            nao_lidos.append(['areacont', err])

        try:
            file_cadterm = self.arquivos.cadterm
            self.cadterm = CadTerm()
            self.cadterm.ler(os.path.join(self.path_, file_cadterm))
        except Exception as err:
            nao_lidos.append(['cadterm', err])

        try:
            file_hidr = self.arquivos.cadusih
            self.hidr = Hidr()
            self.hidr.ler(os.path.join(self.path_, file_hidr))
        except Exception as err:
            nao_lidos.append(['cadusih', err])

        try:
            file_dadvaz = self.arquivos.vazoes
            self.dadvaz = DadVaz()
            self.dadvaz.ler(os.path.join(self.path_, file_dadvaz))
        except Exception as err:
            nao_lidos.append(['vazoes', err])

        try:
            file_deflant = self.arquivos.deflant
            self.deflant = DeflAnt()
            self.deflant.ler(os.path.join(self.path_, file_deflant))
        except Exception as err:
            nao_lidos.append(['deflant', err])

        try:
            file_eolica = self.arquivos.eolica
            self.eolica = Eolica()
            self.eolica.ler(os.path.join(self.path_, file_eolica))
        except Exception as err:
            nao_lidos.append(['eolica', err])

        try:
            file_ilstri = self.arquivos.ilstri
            self.ilstri = Ilstri()
            self.ilstri.ler(os.path.join(self.path_, file_ilstri))
        except Exception as err:
            nao_lidos.append(['ilstri', err])

        try:
            file_infofcf = self.arquivos.infofcf
            self.infofcf = Infofcf()
            self.infofcf.ler(os.path.join(self.path_, file_infofcf))
        except Exception as err:
            nao_lidos.append(['infofcf', err])

        try:
            file_operuh = self.arquivos.operuh
            self.operuh = Operuh()
            self.operuh.ler(os.path.join(self.path_, file_operuh))
        except Exception as err:
            nao_lidos.append(['operuh', err])

        try:
            file_operut = self.arquivos.operut
            self.operut = Operut()
            self.operut.ler(os.path.join(self.path_, file_operut))
        except Exception as err:
            nao_lidos.append(['operut', err])

        try:
            file_ptoper = self.arquivos.ptoper
            self.ptoper = Ptoper()
            self.ptoper.ler(os.path.join(self.path_, file_ptoper))
        except Exception as err:
            nao_lidos.append(['ptoper', err])

        try:
            file_rampas = self.arquivos.rampas
            self.rampas = Rampas()
            self.rampas.ler(os.path.join(self.path_, file_rampas))
        except Exception as err:
            nao_lidos.append(['rampas', err])

        try:
            file_respot = self.arquivos.respot
            self.respot = Respot()
            self.respot.ler(os.path.join(self.path_, file_respot))
        except Exception as err:
            nao_lidos.append(['respot', err])

        try:
            file_respotele = self.arquivos.respotele
            self.respotele = Respotele()
            self.respotele.ler(os.path.join(self.path_, file_respotele))
        except Exception as err:
            nao_lidos.append(['respotele', err])

        try:
            file_restseg = self.arquivos.restseg
            self.restseg = Restseg()
            self.restseg.ler(os.path.join(self.path_, file_restseg))
        except Exception as err:
            nao_lidos.append(['restseg', err])

        try:
            file_dadger = self.arquivos.dadger
            self.dadger = Dadger()
            self.dadger.ler(os.path.join(self.path_, file_dadger))
        except Exception as err:
            nao_lidos.append(['dadger', err])

        try:
            file_rstlpp = self.arquivos.rstlpp
            self.rstlpp = Rstlpp()
            self.rstlpp.ler(os.path.join(self.path_, file_rstlpp))
        except Exception as err:
            nao_lidos.append(['rstlpp', err])

        try:
            file_cotasr11 = self.arquivos.cotasr11
            self.cotasr11 = Cotasr11()
            self.cotasr11.ler(os.path.join(self.path_, file_cotasr11))
        except Exception as err:
            nao_lidos.append(['cotasr11', err])

        try:
            file_curvatviag = self.arquivos.curvtviag
            self.curvatviag = Curvtviag()
            self.curvatviag.ler(os.path.join(self.path_, file_curvatviag))
        except Exception as err:
            nao_lidos.append(['curvtviag', err])

        try:
            file_dessopc = self.arquivos.dessopc
            self.dessopc = Dessopc()
            self.dessopc.ler(os.path.join(self.path_, file_dessopc))
        except Exception as err:
            nao_lidos.append(['dessopc', err])

        try:
            file_ilibs = self.arquivos.ilibs
            self.ilibs = ILibs()
            self.ilibs.ler(os.path.join(self.path_, file_ilibs))

        except Exception as err:
            nao_lidos.append(['ilibs', err])

            # Leitura dos arquivos das funcionalidades libs:
        for idx, value in self.ilibs.bloco_indice["df"].iterrows():

            # Leitura do arquivo vazaolateral.csv:
            if value["identificador"] == "HIDRELETRICA-CADASTRO-RESERVATORIO":

                try:
                    file_vazao_lateral = value["arquivo"]
                    self.vazao_lateral = VazaoLateral()
                    self.vazao_lateral.ler(os.path.join(self.path_, file_vazao_lateral))
                except Exception as err:
                    nao_lidos.append(['vazao_lateral', err])

            else:
                pass

        try:
            file_bateria = self.arquivos.bateria
            self.bateria = Bateria()
            self.bateria.ler(os.path.join(self.path_, file_bateria))
        except Exception as err:
            nao_lidos.append(['bateria', err])

        try:
            file_rmpflx = self.arquivos.rmpflx
            self.rmpflx = Rmpflx()
            self.rmpflx.ler(os.path.join(self.path_, file_rmpflx))
        except Exception as err:
            nao_lidos.append(['rmpflx', err])

        try:
            file_simul = self.arquivos.simul
            self.simul = Simul()
            self.simul.ler(os.path.join(self.path_, file_simul))
        except Exception as err:
            nao_lidos.append(['simul', err])

        try:
            file_tolperd = self.arquivos.tolperd
            self.tolperd = Tolperd()
            self.tolperd.ler(os.path.join(self.path_, file_tolperd))
        except Exception as err:
            nao_lidos.append(['tolperd', err])

        try:
            file_solar = self.arquivos.solar
            self.solar = Solar()
            self.solar.ler(os.path.join(self.path_, file_solar))
        except Exception as err:
            nao_lidos.append(['solar', err])


        try:
            file_desselet = self.arquivos.indelet
            self.indelet = Indelet()
            self.indelet.ler(os.path.join(self.path_, file_desselet))

            # Dicionários para armazenar os arquivos:
            self.arquivos_de_casos_bases = dict()
            self.arquivos_de_modificacao_casos_bases = dict()

            #
            # LEITURA DOS ARQUIVOS DE CASOS BASES
            #

            # Foi utilizado o nome do arquivo e não o padrão (leve, média e pesada), pois foi verificado que em alguns
            # decks estes nomes estavam distintos.
            for idx, value in self.indelet.bloco_base['df'].iterrows():
                chave = value['nome'].replace(' ', '')
                self.arquivos_de_casos_bases[f"{chave}"] = DadosEletricos()
                file_caso_base = value['local'].replace(' ', '')
                try:
                    self.arquivos_de_casos_bases[f"{chave}"].ler(os.path.join(self.path_, file_caso_base))
                except Exception as err:
                    nao_lidos.append([file_caso_base, err])

            #
            # LEITURA DOS ARQUIVOS DE MODIFICAÇÕES DOS CASOS BASES
            #
            for idx, value in self.indelet.bloco_periodo['df'].iterrows():
                chave = value['nome'].replace(' ', '')
                self.arquivos_de_modificacao_casos_bases[f"{chave}"] = DadosEletricos(caso_base=False)
                file_modif_caso_base = value['local'].replace(' ', '')
                try:
                    self.arquivos_de_modificacao_casos_bases[f"{chave}"].ler(os.path.join(self.path_,
                                                                                          file_modif_caso_base))
                except Exception as err:
                    nao_lidos.append([file_modif_caso_base, err])

        except Exception as err:
            nao_lidos.append(['indelet', err])


        if len(nao_lidos) > 0:
            print("Lista de Arquivos Não Lidos:")
            print("----- -- -------- --- ------")
            for arquivo in nao_lidos:
                print("ATENÇÃO! A leitura do arquivo", arquivo[0], "não foi realizada.")
