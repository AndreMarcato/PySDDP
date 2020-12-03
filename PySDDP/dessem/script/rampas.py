# -*- coding: utf-8 -*-
from abc import ABC
from typing import Optional, IO
import re
import numpy as np
import os

import pandas as pd

from PySDDP.dessem.script.templates.rampas import RampasTemplate


class Rampas(RampasTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rampas do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.rampas = dict()
        self.rampas_df: pd.DataFrame()
        self._comentarios_: Optional[list] = None
        self.ute: Optional[dict] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as trajetórias de acionamento/desligamento das unidades térmicas

        Manual do Usuario III.23 Arquivo com as Trajetórias de Acionamento/Desligamento das Unidades Térmicas
        (RAMPAS.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios_ = list()

        # Dicionário para armazenar nome e número da UTE:
        self.ute = {
            "Nome": list(),
            "Num": list()
        }

        # Dicionário para armazenar dados do bloco "RAMP":
        self.rampas['us'] = list()
        self.rampas['uni'] = list()
        self.rampas['seg'] = list()
        self.rampas['C'] = list()
        self.rampas['T'] = list()
        self.rampas['Potencia'] = list()
        self.rampas['Tempo'] = list()
        self.rampas['FlagMeiaHora'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:
                    self.next_line(f)

                    linha = self.linha.strip()

                    if linha == 'FIM':
                        self.bloco_rampas['valor'] = self.rampas
                        self.rampas_df = pd.DataFrame(self.rampas)
                        break

                    else:

                        if linha == '&' or linha == '&&' or linha == 'RAMP' or linha == self.bloco_rampas['descricao'] \
                                or linha == self.bloco_rampas['cabecalho']:
                            self._comentarios_.append(linha)
                            continue

                        else:
                            if linha[0] == '&':
                                self.ute['Nome'].append(linha)
                                numute = re.findall(r'\b\d+\b', linha)
                                numute = int(numute[0])
                                self.ute['Num'].append(numute)
                                continue

                            else:
                                us = int(linha[:3])
                                if us == self.ute['Num'][-1]:
                                    self.rampas['us'].append(self.linha[:3])
                                    self.rampas['uni'].append(self.linha[4:7])
                                    self.rampas['seg'].append(self.linha[8:11])
                                    self.rampas['C'].append(self.linha[12:14])
                                    self.rampas['T'].append(self.linha[15:18])
                                    self.rampas['Potencia'].append(self.linha[19:30])
                                    self.rampas['Tempo'].append(self.linha[31:36])
                                    self.rampas['FlagMeiaHora'].append(self.linha[37:38])
                                    continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                if self.linha[:3].upper() == FIM:
                    self.bloco_rampas['valor'] = self.rampas
                    self.rampas_df = pd.DataFrame(self.rampas)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo do arquivo com as trajetórias de acionamento/desligamento das unidades térmicas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                cont = len(self.ute["Nome"])
                numline = 0
                lines = len(self.rampas_df['us'])

                # Bloco RAMP
                # Imprime Mneumônico
                f.write('RAMP\n')
                f.write('&&\n')

                for icont in range(cont):
                    # print(self.rampas_df)
                    f.write(self.ute['Nome'][icont])
                    f.write('\n')

                    # Imprime Cabeçalho Completo
                    linha = self.bloco_rampas['descricao']
                    f.write(linha)
                    f.write('\n')
                    linha = self.bloco_rampas['cabecalho']
                    f.write(linha)
                    f.write('\n')

                    try:
                        while int(self.rampas_df['us'][numline]) == self.ute['Num'][icont]:
                            numline += 1
                    except:
                        numline = lines

                    rampas_df_new = self.rampas_df.head(numline)

                    info_ad = list()
                    info_ad.append('NotError')

                    for idx, value in rampas_df_new.iterrows():
                        numute = int(value['us'])
                        info_ad.append(value['us'] + value['T'])
                        if numute == self.ute['Num'][icont]:
                            if (value['us'] + value['T']) == info_ad[-2]:
                                linha = self.bloco_rampas['formato'].format(**value)
                                f.write(linha)
                            else:
                                f.write('&\n')
                                linha = self.bloco_rampas['formato'].format(**value)
                                f.write(linha)
                            self.rampas_df = self.rampas_df.drop(index=idx)

                    if icont < cont - 1:
                        f.write('&\n')
                        f.write('&\n')

                f.write('&\n')
                f.write('FIM\n')
        except Exception:
            raise
