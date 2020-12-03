# -*- coding: utf-8 -*-
from typing import Optional, IO

import pandas as pd
import os

from PySDDP.dessem.script.templates.respotele import RespoteleTemplate

MNE = 'REPE'
COMENTARIO = '&'


class Respotele(RespoteleTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Respotele do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.respotele = dict()
        self.respotele_df: pd.DataFrame()
        self._comentarios_: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as reservas de potência para as inequações de fluxo

        Manual do Usuario III.21 Arquivo com as Reservas de Potência para as Inequações de Fluxo
        (RESPOTELE)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios_ = list()

        # Dicionário para armazenar dados do bloco "REPE":
        self.respotele['mne'] = list()
        self.respotele['flag'] = list()
        self.respotele['dref'] = list()
        self.respotele['di'] = list()
        self.respotele['hi'] = list()
        self.respotele['fi'] = list()
        self.respotele['df'] = list()
        self.respotele['hf'] = list()
        self.respotele['ff'] = list()
        self.respotele['valor'] = list()

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

                    elif linha[:4] == MNE:
                        self.respotele['mne'].append(self.linha[:4])
                        self.respotele['flag'].append(self.linha[6:6])
                        self.respotele['dref'].append(self.linha[8:12])
                        self.respotele['di'].append(self.linha[13:15])
                        self.respotele['hi'].append(self.linha[16:18])
                        self.respotele['fi'].append(self.linha[19:19])
                        self.respotele['df'].append(self.linha[21:23])
                        self.respotele['hf'].append(self.linha[24:26])
                        self.respotele['ff'].append(self.linha[27:27])
                        self.respotele['valor'].append(self.linha[29:38])
                        continue

                    else:
                        self.bloco_respotele['valor'] = self.respotele
                        self.respotele_df = pd.DataFrame(self.respotele)
                        break

        except Exception as err:

            if isinstance(err, StopIteration):

                # Verifica se atingiu o final do bloco

                if self.linha[0] == COMENTARIO or self.linha[:4].upper() == MNE:
                    self.bloco_respotele['valor'] = self.respotele
                    self.respotele_df = pd.DataFrame(self.respotele)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para Escrita do arquivo com as reservas de potência para as inequações de fluxo

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Cabeçalho
                linha = self.bloco_respotele['cabecalho']
                f.write(linha)

                for idx, value in self.respotele_df.iterrows():
                    linha = self.bloco_respotele['formato'].format(**value)
                    f.write(linha)

        except Exception:
            raise
