import os
from typing import IO

from PySDDP.newave.script.templates.arquivos import ArquivosTemplate


class Arquivos(ArquivosTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo que contem os nomes dos
        arquivos de entrada e saída para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo

        """

        # Inserir o nome do arquivo PIVO na lista de arquivos de entrada
        self.lista_entrada.clear()
        self.lista_entrada.append(os.path.split(file_name)[1])
        self.lista_entrada.append("HIDR.DAT")
        self.lista_entrada.append("VAZOES.DAT")

        # noinspection PyBroadException
        monitor: dict = dict()
        contador = 0
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                contador = 1
                while continua:

                    self.next_line(f)

                    linha = self.linha.strip()
                    nome = linha[30:].strip()

                    for mneumo in self.arquivos.keys():
                        if self.arquivos[mneumo]["ordem"] == contador:
                            self.arquivos[mneumo]["valor"] = nome
                            monitor[mneumo] = nome
                            # Transformo cada um das chaves do dicionario em atributos da classe
                            setattr(self, mneumo, monitor[mneumo])
                            self.lista_entrada.append(nome)

                    contador += 1

                    if contador == 39:
                        break

        except Exception as err:
            print(self.linha)
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._conteudo_ = monitor
            else:
                raise

        self._numero_registros_ = contador - 1
        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o arquivo que contem os nomes dos
        arquivos para execucao do Newave

        :param file_out: caminho completo para o arquivo
        """
        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        formato = "{descricao: <27}: {valor: <12}\n"
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime dados
                for mneumo in self.arquivos.keys():
                    linha = dict(
                        descricao=self.arquivos[mneumo]["descricao"],
                        valor=self.arquivos[mneumo]["valor"]
                    )
                    f.write(formato.format(**linha))

        except Exception:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")
