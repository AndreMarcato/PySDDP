# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd

from PySDDP.dessem.script.templates.curvtviag import CurvtviagTemplate

COMENTARIO = '&'


class Curvtviag(CurvtviagTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Curvtviag do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.curvtviag = dict()
        self.curvtviag_df: pd.DataFrame()

        self._comentarios_ = None



    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo que contem as curvas de propagação do tempo de viagem

        Manual do Usuario III.2 Arquivo contendo informações sobre as curvas de propagação do tempo de viagem da água
        para as usinas definidas nos registros TVIAG do arquivo ENTDADOS.XXX (CURVTVIAG.XXX).

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        self.curvtviag['mneumo'] = list()
        self.curvtviag['num_mont'] = list()
        self.curvtviag['num_jus'] = list()
        self.curvtviag['tipo_jus'] = list()
        self.curvtviag['num_hr'] = list()
        self.curvtviag['fator'] = list()

        self.curvtviag_comentarios = list()
        self._comentarios_ = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]
                # Seguir o manual do usuario
                continua = True

                while continua:

                    self.next_line(f)

                    linha = self.linha.strip()
                    # Se a linha for comentario não faço nada e pulo pra proxima linha
                    if linha[0] == COMENTARIO:
                        self._comentarios_.append(linha)
                        self.curvtviag_comentarios.append(linha)
                        continue

                    mneumo = linha[:6].strip().lower()
                    self.curvtviag_comentarios.append(linha)
                    # Leitura dos dados
                    self.curvtviag['mneumo'].append(self.linha[:6])
                    self.curvtviag['num_mont'].append(self.linha[9:12])
                    self.curvtviag['num_jus'].append(self.linha[14:17])
                    self.curvtviag['tipo_jus'].append(self.linha[19:20])
                    self.curvtviag['num_hr'].append(self.linha[24:34])
                    self.curvtviag['fator'].append(self.linha[34:44])

                    self.dados['curvtviag']['valores'] = self.curvtviag
                    self.curvtviag_df = pd.DataFrame(self.curvtviag)

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['curvtviag']['valores'] = self.curvtviag
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo com as curvas de propagação do tempo de viagem

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

               num_linhas = len(self.curvtviag_comentarios)
               i_dados = 0

               for i in range(num_linhas):
                   # Verifica comentário
                   linha = self.curvtviag_comentarios[i]
                   self.curvtviag_comentarios[i] = self.curvtviag_comentarios[i].replace('\n', '')
                   verifica_comentario = linha[0] == COMENTARIO
                   if verifica_comentario:
                       f.write(self.curvtviag_comentarios[i])
                       f.write("\n")
                   else:
                        # Tratando caractere '\n'
                        self.curvtviag_df['fator'] = self.curvtviag_df['fator'].str.replace('\n', '')
                        for idx, value in self.curvtviag_df.iterrows():
                            if idx == i_dados:
                                linha = self.dados['curvtviag']['formato'].format(**value)
                                f.write(linha)
                        i_dados = i_dados + 1
        except Exception:
            raise