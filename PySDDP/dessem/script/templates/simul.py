from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class SimulTemplate(ArquivoEntrada):
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
        self.periodo = None
        self.disc = None
        self.voli = None
        self.oper = None

        self.bloco_periodo = {
            'df': None,
            'formato':
                "{dia:>3} {hora:<39} {meiahora:>3} {mes:<39} {ano:>3} {flag_restr:<39}\n",
        }

        self.bloco_disc = {
            'df': None,
            'formato':
                "{mneumo:<39} {dia:>3} {hora:<39} {meiahora:>3} {duracao:>3} {flag_restr:<39}\n",
        }

        self.bloco_voli = {
            'df': None,
            'formato':
                "{mneumo:<39} {usina:>3} {nome:<39} {volume:>3}\n",
        }

        self.bloco_oper = {
            'df': None,
            'formato':
                "{mneumo:<39} {usina:>3} {tipo:<39} {nome:>3} {dia_inicio:<39} {hora_inicio:>3} {meiahora_inicio:<39} "
                "{dia_final:>3} {hora_final:<39} {meiahora_final:>3} {tipo_vazao:<39} {id_tipovazao:>3}"
                "{vazao_retirada:<39} {geracao:>3}\n",
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