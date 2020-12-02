# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class ArquivosTemplate(ArquivoEntrada):
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
        self.const = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        self.dger = None
        self.sistema = None
        self.confhd = None
        self.modif = None
        self.conft = None
        self.term = None
        self.clast = None
        self.exph = None
        self.expt = None
        self.patamar = None
        self.cortes = None
        self.cortesh = None
        self.pmo = None
        self.parp = None
        self.forward = None
        self.forwarh = None
        self.shist = None
        self.manutt = None
        self.newdesp = None
        self.vazpast = None
        self.itaipu = None
        self.bid = None
        self.c_adic = None
        self.loss = None
        self.gtminpat = None
        self.elnino = None
        self.ensoaux = None
        self.dsvagua = None
        self.penalid = None
        self.curva = None
        self.agrint = None
        self.adterm = None
        self.ghmin = None
        self.sar = None
        self.cvar = None
        self.ree = None
        self.re = None
        self.tecno = None

        self.arquivos_fixo = {
            "dger": {
                'tipo': 'binario',
                'funcao': 'entrada',
                'descricao': 'CADASTRO DAS U.HIDRELETRICAS',
                'valor': 'HIDR.DAT'
            },
            "sistema": {
                'tipo': 'binario',
                'funcao': 'entrada',
                'descricao': 'HISTRORICO DE VAZOES UHES   ',
                'valor': 'VAZOES.DAT'
            }
        }

        self.arquivos = {
            "dger": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS GERAIS                ',
                'valor': None,
                'ordem': 1
            },
            "sistema": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DOS SUBSISTEMAS       ',
                'valor': None,
                'ordem': 2
            },
            "confhd": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'CONFIGURACAO HIDRAULICA     ',
                'valor': None,
                'ordem': 3
            },
            "modif": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ALTERACAO DADOS USINAS HIDRO',
                'valor': None,
                'ordem': 4
            },
            "conft": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'CONFIGURACAO TERMICA        ',
                'valor': None,
                'ordem': 5
            },
            "term": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DAS USINAS TERMICAS   ',
                'valor': None,
                'ordem': 6
            },
            "clast": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DAS CLASSES TERMICAS  ',
                'valor': None,
                'ordem': 7
            },
            "exph": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DE EXPANSAO HIDRAULICA',
                'valor': None,
                'ordem': 8
            },
            "expt": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE EXPANSAO TERMICA ',
                'valor': None,
                'ordem': 9
            },
            "patamar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE PATAMARES MERCADO',
                'valor': None,
                'ordem': 10
            },
            "cortes": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CORTES DE BENDERS',
                'valor': None,
                'ordem': 11
            },
            "cortesh": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CABECALHO CORTES ',
                'valor': None,
                'ordem': 12
            },
            "pmo": {
                'tipo': 'texto',
                'funcao': 'saida',
                'descricao': 'RELATORIO DE CONVERGENCIA   ',
                'valor': None,
                'ordem': 13
            },
            "parp": {
                'tipo': 'texto',
                'funcao': 'saida',
                'descricao': 'RELATORIO DE E. SINTETICAS  ',
                'valor': None,
                'ordem': 14
            },
            "forward": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'RELATORIO DETALHADO FORWARD ',
                'valor': None,
                'ordem': 15
            },
            "forwarh": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CABECALHO FORWARD',
                'valor': None,
                'ordem': 16
            },
            "shist": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE S.HISTORICAS S.F.',
                'valor': None,
                'ordem': 17
            },
            "manutt": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': "ARQUIVO DE MANUT.PROG. UTE'S",
                'valor': None,
                'ordem': 18
            },
            "newdesp": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO P/DESPACHO HIDROTERM',
                'valor': None,
                'ordem': 19
            },
            "vazpast": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/TEND. HIDROLOGICA ',
                'valor': None,
                'ordem': 20
            },
            "itaipu": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/DADOS DE ITAIPU   ',
                'valor': None,
                'ordem': 21
            },
            "bid": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/DEMAND S. BIDDING ',
                'valor': None,
                'ordem': 22
            },
            "c_adic": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/CARGAS ADICIONAIS ',
                'valor': None,
                'ordem': 23
            },
            "loss": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/FATORES DE PERDAS ',
                'valor': None,
                'ordem': 24
            },
            "gtminpat": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/PATAMARES GTMIN   ',
                'valor': None,
                'ordem': 25
            },
            "elnino": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO ENSO 1              ',
                'valor': None,
                'ordem': 26
            },
            "ensoaux": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO ENSO 2              ',
                'valor': None,
                'ordem': 27
            },
            "dsvagua": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DSVAGUA             ',
                'valor': None,
                'ordem': 28
            },
            "penalid": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO P/PENALID. POR DESV.',
                'valor': None,
                'ordem': 29
            },
            "curva": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C.GUIA / PENAL.VMINT',
                'valor': None,
                'ordem': 30
            },
            "agrint": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AGRUPAMENTO LIVRE   ',
                'valor': None,
                'ordem': 31
            },
            "adterm": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DESP. ANTEC. GNL    ',
                'valor': None,
                'ordem': 32
            },
            "ghmin": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO GER. HIDR. MIN      ',
                'valor': None,
                'ordem': 33
            },
            "sar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AVERSAO RISCO - SAR ',
                'valor': None,
                'ordem': 34
            },
            "cvar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AVERSAO RISCO - CVAR',
                'valor': None,
                'ordem': 35
            },
            "ree": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DOS RESER.EQ.ENERGIA  ',
                'valor': None,
                'ordem': 36
            },
            "re": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO RESTRICOES ELETRICAS',
                'valor': None,
                'ordem': 37
            },
            "tecno": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE TECNOLOGIAS      ',
                'valor': None,
                'ordem': 38
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
