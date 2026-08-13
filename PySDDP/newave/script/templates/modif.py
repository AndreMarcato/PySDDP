from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ModifTemplate(ArquivoEntrada):
    """
    Classe que contem as modificações de cadastro de todas as Usinas Hidrelétricas do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Modif e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita

    O MODIF.DAT nao possui uma chave unica por registro: uma mesma usina hidreletrica pode ter varias
    modificacoes de cadastro (uma por palavra-chave/vigencia) ao longo do arquivo. Por isso, assim como
    Expt.get/Expt.put e Manutt.get/Manutt.put (blocos que tambem nao possuem chave natural), a identidade de
    cada modificacao em Modif.get/Modif.put e a sua posicao (indice, 0-based) na lista de modificacoes,
    preservada pela chave somente-leitura ``indice_original``.

    Cada registro fisico comeca com uma palavra-chave que determina o formato dos campos ``valorA``/``valorB``/
    ``mes``/``ano``:

        Tipo 0 (NUMCNJ, PRODESP, TEIF, IP, PERDHIDR, VAZMIN, NUMBAS) - somente ``valorA`` (escalar); ``valorB``
        e None e ``mes``/``ano`` valem 0.

        Tipo 1 (NUMMAQ, POTEFE, COEFEVAP, VOLMIN, VOLMAX) - ``valorA`` (escalar) e ``valorB`` (segundo campo,
        geralmente o numero do conjunto/mes ou a unidade 'h'/'%'); ``mes``/``ano`` valem 0.

        Tipo 2 (COTAREA, VOLCOTA) - ``valorA`` e uma lista com os 5 coeficientes do polinomio; ``valorB`` e None
        e ``mes``/``ano`` valem 0.

        Tipo 3 (CFUGA, VAZMINT, CMONT) - ``valorA`` (escalar) com vigencia em ``mes``/``ano``; ``valorB`` e None.

        Tipo 4 (VMINP, VMINT, VMAXT) - ``valorA`` (escalar) com vigencia em ``mes``/``ano`` e ``valorB`` com a
        unidade ('h' ou '%').
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_modifs = None

        self.bloco_usina = {
            'df': None,
            'formatoA': "{area:>3} {conjunto:>1}  {tipo:>1} {usina:>3} {nome_usina:<39}\n",
            }

        self._codigo = {
                    'descricao': 'Codigo da usina hidreletrica modificada',
                    'valor': list()
               }
        self._comentario = {
                    'descricao': 'Comentario associado a usina (geralmente o nome da usina)',
                    'valor': list()
               }
        self._palavra_chave = {
                    'descricao': 'Palavra-chave que identifica o tipo de modificacao cadastral (NUMCNJ, PRODESP, '
                                  'TEIF, IP, PERDHIDR, VAZMIN, NUMBAS, NUMMAQ, POTEFE, COEFEVAP, VOLMIN, VOLMAX, '
                                  'COTAREA, VOLCOTA, CFUGA, VAZMINT, CMONT, VMINP, VMINT ou VMAXT)',
                    'valor': list()
               }
        self._valorA = {
                    'descricao': 'Primeiro valor da modificacao: escalar, exceto para COTAREA/VOLCOTA, em que e '
                                  'uma lista com os 5 coeficientes do polinomio',
                    'valor': list()
               }
        self._valorB = {
                    'descricao': 'Segundo valor da modificacao, quando aplicavel (numero do conjunto/mes ou '
                                  "unidade 'h'/'%'); None quando nao aplicavel a palavra-chave",
                    'valor': list()
               }
        self._mes = {
                    'descricao': 'Mes de vigencia da modificacao (0 quando a palavra-chave nao possui vigencia '
                                  'temporal)',
                    'valor': list()
               }
        self._ano = {
                    'descricao': 'Ano de vigencia da modificacao (0 quando a palavra-chave nao possui vigencia '
                                  'temporal)',
                    'valor': list()
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
