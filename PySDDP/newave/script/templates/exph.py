from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ExphTemplate(ArquivoEntrada):
    """
    Classe que contem as modificações de cadastro de todas as Usinas Hidrelétricas do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Modif e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita

    O EXPH.DAT nao possui uma chave unica por registro: uma mesma usina hidreletrica pode ter varios registros
    (um para o enchimento do volume morto e um para cada maquina/conjunto que entra em operacao) ao longo do
    arquivo. Por isso, assim como Expt.get/Expt.put e Manutt.get/Manutt.put (blocos que tambem nao possuem chave
    natural), a identidade de cada registro em Exph.get/Exph.put e a sua posicao (indice, 0-based) na lista de
    registros, preservada pela chave somente-leitura ``indice_original``.

    Cada registro fisico e de um dos dois tipos abaixo, distinguidos implicitamente pelo preenchimento dos campos
    (tipo 1: mesi_evm/anoi_evm/dura_evm/perc_evm preenchidos e mesi_tur/anoi_tur/comentar/nume_tur/nume_cnj em
    branco; tipo 2: o inverso):

        Tipo 1 - Enchimento do volume morto (primeiro registro de uma usina 'EE' ou 'NE' que ainda vai encher o
                 volume morto):
            colunas  1- 4 (I4)   codigo
            colunas  6-17 (A12)  nome
            colunas 19-20 (I2)   mesi_evm
            colunas 22-25 (I4)   anoi_evm
            colunas 32-33 (I2)   dura_evm
            colunas 38-42 (F5.1) perc_evm

        Tipo 2 - Entrada em operacao de uma maquina/conjunto:
            colunas  1- 4 (I4)   codigo (em branco nos registros seguintes ao primeiro da usina)
            colunas  6-17 (A12)  nome (em branco nos registros seguintes ao primeiro da usina)
            colunas 45-46 (I2)   mesi_tur
            colunas 48-51 (I4)   anoi_tur
            colunas 53-59 (F7.1) comentar (potencia efetiva por maquina na entrada em operacao)
            colunas 61-62 (I2)   nume_tur
            colunas 64-65 (I2)   nume_cnj

    O terminador ``9999`` encerra o bloco de registros de cada usina e nunca corresponde a um registro de dados.
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_exps = None

        self.bloco_usina = {
            'df': None
            }

        self._codigo = {
                    'descricao': 'Codigo da usina hidreletrica',
                    'valor': list()
               }
        self._nome = {
                    'descricao': 'Nome da usina hidreletrica',
                    'valor': list()
               }
        self._mesi_evm = {
                    'descricao': 'Mes de inicio do enchimento do volume morto (registro tipo 1; None quando o '
                                  'registro e do tipo 2 - entrada de maquina/conjunto)',
                    'valor': list()
               }
        self._anoi_evm = {
                    'descricao': 'Ano de inicio do enchimento do volume morto (registro tipo 1; None quando o '
                                  'registro e do tipo 2 - entrada de maquina/conjunto)',
                    'valor': list()
               }
        self._dura_evm = {
                    'descricao': 'Duracao em meses do enchimento do volume morto (registro tipo 1; None quando o '
                                  'registro e do tipo 2 - entrada de maquina/conjunto)',
                    'valor': list()
               }
        self._perc_evm = {
                    'descricao': 'Percentual do volume morto ja enchido no inicio do estudo (registro tipo 1; '
                                  'None quando o registro e do tipo 2 - entrada de maquina/conjunto)',
                    'valor': list()
               }
        self._mesi_tur = {
                    'descricao': 'Mes de entrada em operacao da maquina/conjunto (registro tipo 2; None quando o '
                                  'registro e do tipo 1 - enchimento do volume morto)',
                    'valor': list()
               }
        self._anoi_tur = {
                    'descricao': 'Ano de entrada em operacao da maquina/conjunto (registro tipo 2; None quando o '
                                  'registro e do tipo 1 - enchimento do volume morto)',
                    'valor': list()
               }
        self._comentar = {
                    'descricao': 'Potencia efetiva por maquina na entrada em operacao (registro tipo 2; None '
                                  'quando o registro e do tipo 1 - enchimento do volume morto)',
                    'valor': list()
               }
        self._nume_tur = {
                    'descricao': 'Numero da maquina que entra em operacao (registro tipo 2; None quando o '
                                  'registro e do tipo 1 - enchimento do volume morto)',
                    'valor': list()
               }
        self._nume_cnj = {
                    'descricao': 'Numero do conjunto de maquinas que entra em operacao (registro tipo 2; None '
                                  'quando o registro e do tipo 1 - enchimento do volume morto)',
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
