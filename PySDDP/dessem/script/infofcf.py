# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd

from PySDDP.dessem.script.templates.infofcf import InfofcfTemplate

COMENTARIO = '&'
CABECALHO = 'X'


class Infofcf(InfofcfTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Infofcf do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.mapfcf_sisgnl = dict()
        self.mapfcf_durpat = dict()
        self.fcffix_usit = dict()
        self.mapfcf_tviag = dict()
        self.mapfcf_cgtmin = dict()
        self.mapfcf_sisgnl_df: pd.DataFrame()
        self.mapfcf_durpat_df: pd.DataFrame()
        self.fcffix_usit_df: pd.DataFrame()
        self.mapfcf_tviag_df: pd.DataFrame()
        self.mapfcf_cgtmin_df: pd.DataFrame()

        self.infofcf = None
        self._comentarios_ = None



    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as informações adicionais para os Cortes de Benders

        Manual do Usuario III.2 Arquivo contendo informações adicionais para os Cortes de Benders(INFOFCF.DEC).
        Neste arquivo são fornecidas informações sobre as variáveis de estado dessa função cujos valores não são
        decididos pelo modelo DESSEM. Portanto, os termos referentes a essas variáveis devem ser abatidos do termo
        independente da Função de Custo Futuro.

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        # Listas referentes a MAPFCF SISGNL
        self.mapfcf_sisgnl['mneumo'] = list()
        self.mapfcf_sisgnl['ind'] = list()
        self.mapfcf_sisgnl['num'] = list()
        self.mapfcf_sisgnl['lag'] = list()
        self.mapfcf_sisgnl['patamares'] = list()


        # Listas referentes a MAPFCF DURPAT
        self.mapfcf_durpat['mneumo'] = list()
        self.mapfcf_durpat['lag'] = list()
        self.mapfcf_durpat['patamar'] = list()
        self.mapfcf_durpat['duracao'] = list()

        # Listas referentes a FCFFIX USIT
        self.fcffix_usit['mneumo'] = list()
        self.fcffix_usit['num_ent'] = list()
        self.fcffix_usit['variavel'] = list()
        self.fcffix_usit['lag'] = list()
        self.fcffix_usit['patamar'] = list()
        self.fcffix_usit['valor'] = list()
        self.fcffix_usit['comentario'] = list()

        # Listas referentes a MAPFCF TVIAG
        self.mapfcf_tviag['mneumo'] = list()
        self.mapfcf_tviag['ind'] = list()
        self.mapfcf_tviag['num'] = list()

        # Listas referentes a MAPFCF CGTMIN
        self.mapfcf_cgtmin['mneumo'] = list()
        self.mapfcf_cgtmin['custo'] = list()

        self.infofcf = list()
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
                        self.infofcf.append(linha)

                        continue
                    if linha[0] == CABECALHO:
                        self.infofcf.append(linha)

                        continue
                    mneumo = linha[:14].strip().lower()

                    self.infofcf.append(linha[:14])

                    # Leitura dos dados de acordo com o mneumo correspondente

                    if mneumo == 'mapfcf  sisgnl':
                        self.mapfcf_sisgnl['mneumo'].append(self.linha[:14])
                        self.mapfcf_sisgnl['ind'].append(self.linha[14:18])
                        self.mapfcf_sisgnl['num'].append(self.linha[19:22])
                        self.mapfcf_sisgnl['lag'].append(self.linha[23:26])
                        self.mapfcf_sisgnl['patamares'].append(self.linha[27:30])

                        self.dados['mapfcf_sisgnl']['valores'] = self.mapfcf_sisgnl
                        self.mapfcf_sisgnl_df = pd.DataFrame(self.mapfcf_sisgnl)

                        continue
                    if mneumo == 'mapfcf  durpat':
                        self.mapfcf_durpat['mneumo'].append(self.linha[:14])
                        self.mapfcf_durpat['lag'].append(self.linha[15:18])
                        self.mapfcf_durpat['patamar'].append(self.linha[19:22])
                        self.mapfcf_durpat['duracao'].append(self.linha[24:34])

                        self.dados['mapfcf_durpat']['valores'] = self.mapfcf_durpat
                        self.mapfcf_durpat_df = pd.DataFrame(self.mapfcf_durpat)

                        continue
                    if mneumo == 'fcffix usit':
                        self.fcffix_usit['mneumo'].append(self.linha[:13])
                        self.fcffix_usit['num_ent'].append(self.linha[14:17])
                        self.fcffix_usit['variavel'].append(self.linha[18:24])
                        self.fcffix_usit['lag'].append(self.linha[25:28])
                        self.fcffix_usit['patamar'].append(self.linha[29:32])
                        self.fcffix_usit['valor'].append(self.linha[33:43])
                        self.fcffix_usit['comentario'].append(self.linha[44:64])

                        self.dados['fcffix_usit']['valores'] = self.fcffix_usit
                        self.fcffix_usit_df = pd.DataFrame(self.fcffix_usit)

                        continue
                    if mneumo == 'mapfcf  tviag':
                        self.mapfcf_tviag['mneumo'].append(self.linha[:14])
                        self.mapfcf_tviag['ind'].append(self.linha[15:19])
                        self.mapfcf_tviag['num'].append(self.linha[20:23])

                        self.dados['mapfcf_tviag']['valores'] = self.mapfcf_tviag
                        self.mapfcf_tviag_df = pd.DataFrame(self.mapfcf_tviag)

                        continue
                    if mneumo == 'mapfcf  cgtmin':
                        self.mapfcf_cgtmin['mneumo'].append(self.linha[:14])
                        self.mapfcf_cgtmin['custo'].append(self.linha[16:31])

                        self.dados['mapfcf_cgtmin']['valores'] = self.mapfcf_cgtmin
                        self.mapfcf_cgtmin_df = pd.DataFrame(self.mapfcf_cgtmin)

                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['infofcf']['valores'] = self.infofcf
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo com as informações adicionais para os Cortes de Benders

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Inicializa contadores para o loop
                num_linhas = len(self.infofcf)
                i_sisgnl = 0
                i_durpat = 0
                i_fcffix = 0
                i_tviag = 0
                i_cgtmin = 0

                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.infofcf[i]
                    verifica_comentario = linha[0] == COMENTARIO
                    verifica_cabecalho = linha[0] == CABECALHO

                    if verifica_comentario or verifica_cabecalho:
                        f.write(self.infofcf[i])
                        f.write("\n")
                        continue

                    if linha == 'MAPFCF  SISGNL':

                        for idx, value in self.mapfcf_sisgnl_df.iterrows():
                            if idx == i_sisgnl:
                                linha_sisgnl = self.dados['mapfcf_sisgnl']['formato'].format(**value)
                                f.write(linha_sisgnl)
                                continue

                        i_sisgnl = i_sisgnl + 1
                        continue

                    if linha == 'MAPFCF  DURPAT':
                        for idx, value in self.mapfcf_durpat_df.iterrows():
                            if idx == i_durpat:
                                linha_durpat = self.dados['mapfcf_durpat']['formato'].format(**value)
                                f.write(linha_durpat)
                                continue
                        i_durpat = i_durpat + 1
                        continue

                    if linha == 'FCFFIX USIT   ':
                        for idx, value in self.fcffix_usit_df.iterrows():
                            if idx == i_fcffix:
                                linha_fcffix = self.dados['fcffix_usit']['formato'].format(**value)
                                f.write(linha_fcffix)
                                continue


                        i_fcffix = i_fcffix + 1
                        continue

                    if linha == 'MAPFCF  TVIAG ':
                        for idx, value in self.mapfcf_tviag_df.iterrows():
                            if idx == i_tviag:
                                linha_tviag = self.dados['mapfcf_tviag']['formato'].format(**value)
                                f.write(linha_tviag)
                                continue
                        i_tviag = i_tviag + 1
                        continue

                    if linha == 'MAPFCF  CGTMIN ':
                        for idx, value in self.mapfcf_cgtmin_df.iterrows():
                            if idx == i_cgtmin:
                                linha_cgtmin = self.dados['mapfcf_cgtmin']['formato'].format(**value)
                                f.write(linha_cgtmin)
                                continue
                        i_cgtmin = i_cgtmin + 1
                        continue

        except Exception:
            raise