# -*- coding: utf-8 -*-
import warnings
from typing import IO

import pandas as pd
import os

from PySDDP.decomp.script.templates.polinjus import PolinJusTemplate

comment = '&'

class PolinJus(PolinJusTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo que contem os dados das curvas de jusante
    das usinas hidreletricas (nome nos decks consultados do Decomp: Polinjus.dat).
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementação dos metodos de
    leitura e escrita.
    """

    def __init__(self):

        super().__init__()

        self.registro_curvajus = dict()
        self.registro_pppjus = dict()

        self.list_of_comments = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo polinjus.dat (nome nao obrigatorio).
        Manual do Usuario 30.1: O nome deste arquivo e informado no registro FJ do arquivo dadger.xxx. Desta forma, o
        arquivo informado deve estar presente na pasta do caso e e composto por dois registros.
        Os comentarios podem ser livremente incluidos desde que precedidos por "&".
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.registro_curvajus['id'] = list()
        self.registro_curvajus['cod_uhe'] = list()
        self.registro_curvajus['id_cur_jus'] = list()
        self.registro_curvajus['alt_jus_ref'] = list()
        self.registro_curvajus['quant_pol'] = list()

        self.registro_pppjus['id'] = list()
        self.registro_pppjus['cod_uhe'] = list()
        self.registro_pppjus['id_cur_jus'] = list()
        self.registro_pppjus['lim_inf_vaz'] = list()
        self.registro_pppjus['lim_sup_vaz'] = list()
        self.registro_pppjus['coef_grau0_pol_jus'] = list()
        self.registro_pppjus['coef_grau1_pol_jus'] = list()
        self.registro_pppjus['coef_grau2_pol_jus'] = list()
        self.registro_pppjus['coef_grau3_pol_jus'] = list()
        self.registro_pppjus['coef_grau4_pol_jus'] = list()

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

                    elif self.linha[:8].upper() == 'CURVAJUS':
                        self.registro_curvajus['id'].append(self.linha[:8])
                        self.registro_curvajus['cod_uhe'].append(self.linha[11:15])
                        self.registro_curvajus['id_cur_jus'].append(self.linha[20:23])
                        self.registro_curvajus['alt_jus_ref'].append(self.linha[27:37])
                        self.registro_curvajus['quant_pol'].append(self.linha[39:42])
                        continue

                    elif self.linha[:6].upper() == 'PPPJUS':
                        self.registro_pppjus['id'].append(self.linha[:6])
                        self.registro_pppjus['cod_uhe'].append(self.linha[11:15])
                        self.registro_pppjus['id_cur_jus'].append(self.linha[20:23])
                        self.registro_pppjus['lim_inf_vaz'].append(self.linha[28:48])
                        self.registro_pppjus['lim_sup_vaz'].append(self.linha[49:69])
                        self.registro_pppjus['coef_grau0_pol_jus'].append(self.linha[70:90])
                        self.registro_pppjus['coef_grau1_pol_jus'].append(self.linha[91:111])
                        self.registro_pppjus['coef_grau2_pol_jus'].append(self.linha[112:132])
                        self.registro_pppjus['coef_grau3_pol_jus'].append(self.linha[133:153])
                        self.registro_pppjus['coef_grau4_pol_jus'].append(self.linha[154:174])
                        continue

                    else:
                        self.bloco_curvajus['df'] = pd.DataFrame(self.registro_curvajus)
                        self.bloco_pppjus['df'] = pd.DataFrame(self.registro_pppjus)
                        break

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_curvajus['df'] = pd.DataFrame(self.registro_curvajus)
                self.bloco_pppjus['df'] = pd.DataFrame(self.registro_pppjus)
            else:
                raise

        print(f'OK! Leitura do {os.path.split(file_name)[1]} realizada com sucesso.')

    def escrever(self, file_out: str) -> None:
        """
        Metodo para a escrita do arquivo polinjus.dat (nome nao obrigatorio).
        :param file_out: Conjunto de parâmetros obrigatorios.
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                if self.bloco_curvajus['df'].empty:
                    pass
                else:
                    f.write(self.bloco_curvajus['descricao'])
                    f.write(self.bloco_curvajus['cabecalho'])
                    for idx, value in self.bloco_curvajus['df'].iterrows():
                        if int(value['id_cur_jus']) > 5:
                            warnings.warn('O valor fornecido para o indice e superior a 5!\n'
                                          'Manual do Usuario - Versao 30.1:\n'
                                          '3.3.30\t Funcao de producao das usinas hidreletricas - FPHA e FPHAD '
                                          '(registros FP, FQ e FJ):\n'
                                          '\t\t Registro FJ - Bloco CURVAJUS:\n'
                                          '\t\t "Índice da curva de jusante (1 a 5) a ser informado em ordem sequencial'
                                          '."', category=Warning)
                        elif int(value['quant_pol']) > 5:
                            warnings.warn('O valor fornecido para a quantidade de polinomios que compoe a curva e '
                                          'superior a 5!\n'
                                          'Manual do Usuario - Versao 30.1:\n'
                                          '3.3.30\t Funcao de producao das usinas hidreletricas - FPHA e FPHAD '
                                          '(registros FP, FQ e FJ):\n'
                                          '\t\t Registro FJ - Bloco CURVAJUS:\n'
                                          '\t\t "Quantidade de polinomios que compoe a curva (1 a 5)."',
                                          category=Warning)
                        else:
                            pass
                        line = self.bloco_curvajus['formato'].format(**value)
                        f.write(line)

                if self.bloco_pppjus['df'].empty:
                    pass
                else:
                    f.write(self.bloco_pppjus['descricao'])
                    f.write(self.bloco_pppjus['cabecalho'])
                    for idx, value in self.bloco_pppjus['df'].iterrows():
                        line = self.bloco_pppjus['formato'].format(**value)
                        f.write(line)

        except Exception:
            raise
