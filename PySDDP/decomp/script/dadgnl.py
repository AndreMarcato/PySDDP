# -*- coding: utf-8 -*-
import warnings
from typing import IO

import os
import numpy as np
import pandas as pd

from PySDDP.decomp.script.templates.dadgnl import DadGnlTemplate

comment = '&'


class DadGnl(DadGnlTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo DadGnl do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):

        super().__init__()

        self.registro_tg = dict()
        self.registro_gs = dict()
        self.registro_nl = dict()
        self.registro_gl = dict()

        self._valid_lags = [1, 2]

        self.list_of_comments = None
        
        self._usi_term_gnl = None
        
    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo dadgnl.xxx.
        Manual do Usuário 30.1: Arquivo dadgnl.xxx. Este arquivo contem os dados das usinas termicas GNL.
        Os comentarios podem ser livremente incluidos desde que precedidos por "&".
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.registro_tg['id'] = list()
        self.registro_tg['cod_ute'] = list()
        self.registro_tg['id_subsist'] = list()
        self.registro_tg['nome_ute'] = list()
        self.registro_tg['id_est'] = list()
        self.registro_tg['ger_min_pat1'] = list()
        self.registro_tg['cap_min_pat1'] = list()
        self.registro_tg['cvu_pat1'] = list()
        self.registro_tg['ger_min_pat2'] = list()
        self.registro_tg['cap_min_pat2'] = list()
        self.registro_tg['cvu_pat2'] = list()
        self.registro_tg['ger_min_pat3'] = list()
        self.registro_tg['cap_min_pat3'] = list()
        self.registro_tg['cvu_pat3'] = list()

        self.registro_gs['id'] = list()
        self.registro_gs['id_mes'] = list()
        self.registro_gs['num_interv'] = list()

        self.registro_nl['id'] = list()
        self.registro_nl['cod_ute'] = list()
        self.registro_nl['id_subsist'] = list()
        self.registro_nl['lag'] = list()

        self.registro_gl['id'] = list()
        self.registro_gl['cod_ute'] = list()
        self.registro_gl['id_subsist'] = list()
        self.registro_gl['sem'] = list()
        self.registro_gl['ger_pat1'] = list()
        self.registro_gl['dur_pat1'] = list()
        self.registro_gl['ger_pat2'] = list()
        self.registro_gl['dur_pat2'] = list()
        self.registro_gl['ger_pat3'] = list()
        self.registro_gl['dur_pat3'] = list()
        self.registro_gl['dia'] = list()
        self.registro_gl['mes'] = list()
        self.registro_gl['ano'] = list()

        self.list_of_comments = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:

                    self.next_line(f)

                    if self.linha[0] == comment:
                        self.list_of_comments.append(self.linha)
                        continue

                    elif self.linha[:2].upper() == 'TG':
                        self.registro_tg['id'].append(self.linha[:2])
                        self.registro_tg['cod_ute'].append(self.linha[4:7])
                        self.registro_tg['id_subsist'].append(self.linha[9:11])
                        self.registro_tg['nome_ute'].append(self.linha[14:24])
                        self.registro_tg['id_est'].append(self.linha[24:26])
                        self.registro_tg['ger_min_pat1'].append(self.linha[29:34])
                        self.registro_tg['cap_min_pat1'].append(self.linha[34:39])
                        self.registro_tg['cvu_pat1'].append(self.linha[39:49])
                        self.registro_tg['ger_min_pat2'].append(self.linha[49:54])
                        self.registro_tg['cap_min_pat2'].append(self.linha[54:59])
                        self.registro_tg['cvu_pat2'].append(self.linha[59:69])
                        self.registro_tg['ger_min_pat3'].append(self.linha[69:74])
                        self.registro_tg['cap_min_pat3'].append(self.linha[74:79])
                        self.registro_tg['cvu_pat3'].append(self.linha[79:89])
                        continue

                    elif self.linha[:2].upper() == 'GS':
                        self.registro_gs['id'].append(self.linha[:2])
                        self.registro_gs['id_mes'].append(self.linha[4:6])
                        self.registro_gs['num_interv'].append(self.linha[9])
                        continue

                    elif self.linha[:2].upper() == 'NL':
                        self.registro_nl['id'].append(self.linha[:2])
                        self.registro_nl['cod_ute'].append(self.linha[4:7])
                        self.registro_nl['id_subsist'].append(self.linha[9:11])
                        self.registro_nl['lag'].append(self.linha[14])
                        continue

                    elif self.linha[:2].upper() == 'GL':
                        self.registro_gl['id'].append(self.linha[:2])
                        self.registro_gl['cod_ute'].append(self.linha[4:7])
                        self.registro_gl['id_subsist'].append(self.linha[9:11])
                        self.registro_gl['sem'].append(self.linha[14:16])
                        self.registro_gl['ger_pat1'].append(self.linha[19:29])
                        self.registro_gl['dur_pat1'].append(self.linha[29:34])
                        self.registro_gl['ger_pat2'].append(self.linha[34:44])
                        self.registro_gl['dur_pat2'].append(self.linha[44:49])
                        self.registro_gl['ger_pat3'].append(self.linha[49:59])
                        self.registro_gl['dur_pat3'].append(self.linha[59:64])
                        self.registro_gl['dia'].append(self.linha[65:67])
                        self.registro_gl['mes'].append(self.linha[67:69])
                        self.registro_gl['ano'].append(self.linha[69:73])
                        continue

                    else:
                        self.bloco_tg['df'] = pd.DataFrame(self.registro_tg)
                        self.bloco_gs['df'] = pd.DataFrame(self.registro_gs)
                        self.bloco_nl['df'] = pd.DataFrame(self.registro_nl)
                        self.bloco_gl['df'] = pd.DataFrame(self.registro_gl)
                        break

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_tg['df'] = pd.DataFrame(self.registro_tg)
                self.bloco_gs['df'] = pd.DataFrame(self.registro_gs)
                self.bloco_nl['df'] = pd.DataFrame(self.registro_nl)
                self.bloco_gl['df'] = pd.DataFrame(self.registro_gl)
            else:
                raise

        print(f'OK! Leitura do {os.path.split(file_name)[1]} realizada com sucesso.')

    def database(self) -> object:
        """
        Metodo para armazenar informacoes sobre as usinas termeletricas a GNL.
        :return:
        """

        months = {
            'index': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'name': ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
        }

        self._usi_term_gnl = {
            'nome_ute': self.bloco_tg['df']['nome_ute'].drop_duplicates().to_list(),
            'cod_ute': list(map(int, self.bloco_tg['df']['cod_ute'].drop_duplicates().to_list())),
            'months': None
        }
        self._usi_term_gnl['months'] = np.zeros([len(self._usi_term_gnl['nome_ute']), 12])

    def escrever(self, file_out: str) -> None:
        """
        Metodo para a escrita do arquivo dadgnl.xxx.
        :param file_out: Conjunto de parâmetros obrigatorios.
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
                
                self.database()

                if self.bloco_tg['df'].empty:
                    pass
                else:
                    f.write(self.bloco_tg['descricao'])
                    f.write(self.bloco_tg['cabecalho'])
                    for idx, value in self.bloco_tg['df'].iterrows():
                        line = self.bloco_tg['formato'].format(**value)
                        f.write(line)

                if self.bloco_gs['df'].empty:
                    pass
                else:
                    f.write(self.bloco_gs['descricao'])
                    f.write(self.bloco_gs['cabecalho'])
                    for idx, value in self.bloco_gs['df'].iterrows():
                        line = self.bloco_gs['formato'].format(**value)
                        f.write(line)

                if self.bloco_nl['df'].empty:
                    pass
                else:
                    f.write(self.bloco_nl['descricao'])
                    f.write(self.bloco_nl['cabecalho'])
                    for idx, value in self.bloco_nl['df'].iterrows():
                        if int(value['lag']) in self._valid_lags:
                            pass
                        else:
                            warnings.warn('O valor fornecido para o lag é diferente de 1 ou 2!\n'
                                          'Manual do Usuario - Versao 30.1:\n'
                                          '3.4.3\t Lag de antecipacao de despacho das usinas termicas GNL (registros '
                                          'NL):\n'
                                          '\t\t "Deve-se informar o lag de antecipacao de despacho para cada usina '
                                          'termica a GNL, sendo este obrigatoriamente 1 ou 2."', category=Warning)

                        line = self.bloco_nl['formato'].format(**value)
                        f.write(line)

                if self.bloco_gl['df'].empty:
                    pass
                else:
                    f.write(self.bloco_gl['descricao'])
                    f.write(self.bloco_gl['cabecalho'])
                    for _, value in self.bloco_gl['df'].iterrows():
                        if int(value['cod_ute']) in self._usi_term_gnl['cod_ute']:
                            idx = self._usi_term_gnl['cod_ute'].index(int(value['cod_ute']))
                            f.write(f"{comment} {self._usi_term_gnl['nome_ute'][idx]}\n")
                            del(self._usi_term_gnl['nome_ute'][idx])
                            del (self._usi_term_gnl['cod_ute'][idx])
                        else:
                            pass

                        line = self.bloco_gl['formato'].format(**value)
                        f.write(line)

        except Exception:
            raise
