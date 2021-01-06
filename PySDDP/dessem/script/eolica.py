from PySDDP.dessem.script.templates.eolica import EolicaTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'


class Eolica(EolicaTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Renovaveis do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.usina = dict()
        self.usina['mneumo'] = list()
        self.usina['codigo'] = list()
        self.usina['nome'] = list()
        self.usina['pmax'] = list()
        self.usina['fcap'] = list()
        self.usina['c'] = list()

        self.submercado = dict()
        self.submercado['mneumo'] = list()
        self.submercado['codigo'] = list()
        self.submercado['submercado'] = list()

        self.barra = dict()
        self.barra['mneumo'] = list()
        self.barra['codigo'] = list()
        self.barra['barra'] = list()

        self.geracao = dict()
        self.geracao['mneumo'] = list()
        self.geracao['codigo'] = list()
        self.geracao['DI'] = list()
        self.geracao['HI'] = list()
        self.geracao['FI'] = list()
        self.geracao['DF'] = list()
        self.geracao['HF'] = list()
        self.geracao['FF'] = list()
        self.geracao['geracao'] = list()

        self.comentarios = list()
        self.blocos = list()

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

                    if linha[:11] == 'EOLICABARRA':
                        self.barra['mneumo'].append(linha[0:12].strip())
                        self.barra['codigo'].append(linha[13:19].strip())
                        self.barra['barra'].append(linha[20:26].strip())
                        continue

                    if linha[:10] == 'EOLICASUBM':
                        self.submercado['mneumo'].append(linha[0:11].strip())
                        self.submercado['codigo'].append(linha[12:18].strip())
                        self.submercado['submercado'].append(linha[19:22].strip())
                        continue

                    if linha[:14] == 'EOLICA-GERACAO':
                        self.geracao['mneumo'].append(linha[0:15].strip())
                        self.geracao['codigo'].append(linha[16:22].strip())
                        self.geracao['DI'].append(linha[23:26].strip())
                        self.geracao['HI'].append(linha[27:30].strip())
                        self.geracao['FI'].append(linha[31:33].strip())
                        self.geracao['DF'].append(linha[34:37].strip())
                        self.geracao['HF'].append(linha[38:41].strip())
                        self.geracao['FF'].append(linha[42:44].strip())
                        self.geracao['geracao'].append(linha[45:56].strip())
                        continue

                    if linha[:7] == 'EOLICA ':
                        self.usina['mneumo'].append(linha[0:7].strip())
                        self.usina['codigo'].append(linha[8:14].strip())
                        self.usina['nome'].append(linha[15:56].strip())
                        self.usina['pmax'].append(linha[57:68].strip())
                        self.usina['fcap'].append(linha[69:73].strip())
                        self.usina['c'].append(linha[74].strip())
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_usina['df'] = pd.DataFrame(self.usina)
                self.bloco_barra['df'] = pd.DataFrame(self.barra)
                self.bloco_submercado['df'] = pd.DataFrame(self.submercado)
                self.bloco_geracao['df'] = pd.DataFrame(self.geracao)
                self.blocos = [self.bloco_usina, self.bloco_barra, self.bloco_submercado, self.bloco_geracao]
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for bloco in self.blocos:
                    linha = bloco['cabecalho']
                    f.write(linha)
                    linha = bloco['descricao']
                    f.write(linha)
                    linha = bloco['cabecalho']
                    f.write(linha)
                    for idx, value in bloco['df'].iterrows():
                        linha = bloco['formato'].format(**value)
                        f.write(linha)
        except Exception:
            raise