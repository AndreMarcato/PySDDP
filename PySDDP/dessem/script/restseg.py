# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd

from PySDDP.dessem.script.templates.restseg import RestsegTemplate

COMENTARIO = '&'
CABECALHO = 'X'


class Restseg(RestsegTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Restseg do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.tabseg_indice = dict()
        self.tabseg_tabela = dict()
        self.tabseg_limite = dict()
        self.tabseg_celula = dict()
        self.tabseg_indice_df: pd.DataFrame()
        self.tabseg_tabela_df: pd.DataFrame()
        self.tabseg_limite_df: pd.DataFrame()
        self.tabseg_celula_df: pd.DataFrame()

        self.restseg = None
        self._comentarios_ = None


    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as restricoes de seguranca representadas por tabelas

        Manual do Usuario III.2 Arquivo contendo informações sobre os limites de segurança para a rede eletrica
        fornecidos por tabelas(RESTSEG.XXX).

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        # Listas referentes a TABSEG INDICE
        self.tabseg_indice['mneumo'] = list()
        self.tabseg_indice['num'] = list()
        self.tabseg_indice['descricao'] = list()


        # Listas referentes a TABSEG TABELA
        self.tabseg_tabela['mneumo'] = list()
        self.tabseg_tabela['num1'] = list()
        self.tabseg_tabela['tipo1'] = list()
        self.tabseg_tabela['tipo2'] = list()
        self.tabseg_tabela['num2'] = list()
        self.tabseg_tabela['carg'] = list()

        # Listas referentes a TABSEG LIMITE
        self.tabseg_limite['mneumo'] = list()
        self.tabseg_limite['num'] = list()
        self.tabseg_limite['var_parm_1'] = list()
        self.tabseg_limite['var_parm_2'] = list()
        self.tabseg_limite['var_parm_3'] = list()

        # Listas referentes a TABSEG CELULA
        self.tabseg_celula['mneumo'] = list()
        self.tabseg_celula['num'] = list()
        self.tabseg_celula['limite'] = list()
        self.tabseg_celula['f'] = list()
        self.tabseg_celula['par_1_inf'] = list()
        self.tabseg_celula['par_1_sup'] = list()
        self.tabseg_celula['par_2_inf'] = list()
        self.tabseg_celula['par_2_sup'] = list()
        self.tabseg_celula['par_3_inf'] = list()
        self.tabseg_celula['par_3_sup'] = list()

        self.restseg = list()
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
                        self.restseg.append(linha)

                        continue
                    if linha[0] == CABECALHO:
                        self.restseg.append(linha)

                        continue
                    mneumo = linha[:13].strip().lower()

                    self.restseg.append(linha[:13])

                    # Leitura dos dados de acordo com o mneumo correspondente

                    if mneumo == 'tabseg indice':
                        self.tabseg_indice['mneumo'].append(self.linha[:13])
                        self.tabseg_indice['num'].append(self.linha[14:19])
                        self.tabseg_indice['descricao'].append(self.linha[20:80])


                        self.dados['tabseg_indice']['valores'] = self.tabseg_indice
                        self.tabseg_indice_df = pd.DataFrame(self.tabseg_indice)

                        continue
                    if mneumo == 'tabseg tabela':
                        self.tabseg_tabela['mneumo'].append(self.linha[:13])
                        self.tabseg_tabela['num1'].append(self.linha[14:19])
                        self.tabseg_tabela['tipo1'].append(self.linha[20:26])
                        self.tabseg_tabela['tipo2'].append(self.linha[27:33])
                        self.tabseg_tabela['num2'].append(self.linha[34:39])
                        self.tabseg_tabela['carg'].append(self.linha[40:45])


                        self.dados['tabseg_tabela']['valores'] = self.tabseg_tabela
                        self.tabseg_tabela_df = pd.DataFrame(self.tabseg_tabela)

                        continue
                    if mneumo == 'tabseg limite':
                        self.tabseg_limite['mneumo'].append(self.linha[:13])
                        self.tabseg_limite['num'].append(self.linha[14:19])
                        self.tabseg_limite['var_parm_1'].append(self.linha[20:30])
                        self.tabseg_limite['var_parm_2'].append(self.linha[31:41])
                        self.tabseg_limite['var_parm_3'].append(self.linha[42:52])

                        self.dados['tabseg_limite']['valores'] = self.tabseg_limite
                        self.tabseg_limite_df = pd.DataFrame(self.tabseg_limite)

                        continue
                    if mneumo == 'tabseg celula':
                        self.tabseg_celula['mneumo'].append(self.linha[:13])
                        self.tabseg_celula['num'].append(self.linha[14:19])
                        self.tabseg_celula['limite'].append(self.linha[20:30])
                        self.tabseg_celula['f'].append(self.linha[31:32])
                        self.tabseg_celula['par_1_inf'].append(self.linha[36:46])
                        self.tabseg_celula['par_1_sup'].append(self.linha[48:58])
                        self.tabseg_celula['par_2_inf'].append(self.linha[60:70])
                        self.tabseg_celula['par_2_sup'].append(self.linha[72:82])
                        self.tabseg_celula['par_3_inf'].append(self.linha[84:94])
                        self.tabseg_celula['par_3_sup'].append(self.linha[96:106])

                        self.dados['tabseg_celula']['valores'] = self.tabseg_celula
                        self.tabseg_celula_df = pd.DataFrame(self.tabseg_celula)

                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['restseg']['valores'] = self.restseg
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo com as restrições de segurança representadas por tabelas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Inicializa contadores para o loop
                num_linhas = len(self.restseg)
                i_ind = 0
                i_tab = 0
                i_lim = 0
                i_cel = 0

                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.restseg[i]
                    verifica_comentario = linha[0] == COMENTARIO
                    verifica_cabecalho = linha[0] == CABECALHO

                    if verifica_comentario or verifica_cabecalho:
                        f.write(self.restseg[i])
                        f.write("\n")
                        continue

                    if linha == 'TABSEG INDICE':

                        for idx, value in self.tabseg_indice_df.iterrows():
                            if idx == i_ind:
                                linha_ind = self.dados['tabseg_indice']['formato'].format(**value)
                                f.write(linha_ind)
                                continue

                        i_ind = i_ind + 1
                        continue

                    if linha == 'TABSEG TABELA':
                        # Tratando caractere '\n'
                        self.tabseg_tabela_df['carg'] = self.tabseg_tabela_df['carg'].str.replace('\n', '')

                        for idx, value in self.tabseg_tabela_df.iterrows():
                            if idx == i_tab:
                                linha_tab = self.dados['tabseg_tabela']['formato'].format(**value)
                                f.write(linha_tab)
                                continue
                        i_tab = i_tab + 1
                        continue

                    if linha == 'TABSEG LIMITE':
                        # Tratando o caractere "\n":
                        self.tabseg_limite_df['var_parm_1'] = self.tabseg_limite_df['var_parm_1'].str.replace('\n', '')
                        self.tabseg_limite_df['var_parm_2'] = self.tabseg_limite_df['var_parm_2'].str.replace('\n', '')
                        self.tabseg_limite_df['var_parm_3'] = self.tabseg_limite_df['var_parm_3'].str.replace('\n', '')
                        for idx, value in self.tabseg_limite_df.iterrows():
                            if idx == i_lim:

                                linha_lim = self.dados['tabseg_limite']['formato'].format(**value)
                                f.write(linha_lim)

                                continue


                        i_lim = i_lim + 1
                        continue

                    if linha == 'TABSEG CELULA':
                        # Tratando caractere '\n'
                        self.tabseg_celula_df['par_1_inf'] = self.tabseg_celula_df['par_1_inf'].str.replace('\n', '')
                        self.tabseg_celula_df['par_1_sup'] = self.tabseg_celula_df['par_1_sup'].str.replace('\n', '')
                        self.tabseg_celula_df['par_2_inf'] = self.tabseg_celula_df['par_2_sup'].str.replace('\n', '')
                        self.tabseg_celula_df['par_2_sup'] = self.tabseg_celula_df['par_2_sup'].str.replace('\n', '')
                        self.tabseg_celula_df['par_3_inf'] = self.tabseg_celula_df['par_3_inf'].str.replace('\n', '')
                        self.tabseg_celula_df['par_3_sup'] = self.tabseg_celula_df['par_3_sup'].str.replace('\n', '')

                        for idx, value in self.tabseg_celula_df.iterrows():
                            if idx == i_cel:
                                linha_cel = self.dados['tabseg_celula']['formato'].format(**value)
                                f.write(linha_cel)
                                continue
                        i_cel = i_cel + 1
                        continue

        except Exception:
            raise