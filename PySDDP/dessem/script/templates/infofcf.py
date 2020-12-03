# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class InfofcfTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Infofcf do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.mapfcf_sisgnl = None
        self.mapfcf_durpat = None
        self.fcffix_usit = None
        self.mapfcf_tviag = None
        self.mapfcf_cgtmin = None
        self.mapfcf_sisgnl_df = None
        self.mapfcf_durpat_df = None
        self.fcffix_usit_df = None
        self.mapfcf_tviag_df = None
        self.mapfcf_cgtmin_df = None

        self.infofcf = None




        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "infofcf":{
                'descricao': 'Armazena todos os comentarios e os mneumos',
                'valor': None
            },
            "mapfcf_sisgnl":{
                'descricao':'Identificacao dos subsistemas onde ha usinas com despacho antecipado',
                'cabecalho': "&       Mnem   Ind Num Nlag Npat\n"
                             "&XXXXX  XXXXXX XXX XXX XXX XXX",
                'formato': "{mneumo:>14} {ind:>3} {num:>3} {lag:>3}  {patamares:>3}\n",

                'valor': None
            },
            "mapfcf_durpat": {
                'descricao': 'Duracao dos patamares de carga para os periodos futuros',
                'cabecalho': "&       Mnem   Lag Pat    Dur (h)\n"
                             "&XXXXX  XXXXXX XXX XXX  XXXXXXXXXX",
                'formato': "{mneumo:>14} {lag:>3} {patamar:>3}  {duracao:>9}\n",
                'valor': None
            },
            "fcffix_usit":{
                'descricao':'Valores de geracao termica sinalizada e/ou comandada para as semanas / meses alem do '
                            'horizonte de estudo do modelo dessem',
                'cabecalho': "&      TpEnt IdEnt IdVar lag Pat    Valor        Justificativa"
                             "XXXXXX XXXXXX XXX XXXXXX XXX XXX XXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                'formato':"{mneumo:>13} {num_ent:>3} {variavel:>6} {lag:>3} {patamar:>3} {valor:>10} {comentario:>20}\n",
                'valor': None
            },
            "mapfcf_tviag": {
                'descricao': 'Informacoes para tempos de viagem considerados pelo modelo DECOMP',
                'cabecalho': "&       Mnem    Ind Num\n"
                             "&XXXXX  XXXXXXX XXX XXX",
                'formato':"{mneumo:>14} {ind:>3} {num:>3}\n",
                'valor': None
            },
            "mapfcf_cgtmin": {
                'descricao': 'Custo de geracao termica minima alem do horizonte de estudo',
                'cabecalho': "&       Mnem    Custo\n"
                             "&XXXXX  XXXXXXX XXXXXXXXXXXXXXX",
                'formato': "{mneumo:>14} {custo:>15}\n",
                'valor': None
            },

        }

        # preenchido após o método de leitura ser chamado
        # representa os nomes lidos no script.arq
        self.nome_arquivos = list()

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Metodo abstrato da ArquivoEntrada sendo repassado para as classes filhas
        :param args: conjunto de parametros obrigatorios
        :param kwargs: conjunto de parametros opcionais
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Metodo abstrato da ArquivoEntrada sendo repassado para as classes filhas
        :param args: conjunto de parametros obrigatorios
        :param kwargs: conjunto de parametros opcionais
        :return:
        """
