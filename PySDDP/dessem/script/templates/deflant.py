# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class DeflAntTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Deflant do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.defluencias_uhe_anteriores = None
        self.defluencias_uhe_anteriores_df = None

        self.dados = {
            "defluencias_uhe_anteriores": {
                'descricao': 'Defluencias Anteriores ao Inicio do Estudo\n',
                'cabecalho':
                    "&        Mont Jus TpJ   di hi m df hf m     defluencia\n"
                    "&X       XXX  XXX  X    XX XX X XX XX X     XXXXXXXXXX\n",
                'formato':
                    "{mne: <6} {numuhemon: >3} {numuhejus: >3} {ent:1} {di:>2} "
                    "{hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {defluencia: >10}\n",
                'valor': None
            }
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