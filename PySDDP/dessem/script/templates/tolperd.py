# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class TolperdTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Tolperd do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.registro_ln = None
        self.registro_nv = None

        self.registro_ln_df = None
        self.registro_nv_df = None

        self.tolperd = None



        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "tolperd":{
                'descricao':'Armazena todos os dados',
                'valor': None

            },
            "registro_ln": {
                'descricao': 'Tolerancias individualmente para as linhas de transmissao',
                # 'cabecalho': "&   PONTO DE OPERCAO\n"
                #              "&TOPER TPELEM ID  TP.VAR DI HI M DF HF M  VALORVAR\n"
                #              "&TOPER xxxxxx xxx xxxxxx xx xx x xx xx x xxxxxxxxxx\n",
                'formato': "{mneumo:>2} {de:>4} {para:>4} {num_circuito:>2} {tol_perc:>9} {tol_MW:>9}\n",

                'valor': None

            },
            "registro_nv": {
                'descricao': 'Tolerancias por nivel de tensao',
                # 'cabecalho': "&   PONTO DE OPERCAO\n"
                #              "&TOPER TPELEM ID  TP.VAR DI HI M DF HF M  VALORVAR\n"
                #              "&TOPER xxxxxx xxx xxxxxx xx xx x xx xx x xxxxxxxxxx\n",
                'formato': "{mneumo:>2} {niv_tensao:1} {tol_perc:>9} {tol_MW:>9}\n",

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
