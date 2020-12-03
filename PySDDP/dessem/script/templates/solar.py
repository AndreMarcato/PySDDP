from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class SolarTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Renovaveis do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.usina = None
        self.submercado = None
        self.barra = None
        self.geracao = None
        self.comentarios = None

        self.blocos = None

        self.bloco_usina = {
            'df': None,
            'descricao':
                "&      ;CODIGO;NOME  Usina e Barra                      ;PMAX       ;FCAP;C;\n",
            'cabecalho':
                "&XXXXXX;XXXXX ;XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ;XXXXXXXXXX ;XXX ;X;\n",
            'formato':
                "{mneumo:>6};{codigo:>5};{nome:>41};{pmax:>10};{fcap:>3};{c:>1};\n",
            'colunas': ['&', 'CODIGO', 'NOME Usina e Barra', 'PMAX', 'FCAP', 'C', 'LIXO']
        }

        self.bloco_barra = {
            'df': None,
            'descricao':
                "&           ;CODIGO;BARRA ;\n",
            'cabecalho':
                "&XXXXXXXXXX ;XXXXX ;XXXXX ;\n",
            'formato':
                "{mneumo:>11};{codigo:>5};{barra:>5};\n",
            'colunas': ['&', 'CODIGO', 'BARRA']
        }

        self.bloco_submercado = {
            'df': None,
            'descricao':
                "&          ;CODIGO;SBM;\n",
            'cabecalho':
                "&XXXXXXXXXX;XXXXX ;XX ;\n",
            'formato':
                "{mneumo:>10};{codigo:>5};{submercado:>3};\n",
            'colunas': ['&', 'CODIGO', 'SBM']
        }

        self.bloco_geracao = {
            'df': None,
            'descricao':
                "&              ;CODIGO;       DATA          ;   GERACAO ;\n",
            'cabecalho':
                "&XXXXXXXXXXXXXX;XXXXX ;XX ;XX ;X ;XX ;XX ;X ;XXXXXXXXXX ;\n",
            'formato':
                "{mneumo:>14};{codigo:>5};{DI:>2};{HI:>2};{FI:<2};{DF:>2};{HF:>2};{FF:<2};{geracao:>10};\n",
            'colunas': ['&', 'CODIGO', 'DI', 'HI', 'FI', 'DF', 'HF', 'FF', 'GERACAO']
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