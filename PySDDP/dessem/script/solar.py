from PySDDP.dessem.script.templates.solar import SolarTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'

class Solar(SolarTemplate):

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

                    # Se a linha for um comentário, não faço nada e pulo para próxima linha
                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        continue

                    if linha[:10] == 'SOLARBARRA':
                        self.barra['mneumo'].append(linha[0:11])
                        self.barra['codigo'].append(linha[12:18])
                        self.barra['barra'].append(linha[19:25])
                        continue

                    if linha[:9] == 'SOLARSUBM':
                        self.submercado['mneumo'].append(linha[0:10])
                        self.submercado['codigo'].append(linha[11:17])
                        self.submercado['submercado'].append(linha[18:21])
                        continue

                    if linha[:13] == 'SOLAR-GERACAO':
                        self.geracao['mneumo'].append(linha[0:14])
                        self.geracao['codigo'].append(linha[15:21])
                        self.geracao['DI'].append(linha[22:25])
                        self.geracao['HI'].append(linha[26:29])
                        self.geracao['FI'].append(linha[30:32])
                        self.geracao['HF'].append(linha[33:36])
                        self.geracao['DF'].append(linha[37:40])
                        self.geracao['FF'].append(linha[41:43])
                        self.geracao['geracao'].append(linha[44:55])
                        continue

                    if linha[:6] == 'SOLAR ':
                        self.usina['mneumo'].append(linha[0:6])
                        self.usina['codigo'].append(linha[7:13])
                        self.usina['nome'].append(linha[14:55])
                        self.usina['pmax'].append(linha[56:67])
                        self.usina['fcap'].append(linha[68:72])
                        self.usina['c'].append(linha[73])
                        continue

            print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

        except Exception as err:
           if isinstance(err, StopIteration):
               self.bloco_usina['df'] = pd.DataFrame(self.usina)
               self.bloco_barra['df'] = pd.DataFrame(self.barra)
               self.bloco_submercado['df'] = pd.DataFrame(self.submercado)
               self.bloco_geracao['df'] = pd.DataFrame(self.geracao)
               self.blocos = [self.bloco_usina,self.bloco_barra,self.bloco_submercado,self.bloco_geracao]
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