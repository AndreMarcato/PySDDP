# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class OperutTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Operut do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.condicoes_iniciais = None
        self.condicoes_iniciais_df = None

        self.limites_condicoes = None
        self.limites_condicoes_df = None

        self.bloco_init = {
            'descricao':
                '& CONDICOES INICIAIS DAS UNIDADES\n'
                '&\n'
                'INIT\n',
            'cabecalho':
                '&us     nome       ug   st   GerInic     tempo MH A/D T  TITULINFLX\n'
                '&XX XXXXXXXXXXXX  XXX   XX   XXXXXXXXXX  XXXXX  X  X  X  XXXXXXXXXX\n',
            'formato':
                "{us:>3} {nome:<12} {ug:>3}   {st:>2}   {GerInic:>10}  {tempo:>5}  {MH:1}  {A/D:1}  {T:1}  "
                "{TITULINFLX:>10}\n",
            'valor': None
        }

        self.bloco_oper = {
            'descricao':
                '&\n'
                '&\n'
                '& LIMITES E CONDICOES OPERACIONAIS DAS UNIDADES\n'
                '&\n'
                'OPER\n',
            'cabecalho':
                '&us    nome      un di hi m df hf m Gmin     Gmax       Custo \n'
                '&XX XXXXXXXXXXXX XX XX XX X XX XX X XXXXXXXXXXxxxxxxxxxxXXXXXXXXXX\n',
            'formato':
                '{us:>3} {nome:<12}{un:>2} {di:>2} {hi:>2} {mi:1} '
                '{df:>2} {hf:>2} {mf:1} {Gmin:>10}{Gmax:>10}{Custo:<10}\n',
            'valor': None
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