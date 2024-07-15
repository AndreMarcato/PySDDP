from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class PolinJusTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo PolinJus do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.curva_jusante = None
        self.polinomio = None
        self.segmento = None
        self.afogamento = None

        self.comentarios = None

        self.bloco_curva_jusante = {
            'df': None,
            'descricao':
                " &;Usina;Indice;HjusRef\n",
            'formato': " {identificador};{codigo_usina};{id_curva};{altura_montante}\n",
            'colunas': ['identificador', 'codigo_usina', 'id_curva', 'altura_montante']
        }

        self.bloco_polinomio = {
            'df': None,
            'descricao':
                " &;Usina;Indice;nPol\n",
            'formato': " {identificador};{codigo_usina};{id_curva};{numero_segmentos}\n",
            'colunas': ['identificador', 'codigo_usina', 'id_curva', 'numero_segmentos']
        }

        self.bloco_segmento = {
            'df': None,
            'descricao':
                " &;Usina;IndCurva;IndPolin;QjusMin;QjusMax;a0;a1;a2;a3;a4\n",
            'formato': "{identificador};{codigo_usina};{id_curva};{id_segmento};{limite_inferior};{limite_superior};"
                       "{coeficiente_grau_0};{coeficiente_grau_1};{coeficiente_grau_2};{coeficiente_grau_3};"
                       "{coeficiente_grau_4}\n",
            'colunas': ['identificador', 'codigo_usina', 'id_curva', 'id_segmento', 'limite_inferior',
                        'limite_superior', 'coeficiente_grau_0', 'coeficiente_grau_1', 'coeficiente_grau_2',
                        'coeficiente_grau_3', 'coeficiente_grau_4']
        }

        self.bloco_afogamento = {
            'df': None,
            'descricao': None,
            'formato': "{identificador};{codigo_usina};{flag}\n",
            'colunas': ['identificador', 'codigo_usina', 'flag']
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
