from PySDDP.dessem.script.templates.indelet import IndeletTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '('
FIM_BLOCO = ['9999', '99999', 'FIM']


class Indelet(IndeletTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Desselet do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.base = dict()
        self.base['num'] = list()
        self.base['nome'] = list()
        self.base['local'] = list()

        self.periodo = dict()
        self.periodo['num'] = list()
        self.periodo['nome'] = list()
        self.periodo['ano'] = list()
        self.periodo['mes'] = list()
        self.periodo['dia'] = list()
        self.periodo['hora'] = list()
        self.periodo['minuto'] = list()
        self.periodo['duracao'] = list()
        self.periodo['num_caso'] = list()
        self.periodo['local'] = list()

        self.comentarios = list()

    def ler(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                caso_base = True
                continua = True

                while continua:
                    self.next_line(f)
                    linha = self.linha
                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        continue

                    if caso_base:
                        while linha.strip() not in FIM_BLOCO:

                            if linha[0] != COMENTARIO:
                                self.base['num'].append(linha[0:5])
                                self.base['nome'].append(linha[5:17])
                                self.base['local'].append(linha[19:59].strip())

                            else:
                                self.comentarios.append(linha)

                            self.next_line(f)
                            linha = self.linha
                        caso_base = False
                        continue

                    if not caso_base:
                        while linha.strip() not in FIM_BLOCO:

                            if linha[0] != COMENTARIO:
                                self.periodo['num'].append(linha[0:4])
                                self.periodo['nome'].append(linha[4:18])
                                self.periodo['ano'].append(linha[18:22])
                                self.periodo['mes'].append(linha[22:24])
                                self.periodo['dia'].append(linha[24:26])
                                self.periodo['hora'].append(linha[27:29])
                                self.periodo['minuto'].append(linha[30:32])
                                self.periodo['duracao'].append(linha[32:37])
                                self.periodo['num_caso'].append(linha[40:44])
                                self.periodo['local'].append(linha[45:85].strip())

                            else:
                                self.comentarios.append(linha)

                            self.next_line(f)
                            linha = self.linha
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_base['df'] = pd.DataFrame(self.base)
                self.bloco_periodo['df'] = pd.DataFrame(self.periodo)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for idx, value in self.bloco_base['df'].iterrows():
                    linha = self.bloco_base['formato'].format(**value)
                    f.write(linha)
                f.write('99999\n\n')

                for idx, value in self.bloco_periodo['df'].iterrows():
                    linha = self.bloco_periodo['formato'].format(**value)
                    f.write(linha)
                f.write('99999\nFIM')

        except Exception:
            raise
