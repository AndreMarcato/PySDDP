# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd

from PySDDP.dessem.script.templates.tolperd import TolperdTemplate

COMENTARIO = '&'

class Tolperd(TolperdTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Tolperd do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.registro_ln= dict()
        self.registro_nv = dict()

        self.registro_ln_df: pd.DataFrame()
        self.registro_nv_df: pd.DataFrame()

        self.tolperd = None
        self._comentarios_ = None


    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as tolerâncias para as perdas

        Manual do Usuario III.2 Neste arquivo informam-se as tolerâncias desejadas para a acurácia na representação das
        perdas nas linhas de transmissão. Podem-se definir tolerâncias por nível ou especificamnete determinadas linhas
        (TOLPERD.XXX).

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        # Listas referentes aos Registros LN
        self.registro_ln['mneumo'] = list()
        self.registro_ln['de'] = list()
        self.registro_ln['para'] = list()
        self.registro_ln['num_circuito'] = list()
        self.registro_ln['tol_perc'] = list()
        self.registro_ln['tol_MW'] = list()

        # Listas referentes aos Registros NV
        self.registro_nv_tabela['mneumo'] = list()
        self.registro_nv['niv_tensao'] = list()
        self.registro_nv['tol_perc'] = list()
        self.registro_nv['tol_MW'] = list()

        self.tolperd = list()
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
                        self.tolperd.append(linha)

                        continue

                    mneumo = linha[:2].strip().lower()

                    self.tolperd.append(linha[:2])

                    # Leitura dos dados de acordo com o mneumo correspondente

                    if mneumo == 'ln':
                        self.registro_ln['mneumo'].append(self.linha[:2])
                        self.registro_ln['de'].append(self.linha[3:8])
                        self.registro_ln['para'].append(self.linha[9:14])
                        self.registro_ln['num_circuito'].append(self.linha[15:18])
                        self.registro_ln['tol_perc'].append(self.linha[19:29])
                        self.registro_ln['tol_MW'].append(self.linha[30:40])

                        self.dados['registro_ln']['valores'] = self.registro_ln
                        self.registro_ln_df = pd.DataFrame(self.registro_ln)

                        continue
                    if mneumo == 'nv':
                        self.registro_nv_tabela['mneumo'].append(self.linha[:2])
                        self.registro_nv['niv_tensao'].append(self.linha[3:4])
                        self.registro_nv['tol_perc'].append(self.linha[5:15])
                        self.registro_nv['tol_MW'].append(self.linha[16:26])

                        self.dados['registro_nv']['valores'] = self.registro_nv
                        self.registro_nv_df = pd.DataFrame(self.registro_nv)

                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['tolperd']['valores'] = self.tolperd
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo com as tolerâncias para as perdas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Inicializa contadores para o loop
                num_linhas = len(self.tolperd)
                i_ln = 0
                i_nv = 0

                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.tolperd[i]
                    verifica_comentario = linha[0] == COMENTARIO

                    if verifica_comentario:
                        f.write(self.tolperd[i])
                        f.write("\n")
                        continue

                    if linha == 'LN':
                        # Tratando caractere '\n'
                        self.registro_ln_df['tol_MW'] = self.registro_ln_df['tol_MW'].str.replace('\n', '')

                        for idx, value in self.registro_ln_df.iterrows():
                            if idx == i_ln:
                                linha_ln = self.dados['registro_ln']['formato'].format(**value)
                                f.write(linha_ln)
                                continue

                        i_ln = i_ln + 1
                        continue

                    if linha == 'NV':
                        # Tratando caractere '\n'
                        self.registro_nv_df['tol_MW'] = self.registro_nv_df['tol_MW'].str.replace('\n', '')

                        for idx, value in self.registro_nv_df.iterrows():
                            if idx == i_nv:
                                linha_nv = self.dados['registro_nv']['formato'].format(**value)
                                f.write(linha_nv)
                                continue
                        i_nv = i_nv + 1
                        continue

        except Exception:
            raise