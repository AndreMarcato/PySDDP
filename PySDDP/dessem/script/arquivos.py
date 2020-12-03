import os
from typing import IO

from PySDDP.dessem.script.templates.arquivos import ArquivosTemplate

COMENTARIO = "&"


class Arquivos(ArquivosTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self._comentarios_ = None

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo que contem os nomes dos
        arquivos de entrada para a execucao do DESSEM

        Manual do Usuario III.1 Arquivo Indice (DESSEM.ARQ)

        :param file_name: string com o caminho completo para o arquivo

        """

        # Inserir o nome do arquivo PIVO na lista de arquivos de entrada
        self.lista_entrada.clear()
        self.lista_entrada.append(os.path.split(file_name)[1])

        dir_base = os.path.split(file_name)[0]
        self._numero_registros_ = 0
        self._comentarios_ = list()

        lista_mneumos = list(self.dados.keys()) + list(self.arquivos.keys())

        arquivos: dict = dict()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:

                    self.next_line(f)

                    linha = self.linha.strip()
                    # Se linha for comentário, não faço nada e pulo para a próxima linha
                    if linha[0] == COMENTARIO:
                        self._comentarios_.append(linha)
                        continue

                    mneumo = linha[:9].strip().lower()
                    if mneumo not in lista_mneumos:
                        raise NotImplementedError(f"Mneumonico {mneumo} não manipulado pelo DESSEM!")

                    info = linha[49:].strip()
                    if mneumo in list(self.dados.keys()):
                        arquivos[mneumo] = info
                    else:
                        arquivos[mneumo] = self.verificar_caixa_nome_arquivo(
                            dir_base,
                            info
                        )
                        self.lista_entrada.append(arquivos[mneumo])

                    self._numero_registros_ += 1
                    if mneumo in self.dados:
                        self.dados[mneumo]['valor'] = arquivos[mneumo]

                    if mneumo in self.arquivos:
                        self.arquivos[mneumo]['valor'] = arquivos[mneumo]

                    # Transformo cada um das chaves do dicionario em atributos da classe
                    setattr(self, mneumo, arquivos[mneumo])

        except Exception as err:
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._conteudo_ = arquivos
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Escreve o arquivo que contem os nomes dos
        arquivos para execucao do Newave

        :param file_out: caminho completo para o arquivo
        """

        formato = "{mneumo: <9} {descricao: <38} {valor: <80}\n"
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Cabeçalho
                f.write("&Mnem        Descricao                           Arquivo\n")
                f.write("&XXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")

                # Imprime dados
                for key, value in self.dados.items():
                    if value['valor'] is not None:
                        linha = dict(
                            mneumo=key.upper(),
                            descricao=value['descricao'],
                            valor=value['valor']
                        )
                        f.write(formato.format(**linha))

                # Imprime Arquivos
                for key, value in self.arquivos.items():
                    if value['valor'] is not None:
                        linha = dict(
                            mneumo=key.upper(),
                            descricao=value['descricao'],
                            valor=value['valor']
                        )
                        f.write(formato.format(**linha))

        except Exception:
            raise
