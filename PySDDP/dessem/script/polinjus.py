from PySDDP.dessem.script.templates.polinjus import PolinJusTemplate

import pandas as pd
from typing import IO
import os

class PolinJus(PolinJusTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo PolinJus do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.curva_jusante = dict()
        self.curva_jusante["identificador"] = list()
        self.curva_jusante["codigo_usina"] = list()
        self.curva_jusante["id_curva"] = list()
        self.curva_jusante["altura_montante"] = list()

        self.polinomio = dict()
        self.polinomio["identificador"] = list()
        self.polinomio["codigo_usina"] = list()
        self.polinomio["id_curva"] = list()
        self.polinomio["numero_segmentos"] = list()

        self.segmento = dict()
        self.segmento["identificador"] = list()
        self.segmento["codigo_usina"] = list()
        self.segmento["id_curva"] = list()
        self.segmento["id_segmento"] = list()
        self.segmento["limite_inferior"] = list()
        self.segmento["limite_superior"] = list()
        self.segmento["coeficiente_grau_0"] = list()
        self.segmento["coeficiente_grau_1"] = list()
        self.segmento["coeficiente_grau_2"] = list()
        self.segmento["coeficiente_grau_3"] = list()
        self.segmento["coeficiente_grau_4"] = list()

        self.afogamento = dict()
        self.afogamento["identificador"] = list()
        self.afogamento["codigo_usina"] = list()
        self.afogamento["flag"] = list()

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

                    elif "HIDRELETRICA-CURVAJUSANTE-POLINOMIOPORPARTES-SEGMENTO" in line:
                        dados = line.split(";")
                        self.segmento["identificador"].append(dados[0])
                        self.segmento["codigo_usina"].append(dados[1])
                        self.segmento["id_curva"].append(dados[2])
                        self.segmento["id_segmento"].append(dados[3])
                        self.segmento["limite_inferior"].append(dados[4])
                        self.segmento["limite_superior"].append(dados[5])
                        self.segmento["coeficiente_grau_0"].append(dados[6])
                        self.segmento["coeficiente_grau_1"].append(dados[7])
                        self.segmento["coeficiente_grau_2"].append(dados[8])
                        self.segmento["coeficiente_grau_3"].append(dados[9])
                        self.segmento["coeficiente_grau_4"].append(dados[10])
                        continue

                    elif "HIDRELETRICA-CURVAJUSANTE-POLINOMIOPORPARTES" in line:
                        dados = line.split(";")
                        self.polinomio["identificador"].append(dados[0])
                        self.polinomio["codigo_usina"].append(dados[1])
                        self.polinomio["id_curva"].append(dados[2])
                        self.polinomio["numero_segmentos"].append(dados[3])
                        continue

                    elif "HIDRELETRICA-CURVAJUSANTE-AFOGAMENTO-EXPLICITO-USINA" in line:
                        dados = line.split(";")
                        self.afogamento["identificador"].append(dados[0])
                        self.afogamento["codigo_usina"].append(dados[1])
                        self.afogamento["flag"].append(dados[2])
                        continue

                    elif "HIDRELETRICA-CURVAJUSANTE" in line:
                        dados = line.split(";")
                        self.curva_jusante["identificador"].append(dados[0])
                        self.curva_jusante["codigo_usina"].append(dados[1])
                        self.curva_jusante["id_curva"].append(dados[2])
                        self.curva_jusante["altura_montante"].append(dados[3])
                        continue

                    else:
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_curva_jusante['df'] = pd.DataFrame(self.curva_jusante)
                self.bloco_polinomio['df'] = pd.DataFrame(self.polinomio)
                self.bloco_segmento['df'] = pd.DataFrame(self.segmento)
                self.bloco_afogamento['df'] = pd.DataFrame(self.afogamento)

                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
                f.write(" &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"
                        " & Cadastro das familias de curvas de jusante\n"
                        " &\n"
                        " & Usina: codigo da usina hidraulica\n"
                        " & IndCurva: indice da familia (sequencial)\n"
                        " & HjusRef: nivel de montante da usina de jusante para referencia da familia\n"
                        " & nPol: quantidade de polinomios da familia\n"
                        " &\n"
                        " &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")

                f.write(self.bloco_curva_jusante["descricao"])
                f.write(self.bloco_polinomio["descricao"])

                for idx, value in self.bloco_curva_jusante["df"].iterrows():
                    line = self.bloco_curva_jusante["formato"].format(
                        identificador=value["identificador"],
                        codigo_usina=value["codigo_usina"],
                        id_curva=value["id_curva"],
                        altura_montante=value["altura_montante"]
                    )
                    f.write(line)

                    line = self.bloco_polinomio["formato"].format(
                        identificador=self.bloco_polinomio["df"]["identificador"][idx],
                        codigo_usina=self.bloco_polinomio["df"]["codigo_usina"][idx],
                        id_curva=self.bloco_polinomio["df"]["id_curva"][idx],
                        numero_segmentos=self.bloco_polinomio["df"]["numero_segmentos"][idx]
                    )
                    f.write(line)
                    f.write(" &\n")

                f.write(" &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"
                        " &\n"
                        " & Cadastro dos coeficientes dos polinômios por partes das curvas de jusante\n"
                        " &\n"
                        " & Usina: codigo da usina hidraulica\n"
                        " & IndCurva: indice da familia (sequencial)\n"
                        " & IndPolin Polinomio: indice do polinomio do segmento (sequencial)\n"
                        " & QjusMin: Limite inferior de vazao de jusante (defluencia mais lateral) para janela de "
                        "validade do polinomio\n"
                        " & QjusMax: Limite superior de vazao de jusante (defluencia mais lateral) para janela de "
                        "validade do polinomio\n"
                        " & a0 : coeficiente de grau 0 do polinomio\n"
                        " & a1 : coeficiente de grau 1 do polinomio\n"
                        " & a2 : coeficiente de grau 2 do polinomio\n"
                        " & a3 : coeficiente de grau 3 do polinomio\n"
                        " & a4 : coeficiente de grau 4 do polinomio\n"
                        " &\n"
                        " &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")

                f.write(self.bloco_segmento["descricao"])

                usina = None
                curva = None

                for idx, value in self.bloco_segmento["df"].iterrows():

                    if value["codigo_usina"] == usina and value["id_curva"] == curva:
                        pass
                    else:
                        usina = value["codigo_usina"]
                        curva = value["id_curva"]

                        f.write(" &\n")

                    line = self.bloco_segmento["formato"].format(
                        identificador=value["identificador"],
                        codigo_usina=value["codigo_usina"],
                        id_curva=value["id_curva"],
                        id_segmento=value["id_segmento"],
                        limite_inferior=value["limite_inferior"],
                        limite_superior=value["limite_superior"],
                        coeficiente_grau_0=value["coeficiente_grau_0"],
                        coeficiente_grau_1=value["coeficiente_grau_1"],
                        coeficiente_grau_2=value["coeficiente_grau_2"],
                        coeficiente_grau_3=value["coeficiente_grau_3"],
                        coeficiente_grau_4=value["coeficiente_grau_4"]
                    )
                    f.write(line)

                f.write("&\n")
                for idx, value in self.bloco_afogamento["df"].iterrows():

                    line = self.bloco_afogamento["formato"].format(
                        identificador=value["identificador"],
                        codigo_usina=value["codigo_usina"],
                        flag=value["flag"]
                    )
                    f.write(line)

        except Exception:
            raise
