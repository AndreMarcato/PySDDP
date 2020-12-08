from PySDDP.dessem.script.templates.bateria import BateriaTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'


class Bateria(BateriaTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Bateria do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()
        self.cad = dict()
        self.cad['mneumo'] = list()
        self.cad['num'] = list()
        self.cad['nome'] = list()
        self.cad['capac'] = list()
        self.cad['carreg'] = list()
        self.cad['descarreg'] = list()
        self.cad['eficiencia'] = list()
        self.cad['barra'] = list()
        self.cad['subm'] = list()

        self.inic = dict()
        self.inic['mneumo'] = list()
        self.inic['num'] = list()
        self.inic['carreg'] = list()

        self.comentarios = list()

    def ler(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:
                    self.next_line(f)
                    linha = self.linha.strip()

                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        continue

                    if linha[0:17] == 'ARMAZENAMENTO-CAD':
                        self.cad['mneumo'].append(linha[0:17])
                        self.cad['num'].append(linha[18:22])
                        self.cad['nome'].append(linha[23:35])
                        self.cad['capac'].append(linha[36:46])
                        self.cad['carreg'].append(linha[47:57])
                        self.cad['descarreg'].append(linha[58:68])
                        self.cad['eficiencia'].append(linha[69:79])
                        self.cad['barra'].append(linha[80:85])
                        self.cad['subm'].append(linha[86:89])
                        continue

                    if linha[0:18] == 'ARMAZENAMENTO-INIC':
                        self.inic['mneumo'].append(linha[0:18])
                        self.inic['num'].append(linha[19:23])
                        self.inic['carreg'].append(linha[24:34])
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_inic['df'] = pd.DataFrame(self.inic)
                self.bloco_cad['df'] = pd.DataFrame(self.cad)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for idx, value in self.bloco_cad['df'].iterrows():
                    linha = self.bloco_cad['formato'].format(**value)
                    f.write(linha)

                for idx, value in self.bloco_inic['df'].iterrows():
                    linha = self.bloco_inic['formato'].format(**value)
                    f.write(linha)

        except Exception:
            raise
