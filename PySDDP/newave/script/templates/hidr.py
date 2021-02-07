# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class HidrTemplate(ArquivoEntrada):
    """
    Classe que contem os dados de cadastro de todas as Usinas Hidrelétricas do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Newave e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_postos = None
        self.const = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)

        self._codigo = {
                    'descricao': 'Codigo da UHE',
                    'valor': list()
                 }
        self._nome = {
                    'descricao': 'Nome da UHE',
                    "valor": list()
               }
        self._posto = {
                    'descricao': 'Numero do Posto',
                    "valor": list()
               }
        self._bdh = {
                    'descricao': 'Banco de Dados Hidrometeorologico',
                    "valor": list()
               }
        self._sist = {
                    'descricao': 'Submercado',
                    "valor": list()
               }
        self._empr = {
                    'descricao': 'Codigo da empresa',
                    "valor": list()
               }
        self._jusante = {
                    'descricao': 'Codigo de Jusante',
                    "valor": list()
               }
        self._desvio = {
                    'descricao': 'Desvio de água',
                    "valor": list()
               }
        self._vol_min = {
                    'descricao': 'Volume Minimo',
                    "valor": list()
               }
        self._vol_max = {
                    'descricao': 'Volume Maximo',
                    "valor": list()
               }
        self._vol_vert = {
                    'descricao': 'Volume Vertimento',
                    "valor": list()
               }
        self._vol_min_desv = {
                    'descricao': 'Volume Minimo para Desvio',
                    "valor": list()
               }
        self._cota_min = {
                    'descricao': 'Cota Minima',
                    "valor": list()
               }
        self._cota_max = {
                    'descricao': 'Cota Maxima',
                    "valor": list()
               }
        self._pol_cota_vol = {
                    'descricao': 'Polinomio Cota-Volume',
                    "valor": list()
               }
        self._pol_cota_area = {
                    'descricao': 'Polinomio Cota-Area',
                    "valor": list()
               }
        self._coef_evap = {
                    'descricao': 'Coeficientes de Evaporacao',
                    "valor": list()
               }
        self._num_conj_maq = {
                    'descricao': 'Numero de Conjuntos de Maquinas',
                    "valor": list()
               }
        self._maq_por_conj = {
                    'descricao': 'Numero de Maquinas por Conjunto',
                    "valor": list()
               }
        self._pef_por_conj = {
                    'descricao': 'Potencia Efetiva por Maquina do Conjunto',
                    "valor": list()
               }
        self._cf_hbqt = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
        }
        self._cf_hbqg = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._cf_hbpt = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._alt_efet_conj = {
                    'descricao': 'Altura de Queda Efetiva do Conjunto',
                    "valor": list()
               }
        self._vaz_efet_conj = {
                    'descricao': 'Vazao Efetiva do Conjunto',
                    "valor": list()
               }
        self._prod_esp = {
                    'descricao': 'Produtibilidade Especifica',
                    "valor": list()
               }
        self._perda_hid = {
                    'descricao': 'Perda Hidraulica',
                    "valor": list()
               }
        self._num_pol_vnj = {
                    'descricao': 'Numero de Polinomios Vazao Nivel Jusante',
                    "valor": list()
               }
        self._pol_vaz_niv_jus = {
                    'descricao': 'Polinomios Vazao Nivel Jusante',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._cota_ref_nivel_jus = {
                    'descricao': 'Cota Referencia Nivel de Jusante',
                    "valor": list()
               }
        self._cfmed = {
                    'descricao': 'Cota Media do Canal de Fuga',
                    "valor": list()
               }
        self._inf_canal_fuga = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._fator_carga_max = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._fator_carga_min = {
                    'descricao': 'Fator de Caga Minimo - Checar esta informacao ??????',
                    "valor": list()
               }
        self._vaz_min = {
                    'descricao': 'Vazao Minima Obrigatoria',
                    "valor": list()
               }
        self._unid_base = {
                    'descricao': 'Numero de Unidades de Base',
                    "valor": list()
               }
        self._tipo_turb = {
                    'descricao': 'Tipo de Turbina Hidraulica',
                    "valor": list()
               }
        self._repres_conj = {
                    'descricao': 'Representacao Conjunto de Maquina - Checar esta informacao ?????',
                    "valor": list()
               }
        self._teifh = {
                    'descricao': 'Taxa Equivalente de Indisponibilidade Forcada Hidraulica',
                    "valor": list()
               }
        self._ip = {
                    'descricao': 'Indisponibilidade Programada',
                    "valor": list()
               }
        self._tipo_perda = {
                    'descricao': 'Tipo Perda Hidraulica - (1) Percentual - (2) Metros',
                    "valor": list()
               }
        self._data = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._observ = {
                    'descricao': 'Observacao',
                    "valor": list()
               }
        self._vol_ref = {
                    'descricao': 'Volume de Referencia',
                    "valor": list()
               }
        self._tipo_reg = {
                    'descricao': 'Tipo de Regularizacao',
                    "valor": list()
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
