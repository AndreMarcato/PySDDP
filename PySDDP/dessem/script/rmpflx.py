# -*- coding: utf-8 -*-
from typing import Optional, IO

import pandas as pd
import os

from PySDDP.dessem.script.templates.rmpflx import RmpflxTemplate

MNE = 'RMPFLX'
COMENTARIO = '&'


class Rmpflx(RmpflxTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rmpflx do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.rest = dict()
        self.rest_df: pd.DataFrame()

        self.limi = dict()
        self.limi_df: pd.DataFrame()

        self._comentarios_: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as rampas das inequações de fluxo

        Manual do Usuario III.20 Arquivo com as Rampas das Inequações de Fluxo
        (RMPFLX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios_ = list()

        # Dicionário para armazenar dados do bloco "REST":
        self.rest['mne'] = list()
        self.rest['rest'] = list()
        self.rest['num'] = list()
        self.rest['valor'] = list()
        self.rest['tipo'] = list()

        # Dicionário para armazenar dados do bloco "LIMI":
        self.limi['mne'] = list()
        self.limi['limi'] = list()
        self.limi['di'] = list()
        self.limi['hi'] = list()
        self.limi['fi'] = list()
        self.limi['df'] = list()
        self.limi['hf'] = list()
        self.limi['ff'] = list()
        self.limi['num'] = list()
        self.limi['rinferior'] = list()
        self.limi['rsuperior'] = list()
        self.limi['t'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:
                    self.next_line(f)

                    linha = self.linha.strip()

                    if linha[0] == COMENTARIO:
                        self._comentarios_.append(linha)
                        continue

                    elif linha[:6] == MNE:

                        if linha[7:11] == 'REST':
                            self.rest['mne'].append(self.linha[:6])
                            self.rest['rest'].append(self.linha[7:11])
                            self.rest['num'].append(self.linha[12:16])
                            self.rest['valor'].append(self.linha[17:27])
                            self.rest['tipo'].append(self.linha[28:29])

                        elif linha[8:11] == 'LIMI':
                            self.limi['mne'].append(self.linha[:6])
                            self.limi['limi'].append(self.linha[7:11])
                            self.limi['di'].append(self.linha[12:14])
                            self.limi['hi'].append(self.linha[15:17])
                            self.limi['fi'].append(self.linha[18:19])
                            self.limi['df'].append(self.linha[20:22])
                            self.limi['hf'].append(self.linha[23:25])
                            self.limi['ff'].append(self.linha[26:27])
                            self.limi['num'].append(self.linha[28:32])
                            self.limi['rinferior'].append(self.linha[33:43])
                            self.limi['rsuperior'].append(self.linha[44:54])
                            self.limi['t'].append(self.linha[55:56])

                        else:
                            self.blocorest['valor'] = self.rest
                            self.rest_df = pd.DataFrame(self.rest)
                            self.blocolimi['valor'] = self.limi
                            self.limi_df = pd.DataFrame(self.limi)
                            break

                        continue

                    else:
                        self.blocorest['valor'] = self.rest
                        self.rest_df = pd.DataFrame(self.rest)
                        self.blocolimi['valor'] = self.limi
                        self.limi_df = pd.DataFrame(self.limi)
                        break

        except Exception as err:

            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                if self.linha[0] == COMENTARIO or self.linha[:6].upper() == MNE:
                    self.blocorest['valor'] = self.rest
                    self.rest_df = pd.DataFrame(self.rest)
                    self.blocolimi['valor'] = self.limi
                    self.limi_df = pd.DataFrame(self.limi)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para Escrita do arquivo com as rampas das inequações de fluxo

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Cabeçalho
                linha = self.blocorest['cabecalho']
                f.write(linha)

                for idx, value in self.rest_df.iterrows():
                    linha = self.blocorest['formato'].format(**value)
                    f.write(linha)

                # Imprime Cabeçalho
                linha = self.blocolimi['cabecalho']
                f.write(linha)

                for idx, value in self.limi_df.iterrows():
                    linha = self.blocolimi['formato'].format(**value)
                    f.write(linha)

        except Exception:
            raise
