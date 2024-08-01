# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada


class PolinJusTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo que contem os dados das curvas de jusante
    das usinas hidreletricas (nome nos decks consultados do Decomp: Polinjus.dat).
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.bloco_curvajus = {
            'descricao': '& Proposta arquivo polijus.dat\n'
                         '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n'
                         '& Cadastro das famílias de curvas de jusante\n'
                         '&\n'
                         '& Usina: código da usina hidráulica\n'
                         '& Índice: índice da família (sequencial)\n'
                         '& HjusRef: nível de montante da usina de jusante para referência da família\n'
                         '& nPol: quantidade de polinômios da família\n'
                         '&\n'
                         '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n',
            'cabecalho': '&         Usina    Indice   HjusRef    nPol\n'
                         '&XXXXXXX   XXXX     XXX    XXXXXXXXXX  XXX\n',
            'formato': '{id:<8}   {cod_uhe:>4}     {id_cur_jus:>3}    {alt_jus_ref:>10}  {quant_pol:>3}\n',
            'df': None
        }

        self.bloco_pppjus = {
            'descricao': '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n'
                         '&\n'
                         '& Cadastro dos coeficientes dos polinômios por partes das curvas de jusante\n'
                         '&\n'
                         '& Usina: código da usina hidráulica\n'
                         '& Índice: índice da família (sequencial)\n'
                         '& QjusMin: limite inferior de vazão de jusante (defluência mais lateral) para janela de '
                         'validade do polinômio\n'
                         '& QjusMax: limite superior de vazão de jusante (defluência mais lateral) para janela de '
                         'validade do polinômio\n'
                         '& a0 : coeficiente de grau 0 do polinômio\n'
                         '& a1 : coeficiente de grau 1 do polinômio\n'
                         '& a2 : coeficiente de grau 2 do polinômio\n'
                         '& a3 : coeficiente de grau 3 do polinômio\n'
                         '& a4 : coeficiente de grau 4 do polinômio\n'
                         '&\n'
                         '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n',
            'cabecalho': '&          Usina    Indice      QjusMin               QjusMax                  a0            '
                         '      a1                    a2                   a3                   a4\n'
                         '&XXXXX     XXXX     XXX     XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX XX'
                         'XXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX\n',
            'formato': '{id:<6}     {cod_uhe:<4}     {id_cur_jus:>3}     {lim_inf_vaz:>20} {lim_sup_vaz:>20} '
                         '{coef_grau0_pol_jus:>20} {coef_grau1_pol_jus:>20} {coef_grau2_pol_jus:>20} '
                       '{coef_grau3_pol_jus:>20} {coef_grau4_pol_jus:>20}\n',
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
