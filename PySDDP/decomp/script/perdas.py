# -*- coding: utf-8 -*-
import os
from typing import IO

import pandas as pd

from PySDDP.decomp.script.templates.perdas import PerdasTemplate

end = '9999'


class Perdas(PerdasTemplate):
    """
    Classe que contém todos os elementos comuns a qualquer versão do arquivo Perdas do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):

        super().__init__()

        self.bloco_usi_hidr = dict()
        self.bloco_usi_term = dict()
        self.bloco_dem_subsist = dict()
        self.bloco_inter_subsist = dict()

    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo perdas.dat.
        Manual do Usuario 30.1: Arquivo perdas.dat. Este arquivo contém 4 blocos de dados, descrevendo os fatores mensais
        de perda na geração para o centro de gravidade da carga (CGC) para cada usina hidreletrica e termica, perdas na
        demanda nos subsistemas e perdas nos intercambios entre os subsistemas também em relacao ao centro de gravidade
        da carga (CGC). Cada bloco de dados inicia com dois registros que são ignorados pelo programa.
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.bloco_usi_hidr['num_usi'] = list()
        self.bloco_usi_hidr['num_pat_car'] = list()
        self.bloco_usi_hidr['fat_perda_jan'] = list()
        self.bloco_usi_hidr['fat_perda_fev'] = list()
        self.bloco_usi_hidr['fat_perda_mar'] = list()
        self.bloco_usi_hidr['fat_perda_abr'] = list()
        self.bloco_usi_hidr['fat_perda_mai'] = list()
        self.bloco_usi_hidr['fat_perda_jun'] = list()
        self.bloco_usi_hidr['fat_perda_jul'] = list()
        self.bloco_usi_hidr['fat_perda_ago'] = list()
        self.bloco_usi_hidr['fat_perda_set'] = list()
        self.bloco_usi_hidr['fat_perda_out'] = list()
        self.bloco_usi_hidr['fat_perda_nov'] = list()
        self.bloco_usi_hidr['fat_perda_dez'] = list()

        self.bloco_usi_term['num_usi'] = list()
        self.bloco_usi_term['num_pat_car'] = list()
        self.bloco_usi_term['fat_perda_jan'] = list()
        self.bloco_usi_term['fat_perda_fev'] = list()
        self.bloco_usi_term['fat_perda_mar'] = list()
        self.bloco_usi_term['fat_perda_abr'] = list()
        self.bloco_usi_term['fat_perda_mai'] = list()
        self.bloco_usi_term['fat_perda_jun'] = list()
        self.bloco_usi_term['fat_perda_jul'] = list()
        self.bloco_usi_term['fat_perda_ago'] = list()
        self.bloco_usi_term['fat_perda_set'] = list()
        self.bloco_usi_term['fat_perda_out'] = list()
        self.bloco_usi_term['fat_perda_nov'] = list()
        self.bloco_usi_term['fat_perda_dez'] = list()

        self.bloco_dem_subsist['num_subsist'] = list()
        self.bloco_dem_subsist['num_pat_car'] = list()
        self.bloco_dem_subsist['fat_perda_jan'] = list()
        self.bloco_dem_subsist['fat_perda_fev'] = list()
        self.bloco_dem_subsist['fat_perda_mar'] = list()
        self.bloco_dem_subsist['fat_perda_abr'] = list()
        self.bloco_dem_subsist['fat_perda_mai'] = list()
        self.bloco_dem_subsist['fat_perda_jun'] = list()
        self.bloco_dem_subsist['fat_perda_jul'] = list()
        self.bloco_dem_subsist['fat_perda_ago'] = list()
        self.bloco_dem_subsist['fat_perda_set'] = list()
        self.bloco_dem_subsist['fat_perda_out'] = list()
        self.bloco_dem_subsist['fat_perda_nov'] = list()
        self.bloco_dem_subsist['fat_perda_dez'] = list()

        self.bloco_inter_subsist['num_subsist_exp'] = list()
        self.bloco_inter_subsist['num_subsist_imp'] = list()
        self.bloco_inter_subsist['num_pat_car'] = list()
        self.bloco_inter_subsist['fat_perda_jan'] = list()
        self.bloco_inter_subsist['fat_perda_fev'] = list()
        self.bloco_inter_subsist['fat_perda_mar'] = list()
        self.bloco_inter_subsist['fat_perda_abr'] = list()
        self.bloco_inter_subsist['fat_perda_mai'] = list()
        self.bloco_inter_subsist['fat_perda_jun'] = list()
        self.bloco_inter_subsist['fat_perda_jul'] = list()
        self.bloco_inter_subsist['fat_perda_ago'] = list()
        self.bloco_inter_subsist['fat_perda_set'] = list()
        self.bloco_inter_subsist['fat_perda_out'] = list()
        self.bloco_inter_subsist['fat_perda_nov'] = list()
        self.bloco_inter_subsist['fat_perda_dez'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                # Bloco 1 - Usinas hidreletricas:
                # Este bloco possui dois registros iniciais de comentários:
                self.next_line(f)
                self.next_line(f)

                self.linha = self.next_line(f)

                while self.linha[:5].strip() != end:
                    self.bloco_usi_hidr['num_usi'].append(self.linha[1:5])
                    self.bloco_usi_hidr['num_pat_car'].append(self.linha[8])
                    self.bloco_usi_hidr['fat_perda_jan'].append(self.linha[11:16])
                    self.bloco_usi_hidr['fat_perda_fev'].append(self.linha[17:22])
                    self.bloco_usi_hidr['fat_perda_mar'].append(self.linha[23:28])
                    self.bloco_usi_hidr['fat_perda_abr'].append(self.linha[29:34])
                    self.bloco_usi_hidr['fat_perda_mai'].append(self.linha[35:40])
                    self.bloco_usi_hidr['fat_perda_jun'].append(self.linha[41:46])
                    self.bloco_usi_hidr['fat_perda_jul'].append(self.linha[47:52])
                    self.bloco_usi_hidr['fat_perda_ago'].append(self.linha[53:58])
                    self.bloco_usi_hidr['fat_perda_set'].append(self.linha[59:64])
                    self.bloco_usi_hidr['fat_perda_out'].append(self.linha[65:70])
                    self.bloco_usi_hidr['fat_perda_nov'].append(self.linha[71:76])
                    self.bloco_usi_hidr['fat_perda_dez'].append(self.linha[77:82])
                    self.linha = self.next_line(f)

                # Bloco 2 - Usinas termicas:
                # Este bloco possui dois registros iniciais de comentarios:
                self.next_line(f)
                self.next_line(f)

                self.linha = self.next_line(f)

                while self.linha[:5].strip() != end:
                    self.bloco_usi_term['num_usi'].append(self.linha[1:5])
                    self.bloco_usi_term['num_pat_car'].append(self.linha[8])
                    self.bloco_usi_term['fat_perda_jan'].append(self.linha[11:16])
                    self.bloco_usi_term['fat_perda_fev'].append(self.linha[17:22])
                    self.bloco_usi_term['fat_perda_mar'].append(self.linha[23:28])
                    self.bloco_usi_term['fat_perda_abr'].append(self.linha[29:34])
                    self.bloco_usi_term['fat_perda_mai'].append(self.linha[35:40])
                    self.bloco_usi_term['fat_perda_jun'].append(self.linha[41:46])
                    self.bloco_usi_term['fat_perda_jul'].append(self.linha[47:52])
                    self.bloco_usi_term['fat_perda_ago'].append(self.linha[53:58])
                    self.bloco_usi_term['fat_perda_set'].append(self.linha[59:64])
                    self.bloco_usi_term['fat_perda_out'].append(self.linha[65:70])
                    self.bloco_usi_term['fat_perda_nov'].append(self.linha[71:76])
                    self.bloco_usi_term['fat_perda_dez'].append(self.linha[77:82])
                    self.linha = self.next_line(f)

                # Bloco 3 - Demanda dos subsistemas:
                # Este bloco possui dois registros iniciais de comentarios:
                self.next_line(f)
                self.next_line(f)

                self.linha = self.next_line(f)

                while self.linha[:5].strip() != end:
                    self.bloco_dem_subsist['num_usi'].append(self.linha[1:5])
                    self.bloco_dem_subsist['num_pat_car'].append(self.linha[8])
                    self.bloco_dem_subsist['fat_perda_jan'].append(self.linha[11:16])
                    self.bloco_dem_subsist['fat_perda_fev'].append(self.linha[17:22])
                    self.bloco_dem_subsist['fat_perda_mar'].append(self.linha[23:28])
                    self.bloco_dem_subsist['fat_perda_abr'].append(self.linha[29:34])
                    self.bloco_dem_subsist['fat_perda_mai'].append(self.linha[35:40])
                    self.bloco_dem_subsist['fat_perda_jun'].append(self.linha[41:46])
                    self.bloco_dem_subsist['fat_perda_jul'].append(self.linha[47:52])
                    self.bloco_dem_subsist['fat_perda_ago'].append(self.linha[53:58])
                    self.bloco_dem_subsist['fat_perda_set'].append(self.linha[59:64])
                    self.bloco_dem_subsist['fat_perda_out'].append(self.linha[65:70])
                    self.bloco_dem_subsist['fat_perda_nov'].append(self.linha[71:76])
                    self.bloco_dem_subsist['fat_perda_dez'].append(self.linha[77:82])
                    self.linha = self.next_line(f)

                # Bloco 4 - Intercambio entre subsistemas:
                # Este bloco possui dois registros iniciais de comentarios:
                self.next_line(f)
                self.next_line(f)

                self.linha = self.next_line(f)

                while self.linha[:5].strip() != end:
                    self.bloco_inter_subsist['num_subsist_exp'].append(self.linha[1:5])
                    self.bloco_inter_subsist['num_subsist_imp'].append(self.linha[5:9])
                    self.bloco_inter_subsist['num_pat_car'].append(self.linha[13])
                    self.bloco_inter_subsist['fat_perda_jan'].append(self.linha[16:21])
                    self.bloco_inter_subsist['fat_perda_fev'].append(self.linha[22:27])
                    self.bloco_inter_subsist['fat_perda_mar'].append(self.linha[28:33])
                    self.bloco_inter_subsist['fat_perda_abr'].append(self.linha[34:39])
                    self.bloco_inter_subsist['fat_perda_mai'].append(self.linha[40:45])
                    self.bloco_inter_subsist['fat_perda_jun'].append(self.linha[46:51])
                    self.bloco_inter_subsist['fat_perda_jul'].append(self.linha[52:57])
                    self.bloco_inter_subsist['fat_perda_ago'].append(self.linha[58:63])
                    self.bloco_inter_subsist['fat_perda_set'].append(self.linha[64:69])
                    self.bloco_inter_subsist['fat_perda_out'].append(self.linha[70:75])
                    self.bloco_inter_subsist['fat_perda_nov'].append(self.linha[76:81])
                    self.bloco_inter_subsist['fat_perda_dez'].append(self.linha[82:87])
                    self.linha = self.next_line(f)

                self.usi_hidr['df'] = pd.DataFrame(self.bloco_usi_hidr)
                self.usi_term['df'] = pd.DataFrame(self.bloco_usi_term)
                self.dem_subsist['df'] = pd.DataFrame(self.bloco_dem_subsist)
                self.inter_subsist['df'] = pd.DataFrame(self.bloco_inter_subsist)

        except Exception as err:
            if isinstance(err, StopIteration):

                self.usi_hidr['df'] = pd.DataFrame(self.bloco_usi_hidr)
                self.usi_term['df'] = pd.DataFrame(self.bloco_usi_term)
                self.dem_subsist['df'] = pd.DataFrame(self.bloco_dem_subsist)
                self.inter_subsist['df'] = pd.DataFrame(self.bloco_inter_subsist)
            else:
                raise

        print(f'OK! Leitura do {os.path.split(file_name)[1]} realizada com sucesso.')

    def escrever(self, file_out: str) -> None:
        """
        Metodo para a escrita do arquivo perdas.dat (nome não obrigatorio).
        :param file_out: Conjunto de parametros obrigatorios.
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write(self.usi_hidr['cabecalho'])
                if self.usi_hidr['df'].empty:
                    pass
                else:
                    for idx, value in self.usi_hidr['df'].iterrows():
                        line = self.usi_hidr['formato'].format(**value)
                        f.write(line)
                f.write(f' {end}\n')

                f.write(self.usi_term['cabecalho'])
                if self.usi_term['df'].empty:
                    pass
                else:
                    for idx, value in self.usi_term['df'].iterrows():
                        line = self.usi_term['formato'].format(**value)
                        f.write(line)
                f.write(f' {end}\n')

                f.write(self.dem_subsist['cabecalho'])
                if self.dem_subsist['df'].empty:
                    pass
                else:
                    for idx, value in self.dem_subsist['df'].iterrows():
                        line = self.dem_subsist['formato'].format(**value)
                        f.write(line)
                f.write(f' {end}\n')

                f.write(self.inter_subsist['cabecalho'])
                if self.inter_subsist['df'].empty:
                    pass
                else:
                    f.write(self.inter_subsist['cabecalho'])
                    for idx, value in self.inter_subsist['df'].iterrows():
                        line = self.inter_subsist['formato'].format(**value)
                        f.write(line)
                f.write(f' {end}\n')

        except Exception:
            raise
