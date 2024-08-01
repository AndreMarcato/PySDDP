# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada


class CasoTemplate(ArquivoEntrada):
    """
    Classe que contém todos os elementos comuns a qualquer versão do arquivo Caso do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nível de especificação
    dentro da fábrica. Além disso, esta classe deve passar adiante a responsabilidade da implementação dos métodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.bloco_caso = {
            'descricao': 'Nome do arquivo índice',
            'cabecalho': None,
            'formato': '{nome_arq:<80}\n',
            'df': None
        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Método abstrato do ArquivoEntrada sendo repassado para as classes filhas.
        :param args: Conjunto de parâmetros obrigatórios.
        :param kwargs: Conjunto de parâmetros opcionais.
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Método abstrato da ArquivoEntrada sendo repassado para as classes filhas.
        :param args: conjunto de parâmetros obrigatórios.
        :param kwargs: conjunto de parâmetros opcionais.
        :return:
        """
