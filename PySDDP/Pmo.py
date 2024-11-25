import os
from PySDDP.decomp.script.caso import Caso
from PySDDP.decomp.script.indice import Indice
from PySDDP.decomp.script.hidr import Hidr
from PySDDP.decomp.script.perdas import Perdas
from PySDDP.decomp.script.dadgnl import DadGnl
from PySDDP.decomp.script.polinjus import PolinJus
from PySDDP.decomp.script.vazoes import Vazoes

class Decomp(object):

    def __init__(self, caminho):

        nao_lidos = list()

        self.path = caminho

        # Define revisao default:
        self.rev = "rv0"

        try:
            file_caso = 'caso.dat'
            self.caso = Caso()
            self.caso.ler(os.path.join(self.path, file_caso))
            self.rev = self.caso.bloco_caso["df"]["nome_arq_ind"][0].strip()
            print("OK! Leitura do caso.dat realizada com sucesso.")
        except Exception as err:
            nao_lidos.append(['caso', err])

        try:
            file_dadgnl = f"dadgnl.{self.rev}"
            self.dadgnl = DadGnl()
            self.dadgnl.ler(os.path.join(self.path, file_dadgnl))
            print(f"OK! Leitura do dadgnl.{self.rev} realizada com sucesso.")
        except Exception as err:
            nao_lidos.append(['dadgnl', err])

        try:
            file_hidr = "hidr.dat"
            self.hidr = Hidr()
            self.hidr.ler(os.path.join(self.path, file_hidr))
        except Exception as err:
            nao_lidos.append(['hidr', err])

        try:
            file_perdas = "perdas.dat"
            self.perdas = Perdas()
            self.perdas.ler(os.path.join(self.path, file_perdas))
            print("OK! Leitura do perdas.dat realizada com sucesso.")
        except Exception as err:
            nao_lidos.append(['perdas', err])

        try:
            file_polinjus = "polinjus.dat"
            self.polinjus = PolinJus()
            self.polinjus.ler(os.path.join(self.path, file_polinjus))
            print("OK! Leitura do polinjus.dat realizada com sucesso.")
        except Exception as err:
            nao_lidos.append(['polinjus', err])

        try:
            file_vazoes = f"vazoes.{self.rev}"
            self.vazoes = Vazoes(nreg=320)
            self.vazoes.ler(os.path.join(self.path, file_vazoes))
            print(f"OK! Leitura do vazoes.{self.rev} realizada com sucesso.")
        except Exception as err:
            nao_lidos.append(['vazoes', err])

        if len(nao_lidos) > 0:
            print("Lista de Arquivos Não Lidos:")
            print("----- -- -------- --- ------")
            for arquivo in nao_lidos:
                print("ATENÇÃO! A leitura do arquivo", arquivo[0], "não foi realizada.")