# -*- coding: utf-8 -*-
from abc import abstractmethod
from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class RstlppTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Rstlpp do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.rstseg = None
        self.rstseg_df = None

        self.adicrs = None
        self.adicrs_df = None

        self.param = None
        self.param_df = None

        self.vparm = None
        self.vparm_df = None

        self.reslpp = None
        self.reslpp_df = None

        self.blocorstseg = {
            'mne': 'RSTSEG',
            'descricao': None,
            'cabecalho': '&MNEM  CHA1    NUM  DREF CHAVE IDENT   DESCRICAO\n'
                         '&XXXXX xxxxxxx XXXX XXXX xxxxx xxxxx XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n',
            'formato': '{mne:<6} {cha1:<7} {num:>4}{flag:1}{dref:>4} {chave:<5} {ident:>5} {descricao:<40}\n',
            'valor': None
        }

        self.blocoadicrs = {
            'mne': 'ADICRS',
            'descricao': None,
            'cabecalho': '&MNEM  CHA1    NUM  DREF CHAVE IDENT   DESCRICAO\n'
                         '&XXXXX xxxxxxx XXXX XXXX xxxxx xxxxx XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n',
            'formato': '{mne:<6} {cha1:<7} {num:>4}{flag:1}{dref:>4} {chave:<5} {ident:>5} {descricao:<40}\n',
            'valor': None
        }

        self.blocoparam = {
            'mne': 'PARAM',
            'descricao': None,
            'cabecalho': '&XXXX XXXX XXXXX XXXXX\n',
            'formato': '{param:<5} {num:>4} {chave:<5} {ident:>5}\n',
            'valor': None
        }

        self.blocovparm = {
            'mne': 'VPARM',
            'descricao': None,
            'cabecalho': '&XXXX XXXX XX XXXXXXXXX\n',
            'formato': '{vparm:<5} {num:>4} {numcurva:>2} {valinfpri:>10} {valsuppri:>10} {valinfseg:>10} '
                       '{valsupseg:>10}\n',
            'valor': None
        }

        self.blocoreslpp = {
            'mne': 'RESLPP',
            'descricao': None,
            'cabecalho': '&mnem   num p i coefangula coeflin    2 contro\n'
                         '&xxxxx xxxx x x xxxxxxxxxx xxxxxxxxxx xxxxxxxxxx\n',
            'formato': '{mne:<6} {num:>4} {p:1} {i:1} {coefangula:>10} {coeflin:>10} '
                       '{2 contro:>10} {3 contro:>10} {4 contro:>10}\n',
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