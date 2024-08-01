# -*- coding: utf-8 -*-
from abc import abstractmethod

from PySDDP.decomp.script.templates.arquivo_entrada import ArquivoEntrada


class IndiceTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Indice do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.bloco_indice = {
            'descricao': 'Este arquivo contem o indice dos arquivos de dados de entrada sob gerenciamento do usuario. E'
                         'composto por um unico bloco de dados com cinco ou seis (nos casos em que existem usinas '
                         'termicas GNL) registros ordenados contendo a especificacao dos demais arquivos de dados de '
                         'entrada.',
            'cabecalho': None,
            'formato': '{nome_arq:<80}\n',
            'df': None
        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Metodo abstrato do ArquivoEntrada sendo repassado para as classes filhas.
        :param args: Conjunto de parametros obrigatorios.
        :param kwargs: Conjunto de parametros opcionais.
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Metodo abstrato do ArquivoEntrada sendo repassado para as classes filhas.
        :param args: Conjunto de parametros obrigatorios.
        :param kwargs: Conjunto de parametros opcionais.
        :return:
        """
