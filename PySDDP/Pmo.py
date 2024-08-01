import os
from PySDDP.decomp.script.caso import Caso
from PySDDP.decomp.script.indice import Indice
from PySDDP.decomp.script.hidr import Hidr
from PySDDP.decomp.script.perdas import Perdas
from PySDDP.decomp.script.dadgnl import DadGnl
from PySDDP.decomp.script.polinjus import PolinJus

class Decomp(object):

    def __init__(self, caminho):

        nao_lidos = list()

        self._path = caminho
        self._file = "caso.dat"

        self.caso = Caso()
        self.caso.ler(os.path.join(self._path, self._file))

        try:
            file_indice = self.caso.bloco_caso["df"]["nome_arq"][0]
            self.indice = Indice()
            self.indice.ler(os.path.join(self._path, file_indice))
        except Exception as err:
            nao_lidos.append([self.caso.bloco_caso["df"]["nome_arq"][0], err])

        # Implementar dadger.rvx:
        nao_lidos.append(["dadger." + self.caso.bloco_caso["df"]["nome_arq"][0], None])

        # Implementar vazoes.rvx:
        nao_lidos.append(["vazoes." + self.caso.bloco_caso["df"]["nome_arq"][0], None])

        file_hidr = "hidr.dat"
        if file_hidr in self.indice.bloco_indice["df"]["arquivo"].tolist():
            try:
                self.hidr = Hidr()
                self.hidr.ler(os.path.join(self._path, file_hidr))
            except Exception as err:
                nao_lidos.append(["hidr.dat", err])
        else:
            nao_lidos.append([file_hidr, None])

        # Implementar mlt.dat:
        nao_lidos.append(["mlt.dat", None])

        file_perdas = "perdas.dat"
        if file_perdas in self.indice.bloco_indice["df"]["arquivo"].tolist():
            try:
                self.perdas = Perdas()
                self.perdas.ler(os.path.join(self._path, file_perdas))
            except Exception as err:
                nao_lidos.append([file_perdas, err])
        else:
            nao_lidos.append([file_perdas, None])

        file_dadgnl = "dadgnl." + self.caso.bloco_caso["df"]["nome_arq"][0]
        if file_dadgnl in self.indice.bloco_indice["df"]["arquivo"].tolist():
            try:
                self.dadgnl = DadGnl()
                self.dadgnl.ler(os.path.join(self._path, file_dadgnl))
            except Exception as err:
                nao_lidos.append([file_dadgnl, err])
        else:
            nao_lidos.append([file_dadgnl, None])

        file_polinjus = "polinjus.dat"
        if os.path.exists(self._path + "/" + file_polinjus):
            try:
                self.polinjus = PolinJus()
                self.polinjus.ler(os.path.join(self._path, file_polinjus))
            except Exception as err:
                nao_lidos.append([file_polinjus, err])
        else:
            nao_lidos.append([file_polinjus, None])

        if len(nao_lidos) > 0:
            print("Lista de arquivos nao lidos:")
            print("----- -- -------- --- ------")
            for arquivo in nao_lidos:
                print("ATENÇÃO! A leitura do arquivo", arquivo[0], "não foi realizada.")
