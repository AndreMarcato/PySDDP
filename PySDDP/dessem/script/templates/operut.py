# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class OperutTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Operut do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.condicoes_iniciais = None
        self.condicoes_iniciais_df = None

        self.limites_condicoes = None
        self.limites_condicoes_df = None

        self._flags_ = None
        self._flags_df = None

        self.bloco_init = {
            'descricao':
                '& CONDICOES INICIAIS DAS UNIDADES\n'
                '&\n'
                'INIT\n',
            'cabecalho':
                '&us     nome       ug   st   GerInic     tempo MH A/D\n'
                '&XX XXXXXXXXXXXX  XXX   XX   XXXXXXXXXX  XXXXX  X  X\n',
            'formato':
                "{us:>3} {nome:<12} {ug:>3} {st:>2} {GerInic:>10} {tempo:>5} {MH:1} {A/D:1}\n",
            'valor': None
        }

        self.bloco_oper = {
            'descricao':
                '&\n'
                '&\n'
                '& LIMITES E CONDICOES OPERACIONAIS DAS UNIDADES\n'
                '&\n'
                'OPER\n',
            'cabecalho':
                '&us    nome      un di hi m df hf m Gmin     Gmax       Custo \n'
                '&XX XXXXXXXXXXXX XX XX XX X XX XX X XXXXXXXXXXxxxxxxxxxxXXXXXXXXXX\n',
            'formato':
                '{us:>3} {nome:<12} {un:>2} {di:>2} {hi:>2} {mi:1} '
                '{df:>2} {hf:>2} {mf:1} {Gmin:>10} {Gmax:>10} {Custo:<10}\n',
            'valor': None
        }

        self.flags = {
            '1': {
                'descricao': 'UCTERM',
                'formato': '{ucterm:<6} {metodologia:1}',
                'valor': None
            },
            '2': {
                'descricao': 'REGRANPTV',
                'formato': '{regranptv:<9} {regra:1} {flag:<2} {numpon:<2}',
                'valor': None
            },
            '3': {
                'descricao': 'TOLERILH',
                'formato': '{tolerilh:<8} {valor:1}',
                'valor': None
            },
            '4': {
                'descricao': 'PENINTE',
                'formato': '{peninte:<7} {fator:>5}',
                'valor': None
            },
            '5': {
                'descricao': 'DEFICIT',
                'formato': '{deficit:<7} {valor:1}',
                'valor': None
            },
            '6': {
                'descricao': 'S/DECLARACAO',
                'formato': None,
                'valor': None
            },
            '7': {
                'descricao': 'MILPIN',
                'formato': '{milpin:<6}',
                'valor': None
            },
            '8': {
                'descricao': 'AJUSTEFCF',
                'formato': '{ajustefcf:<9}',
                'valor': None
            },
            '9': {
                'descricao': 'UCTSER',
                'formato': '{uctser:<6}',
                'valor': None
            },
            '10': {
                'descricao': 'AVLCMO',
                'formato': '{avlcmo:<6} {flag:1}',
                'valor': None
            },
            '11': {
                'descricao': 'ENGOLIMENTO',
                'formato': '{engolimento:<11} {flag:1}',
                'valor': None
            },
            '12': {
                'descricao': 'UCTPAR',
                'formato': '{uctpar:<6} {numnuc:<2}',
                'valor': None
            },
            '13': {
                'descricao': 'CPXPRESLV',
                'formato': '{cpxpreslv:<9}',
                'valor': None
            },
            '14': {
                'descricao': 'FLGUTERM',
                'formato': '{flgucterm:<9}',
                'valor': None
            },
            '15': {
                'descricao': 'UCTBUSLOC',
                'formato': '{uctbusloc:<9}',
                'valor': None
            },
            '16': {
                'descricao': 'PINT',
                'formato': '{pint:<4}',
                'valor': None
            },

            '17': {
                'descricao': 'UCTHEURFP',
                'formato': '{uctheurfp:<9} {numrel:>3} {numvar:>3}',
                'valor': None
            },
            '18': {
                'descricao': 'CONSTDADOS',
                'formato': '{constdados:<10} {flag:1}',
                'valor': None
            }
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