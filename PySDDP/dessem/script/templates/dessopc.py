# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class DessopcTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Dessopc do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.peninte = dict()
        self.deficit = dict()
        self.tolerilh = dict()
        self.trata_inviab_ilha = dict()
        self.regranptv = dict()
        self.engolimento = dict()
        self.solvertd = dict()
        self.zeralimuh = dict()
        self.fphadessem = dict()
        self.ucterm = dict()
        self.flgucterm = dict()
        self.constdados = dict()
        self.flgtitul = dict()
        self.ajustefcf = dict()
        self.milpin = dict()
        self.pint = dict()
        self.uctbusloc = dict()
        self.prsvlplfinal = dict()
        self.crossover = dict()
        self.uctheurfp = dict()
        self.cpxpreslv = dict()
        self.uctser = dict()
        self.uctpar = dict()
        self.avlcmo = dict()
        # Flag nao informada no manual:
        self.cplexlog = dict()
        self.impavl = dict()

        self.flags = {
            'peninte': {
                'descricao': 'PENINTE',
                'formato': '{peninte:<7} {fator:>5}\n',
                'valor': None
            },
            'deficit': {
                'descricao': 'DEFICIT',
                'formato': '{deficit:<7} {valor:1}\n',
                'valor': None
            },
            'tolerilh': {
                'descricao': 'TOLERILH',
                'formato': '{tolerilh:<8} {valor:1}\n',
                'valor': None
            },
            'trata_inviab_ilha': {
                'descricao': 'TRATA_INVIAB_ILHA',
                'formato': '{trata_inviab_ilha:<17}  {valor:1}\n',
                'valor': None
            },
            'regranptv': {
                'descricao': 'REGRANPTV',
                'formato': '{regranptv:<9} {regra:1} {flag:<2} {numpon:<2}\n',
                'valor': None
            },
            'engolimento': {
                'descricao': 'ENGOLIMENTO',
                'formato': '{engolimento:<11} {flag:1}\n',
                'valor': None
            },
            'solvertd': {
                'descricao': 'SOLVERTD',
                'formato': '{solvertd:<8}\n',
                'valor': None
            },
            'zeralimuh': {
                'descricao': 'ZERALIMUH',
                'formato': '{zeralimuh:<12}\n',
                'valor': None
            },
            'fphadessem': {
                'descricao': 'FPHADESSEM',
                'formato': '{fphadessem:<10}\n',
                'valor': None
            },
            'ucterm': {
                'descricao': 'UCTERM',
                'formato': '{ucterm:<6} {metodologia:1}\n',
                'valor': None
            },
            'flgucterm': {
                'descricao': 'FLGUCTERM',
                'formato': '{flgucterm:<9}\n',
                'valor': None
            },
            'constdados': {
                'descricao': 'CONSTDADOS',
                'formato': '{constdados:<10} {flag:1}\n',
                'valor': None
            },
            'flgtitul': {
                'descricao': 'FLGTITUL',
                'formato': '{flgtitul:<8}\n',
                'valor': None
            },
            'ajustefcf': {
                'descricao': 'AJUSTEFCF',
                'formato': '{ajustefcf:<9} {regra_1:1} {regra_2:1} {regra_3:1}\n',
                'valor': None
            },
            'milpin': {
                'descricao': 'MILPIN',
                'formato': '{milpin:<6}\n',
                'valor': None
            },
            'pint': {
                'descricao': 'PINT',
                'formato': '{pint:<4}\n',
                'valor': None
            },
            'uctbusloc': {
                'descricao': 'UCTBUSLOC',
                'formato': '{uctbusloc:<9}\n',
                'valor': None
            },
            'prsvlplfinal': {
                'descricao': 'PRSVLPLFINAL',
                'formato': '{prsvlplfinal:<12}\n',
                'valor': None
            },
            'crossover': {
                'descricao': 'CROSSOVER',
                'formato': '{crossover:<9} {campo_1:1} {campo_2:1} {campo_3:1} {campo_4:1} {campo_5:1}\n',
                'valor': None
            },
            'uctheurfp': {
                'descricao': 'UCTHEURFP',
                'formato': '{uctheurfp:<9} {numrel:>3} {numvar:>3}\n',
                'valor': None
            },
            'cpxpreslv': {
                'descricao': 'CPXPRESLV',
                'formato': '{cpxpreslv:<9}\n',
                'valor': None
            },
            'uctser': {
                'descricao': 'UCTSER',
                'formato': '{uctser:<6}\n',
                'valor': None
            },
            'uctpar': {
                'descricao': 'UCTPAR',
                'formato': '{uctpar:<6} {numnuc:<2}\n',
                'valor': None
            },
            'avlcmo': {
                'descricao': 'AVLCMO',
                'formato': '{avlcmo:<6} {flag:1}\n',
                'valor': None
            },
            'cplexlog': {
                'descricao': 'CPLEXLOG',
                'valor': None
            },
            'impavl': {
                'descricao': 'IMPALV',
                'formato': '{impavl:<6} {flag:1}\n',
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