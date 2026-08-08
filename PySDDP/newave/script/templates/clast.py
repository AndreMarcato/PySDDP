# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ClastTemplate(ArquivoEntrada):
    """
    Classe que contem o cadastro de classes termicas e as alteracoes temporais
    de custo do newave (CLAST.DAT).

    O arquivo possui dois blocos de registros, separados por dois registros de
    comentario:

        Tipo 1 - cadastro da classe termica e custo por ano do horizonte de
                 planejamento, ate o sentinela ``9999`` no campo
                 numero_classe_termica;
        Tipo 2 - alteracoes de custo com vigencia temporal.

    Esta classe tem como intuito fornecer duck typing para a classe Clast e
    ainda adicionar um nivel de especificacao dentro da fabrica. Alem disso
    esta classe deve passar adiante a responsabilidade da implementacao dos
    metodos de leitura e escrita.
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_classes = 0
        self.numero_alteracoes = 0
        self.nanos = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Mapa numero_classe_termica -> posicao nas listas do bloco Tipo 1
        self._mapa = dict()

        # Bloco Tipo 1 - cadastro das classes termicas e custos anuais
        self._numero_classe_termica = {
                    'descricao': 'Numero da classe termica (9999 encerra o bloco)',
                    'valor': list()
               }
        self._nome_classe_termica = {
                    'descricao': 'Nome da classe termica',
                    'valor': list()
               }
        self._tipo_combustivel = {
                    'descricao': 'Tipo de combustivel da classe termica',
                    'valor': list()
               }
        self._custos = {
                    'descricao': 'Custo de operacao por ano do horizonte de planejamento, em $/MWh',
                    'valor': list()
               }

        # Bloco Tipo 2 - alteracoes temporais de custo
        self._alt_numero_classe_termica = {
                    'descricao': 'Numero da classe termica afetada pela alteracao',
                    'valor': list()
               }
        self._alt_novo_custo = {
                    'descricao': 'Novo custo de operacao, em $/MWh',
                    'valor': list()
               }
        self._alt_mes_inicio = {
                    'descricao': 'Mes inicial da modificacao (campo opcional)',
                    'valor': list()
               }
        self._alt_ano_inicio = {
                    'descricao': 'Ano inicial da modificacao (campo opcional)',
                    'valor': list()
               }
        self._alt_mes_fim = {
                    'descricao': 'Mes final da modificacao (campo opcional)',
                    'valor': list()
               }
        self._alt_ano_fim = {
                    'descricao': 'Ano final da modificacao (campo opcional)',
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
