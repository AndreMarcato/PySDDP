# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class RampasTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rampas do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.rampas = None
        self.rampas_df = None

        self.bloco_rampas = {
            'ute': None,
            'descricao':
                "&us uni seg  C   T  Potencia   Tempo Flag meia hora",
            'cabecalho':
                "&XX XXX XXX  X   X  XXXXXXXXXX XXXXX X",
            'formato':
                "{us:>3} {uni:>3} {seg:>3} {C:1} {T:1} {Potencia:>10} {Tempo:>5} {FlagMeiaHora:1}\n",
            'valor': None
        }

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