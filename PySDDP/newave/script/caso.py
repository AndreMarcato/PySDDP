import os
from typing import IO

from PySDDP.newave.script.templates.caso import CasoTemplate


class Caso(CasoTemplate):
    def __init__(self):
        super().__init__()

        self._conteudo_ = None

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo CASO.DAT que contem o nome do
        com a lista de arquivos de entrada para a execucao do NEWAVE


        :param file_name: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)

                linha = self.linha.strip()

                self.nome_arquivos = self.verificar_caixa_nome_arquivo(
                        self.dir_base,
                        linha
                    )

        except Exception as err:
            print(self.linha)
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._conteudo_ = None
            else:
                raise

        print("OK! Leitura do CASO.DAT realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o arquivo CASO.DAT que contem o nome do
        arquivo que contém a lista de arquivos de entrada para execucao do Newave

        :param file_out: caminho completo para o arquivo
        """

        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        formato = "{nome: <12}\n"
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                linha = dict(nome=self.nome_arquivos)
                f.write(formato.format(**linha))

        except Exception:
            raise

        print("OK! Escrita do CASO.DAT realizada com sucesso.")
