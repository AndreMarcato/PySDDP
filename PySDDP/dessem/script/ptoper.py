# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd

from PySDDP.dessem.script.templates.ptoper import PtoperTemplate

COMENTARIO = '&'


class Ptoper(PtoperTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Ptoper do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.ptoper = dict()
        self.ptoper_df: pd.DataFrame()

        self._comentarios_ = None


    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de ponto de operação

        Manual do Usuario III.2 Arquivo contendo informações sobre o ponto de operação de algumas variáveis do problema
        pode ser fixado por meio dos registros PTOPER, que podem ser fornecidos no arquivo ENTDADOS ou em arquivo
         específico, cujo nome é fornecido no arquivo DESSEM.ARQ, sob o mnemônico "PTOPER"(PTOPER.XXX).

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        self.ptoper['mneumo'] = list()
        self.ptoper['id'] = list()
        self.ptoper['tp_var'] = list()
        self.ptoper['di'] = list()
        self.ptoper['hi'] = list()
        self.ptoper['mi'] = list()
        self.ptoper['df'] = list()
        self.ptoper['hf'] = list()
        self.ptoper['mf'] = list()
        self.ptoper['valor_var'] = list()

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
                        continue

                    mneumo = linha[:13].strip().lower()

                    # Leitura dos dados
                    self.ptoper['mneumo'].append(self.linha[:13])
                    self.ptoper['id'].append(self.linha[14:17])
                    self.ptoper['tp_var'].append(self.linha[18:24])
                    self.ptoper['di'].append(self.linha[25:27])
                    self.ptoper['hi'].append(self.linha[28:30])
                    self.ptoper['mi'].append(self.linha[31:32])
                    self.ptoper['df'].append(self.linha[33:35])
                    self.ptoper['hf'].append(self.linha[36:38])
                    self.ptoper['mf'].append(self.linha[39:40])
                    self.ptoper['valor_var'].append(self.linha[41:54])

                    self.dados['ptoper']['valores'] = self.ptoper
                    self.ptoper_df = pd.DataFrame(self.ptoper)

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['ptoper']['valores'] = self.ptoper
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de ponto de operação

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                linha = self.dados['ptoper']['cabecalho']
                f.write(linha)

                # Tratando caractere '\n'
                self.ptoper_df['valor_var'] = self.ptoper_df['valor_var'].str.replace('\n', '')

                for idx, value in self.ptoper_df.iterrows():
                    linha = self.dados['ptoper']['formato'].format(**value)
                    f.write(linha)

        except Exception:
            raise