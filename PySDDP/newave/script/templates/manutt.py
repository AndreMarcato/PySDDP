# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ManuttTemplate(ArquivoEntrada):
    """
    Classe que contem os dados de manutencao programada das Usinas
    Termeletricas do newave (MANUTT.DAT).

    O arquivo comeca com dois registros de comentario/orientacao
    (preservados verbatim na escrita) seguidos de um registro de largura
    fixa por evento de manutencao, ate o fim do arquivo. Cada registro
    fisico possui 13 campos, dos quais apenas os seis abaixo sao lidos pelo
    NEWAVE:

        colunas 18-20 (I3)   codigo_usina
        colunas 41-42 (I2)   dia_inicio
        colunas 43-44 (I2)   mes_inicio
        colunas 45-48 (I4)   ano_inicio
        colunas 50-52 (I3)   duracao
        colunas 56-62 (F7.2) potencia

    Os demais trechos de cada linha (demais campos e preenchimento ate a
    largura fixa de 200 colunas) nao sao interpretados, mas sao preservados
    verbatim para garantir round-trip sem perda.
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_manutencoes = 0

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Registros de comentario/orientacao (preservados verbatim)
        self._cabecalho: list = list()

        # Linhas fisicas originais, uma por evento de manutencao, usadas
        # para preservar os campos nao interpretados no round-trip
        self._linhas: list = list()

        self._codigo_usina = {
                    'descricao': 'Codigo/numero da usina termica em manutencao',
                    'valor': list()
               }
        self._dia_inicio = {
                    'descricao': 'Dia de inicio da manutencao',
                    'valor': list()
               }
        self._mes_inicio = {
                    'descricao': 'Mes de inicio da manutencao',
                    'valor': list()
               }
        self._ano_inicio = {
                    'descricao': 'Ano de inicio da manutencao',
                    'valor': list()
               }
        self._duracao = {
                    'descricao': 'Duracao da manutencao, em dias',
                    'valor': list()
               }
        self._potencia = {
                    'descricao': 'Potencia retirada de operacao durante a manutencao, em MW',
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
