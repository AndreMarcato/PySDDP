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
        self.const = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        self.caso = None
        self.titulo = None
        self.vazoes = None
        self.dadger = None
        self.mapfcf = None
        self.crtfcf = None
        self.cadusih = None
        self.operuh = None
        self.deflant = None
        self.cadterm = None
        self.operut = None
        self.indelet = None
        self.ilstri = None
        self.cotasr11 = None
        self.simul = None
        self.areacont = None
        self.respot = None
        self.mlt = None
        self.tolperd = None
        self.curvtviag = None
        self.ptoper = None
        self.infofcf = None
        self.meta = None
        self.ree = None
        self.eolica = None
        self.rampas = None
        self.rmpflx = None
        self.restseg = None
        self.respotele = None
        self.rstlpp = None
        self.solar = None
        self.bateria = None
        self.versdeco = None
        self.ilibs = None
        self.dessopc = None

        # O arquivo script.arq possuem tanto dados quanto nomes de arquivos,
        # então resolvi criar duas estruturas para armazenar estas informações
        # e ficar mais fácil na hora da escrita
        # {chave: valor}
        # chave -> mneumonico ou nome do registro
        # valor -> dicionários contendo:
        #    tipo: 0 para dados ou 1 para arquivos
        #    descricao: Descricação de cada mneumomico usada na impressao do arquivo
        self.dados = {
            "caso": {
                'tipo': 0,
                'descricao': 'NOME DO CASO',
                'valor': None
            },
            "titulo": {
                'tipo': 0,
                'descricao': 'TITULO DO ESTUDO',
                'valor': None
            }
        }
        self.arquivos = {
            "vazoes": {
                'tipo': 1,
                'descricao': 'VAZOES NATURAIS',
                'valor': None
            },
            "dadger": {
                'tipo': 1,
                'descricao': 'DADOS GERAIS DO PROBLEMA',
                'valor': None
            },
            "mapfcf": {
                'tipo': 1,
                'descricao': 'MAPA DOS CORTES DO DECOMP',
                'valor': None
            },
            "cortfcf": {
                'tipo': 1,
                'descricao': 'CORTES DO DECOMP',
                'valor': None
            },
            "cadusih": {
                'tipo': 1,
                'descricao': 'CADASTRO DAS USINAS HIDROELETRICAS',
                'valor': None
            },
            "operuh": {
                'tipo': 1,
                'descricao': 'RESTRICOES DE OPERACAO HIDRAULICA',
                'valor': None
            },
            "deflant": {
                'tipo': 1,
                'descricao': 'DEFLUENCIAS ANTERIORES',
                'valor': None
            },
            "cadterm": {
                'tipo': 1,
                'descricao': 'CADASTRO DAS USINAS TERMICAS',
                'valor': None
            },
            "operut": {
                'tipo': 1,
                'descricao': 'OPERACAO DAS UNIDADES TERMICAS',
                'valor': None
            },
            "indelet": {
                'tipo': 1,
                'descricao': 'ARQ. INDICE DA REDE ELETRICA',
                'valor': None
            },
            "ilstri": {
                'tipo': 1,
                'descricao': 'CANAL PEREIRA BARRETO',
                'valor': None
            },
            "cotasr11": {
                'tipo': 1,
                'descricao': 'COTAS NA R11 ANTERIORES',
                'valor': None
            },
            "simul": {
                'tipo': 1,
                'descricao': 'ARQ. COM DADOS PARA A SIMULACAO',
                'valor': None
            },
            "areacont": {
                'tipo': 1,
                'descricao': 'CADASTRO DE RESERVA DE POTENCIA',
                'valor': None
            },
            "respot": {
                'tipo': 1,
                'descricao': 'ESTUDO DE  RESERVA DE POTENCIA',
                'valor': None
            },
            "mlt": {
                'tipo': 1,
                'descricao': 'DADOS PARA A FPHA (MLT)',
                'valor': None
            },
            "tolperd": {
                'tipo': 1,
                'descricao': 'ARQ. DE TOLERANCIAS DAS PERDAS',
                'valor': None
            },
            "curvtviag": {
                'tipo': 1,
                'descricao': 'CURVA DE PROPAGACAO DO TVIAG',
                'valor': None
            },
            "ptoper": {
                'tipo': 1,
                'descricao': 'PONTO DE OPERACAO DE USINAS GNL',
                'valor': None
            },
            "infofcf": {
                'tipo': 1,
                'descricao': 'INFORMACAO SOBRE OS CORTES',
                'valor': None
            },
            "meta": {
                'tipo': 1,
                'descricao': 'RESTRICOES DE METAS',
                'valor': None
            },
            "ree": {
                'tipo': 1,
                'descricao': 'RESERVATORIO EQUIVALENTES DE ENERGIA',
                'valor': None
            },
            "eolica": {
                'tipo': 1,
                'descricao': 'USINAS EOLICAS - RENOVAVEIS',
                'valor': None
            },
            "rampas": {
                'tipo': 1,
                'descricao': 'ARQUIVO DE TRAJETORIAS',
                'valor': None
            },
            "rmpflx": {
                'tipo': 1,
                'descricao': 'RESTRICOES RAMPA REDE ELETRICA',
                'valor': None
            },
            "rstlpp": {
                'tipo': 1,
                'descricao': 'RESTRICOES LPP',
                'valor': None
            },
            "restseg": {
                'tipo': 1,
                'descricao': 'RESTRICOES TABELA',
                'valor': None
            },
            "respotele": {
                'tipo': 1,
                'descricao': 'RESERVA DE POTENCIA REDE ELETRICA',
                'valor': None
            },
            "solar": {
                'tipo': 1,
                'descricao': 'USINAS SOLARES - RENOVAVEIS',
                'valor': None
            },
            "bateria": {
                'tipo': 1,
                'descricao': 'UNIDADE DE ARMAZENAMENTO DE ENERGIA',
                'valor': None
            },
            "versdeco": {
                'tipo': 1,
                'descricao': 'NUMERO DA VERSAO DO DECOMP',
                'valor': None
            },
            "ilibs": {
                'tipo': 1,
                'descricao': '',
                'valor': None
            },
            "dessopc": {
                'tipo': 1,
                'descricao': '',
                'valor': None
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
