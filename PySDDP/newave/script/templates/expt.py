# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ExptTemplate(ArquivoEntrada):
    """
    Classe que contem os dados de expansao termica do newave (EXPT.DAT).

    O arquivo comeca com dois registros de comentario (preservados verbatim
    na escrita) seguidos de um registro de largura fixa por modificacao de
    cadastro de usina termica, ate o fim do arquivo, com sete campos:

        colunas  1- 4 (I4)   codigo_usina
        colunas  6-10 (A5)   tipo_modificacao (GTMIN, POTEF, FCMAX, IPTER ou TEIFT)
        colunas 12-19 (F8.2) novo_valor
        colunas 21-22 (I2)   mes_inicio
        colunas 24-27 (I4)   ano_inicio
        colunas 29-30 (I2)   mes_fim (campo opcional)
        colunas 32-35 (I4)   ano_fim (campo opcional)

    Embora nao especificado no manual do NEWAVE, o deck real tambem usa,
    a partir da coluna 38 (12 caracteres, campo opcional), um comentario
    livre normalmente preenchido com o nome da usina - util para
    identificar visualmente qual usina esta sofrendo a modificacao:

        colunas 38-49 (A12)  comentario (campo opcional, geralmente o nome da usina)
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_expansoes = 0

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Registros de comentario (preservados verbatim)
        self._cabecalho: list = list()

        # Linhas fisicas originais, uma por modificacao, usadas para
        # preservar os campos nao interpretados (ex.: comentario) no
        # round-trip
        self._linhas: list = list()

        self._codigo_usina = {
                    'descricao': 'Codigo/numero da usina termica',
                    'valor': list()
               }
        self._tipo_modificacao = {
                    'descricao': "Tipo de modificacao (GTMIN, POTEF, FCMAX, IPTER ou TEIFT)",
                    'valor': list()
               }
        self._novo_valor = {
                    'descricao': 'Novo valor do parametro modificado (unidade depende do tipo)',
                    'valor': list()
               }
        self._mes_inicio = {
                    'descricao': 'Mes de inicio de vigencia da modificacao',
                    'valor': list()
               }
        self._ano_inicio = {
                    'descricao': 'Ano de inicio de vigencia da modificacao',
                    'valor': list()
               }
        self._mes_fim = {
                    'descricao': 'Mes final de vigencia da modificacao (campo opcional)',
                    'valor': list()
               }
        self._ano_fim = {
                    'descricao': 'Ano final de vigencia da modificacao (campo opcional)',
                    'valor': list()
               }
        self._comentario = {
                    'descricao': 'Comentario livre (geralmente o nome da usina); campo opcional, '
                                  'nao especificado no manual do NEWAVE, mas presente no deck real',
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
