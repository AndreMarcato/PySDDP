# -*- coding: utf-8 -*-
from abc import abstractmethod

# from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class VazoesTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Arquivos do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Newave e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.nr_postos = None
        self.vaz_nat = None

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
