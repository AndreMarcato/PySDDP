# -*- coding: utf-8 -*-
from typing import Optional, IO

import os

import pandas as pd

from PySDDP.dessem.script.templates.rampas import RampasTemplate

FIM = "FIM"


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
                        if linha[0] == '&' or linha[:4] == 'RAMP':
                            self._comentarios_.append(linha)
                            continue

                        else:
                            self.rampas['us'].append(self.linha[:3])
                            self.rampas['uni'].append(self.linha[4:7])
                            self.rampas['seg'].append(self.linha[8:11])
                            self.rampas['C'].append(self.linha[12:14])
                            self.rampas['T'].append(self.linha[15:18])
                            self.rampas['Potencia'].append(self.linha[19:30])
                            self.rampas['Tempo'].append(self.linha[31:36])
                            self.rampas['FlagMeiaHora'].append(self.linha[37])
                            continue

                if self.linha[:3].upper() == FIM:
                    self.bloco_rampas['valor'] = self.rampas
                    self.rampas_df = pd.DataFrame(self.rampas)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise

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

                # Bloco RAMP
                # Imprime Mneumônico
                f.write('RAMP\n')
                f.write('&&\n')

                usi, traj = None, None

                for idx, value in self.rampas_df.iterrows():
                    linha = self.bloco_rampas['formato'].format(**value)
                    if value['us'] == usi:
                        if value['T'] == traj:
                            f.write(linha)
                        else:
                            f.write('&\n')
                            f.write(linha)

                    else:
                        # Imprime Cabeçalho Completo
                        f.write('&\n')
                        f.write('&\n')
                        f.write(self.bloco_rampas['descricao'])
                        f.write('\n')
                        f.write(self.bloco_rampas['cabecalho'])
                        f.write('\n')
                        f.write(linha)

                    usi = value['us']
                    traj = value['T']

                f.write('&\n')
                f.write('FIM\n')
        except Exception:
            raise
