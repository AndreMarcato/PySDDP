# -*- coding: utf-8 -*-
from typing import Optional, IO
import pandas as pd
from PySDDP.dessem.script.templates.rstlpp import RstlppTemplate
import os

class Rstlpp(RstlppTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rstlpp do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.rstseg = dict()
        self.rstseg_df: pd.DataFrame()

        self.adicrs = dict()
        self.adicrs_df: pd.DataFrame()

        self.param = dict()
        self.param_df: pd.DataFrame()

        self.vparm = dict()
        self.vparm_df: pd.DataFrame()

        self.reslpp = dict()
        self.reslpp_df: pd.DataFrame()

        self._comentarios_: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as restrições de segurança - funções lineares por parte (LPP)

        Manual do Usuario III.22 Arquivo com as Restrições de Segurança - Funções lineares por Parte - LPP
        (RSTLPP.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios_ = list()
        self.rstlpp = list()
        # Dicionário para armazenar registros de definição:
        self.rstseg['mne'] = list()
        self.rstseg['cha1'] = list()
        self.rstseg['num'] = list()
        self.rstseg['flag'] = list()
        self.rstseg['dref'] = list()
        self.rstseg['chave'] = list()
        self.rstseg['ident'] = list()
        self.rstseg['descricao'] = list()

        # Dicionário para armazenar registros de adição de mais de uma restrição controlada:
        self.adicrs['mne'] = list()
        self.adicrs['cha1'] = list()
        self.adicrs['num'] = list()
        self.adicrs['flag'] = list()
        self.adicrs['dref'] = list()
        self.adicrs['chave'] = list()
        self.adicrs['ident'] = list()
        # self.adicrs['numident'] = list()
        self.adicrs['descricao'] = list()

        # Dicionário para armazenar registros de definição de parâmetros:
        self.param['param'] = list()
        self.param['num'] = list()
        self.param['chave'] = list()
        self.param['ident'] = list()

        # Dicionário para armazenar registros dos valores dos parâmetros para a escolha da LPP:
        self.vparm['vparm'] = list()
        self.vparm['num'] = list()
        self.vparm['numcurva'] = list()
        self.vparm['valinfpri'] = list()
        self.vparm['valsuppri'] = list()
        self.vparm['valinfseg'] = list()
        self.vparm['valsupseg'] = list()

        # Dicionário para armazenar registros de definição das LPP para cada valor de parâmetro definido nos registrios
        # III.22.1.4:
        self.reslpp['mne'] = list()
        self.reslpp['num'] = list()
        self.reslpp['p'] = list()
        self.reslpp['i'] = list()
        self.reslpp['coefangula'] = list()
        self.reslpp['coeflin'] = list()
        self.reslpp['2 contro'] = list()
        self.reslpp['3 contro'] = list()
        self.reslpp['4 contro'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:
                    self.next_line(f)
                    linha = self.linha.strip()
                    # Se a linha for comentario não faço nada e pula para proxima linha
                    if linha[0] == '&':
                        self.rstlpp.append(linha)
                        continue
                    mneumo = linha[:6].strip().lower()
                    self.rstlpp.append(linha[:6])
                    if linha[:6] == 'RSTSEG':

                        self.rstseg['mne'].append(self.linha[:6])
                        self.rstseg['cha1'].append(self.linha[7:14])
                        self.rstseg['num'].append(self.linha[15:19])
                        self.rstseg['flag'].append(self.linha[19:20])
                        self.rstseg['dref'].append(self.linha[20:24])
                        self.rstseg['chave'].append(self.linha[25:30])
                        self.rstseg['ident'].append(self.linha[31:36])
                        self.rstseg['descricao'].append(self.linha[37:79])

                        continue

                    elif linha[:6] == 'ADICRS':

                        self.adicrs['mne'].append(self.linha[:6])
                        # Campo 'cha1' não consta no manual, mas consta no arquivo: verificar!
                        self.adicrs['cha1'].append(self.linha[7:14])
                        # Campo 'num' não consta no manual, mas consta no arquivo: verificar!
                        self.adicrs['num'].append(self.linha[15:19])
                        self.adicrs['flag'].append(self.linha[19:20])
                        # Campo 'dref' não consta no manual, mas consta no arquivo: verificar!
                        self.adicrs['dref'].append(self.linha[20:24])
                        self.adicrs['chave'].append(self.linha[25:30])
                        self.adicrs['ident'].append(self.linha[31:36])
                        # Campo 'descricao' não consta no manual, mas consta no arquivo: verificar!
                        self.adicrs['descricao'].append(self.linha[37:77])

                        continue

                    elif linha[:5] == 'PARAM':

                        self.param['param'].append(self.linha[:5])
                        self.param['num'].append(self.linha[6:10])
                        self.param['chave'].append(self.linha[11:16])
                        self.param['ident'].append(self.linha[17:22])

                        continue

                    elif linha[:5] == 'VPARM':

                        self.vparm['vparm'].append(self.linha[:5])
                        self.vparm['num'].append(self.linha[6:10])
                        self.vparm['numcurva'].append(self.linha[11:13])
                        self.vparm['valinfpri'].append(self.linha[14:24])
                        self.vparm['valsuppri'].append(self.linha[25:35])
                        self.vparm['valinfseg'].append(self.linha[36:46])
                        self.vparm['valsupseg'].append(self.linha[47:57])

                        continue

                    elif linha[:6] == 'RESLPP':

                        self.reslpp['mne'].append(self.linha[:6])
                        self.reslpp['num'].append(self.linha[7:11])
                        self.reslpp['p'].append(self.linha[12:13])
                        self.reslpp['i'].append(self.linha[14:15])
                        self.reslpp['coefangula'].append(self.linha[16:26])
                        self.reslpp['coeflin'].append(self.linha[27:37])
                        self.reslpp['2 contro'].append(self.linha[38:48])
                        self.reslpp['3 contro'].append(self.linha[49:59])
                        self.reslpp['4 contro'].append(self.linha[60:70])

                        continue

                    elif linha[0] == '&':
                        self._comentarios_.append(self.linha)
                        continue

                    else:
                        raise NotImplementedError(f'A linha {self.linha} não corresponde aos registros do arquivo ou o '
                                                  f'fim da leitura foi concluído!')


        except Exception as err:
            if isinstance(err, StopIteration):

                # Verificar se é o fim do arquivo:

                # Armazena dados nos respectivos dicionários e os tranforma num DataFrame:
                self.blocorstseg['valor'] = self.rstseg
                self.rstseg_df = pd.DataFrame(self.rstseg)

                self.blocoadicrs['valor'] = self.adicrs
                self.adicrs_df = pd.DataFrame(self.adicrs)

                self.blocoparam['valor'] = self.param
                self.param_df = pd.DataFrame(self.param)

                self.blocovparm['valor'] = self.vparm
                self.vparm_df = pd.DataFrame(self.vparm)

                self.blocoreslpp['valor'] = self.reslpp
                self.reslpp_df = pd.DataFrame(self.reslpp)

                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para Escrita do arquivo com as restrições de segurança - funções lineares por parte (LPP)

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                num_linhas = len(self.rstlpp)
                i_rstseg = 0
                i_param = 0
                i_vparam = 0
                i_adicrs = 0
                i_reslpp = 0
                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.rstlpp[i]
                    verifica_comentario = linha[0] == '&'

                    if verifica_comentario:
                        f.write(self.rstlpp[i])
                        f.write("\n")
                        continue

                    if linha == 'RSTSEG':
                        self.rstseg_df['descricao'] = self.rstseg_df['descricao'].str.replace('\n', '')
                        # Escreve registros de definição:
                        for idx, value in self.rstseg_df.iterrows():
                            if idx == i_rstseg:
                                linha = self.blocorstseg['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_rstseg = i_rstseg + 1
                        continue
                    if linha == 'ADICRS':
                        self.adicrs_df['descricao'] = self.adicrs_df['descricao'].str.replace('\n','')
                        # Escreve registros de adição de mais de uma restrição controlada:
                        for idx, value in self.adicrs_df.iterrows():
                            if idx == i_adicrs:
                                linha = self.blocoadicrs['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_adicrs = i_adicrs + 1
                        continue
                    if linha == 'PARAM ':
                        self.param_df['ident'] = self.param_df['ident'].str.replace('\n','')
                        # Escreve registros de definição dos parâmetros:
                        for idx, value in self.param_df.iterrows():
                            if idx == i_param:
                                linha = self.blocoparam['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_param = i_param + 1
                        continue
                    if linha == 'VPARM ':
                        self.vparm_df['valsupseg'] = self.vparm_df['valsupseg'].str.replace('\n','')
                        self.vparm_df['valsuppri'] = self.vparm_df['valsuppri'].str.replace('\n', '')
                        # Escreve registros de definição dos valores dos parâmetros para a escolha da LPP:
                        for idx, value in self.vparm_df.iterrows():
                            if idx == i_vparam:
                                linha = self.blocovparm['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_vparam = i_vparam + 1
                        continue
                    if linha == 'RESLPP':
                        self.reslpp_df['4 contro'] = self.reslpp_df['4 contro'].str.replace('\n','')
                        self.reslpp_df['3 contro'] = self.reslpp_df['3 contro'].str.replace('\n', '')
                        self.reslpp_df['2 contro'] = self.reslpp_df['2 contro'].str.replace('\n', '')
                        self.reslpp_df['coeflin'] = self.reslpp_df['coeflin'].str.replace('\n', '')
                # Escreve registros de definição das LPP para cada valor de parâmetro definido nos resgitros III.22.1.4:
                        for idx, value in self.reslpp_df.iterrows():
                            if idx == i_reslpp:
                                linha = self.blocoreslpp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_reslpp = i_reslpp + 1
                        continue

        except Exception:
            raise
