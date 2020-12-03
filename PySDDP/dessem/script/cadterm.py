# -*- coding: utf-8 -*-
import os
from typing import IO
import pandas as pd


from PySDDP.dessem.script.templates.cadterm import CadTermTemplate

COMENTARIO = '&'


class CadTerm(CadTermTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo CadTerm do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.cadusit = dict()
        self.cadunidt = dict()
        self.cadconf = dict()
        self.cadmin = dict()
        self.cadusit_df: pd.DataFrame()
        self.cadunidt_df: pd.DataFrame()
        self.cadconf_df: pd.DataFrame()
        self.cadmin_df: pd.DataFrame()

        self.termo = None
        self._comentarios_ = None



    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de cadastro das usinas termoeletricas

        Manual do Usuario III.2 Arquivo contendo informações sobre os dados fisicos das usinas termoeletricas (TERM.DAT).
        Este arquivo é composto por dois tipos de registros: o primeiro contém informações sobre o início de
        comissionamento e número de unidades de cada usina termoelétrica, enquanto o segundo tipo de registro fornece as
        características físicas de cada unidade geradora das usinas.

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        # Listas referentes a CADUSIT
        self.cadusit['mneumo'] = list()
        self.cadusit['num_usi'] = list()
        self.cadusit['nome'] = list()
        self.cadusit['num_subsistema'] = list()
        self.cadusit['ano'] = list()
        self.cadusit['mes'] = list()
        self.cadusit['di'] = list()
        self.cadusit['hr'] = list()
        self.cadusit['m'] = list()
        self.cadusit['num_ger'] = list()

        # Listas referentes a CADUNIDT
        self.cadunidt['mneumo'] = list()
        self.cadunidt['num_usi'] = list()
        self.cadunidt['ind_ger'] = list()
        self.cadunidt['ano'] = list()
        self.cadunidt['mes'] = list()
        self.cadunidt['di'] = list()
        self.cadunidt['hr'] = list()
        self.cadunidt['m'] = list()
        self.cadunidt['pot'] = list()
        self.cadunidt['ger_min'] = list()
        self.cadunidt['temp_on'] = list()
        self.cadunidt['temp_off'] = list()
        self.cadunidt['custo_frio'] = list()
        self.cadunidt['custo_desl'] = list()
        self.cadunidt['ramp_tom'] = list()
        self.cadunidt['ramp_alivio'] = list()
        self.cadunidt['flag_rest'] = list()
        self.cadunidt['num_oscilacao'] = list()
        self.cadunidt['flag_equiv'] = list()
        self.cadunidt['ramp_trans'] = list()

        # Listas referentes a CADCONF
        self.cadconf['mneumo'] = list()
        self.cadconf['num_usi'] = list()
        self.cadconf['ind_equi'] = list()
        self.cadconf['ind_ger'] = list()

        # Listas referentes a CADMIN
        self.cadmin['mneumo'] = list()
        self.cadmin['num_usi'] = list()
        self.cadmin['ind_equi'] = list()
        self.cadmin['ind_ger'] = list()

        self.termo = list()
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
                        self.termo.append(linha)

                        continue
                    mneumo = linha[:8].strip().lower()

                    self.termo.append(linha[:8])

                    # Leitura dos dados de acordo com o mneumo correspondente

                    if mneumo == 'cadusit':
                        self.cadusit['mneumo'].append(self.linha[:7])
                        self.cadusit['num_usi'].append(self.linha[8:11])
                        self.cadusit['nome'].append(self.linha[12:24])
                        self.cadusit['num_subsistema'].append(self.linha[25:27])
                        self.cadusit['ano'].append(self.linha[28:32])
                        self.cadusit['mes'].append(self.linha[33:35])
                        self.cadusit['di'].append(self.linha[36:38])
                        self.cadusit['hr'].append(self.linha[39:41])
                        self.cadusit['m'].append(self.linha[42:43])
                        self.cadusit['num_ger'].append(self.linha[45:48])

                        self.dados['cadusit']['valores'] = self.cadusit
                        self.cadusit_df = pd.DataFrame(self.cadusit)

                        continue
                    if mneumo == 'cadunidt':
                        self.cadunidt['mneumo'].append(self.linha[:8])
                        self.cadunidt['num_usi'].append(self.linha[9:12])
                        self.cadunidt['ind_ger'].append(self.linha[12:15])
                        self.cadunidt['ano'].append(self.linha[16:20])
                        self.cadunidt['mes'].append(self.linha[21:23])
                        self.cadunidt['di'].append(self.linha[24:26])
                        self.cadunidt['hr'].append(self.linha[27:29])
                        self.cadunidt['m'].append(self.linha[30:31])
                        self.cadunidt['pot'].append(self.linha[33:43])
                        self.cadunidt['ger_min'].append(self.linha[44:54])
                        self.cadunidt['temp_on'].append(self.linha[55:60])
                        self.cadunidt['temp_off'].append(self.linha[61:66])
                        self.cadunidt['custo_frio'].append(self.linha[67:77])
                        self.cadunidt['custo_desl'].append(self.linha[89:99])
                        self.cadunidt['ramp_tom'].append(self.linha[100:110])
                        self.cadunidt['ramp_alivio'].append(self.linha[111:121])
                        self.cadunidt['flag_rest'].append(self.linha[122:123])
                        self.cadunidt['num_oscilacao'].append(self.linha[124:126])
                        self.cadunidt['flag_equiv'].append(self.linha[127:130])
                        self.cadunidt['ramp_trans'].append(self.linha[131:141])

                        self.dados['cadunidt']['valores'] = self.cadunidt
                        self.cadunidt_df = pd.DataFrame(self.cadunidt)

                        continue
                    if mneumo == 'cadconf':
                        self.cadconf['mneumo'].append(self.linha[:7])
                        self.cadconf['num_usi'].append(self.linha[8:11])
                        self.cadconf['ind_equi'].append(self.linha[12:15])
                        self.cadconf['ind_ger'].append(self.linha[16:19])

                        self.dados['cadconf']['valores'] = self.cadconf
                        self.cadconf_df = pd.DataFrame(self.cadconf)

                        continue
                    if mneumo == 'cadmin':
                        self.cadmin['mneumo'].append(self.linha[:6])
                        self.cadmin['num_usi'].append(self.linha[8:11])
                        self.cadmin['ind_equi'].append(self.linha[12:15])
                        self.cadmin['ind_ger'].append(self.linha[16:19])

                        self.dados['cadmin']['valores'] = self.cadmin
                        self.cadmin_df = pd.DataFrame(self.cadmin)

                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                self.dados['termo']['valores'] = self.termo
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de cadastro das usinas termoeletricas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Inicializa contadores para o loop
                num_linhas = len(self.termo)
                i_sit = 0
                i_nidt = 0
                i_conf = 0
                i_min = 0


                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.termo[i]
                    verifica_comentario = linha[0] == COMENTARIO

                    if verifica_comentario:
                        f.write(self.termo[i])
                        f.write("\n")
                        continue

                    if linha == 'CADUSIT ':

                        for idx, value in self.cadusit_df.iterrows():
                            if idx == i_sit:
                                linha_sit = self.dados['cadusit']['formato'].format(**value)
                                f.write(linha_sit)
                                continue

                        i_sit = i_sit + 1
                        continue

                    if linha == 'CADUNIDT':
                        self.cadunidt_df['temp_off'] = self.cadunidt_df['temp_off'].str.replace('\n', '')
                        self.cadunidt_df['custo_frio'] = self.cadunidt_df['custo_frio'].str.replace('\n', '')
                        self.cadunidt_df['custo_desl'] = self.cadunidt_df['custo_desl'].str.replace('\n', '')
                        self.cadunidt_df['ramp_tom'] = self.cadunidt_df['ramp_tom'].str.replace('\n', '')
                        self.cadunidt_df['ramp_alivio'] = self.cadunidt_df['ramp_alivio'].str.replace('\n', '')
                        self.cadunidt_df['flag_rest'] = self.cadunidt_df['flag_rest'].str.replace('\n', '')
                        self.cadunidt_df['num_oscilacao'] = self.cadunidt_df['num_oscilacao'].str.replace('\n', '')
                        self.cadunidt_df['flag_equiv'] = self.cadunidt_df['flag_equiv'].str.replace('\n', '')
                        self.cadunidt_df['ramp_trans'] = self.cadunidt_df['ramp_trans'].str.replace('\n', '')

                        for idx, value in self.cadunidt_df.iterrows():
                            if idx == i_nidt:
                                linha_nidt = self.dados['cadunidt']['formato'].format(**value)
                                if len(linha_nidt) <= 139:
                                    linha_nidt = self.dados['cadunidt']['formato'].format(**value)
                                    f.write(linha_nidt)
                                else:
                                    f.write(linha_nidt)
                                continue
                        i_nidt = i_nidt + 1
                        continue

                    if linha == 'CADCONF ':
                        for idx, value in self.cadconf_df.iterrows():
                            if idx == i_conf:
                                linha_conf = self.dados['cadconf']['formato'].format(**value)
                                f.write(linha_conf)
                                continue
                        i_conf = i_conf + 1
                        continue

                    if linha == 'CADMIN  ':
                        for idx, value in self.cadmin_df.iterrows():
                            if idx == i_min:
                                linha_min = self.dados['cadmin']['formato'].format(**value)
                                f.write(linha_min)
                                continue
                        i_min = i_min + 1
                        continue

        except Exception:
            raise