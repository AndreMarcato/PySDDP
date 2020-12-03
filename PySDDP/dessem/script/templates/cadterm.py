# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class CadTermTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo CadTerm do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.cadusit = None
        self.cadunidt = None
        self.cadconf = None
        self.cadmin = None
        self.cadusit_df = None
        self.cadunidt_df = None
        self.cadconf_df = None
        self.cadmin_df = None

        self.termo = None




        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "termo":{
                'descricao': 'Armazena todos os dados',
                'valor': None
            },
            "cadusit":{
                'descricao':'Caracteristicas das usinas termoeletricas',
                'cabecalho': "&ADUSIT  us     nome     ss yyyy mm dd hr mh nunid\n"
                             "&ADUSIT XXX XXXXXXXXXXXX XX XXXX XX XX XX X   XX",
                'formato': "{mneumo:>7} {num_usi:>3} {nome:>12} {num_subsistema:1} {ano:>4} {mes:>2} {di:>2} {hr:>2} "
                           "{m:1}  {num_ger:>2}\n",
                'valor': None
            },
            "cadunidt": {
                'descricao': 'Caracteristicas das unidadaes geradoras de cada usinas termoeletrica',
                'cabecalho': "&ADUNIDT  us un yyyy mm dd hr mh     Pot        PotMin    On    Of      CCold       "
                             "CHot       CSTD       RUp     RDown   F No Equ Rampa tran\n"
                             "&ADUNIDT XXX XX XXXX xx XX XX X  XXXXXXXXXX XXXXXXXXXX XXXXX XXXXX XXXXXXXXXX XXXXXXXXXX "
                             "XXXXXXXXXX XXXXXXXXXX  XXXXXXXXX X XX XXX XXXXXXXXXX",
                'formato': "{mneumo:>8} {num_usi:>3}{ind_ger:>2} {ano:>4} {mes:>2} {di:>2} {hr:>2} {m:1}  {pot:>10} "
                           "{ger_min:>10} {temp_on:>5} {temp_off:>5}{custo_frio:>10}{custo_desl:>10}              {ramp_tom:>9}"
                           " {ramp_alivio:>9} {flag_rest:1} {num_oscilacao:>2} {flag_equiv:>3} {ramp_trans:>9}\n",

                'valor': None
            },"cadconf":{
                'descricao':'Relacao entre Unidades Equivalentes e Reais',
                'cabecalho': "&ADCONF USI EQU UNI\n &XXXXXX XXX XXX XXX",
                'formato':"{mneumo:>7} {num_usi:>3} {ind_equi:>3} {ind_ger:>3}\n",
                'valor': None
            },
            "cadmin": {
                'descricao': 'Relacao de quantidade de unidades reais disponiveis minimas para acionamento da unidade'
                             'equivalente',
                'cabecalho': "&ADMIN  USI EQU UNI\n &XXXXX  XXX XXX XXX",
                'formato': "{mneumo:>6}  {num_usi:>3} {ind_equi:>3} {ind_ger:>3}\n",
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
