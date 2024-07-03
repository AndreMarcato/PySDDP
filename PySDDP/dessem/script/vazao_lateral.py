from PySDDP.dessem.script.templates.vazao_lateral import VazaoLateralTemplate

import pandas as pd
from typing import IO
import os


class VazaoLateral(VazaoLateralTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Vazao Lateral do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.defluencia = dict()
        self.defluencia["identificador"] = list()
        self.defluencia["codigo_usina_influenciada"] = list()
        self.defluencia["fator_turbinamento"] = list()
        self.defluencia["fator_vertimento"] = list()

        self.posto = dict()
        self.posto["identificador"] = list()
        self.posto["codigo_usina_influenciada"] = list()
        self.posto["codigo_posto"] = list()
        self.posto["fator"] = list()

        self.usina = dict()
        self.usina["identificador"] = list()
        self.usina["codigo_usina_influenciada"] = list()
        self.usina["codigo_usina_influenciadora"] = list()
        self.usina["fator"] = list()

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

                    if line[:48] == "HIDRELETRICA-VAZAO-JUSANTE-INFLUENCIA-DEFLUENCIA":
                        dados = line.split(";")
                        self.defluencia["identificador"].append(dados[0].strip())
                        self.defluencia["codigo_usina_influenciada"].append(dados[1].strip())
                        self.defluencia["fator_turbinamento"].append(dados[2].strip())
                        self.defluencia["fator_vertimento"].append(dados[3].strip())
                        continue

                    if line[:43] == "HIDRELETRICA-VAZAO-JUSANTE-INFLUENCIA-POSTO":
                        dados = line.split(";")
                        self.posto["identificador"].append(dados[0].strip())
                        self.posto["codigo_usina_influenciada"].append(dados[1].strip())
                        self.posto["codigo_posto"].append(dados[2].strip())
                        self.posto["fator"].append(dados[3].strip())
                        continue

                    if line[:43] == "HIDRELETRICA-VAZAO-JUSANTE-INFLUENCIA-USINA":
                        dados = line.split(";")
                        self.usina["identificador"].append(dados[0].strip())
                        self.usina["codigo_usina_influenciada"].append(dados[1].strip())
                        self.usina["codigo_usina_influenciadora"].append(dados[2].strip())
                        self.usina["fator"].append(dados[3].strip())
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_defluencia['df'] = pd.DataFrame(self.defluencia)
                self.bloco_posto['df'] = pd.DataFrame(self.posto)
                self.bloco_usina['df'] = pd.DataFrame(self.usina)

                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
                f.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"
                        "& Influências laterais\n"
                        "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")

                for _, row in self.bloco_defluencia["df"].iterrows():
                    line = self.bloco_defluencia["formato"].format(
                        identificador=row["identificador"],
                        codigo_usina_influenciada=row["codigo_usina_influenciada"],
                        fator_turbinamento=row["fator_turbinamento"],
                        fator_vertimento=row["fator_vertimento"]
                    )
                    f.write(self.bloco_defluencia["descricao"])
                    f.write(line)
                    f.write("&\n")

                for _, row in self.bloco_posto["df"].iterrows():
                    line = self.bloco_posto["formato"].format(
                        identificador=row["identificador"],
                        codigo_usina_influenciada=row["codigo_usina_influenciada"],
                        codigo_posto=row["codigo_posto"],
                        fator=row["fator"]
                    )
                    f.write(self.bloco_posto["descricao"])
                    f.write(line)
                    f.write("&\n")

                for _, row in self.bloco_usina["df"].iterrows():
                    line = self.bloco_usina["formato"].format(
                        identificador=row["identificador"],
                        codigo_usina_influenciada=row["codigo_usina_influenciada"],
                        codigo_usina_influenciadora=row["codigo_usina_influenciadora"],
                        fator=row["fator"]
                    )
                    f.write(self.bloco_usina["descricao"])
                    f.write(line)
                    f.write("&\n")

        except Exception:
            raise
