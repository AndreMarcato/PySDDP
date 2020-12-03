from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class AreacontTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Areacont do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.comentarios = None
        self.area = None
        self.usina = None

        self.bloco_area = {
            'df': None,
            'formato':
                "{area:>3}      {nome_area:<39}\n",
        }

        self.bloco_usina = {
            'df': None,
            'formato':
                "{area:>3} {conjunto:>1}  {tipo:>1} {usina:>3} {nome_usina:<39}\n",
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
