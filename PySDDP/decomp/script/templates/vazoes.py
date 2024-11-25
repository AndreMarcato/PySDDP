# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada

class VazoesTemplate(ArquivoEntrada):
    """
    Classe que contém todos os elementos comuns a qualquer versão do arquivo Vazoes do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nível de especificação
    dentro da fábrica. Além disso, esta classe deve passar adiante a responsabilidade da implementação dos métodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.nreg: int = None

        # Dados do registro 1
        self.__reg1__ = None
        self.numero_postos = None
        self.numero_estagios = None
        self.numero_aberturas = None
        self.total_aberturas = None

        # Dados do Registro 2
        self.__reg2__ = None
        self.codigo_uhes = None

        # Dados do Registro3
        self.__reg3__ = None
        self.numero_semanas_completas = None
        self.numero_dias_excluidos = None
        self.mes_inicial_estudo = None
        self.ano_inicial_estudo = None

        # Dados do Registro 4 e subsequentes
        self.__reg4__ = None
        self.probabilidade_no = None

        # Dados do Registro 5 e subsequentes
        self.__reg5__ = None
        self.vazao_incremental = None
        self.vazao_incremental_art = None

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