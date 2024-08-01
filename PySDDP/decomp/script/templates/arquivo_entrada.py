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
        Parâmetros aceitos nesse método:
        folder: String com o caminho para o diretório
        file_name: String com o nome do arquivo
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Método estático para Escrita de um arquivo de entrada do Decomp
        key: Chave
        reg: Registro
        fid: Apontador para última posição lida
        Retorna ponteiro para próxima linha
        """

    @staticmethod
    def verificar_caixa_nome_arquivo(dir_base: str, nome_arq: str) -> str:
        """
        Verifica se o arquivo existe com o nome em caixa baixa ou caixa alta
        :param dir_base: Diretório onde está o arquivo
        :param nome_arq: Nome do arquivo
        :return:
        """

        # Se existir o arquivo com nome em letras maiúsculas e minúsculas em qualquer ordem, usar o nome
        if os.path.exists(os.path.join(dir_base, nome_arq)):
            return nome_arq
        # Caso exista o nome somente em letras minúsculas, usá-lo
        elif os.path.exists(os.path.join(dir_base, nome_arq.lower())):
            return nome_arq.lower()
        # Caso exista o nome somente em letras maiúsculas, usá-lo
        elif os.path.exists(os.path.join(dir_base, nome_arq.upper())):
            return nome_arq.upper()
        else:
            # Caso do arquivo não existir (resultados de um caso não executado), dar preferência para minúsculas
            return nome_arq.lower()

    def next_line(self, f: IO) -> str:
        """
        Método que lê a próxima linha e atualiza o contador
        :param f: Apontador para a última linha lida
        :return: linha lida
        """
        self.linha = next(f)
        self.cont += 1

        return self.linha
