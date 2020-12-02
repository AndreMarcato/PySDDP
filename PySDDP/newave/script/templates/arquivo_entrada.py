import os

from typing import IO
from abc import abstractmethod, ABCMeta


class ArquivoEntrada(object,  metaclass=ABCMeta):

    def __init__(self):
        self.linha: str = ''
        self.cont: int = 0

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Parametros aceitos nesse metodo:

        folder: string com o caminho para o diretorio
        file_name: string com o nome do arquivo
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Método estático para Escrita de um arquivo de entrada do newave

        key: chave
        reg: registro
        fid: apontador para ultima posicao lida

        retorna ponteiro para proxima linha
        """

    @staticmethod
    def verificar_caixa_nome_arquivo(dir_base: str, nome_arq: str) -> str:
        """
        Verifica se o arquivo existe com o nome em caixa baixa ou caixa alta
        :param dir_base: diretorio onde esta o arquivo
        :param nome_arq: nome do arquivo
        :return:
        """

        # se existir o arquivo com nome em letras maiusculas e minusculas em qualquer ordem, usar o nome
        if os.path.exists(os.path.join(dir_base, nome_arq)):
            return nome_arq
        # caso exista o nome somente em letras minusculas, usa-lo
        elif os.path.exists(os.path.join(dir_base, nome_arq.lower())):
            return nome_arq.lower()
            # caso exista o nome somente em letras maiusculas, usa-lo
        elif os.path.exists(os.path.join(dir_base, nome_arq.upper())):
            return nome_arq.upper()
        else:
            # em caso do arquivo na existir (resultados de um caso nao executado) dar preferencia para minusculas
            return nome_arq.lower()

    def next_line(self, f: IO) -> str:
        """
        Metodo que le a proxima linha e atualiza contador

        :param f: apontador para a ultima linha lida
        :return: linha lida
        """
        self.linha = next(f)
        self.cont += 1

        return self.linha
