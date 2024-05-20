# -*- coding: utf-8 -*-
from abc import ABC
from typing import Optional, IO

import pandas as pd
import os

from PySDDP.dessem.script.templates.operut import OperutTemplate

INIT = 'INIT'
OPER = 'OPER'
FIM = 'FIM'
COMENTARIO = '&'


class Operut(OperutTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Operut do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.condicoes_iniciais = dict()
        self.condicoes_iniciais_df: pd.DataFrame()

        self.limites_condicoes = dict()
        self.limites_condicoes_df: pd.DataFrame()

        self._comentarios_: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de dados operativos para as unidades termoelétricas

        Manual do Usuario III.10 Arquivo com as Condições Operativas das Unidades Geradoras Termoelétricas (OPERUT.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios_ = list()

        # Dicionário para armazenar dados do bloco "INIT"
        self.condicoes_iniciais['us'] = list()
        self.condicoes_iniciais['nome'] = list()
        self.condicoes_iniciais['ug'] = list()
        self.condicoes_iniciais['st'] = list()
        self.condicoes_iniciais['GerInic'] = list()
        self.condicoes_iniciais['tempo'] = list()
        self.condicoes_iniciais['MH'] = list()
        self.condicoes_iniciais['A/D'] = list()
        self.condicoes_iniciais['T'] = list()
        self.condicoes_iniciais['TITULINFLX'] = list()

        # Dicionário para armazenar dados do bloco "OPER"
        self.limites_condicoes['us'] = list()
        self.limites_condicoes['nome'] = list()
        self.limites_condicoes['un'] = list()
        self.limites_condicoes['di'] = list()
        self.limites_condicoes['hi'] = list()
        self.limites_condicoes['mi'] = list()
        self.limites_condicoes['df'] = list()
        self.limites_condicoes['hf'] = list()
        self.limites_condicoes['mf'] = list()
        self.limites_condicoes['Gmin'] = list()
        self.limites_condicoes['Gmax'] = list()
        self.limites_condicoes['Custo'] = list()

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

                    # Leitura do bloco "INIT"
                    elif linha == INIT:

                        self.next_line(f)
                        linha = self.linha.strip()

                        while linha[:3] != FIM:

                            # Consideração caso haja comentário no meio do bloco
                            if linha[0] == COMENTARIO:
                                self._comentarios_.append(linha)
                                self.next_line(f)
                                linha = self.linha.strip()

                            else:
                                self.condicoes_iniciais['us'].append(self.linha[:3])
                                self.condicoes_iniciais['nome'].append(self.linha[4:17])
                                self.condicoes_iniciais['ug'].append(self.linha[18:21])
                                self.condicoes_iniciais['st'].append(self.linha[24:26])
                                self.condicoes_iniciais['GerInic'].append(self.linha[29:39])
                                self.condicoes_iniciais['tempo'].append(self.linha[41:46])
                                self.condicoes_iniciais['MH'].append(self.linha[48:49])
                                self.condicoes_iniciais['A/D'].append(self.linha[51:52])
                                self.condicoes_iniciais['T'].append(self.linha[54:55])
                                self.condicoes_iniciais['TITULINFLX'].append(self.linha[57:67])
                                self.next_line(f)
                                linha = self.linha.strip()

                    # Leitura do bloco "OPER"
                    elif linha[:4] == OPER:

                        self.next_line(f)
                        linha = self.linha.strip()

                        while linha[:3] != FIM:

                            # Consideração caso haja comentário no meio do bloco
                            if linha[0] == COMENTARIO:
                                self._comentarios_.append(linha)
                                self.next_line(f)
                                linha = self.linha.strip()

                            else:
                                self.limites_condicoes['us'].append(self.linha[:3])
                                self.limites_condicoes['nome'].append(self.linha[4:16])
                                self.limites_condicoes['un'].append(self.linha[16:19])
                                self.limites_condicoes['di'].append(self.linha[20:22])
                                self.limites_condicoes['hi'].append(self.linha[23:25])
                                self.limites_condicoes['mi'].append(self.linha[26:27])
                                self.limites_condicoes['df'].append(self.linha[28:30])
                                self.limites_condicoes['hf'].append(self.linha[31:33])
                                self.limites_condicoes['mf'].append(self.linha[34:35])
                                self.limites_condicoes['Gmin'].append(self.linha[36:46])
                                self.limites_condicoes['Gmax'].append(self.linha[46:56])
                                self.limites_condicoes['Custo'].append(self.linha[56:66])
                                self.next_line(f)
                                linha = self.linha.strip()

                        self.bloco_init['valor'] = self.condicoes_iniciais
                        self.condicoes_iniciais_df = pd.DataFrame(self.condicoes_iniciais)
                        self.bloco_oper['valor'] = self.limites_condicoes
                        self.limites_condicoes_df = pd.DataFrame(self.limites_condicoes)

                        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                        break

                    else:
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                if self.linha[:3].upper() == FIM:
                    self.bloco_init['valor'] = self.condicoes_iniciais
                    self.condicoes_iniciais_df = pd.DataFrame(self.condicoes_iniciais)
                    self.bloco_oper['valor'] = self.limites_condicoes
                    self.limites_condicoes_df = pd.DataFrame(self.limites_condicoes)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrita do arquivo de dados operativos para as unidades termoelétricas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Bloco INIT
                # Imprime Descrição
                linha = self.bloco_init['descricao']
                f.write(linha)

                # Imprime Cabeçalho
                linha = self.bloco_init['cabecalho']
                f.write(linha)

                for idx, value in self.condicoes_iniciais_df.iterrows():
                    linha = self.bloco_init['formato'].format(**value)
                    f.write(linha)

                # Imprime Mnemônico FIM
                linha = FIM
                f.write(linha)
                f.write('\n')

                # Bloco OPER
                # Imprime Descrição
                linha = self.bloco_oper['descricao']
                f.write(linha)

                # Imprime Cabeçalho
                linha = self.bloco_oper['cabecalho']
                f.write(linha)

                for idx, value in self.limites_condicoes_df.iterrows():
                    linha = self.bloco_oper['formato'].format(**value)
                    f.write(linha)

                # Imprime Mnemônico FIM
                linha = FIM
                f.write(linha)

        except Exception:
            raise
