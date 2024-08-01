# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada


class PerdasTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Perdas do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementação dos metodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.usi_hidr = {
            'descricao': None,
            'cabecalho': 'FAT. PERDA HIDRO (HAVERA TANTOS REGISTROS QUANTOS FOREM O No DE PATAMARES DE CARGA)\n'
                         ' XXXX   X  X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX\n',
            'formato': ' {num_usi:>4}   {num_pat_car:1}  {fat_perda_jan:>5} {fat_perda_fev:>5} {fat_perda_mar:>5} '
                       '{fat_perda_abr:>5} {fat_perda_mai:>5} {fat_perda_jun:>5} {fat_perda_jul:>5} {fat_perda_ago:>5} '
                       '{fat_perda_set:>5} {fat_perda_out:>5} {fat_perda_nov:>5} {fat_perda_dez:>5}\n',
            'df': None
        }

        self.usi_term = {
            'descricao': None,
            'cabecalho': 'FAT. PERDA TERMO (HAVERA TANTOS REGISTROS QUANTOS FOREM O No DE PATAMARES DE CARGA)\n'
                         '  XXX   X  X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX\n',
            'formato': ' {num_usi:>4}   {num_pat_car:1}  {fat_perda_jan:>5} {fat_perda_fev:>5} {fat_perda_mar:>5} '
                       '{fat_perda_abr:>5} {fat_perda_mai:>5} {fat_perda_jun:>5} {fat_perda_jul:>5} {fat_perda_ago:>5} '
                       '{fat_perda_set:>5} {fat_perda_out:>5} {fat_perda_nov:>5} {fat_perda_dez:>5}\n',
            'df': None
        }

        self.dem_subsist = {
            'descricao': None,
            'cabecalho': 'FAT. PERDA SISTEM (HAVERA TANTOS REGISTROS QUANTOS FOREM O No DE PATAMARES DE CARGA)\n'
                         '  XX    X  X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX\n',
            'formato': ' {num_subsist:>4}   {num_pat_car:1}  {fat_perda_jan:>5} {fat_perda_fev:>5} {fat_perda_mar:>5} '
                       '{fat_perda_abr:>5} {fat_perda_mai:>5} {fat_perda_jun:>5} {fat_perda_jul:>5} {fat_perda_ago:>5} '
                       '{fat_perda_set:>5} {fat_perda_out:>5} {fat_perda_nov:>5} {fat_perda_dez:>5}\n',
            'df': None
        }

        self.inter_subsist = {
            'descricao': None,
            'cabecalho': 'FAT. PERDA INTER (HAVERA TANTOS REGISTROS QUANTOS FOREM O No DE PATAMARES DE CARGA)\n'
                         ' XXX  XXX    X  X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX X.XXX\n',
            'formato': ' {num_subsist_exp:>4}{num_subsist_imp:>4}    {num_pat_car:1}  {fat_perda_jan:>5} '
                       '{fat_perda_fev:>5} {fat_perda_mar:>5} {fat_perda_abr:>5} {fat_perda_mai:>5} {fat_perda_jun:>5} '
                       '{fat_perda_jul:>5} {fat_perda_ago:>5} {fat_perda_set:>5} {fat_perda_out:>5} {fat_perda_nov:>5} '
                       '{fat_perda_dez:>5}\n',
            'df': None

        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Metodo abstrato do ArquivoEntrada sendo repassado para as classes filhas.
        :param args: Conjunto de parâmetros obrigatórios.
        :param kwargs: Conjunto de parâmetros opcionais.
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Metodo abstrato da ArquivoEntrada sendo repassado para as classes filhas.
        :param args: conjunto de parâmetros obrigatórios.
        :param kwargs: conjunto de parâmetros opcionais.
        :return:
        """
