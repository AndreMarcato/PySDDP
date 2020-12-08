from PySDDP.dessem.script.templates.cotasr11 import Cotasr11Template

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'


class Cotasr11(Cotasr11Template):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Renovaveis do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.comentarios = list()
        self.cotasr11 = list()
        self.dados = dict()

    def ler(self, file_name: str) -> None:

        # listas referentes ao dicionário DADOS
        self.dados['dia'] = list()
        self.dados['hora'] = list()
        self.dados['meiahora'] = list()
        self.dados['cota'] = list()
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:
                    self.next_line(f)
                    linha = self.linha.strip()

                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        self.cotasr11.append(linha)
                        continue

                    else:
                        self.dados['dia'].append(linha[0:2])
                        self.dados['hora'].append(linha[3:5])
                        self.dados['meiahora'].append(linha[6])
                        self.dados['cota'].append(linha[16:26])
                        self.cotasr11.append(linha)
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_dados['df'] = pd.DataFrame(self.dados)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
                num_linhas = len(self.cotasr11)
                i_dados = 0
                for i in range(num_linhas):
                    # Verifica comentário
                    linha = self.cotasr11[i]
                    self.cotasr11[i] = self.cotasr11[i].replace('\n', '')
                    verifica_comentario = linha[0] == COMENTARIO
                    if verifica_comentario:
                        f.write(self.cotasr11[i])
                        f.write("\n")
                    else:
                        for idx, value in self.bloco_dados['df'].iterrows():
                            if idx == i_dados:
                                linha = self.bloco_dados['formato'].format(**value)
                                f.write(linha)
                        i_dados = i_dados + 1
        except Exception:
            raise