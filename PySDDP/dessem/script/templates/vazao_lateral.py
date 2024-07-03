from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class VazaoLateralTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Vazao Lateral do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.defluencia = None
        self.posto = None
        self.usina = None

        self.comentarios = None

        self.bloco_defluencia = {
            'df': None,
            'descricao':
                "&;UsinaInfluenciada;FatorTurbinamento;FatorVertimento\n",
            'formato': "{identificador};{codigo_usina_influenciada};{fator_turbinamento};{fator_vertimento}\n",
            'colunas': ['identificador', 'codigo_usina_influenciada', 'fator_turbinamento', 'fator_vertimento']
        }

        self.bloco_posto = {
            'df': None,
            'descricao':
                "&;UsinaInfluenciada;CodigoPostoInfluenciador;Fator\n",
            'formato': "{identificador};{codigo_usina_influenciada};{codigo_posto};{fator}\n",
            'colunas': ['identificador', 'codigo_usina_influenciada', 'codigo_posto', 'fator']
        }

        self.bloco_usina = {
            'df': None,
            'descricao':
                "&;UsinaInfluenciada;CodigoUsinaInfluenciadora;Fator\n",
            'formato': "{identificador};{codigo_usina_influenciada};{codigo_usina_influenciadora};{fator}\n",
            'colunas': ['identificador', 'codigo_usina_influenciada', 'codigo_usina_influenciadora', 'fator']
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
