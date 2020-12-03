from PySDDP.dessem.script.templates.ilstri import IlstriTemplate
import numpy as np
from typing import IO
import os

COMENTARIO = '&'


class Ilstri(IlstriTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Ils_tri do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.niv = list()
        self.nor = list()
        self.max = list()
        self.dados = list()

        self.comentarios = list()

    def ler(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:
                    self.next_line(f)
                    linha = self.linha

                    # Se a linha for um comentário, não faço nada e pulo para próxima linha
                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        continue

                    if linha[:3] == 'NIV':
                        self.niv.append(linha[:4])
                        for i in np.arange(4, 138, 7):
                            self.niv.append(linha[i:i+7])
                        continue

                    if linha[:3] == 'NOR':
                        self.nor.append(linha[:4])
                        for i in np.arange(4, 138, 7):
                            self.nor.append(linha[i:i+7])
                        continue

                    if linha[:3] == 'MAX':
                        self.max.append(linha[:4])
                        for i in np.arange(4, 138, 7):
                            self.max.append(linha[i:i+7])
                        continue

                    self.dados.append(linha[:4])
                    for i in np.arange(4, 138, 7):
                        self.dados.append(linha[i:i+7])

        except Exception as err:
            if isinstance(err, StopIteration):
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for value in self.niv:
                    f.write(value)
                for value in self.dados:
                    f.write(value)
                for value in self.nor:
                    f.write(value)
                for value in self.max:
                    f.write(value)

        except Exception:
            raise