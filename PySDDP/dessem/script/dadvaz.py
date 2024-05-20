# -*- coding: utf-8 -*-
import os
import io
import pandas as pd

from abc import abstractmethod
from typing import Optional
from datetime import datetime

from PySDDP.dessem.script.templates.dadvaz import DadVazTemplate

FIM_BLOCO = 'FIM'


class DadVaz(DadVazTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo DadVaz do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.vazoes_diarias = dict()
        self.vazoes_diarias_df: pd.DataFrame()

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de dados de vazoes

        Manual do Usuario III.2 Arquivo contendo informações sobre o caso e dados de vazões naturais (DADVAZ.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        self.vazoes_diarias['num'] = list()
        self.vazoes_diarias['nome'] = list()
        self.vazoes_diarias['itp'] = list()
        self.vazoes_diarias['di'] = list()
        self.vazoes_diarias['hi'] = list()
        self.vazoes_diarias['mi'] = list()
        self.vazoes_diarias['df'] = list()
        self.vazoes_diarias['hf'] = list()
        self.vazoes_diarias['mf'] = list()
        self.vazoes_diarias['vazao'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]
                # Seguir o manual do usuario

                # Leitura dos Registros de 1 a 9
                for _ in range(9):
                    self.next_line(f)

                # Leitura do Registro 10
                self.next_line(f)

                # O ideal seria validarmos os valores
                linha = self.linha.strip()

                # Carrega o atributo referente ao registro 10
                self.data_hora = pd.to_datetime(linha, format="%H %d %m %Y")
                self.dados['data_hora']['valor'] = self.data_hora

                # Leitura dos Registros de 11 e 12
                for _ in range(2):
                    self.next_line(f)

                # Leitura do Registro 13
                self.next_line(f)

                # O ideal seria validarmos os valores
                linha = self.linha.strip().split()
                self.conf_gerais = [int(w) for w in linha]
                self.dados['conf_gerais']['valor'] = self.conf_gerais

                # Carrega os atributos referentes aos registros lidos
                self.numero_dia_inicial, self.semana_fcf, self.numero_semanas, self.pre_interesse = self.conf_gerais

                # Leitura dos Registros de 14 a 16
                for _ in range(3):
                    self.next_line(f)

                # Leitura do Registro 17 em diante
                continua = True

                while continua:
                    # Le a proxima linha
                    self.next_line(f)

                    # Encontrou caractere de final de bloco então para a leitura
                    if self.linha[:3] == FIM_BLOCO:
                        self.dados['vazoes_diarias']['valores'] = self.vazoes_diarias
                        self.vazoes_diarias_df = pd.DataFrame(self.vazoes_diarias)
                        break

                    # O ideal seria validarmos antes de carregar na estrutura
                    self.vazoes_diarias['num'].append(self.linha[:3])
                    self.vazoes_diarias['nome'].append(self.linha[4:16])
                    self.vazoes_diarias['itp'].append(self.linha[19:20])
                    self.vazoes_diarias['di'].append(self.linha[24:26])
                    self.vazoes_diarias['hi'].append(self.linha[27:29])
                    self.vazoes_diarias['mi'].append(self.linha[30:31])
                    self.vazoes_diarias['df'].append(self.linha[32:34])
                    self.vazoes_diarias['hf'].append(self.linha[35:37])
                    self.vazoes_diarias['mf'].append(self.linha[38:39])
                    self.vazoes_diarias['vazao'].append(self.linha[44:53])

                if self.linha[:3].upper() == FIM_BLOCO:
                    self.dados['vazoes_diarias']['valores'] = self.vazoes_diarias
                    self.vazoes_diarias_df = pd.DataFrame(self.vazoes_diarias)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco

                if self.linha[:3].upper() == FIM_BLOCO:
                    self.dados['vazoes_diarias']['valores'] = self.vazoes_diarias
                    self.vazoes_diarias_df = pd.DataFrame(self.vazoes_diarias)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de dados de vazoes

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime registros de 1 a 7
                for _ in range(7):
                    f.write("\n")

                # Imprime Registros 8 e 9 que sao cabecalhos para o registro 10
                linha = self.dados['data_hora']['cabecalho']
                f.write(linha)

                # Imprime o registro 10
                linha = self.data_hora.strftime("%H %d %m %Y")
                f.write(linha)

                # Imprime Registros 11 e 12 que sao cabecalhos para o registro 13
                linha = self.dados['conf_gerais']['cabecalho']
                f.write(linha)

                # Imprime o registro 13
                linha = self.conf_gerais
                formato = self.dados['conf_gerais']['formato']
                f.write(formato.format(*linha))

                # Imprime Registros 14 a 16 que sao cabecalhos para os registros de 17 em diante
                linha = self.dados['vazoes_diarias']['cabecalho']
                f.write(linha)

                for idx, value in self.vazoes_diarias_df.iterrows():
                    linha = self.dados['vazoes_diarias']['formato'].format(**value)
                    f.write(linha)

                f.write(f"{FIM_BLOCO}\n")

        except Exception:
            raise