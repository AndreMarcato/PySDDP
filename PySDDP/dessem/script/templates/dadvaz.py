# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class DadVazTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo DadVaz do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.data_hora = None
        self.conf_gerais = None
        self.numero_dia_inicial = None
        self.semana_fcf = None
        self.numero_semanas = None
        self.pre_interesse = None

        self.vazoes_diarias = None
        self.vazoes_diarias_df = None

        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "data_hora": {
                'descricao': 'Data para o início do período de otimização',
                'cabecalho': "Hr  Dd  Mm  Ano\nXX  XX  XX  XXXX\n",
                'formato': "{hora:02}  {dia:02}  {mes:02}  {ano:04}\n",
                'valor': None
            },
            "conf_gerais": {
                'descricao': 'Configuracoes Gerais',
                'cabecalho': "Dia inic(1-SAB...7-SEX); sem da FCF; n. semanas; pre-interesse\nX X X X\n",
                'formato': "{:01} {:01} {:01} {:01}\n",
                'valor': None
            },
            "vazoes_diarias": {
                'descricao': 'Vazoes Naturais Afluentes Diarias das Usinas Hidraulicas',
                'cabecalho': "VAZOES DIARIAS PARA CADA USINA (m3/s)\nNUM     NOME      itp   DI HI M DF HF M      VAZAO\nXXX XXXXXXXXXXXX   X    XXxXXxXxXXxXXxX     XXXXXXXXX\n",
                'formato': "{num: >3} {nome: <12}   {itp:1}    {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1}     {vazao: >9}\n",
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
