# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


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
            "hidr": {
                'tipo': 'binario',
                'funcao': 'entrada',
                'descricao': 'CADASTRO DAS U.HIDRELETRICAS',
                'valor': 'HIDR.DAT'
            },
            "vazoes": {
                'tipo': 'binario',
                'funcao': 'entrada',
                'descricao': 'HISTRORICO DE VAZOES UHES   ',
                'manual': '',
                'valor': 'VAZOES.DAT'
            }
        }

        self.arquivos = {
            "dger": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS GERAIS                ',
                'manual': 'Nome do arquivo de dados gerais.',
                'valor': None,
                'ordem': 1
            },
            "sistema": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DOS SUBSISTEMAS       ',
                'manual': 'Nome do arquivo de dados dos subsistemas/submercados.',
                'valor': None,
                'ordem': 2
            },
            "confhd": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'CONFIGURACAO HIDRAULICA     ',
                'manual': 'Nome do arquivo de dados da configuração hidroelétrica.',
                'valor': None,
                'ordem': 3
            },
            "modif": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ALTERACAO DADOS USINAS HIDRO',
                'manual': 'Nome do arquivo de dados de alteração da configuração de usinas hidroelétricas.',
                'valor': None,
                'ordem': 4
            },
            "conft": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'CONFIGURACAO TERMICA        ',
                'manual': 'Nome do arquivo de dados da configuração termoelétrica.',
                'valor': None,
                'ordem': 5
            },
            "term": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DAS USINAS TERMICAS   ',
                'manual': 'Nome do arquivo de dados das usinas termoelétricas.',
                'valor': None,
                'ordem': 6
            },
            "clast": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DAS CLASSES TERMICAS  ',
                'manual': 'Nome do arquivo de dados de classes térmicas.',
                'valor': None,
                'ordem': 7
            },
            "exph": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DE EXPANSAO HIDRAULICA',
                'manual': 'Nome do arquivo de dados que contém a expansão das usinas hidroelétricas.',
                'valor': None,
                'ordem': 8
            },
            "expt": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE EXPANSAO TERMICA ',
                'manual': 'Nome do arquivo de dados que contém a expansão das usinas termoelétricas.',
                'valor': None,
                'ordem': 9
            },
            "patamar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'manual': 'Nome do arquivo de dados que contém os patamares de mercado.',
                'descricao': 'ARQUIVO DE PATAMARES MERCADO',
                'valor': None,
                'ordem': 10
            },
            "cortes": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CORTES DE BENDERS',
                'manual': 'Nome do arquivo que contém a função de custo futuro - cortes de Benders.',
                'valor': None,
                'ordem': 11
            },
            "cortesh": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CABECALHO CORTES ',
                'manual': 'Nome do arquivo que contém os apontadores de início da função de custo futuro de cada ' +
                          'stágio.',
                'valor': None,
                'ordem': 12
            },
            "pmo": {
                'tipo': 'texto',
                'funcao': 'saida',
                'descricao': 'RELATORIO DE CONVERGENCIA   ',
                'manual': 'Nome do arquivo que contém o relatório de acompanhamento do programa.',
                'valor': None,
                'ordem': 13
            },
            "parp": {
                'tipo': 'texto',
                'funcao': 'saida',
                'descricao': 'RELATORIO DE E. SINTETICAS  ',
                'manual': 'Nome do arquivo que contém o relatório de acompanhamento do modelo PAR(p).',
                'valor': None,
                'ordem': 14
            },
            "forward": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'RELATORIO DETALHADO FORWARD ',
                'manual': 'Nome do arquivo que contém os dados para obtenção do relatório opcional detalhado de '+
                          'acompanhamento da simulação forward.',
                'valor': None,
                'ordem': 15
            },
            "forwarh": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO DE CABECALHO FORWARD',
                'manual': 'Nome do arquivo que contém o cabeçalho do arquivo de acompanhamento da simulação forward.',
                'valor': None,
                'ordem': 16
            },
            "shist": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE S.HISTORICAS S.F.',
                'manual': 'Nome do arquivo que contém os parâmetros necessários à simulação com a série histórica.',
                'valor': None,
                'ordem': 17
            },
            "manutt": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': "ARQUIVO DE MANUT.PROG. UTE'S",
                'manual': 'Nome do arquivo que contém informações sobre manutenções programadas em usinas térmicas, ' +
                        'para o cálculo da indisponibilidade programada.',
                'valor': None,
                'ordem': 18
            },
            "newdesp": {
                'tipo': 'binario',
                'funcao': 'saida',
                'descricao': 'ARQUIVO P/DESPACHO HIDROTERM',
                'manual': 'Nome do arquivo de saída que contém as configurações dos sistemas, das usinas térmicas ' +
                          ' das hidroelétricas.',
                'valor': None,
                'ordem': 19
            },
            "vazpast": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/TEND. HIDROLOGICA ',
                'manual': 'Nome do arquivo que contém a tendência hidrológica.',
                'valor': None,
                'ordem': 20
            },
            "itaipu": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/DADOS DE ITAIPU   ',
                'manual': 'Nome do arquivo que contém os dados referentes à usina de Itaipu (não usado).',
                'valor': None,
                'ordem': 21
            },
            "bid": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/DEMAND S. BIDDING ',
                'manual': 'Nome do arquivo que contém informações sobre o “bidding” de demanda (não implementado).',
                'valor': None,
                'ordem': 22
            },
            "c_adic": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/CARGAS ADICIONAIS ',
                'manual': 'Nome do arquivo que contém dados de cargas adicionais.',
                'valor': None,
                'ordem': 23
            },
            "loss": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/FATORES DE PERDAS ',
                'manual': 'Nome do arquivo que contém informações sobre perdas.',
                'valor': None,
                'ordem': 24
            },
            "gtminpat": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C/PATAMARES GTMIN   ',
                'manual': 'Nome do arquivo descrevendo geração térmica mínima por patamar.',
                'valor': None,
                'ordem': 25
            },
            "elnino": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO ENSO 1              ',
                'manual': 'Nome do arquivo com os índices mensais ENSO (não implementado).',
                'valor': None,
                'ordem': 26
            },
            "ensoaux": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO ENSO 2              ',
                'manual': 'Nome do arquivo com as fases ENSO p/ cada REE (não implementado).',
                'valor': None,
                'ordem': 27
            },
            "dsvagua": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DSVAGUA             ',
                'manual': 'Nome do arquivo com outros usos da água (irrigação, por exemplo).',
                'valor': None,
                'ordem': 28
            },
            "penalid": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO P/PENALID. POR DESV.',
                'manual': 'Nome do arquivo com penalidades',
                'valor': None,
                'ordem': 29
            },
            "curva": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO C.GUIA / PENAL.VMINT',
                'manual': 'Nome do arquivo com dados da curva de aversão ou com penalidades para o não atendimento ' +
                          'ao volume mínimo operativo.',
                'valor': None,
                'ordem': 30
            },
            "agrint": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AGRUPAMENTO LIVRE   ',
                'manual': 'Nome do arquivo com dados de agrupamentos de intercâmbio',
                'valor': None,
                'ordem': 31
            },
            "adterm": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DESP. ANTEC. GNL    ',
                'manual': 'Nome do arquivo com dados de antecipação de despacho de usinas térmicas a gás natural liquefeito (GNL)',
                'valor': None,
                'ordem': 32
            },
            "ghmin": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO GER. HIDR. MIN      ',
                'manual': 'Nome do arquivo com os dados de geração hidráulica mínima.',
                'valor': None,
                'ordem': 33
            },
            "sar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AVERSAO RISCO - SAR ',
                'manual': 'Nome do arquivo de dados do Mecanismo de Aversão a Risco: SAR',
                'valor': None,
                'ordem': 34
            },
            "cvar": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO AVERSAO RISCO - CVAR',
                'manual': 'Nome do arquivo de dados do Mecanismo de Aversão a Risco: CVaR',
                'valor': None,
                'ordem': 35
            },
            "ree": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'DADOS DOS RESER.EQ.ENERGIA  ',
                'manual': 'Nome do arquivo de dados dos REEs',
                'valor': None,
                'ordem': 36
            },
            "re": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO RESTRICOES ELETRICAS',
                'manual': 'Nome do arquivo contendo os dados das restrições elétricas internas aos REEs',
                'valor': None,
                'ordem': 37
            },
            "tecno": {
                'tipo': 'texto',
                'funcao': 'entrada',
                'descricao': 'ARQUIVO DE TECNOLOGIAS      ',
                'manual': 'Nome do arquivo contendo as tecnologias de geração de energia elétrica',
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
