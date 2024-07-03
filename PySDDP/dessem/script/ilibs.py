from PySDDP.dessem.script.templates.ilibs import ILibsTemplate

import pandas as pd
from typing import IO
import os


class ILibs(ILibsTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo ILibs do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.indice = dict()
        self.indice["identificador"] = list()
        self.indice["funcionalidade"] = list()
        self.indice["arquivo"] = list()

        self.comentarios = list()

    def ler(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:
                    self.next_line(f)
                    line = self.linha.strip()

                    if line[0] == "&":
                        self.comentarios.append(line)
                        continue
                    else:
                        dados = line.split(";")
                        self.indice["identificador"].append(dados[0].strip())
                        self.indice["funcionalidade"].append(dados[1].strip())
                        self.indice["arquivo"].append(dados[2].strip())
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_indice['df'] = pd.DataFrame(self.indice)

                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
                f.write("& arquivo indice\n")

                for _, row in self.bloco_indice["df"].iterrows():
                    line = self.bloco_indice["formato"].format(
                        identificador=row["identificador"],
                        funcionalidade=row["funcionalidade"],
                        arquivo=row["arquivo"]
                    )
                    f.write(line)

                f.write("&\n")

        except Exception:
            raise
