# -*- coding: utf-8 -*-
from abc import abstractmethod
from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class RmpflxTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rmpflx do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.rest = None
        self.rest_df = None

        self.limi = None
        self.limi_df = None

        self.blocorest = {
            'mne': 'REST',
            'descricao': 'Registros de Definição',
            'cabecalho': '&MPFLX REST NUM  VALOR      T\n'
                         '&XXXXX XXXX XXXX XXXXXXXXXX X\n',
            'formato': '{mne:<11} {num:>4} {valor:<10} {tipo:1}\n',
            'valor': None
        }

        self.blocolimi = {
            'mne': 'LIMI',
            'descricao': None,
            'cabecalho': '&MPFLX LIMI DI HI F DF HF F NUM  RINFERIOR  RSUPERIOR  T\n'
                         '&XXXXX XXXX XX XX X XX XX X XXXX XXXXXXXXXX XXXXXXXXXX X\n',
            'formato': '{mne:<11} {di:<2} {hi:<2} {fi:1} {df:<2} {hf:<2} {ff:1} {num:<4} {rinferior:<10}'
                       ' {rsuperior:<10} {t:1}\n',
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