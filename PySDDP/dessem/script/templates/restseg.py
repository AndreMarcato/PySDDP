# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class RestsegTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Restseg do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.tabseg_indice = None
        self.tabseg_tabela = None
        self.tabseg_limite = None
        self.tabseg_celula = None
        self.tabseg_indice_df = None
        self.tabseg_tabela_df = None
        self.tabseg_limite_df = None
        self.tabseg_celula_df = None

        self.restseg = None




        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "restseg":{
                'descricao': 'Armazena todos os comentarios e os mneumos',
                'valor': None
            },
            "tabseg_indice":{
                'descricao':'Fornecem-se o cadastro das restricoes operativas de seguranca representada por tabelas',
                'cabecalho': "&ABSEG INDICE NUM   DESCRICAO\n"
                             "&XXXXX XXXXXX XXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                             "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                'formato': "{mneumo:>13} {num:>5} {descricao:>10}",

                'valor': None
            },
            "tabseg_tabela": {
                'descricao': 'Nestes registros, sao declarados: a equacao de fluxo (DREF) para a qual o limite sera'
                             'definido por tabela e os parametros a serem utilizados para consultar a tabela',
                'cabecalho': "&ABSEG TABELA NUM   TIPO1  TIPO2  NUM   %CARG\n"
                             "XXXXXX XXXXXX XXXXX XXXXXX XXXXXX XXXXX XXXXX",
                'formato': "{mneumo:>13} {num1:>5} {tipo1:>6} {tipo2:>6} {num2:>5} {carg:>5}\n",
                'valor': None
            },
            "tabseg_limite":{
                'descricao':'Nestes registros sao declarados os limites para os parametros',
                'cabecalho': "&ABSEG LIMITE NUM   VAR PARM 1 VAR PARM 2 VAR PARM 3"
                             "&XXXXX XXXXXX XXXXX XXXXXXXXXX XXXXXXXXXX XXXXXXXXXX",
                'formato':"{mneumo:>13} {num:>5} {var_parm_1:>10} {var_parm_2:>10} {var_parm_3:>10}\n",
                'valor': None
            },
            "tabseg_celula": {
                'descricao': 'Nestes registros sao declarados os limites para cada intervalo dos parametros',
                'cabecalho': "&ABSEG CELULA NUM   LIMITE     F    PAR.1.INF   PAR.1.SUP   PAR.2.INF   PAR.2.SUP   "
                             "PAR.3.INF   PAR.3.SUP \n"
                             "&XXXXX XXXXXX XXXXX XXXXXXXXXX X    XXXXXXXXXX  XXXXXXXXXX  XXXXXXXXXX  XXXXXXXXXX  "
                             "XXXXXXXXXX  XXXXXXXXXX",

                'formato': "{mneumo:>13} {num:>5} {limite:>10} {f:1}    {par_1_inf:>10}  {par_1_sup:>10}  "
                           "{par_2_inf:>10}  {par_2_sup:>10}  {par_3_inf:>10}  {par_3_sup:>10}\n",
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
