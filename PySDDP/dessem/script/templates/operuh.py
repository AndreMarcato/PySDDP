# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class OperuhTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Operuh do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.restricoes_operativas = None
        self.rest  = None
        self.elem = None
        self.lim = None
        self.var = None
        self.rest_df = None
        self.elem_df = None
        self.lim_df = None
        self.var_df = None



        self.dados = {
            "operuh rest": {
                'descricao': 'Definir o numero e tipo (restricao de limite ou variacao) das restricoes operativas',
                'cabecalho':"&PERUH REST   Ind    T     Descricao    VL Inicial \n"
                            "&XXXXX XXXXXX xxxxx  x     xxxxxxxxxxxx xxxxxxxxxx",
                'formato':"{mneumo: <13} {ind:>5}  {tipo:1}     {descricao:>12} {vl: >8}\n",
                'valor': None

            },
            "operuh elem": {
                'descricao': 'Informa se as usinas hidroeletricas e elevatorias que pertencem a cada restricao',
                'cabecalho': "&PERUH ELEM   Ind   Num  Nome         U CD Fator \n"
                             "&XXXXX XXXXXX xxxxx xxx  xxxxxxxxxxxx x xx xxxxx",
                'formato':"{mneumo: <13} {ind:>5} {num:>3}  {nome:>12} {codigo: >4} {fator:>5}\n",
                'valor': None

            },
            "operuh lim":{
                'descricao': 'Informa se os limites inferior e superior para as restricoes operativas de limite',
                'cabecalho':"&PERUH LIM    Ind   DI HI I DF HF F     Minimo    Maximo  \n"
                            "&XXXXX XXXXXX xxxxx xx xx x xx xx x   xxxxxxxxxxXXXXXXXXXX",
                'formato': "{mneumo: <13} {ind:>5} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1}   {vmin:>3}{vmax:>3}\n",
                'valor': None
            },
            "operuh var": {
                'descricao':'Informa se os valores das rampas maximas horarias',
                'cabecalho':"&PERUH VAR    Ind  DI HI I DF HF F   VarMin(%)  VarMax(%)  VarMin    VarMax  \n"
                            "&XXXXX XXXXXX xxxxxXXXXXXXXXXXXXXX   xxxxxxxxxxXXXXXXXXXXxxxxxxxxxxXXXXXXXXXX",
                'formato': "{mneumo: <13} {ind:>5}{di:1} {hi:>2} {mi:1} {df:>2} {hf:>2}{mf:1}                        "
                           "{vmin:>3}{vmax:>3}{vmin_rel:>3}{vmax_rel:>3}\n",
                'valor': None

            },
            "operuh armazena":{
                'descricao': 'Armazena todos os dados',
                'valor': None
            }
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