# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada

class RespotTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Respot do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.reserva_potencia = None
        self.reserva_potencia_df = None


        self.dados = {
            "rp":{
                'descricao': 'Áreas de controle de reserva de potência que participarão do estudo',
                'formato':'{mneumo: >2}    {num:>2}   {di:>2}  {hi:>2} {mi:1}  {df:>2} {hf:>2} {mf:1}           {coment:>27}\n',
                'valor': None

            },
            "lm":{
                'descricao': 'Controle de reservas de potência ao longo do horizonte de estudo',
                'formato': '{mneumo: >2}    {num:>2}   {di:>2}  {hi:>2} {mi:1}  {df:>2} {hf:>2} {mf:1}            {potencia:>4}\n',
                'valor': None

            },
            "potencia":{
                'descricao': 'Reserva mínima de potência para a área',
                'formato': '{mneumo: >2}    {num:>2}   {di:>2}  {hi:>2} {mi:1}  {df:>2} {hf:>2} {mf:1}            {potencia:>4}',
                'valor': None
            }
        }

        # preenchido após o método de leitura ser chamado
        # representa os nomes lidos no script.arq
        self.nome_arquivos = list()

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
