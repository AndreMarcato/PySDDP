# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ConftTemplate(ArquivoEntrada):
    """
    Classe que contem os dados de configuracao das Usinas Termeletricas do newave (CONFT.DAT).
    Esta classe tem como intuito fornecer duck typing para a classe Conft e ainda adicionar um nivel de
    especificacao dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da
    implementacao dos metodos de leitura e escrita.

    Alem dos sete campos fisicos do CONFT.DAT, cada usina possui cinco matrizes de evolucao temporal
    (nanos x 12), a exemplo de Confhd/engol_tempo: gtmin_tempo, pot_tempo, fcmax_tempo, ip_tempo e
    teif_tempo, iniciadas com o cadastro da classe Term e atualizadas ano/mes a ano/mes pelas
    modificacoes GTMIN/POTEF/FCMAX/IPTER/TEIFT da classe Expt (ver Conft.ler/Conft._acerta_expt).
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_usinas = 0
        self.nanos = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Mapa codigo_usina -> posicao nas listas abaixo
        self._mapa = dict()

        self._codigo_usina = {
                    'descricao': 'Codigo/numero da usina termica',
                    'valor': list()
               }
        self._nome_usina = {
                    'descricao': 'Nome da usina termica',
                    'valor': list()
               }
        self._codigo_submercado = {
                    'descricao': 'Numero do subsistema/submercado da usina',
                    'valor': list()
               }
        self._status = {
                    'descricao': 'Status da UTE (EX-Existente, EE-Exist em Expansao, '
                                  'NE-Nao Existente em Expansao, NC-Nao Considerada)',
                    'valor': list()
               }
        self._codigo_classe_termica = {
                    'descricao': 'Numero da classe termica da usina (ver CLAST.DAT)',
                    'valor': list()
               }
        self._codigo_tecnologia = {
                    'descricao': 'Tecnologia para calculo de emissoes de GEE (campo opcional)',
                    'valor': list()
               }
        self._codigo_classe_gas = {
                    'descricao': 'Numero da classe de gas natural da usina (campo opcional)',
                    'valor': list()
               }

        # Evolucao temporal (nanos x 12) dos parametros de cadastro/expansao
        # termica, iniciada com o cadastro da classe Term e atualizada pelas
        # modificacoes temporais da classe Expt (ver Conft._acerta_expt,
        # a exemplo de Confhd._engol_tempo/Confhd._acerta_exph)
        self._gtmin_tempo = {
                    'descricao': 'Geracao termica minima (MW) por ano/mes do horizonte de planejamento, '
                                  'iniciada com o cadastro de TERM.DAT e atualizada pelas modificacoes GTMIN do EXPT.DAT',
                    'valor': list()
               }
        self._pot_tempo = {
                    'descricao': 'Potencia efetiva (MW) por ano/mes do horizonte de planejamento, '
                                  'iniciada com o cadastro de TERM.DAT e atualizada pelas modificacoes POTEF do EXPT.DAT',
                    'valor': list()
               }
        self._fcmax_tempo = {
                    'descricao': 'Fator de capacidade maximo (%) por ano/mes do horizonte de planejamento, '
                                  'iniciado com o cadastro de TERM.DAT e atualizado pelas modificacoes FCMAX do EXPT.DAT',
                    'valor': list()
               }
        self._ip_tempo = {
                    'descricao': 'Indisponibilidade programada - IP (%) por ano/mes do horizonte de planejamento, '
                                  'iniciada com o cadastro de TERM.DAT e atualizada pelas modificacoes IPTER do EXPT.DAT',
                    'valor': list()
               }
        self._teif_tempo = {
                    'descricao': 'Taxa equivalente de indisponibilidade forcada - TEIF (%) por ano/mes do horizonte '
                                  'de planejamento, iniciada com o cadastro de TERM.DAT e atualizada pelas '
                                  'modificacoes TEIFT do EXPT.DAT',
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
