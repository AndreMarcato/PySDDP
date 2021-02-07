from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ReeTemplate(ArquivoEntrada):
    """
    Classe que contem os reservatórios equivalentes de energia do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Ree e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_rees = None

        self.bloco_ree = {
            'df': None,
            'formatoA': " {codigo:>3} {nome:<10}   {submercado:>3}  {mes:>2} {ano:>4}\n",
            'formatoB': " {codigo:>3} {nome:<10}   {submercado:>3}\n"
        }

        self.bloco_ficticias = {
            'flag': None,
            'formato': "{flag:>25}"
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