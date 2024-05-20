from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada

class TermTemplate(ArquivoEntrada):
    """
    Classe que contem o cadastro de usinas termicas do caso em estudo.
    Esta classe tem como intuito fornecer duck typing para a classe Term e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_terms = None

        self.bloco_term = {
            'df': None,
        }

        # listas referentes ao dicionário REE
        self._term = {
                    'codigo': list(),
                    'nome': list(),
                    'pot': list(),
                    'fcmax': list(),
                    'teif': list(),
                    'ip': list(),
                    'gtmin': list()
        }

        self._codigo = {
                    'descricao': 'Codigo da UTE',
                    'valor': list()
                 }

        self._nome =  {
                    'descricao': 'Nome da UTE',
                    'valor': list()
                 }

        self._pot =  {
                    'descricao': 'Potencia Instalada da UTE',
                    'valor': list()
                 }

        self._fcmax =  {
                    'descricao': 'Fator de capacidade máximo da UTE',
                    'valor': list()
                 }

        self._teif =  {
                    'descricao': 'Taxa Equivalente de Indisponibilidade Forcada',
                    'valor': list()
                 }

        self._ip =  {
                    'descricao': 'Indisponibilidade Programada',
                    'valor': list()
                 }

        self._gtmin = {
            'descricao': 'Indisponibilidade Programada',
            'valor': list(),
            'valor_2': list(),
            'valor_3': list(),
            'valor_4': list(),
            'valor_5': list(),
            'valor_6': list(),
            'valor_7': list(),
            'valor_8': list(),
            'valor_9': list(),
            'valor_10': list(),
            'valor_11': list(),
            'valor_12': list(),
            'valor_DemaisAnos': list()
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