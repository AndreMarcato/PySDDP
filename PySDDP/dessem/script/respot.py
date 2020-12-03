# -*- coding: utf-8 -*-
import os
import io
import pandas as pd

from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.respot import RespotTemplate

COMENTARIO = '&'
FIM_BLOCO = '9999'


class Respot(RespotTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Respot do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.reserva_potencia = dict()
        self.reserva_potencia_df: pd.DataFrame()

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de dados de reserva de potência

        Manual do Usuario III.2 Arquivo contendo informações sobre registros e dados de reservas de potência (RESPOT.XXX)

        Este arqquivo informam-se uma série de registros identificando as áreas de controle de reserva de potência que
        participarão do estudo (registros RP) e suas respectivas reservas de potência ao longo do horizonte de estudo
        (registro LM).

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        self.reserva_potencia['mneumo'] = list()
        self.reserva_potencia['num'] = list()
        self.reserva_potencia['di'] = list()
        self.reserva_potencia['hi'] = list()
        self.reserva_potencia['mi'] = list()
        self.reserva_potencia['df'] = list()
        self.reserva_potencia['hf'] = list()
        self.reserva_potencia['mf'] = list()
        self.reserva_potencia['potencia'] = list()


        self._comentarios_ = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]
                # Seguir o manual do usuario

                continua = True
                while continua:
                    self.next_line(f)
                    linha = self.linha.strip()

                    # Se a linha for um comentário, não faço nada e pulo para próxima linha
                    if linha == COMENTARIO:
                        self._comentarios_.append(linha)

                        continue

                    # Encontrou o caractere de final de bloco então para a leitura
                    if self.linha[:4] == FIM_BLOCO:
                        self.dados['potencia']['valores'] = self.reserva_potencia
                        self.reserva_potencia_df = pd.DataFrame(self.reserva_potencia)
                        break

                    # O ideal seria validarmos antes de carregar na estrutura
                    self.reserva_potencia['mneumo'].append(self.linha[:2])
                    self.reserva_potencia['num'].append(self.linha[4:7])
                    self.reserva_potencia['di'].append(self.linha[9:11])
                    self.reserva_potencia['hi'].append(self.linha[12:14])
                    self.reserva_potencia['mi'].append(self.linha[15:16])
                    self.reserva_potencia['df'].append(self.linha[17:19])
                    self.reserva_potencia['hf'].append(self.linha[20:22])
                    self.reserva_potencia['mf'].append(self.linha[23:24])
                    self.reserva_potencia['potencia'].append(self.linha[30:70])

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                if self.linha[:4].upper() == FIM_BLOCO:
                    self.dados['potencia']['valores'] = self.reserva_potencia
                    self.reserva_potencia_df = pd.DataFrame(self.reserva_potencia)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de dados de reserva de potência

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for idx, value in self.reserva_potencia_df.iterrows():
                    linha = self.dados['potencia']['formato'].format(**value)

                    if value['mneumo'] == 'RP':
                        f.write("&\n")
                        f.write(linha)
                        f.write("&\n")
                    else:
                        f.write(linha)

                f.write(f"{FIM_BLOCO}\n")


        except Exception:
            raise