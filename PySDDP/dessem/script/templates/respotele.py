# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class RespoteleTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Respotele do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.respotele = None
        self.respotele_df = None

        self.bloco_respotele = {
            'cabecalho':
                "&      DREF DI HI F DF HF F Valor\n"
                "&xxx   xxxx xx xx x xx xx x xxxxxxxxxx",
            'formato':
                "{mne:<4} {flag:1} {dref:>4} {di:>2} {hi:>2} {fi:1} {df:>2} {hf:>2} {ff:1} {valor:<10}\n",
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