# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada


class DadGnlTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo DadGnl do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Além disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.bloco_tg = {
            'descricao': '&----------------------------------------------------------------------------------------\n'
                         '&         BLOCO 1 *** TERMICAS A GNL ***\n'
                         '&         (REGISTRO TG)\n'
                         '&----------------------------------------------------------------------------------------\n',
            'cabecalho': '&      Usina           Est           Pat 1               Pat 2               Pat3\n'
                         '&   cod  ss      nome   ip   infl disp    cvu    infl disp    cvu    infl disp    cvu\n'
                         '&x  xxx  xx   xxxxxxxxxxXX   xxxxxXXXXXxxxxxxxxxxXXXXXxxxxxXXXXXXXXXXxxxxxXXXXXxxxxxxxxxx\n',
            'formato': '{id:<2}  {cod_ute:>3}  {id_subsist:>2}   {nome_ute:<10}{id_est:>2}   {ger_min_pat1:>5}'
                       '{cap_min_pat1:>5}{cvu_pat1:>10}{ger_min_pat2:>5}{cap_min_pat2:>5}{cvu_pat2:>10}'
                       '{ger_min_pat3:>5}{cap_min_pat3:>5}{cvu_pat3:>10}\n',
            'comentario': list(),
            'df': None
        }

        self.bloco_gs = {
            'descricao': '&----------------------------------------------------------------------------------------\n'
                         '&         BLOCO 2 *** NUMERO DE SEMANAS ***\n'
                         '&         (REGISTRO GS)\n'
                         '&----------------------------------------------------------------------------------------\n',
            'cabecalho': '&  mes  semanas\n'
                         '&x  xx   x\n',
            'formato': '{id:<2}  {id_mes:>2}   {num_interv:1}\n',
            'comentario': list(),
            'df': None
        }

        self.bloco_nl = {
            'descricao': '&----------------------------------------------------------------------------------------\n'
                         '&         BLOCO 3 *** LAG DE ANTECIPACAO DE DESPACHO ***\n'
                         '&         (REGISTRO NL)\n'
                         '&----------------------------------------------------------------------------------------\n',
            'cabecalho': '&   cod  ss  lag\n'
                         '&x  xxx  xx   x\n',
            'formato': '{id:<2}  {cod_ute:>3}  {id_subsist:>2}   {lag:1}\n',
            'comentario': list(),
            'df': None
        }

        self.bloco_gl = {
            'descricao': '&----------------------------------------------------------------------------------------\n'
                         '&         BLOCO 4 *** GERACOES DE TERMICAS GNL JA COMANDADAS ***\n'
                         '&         (REGISTRO GL)\n'
                         '&----------------------------------------------------------------------------------------\n',
            'cabecalho': '&    Usina             Pat 1           Pat 2          Pat3\n'
                         '&   cod  ss  sem    geracao   dur  geracao   dur  geracao   dur  data inic\n'
                         '&x  xxx  xx   xx   xxxxxxxxxxXXXXXxxxxxxxxxxXXXXXxxxxxxxxxxXXXXX xxXXxxxx\n',
            'formato': '{id:<2}  {cod_ute:>3}  {id_subsist:>2}   {sem:>2}   {ger_pat1:>10}{dur_pat1:>5}{ger_pat2:>10}'
                       '{dur_pat2:>5}{ger_pat3:>10}{dur_pat3:>5} {dia:>2}{mes:>2}{ano:>4}\n',
            'comentario': list(),
            'df': None
        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Método abstrato do ArquivoEntrada sendo repassado para as classes filhas.
        :param args: Conjunto de parâmetros obrigatórios.
        :param kwargs: Conjunto de parâmetros opcionais.
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Método abstrato da ArquivoEntrada sendo repassado para as classes filhas.
        :param args: conjunto de parâmetros obrigatórios.
        :param kwargs: conjunto de parâmetros opcionais.
        :return:
        """
