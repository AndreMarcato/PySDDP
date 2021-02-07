from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class SistemaTemplate(ArquivoEntrada):
    """
    Classe que contem os submercados a serem considerados pelo newave (Geralmente: SE, S, N, NE).
    Esta classe tem como intuito fornecer duck typing para a classe Sistema e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_sistemas = None
        self.numero_intercambios = None

        self.bloco_patamar_deficit = {
            'nr_pat_def': None,
            'descricao': "Número de patamares de déficit"
            }

        self.bloco_sistema = {
            'df': None,
            'descricao': "Bloco com nome/códigos dos submercados e respectivas profundidades/custos de déficit."
            }

        self.bloco_intercambio = {
            'df': None,
            'descricao': "Bloco com os limites de intercâmbio de energia de/para e para/de entre os submercados."
            }

        self.bloco_mercado = {
            'df': None,
            'descricao': 'Bloco com o mercado bruto de cada um dos submercados.'
            }

        self.bloco_nao_simuladas = {
            'df': None,
            'descricao': 'Geracao de energia proveniente de usinas não simuladas.'
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