import os
from typing import IO
import numpy as np
import struct

from PySDDP.newave.script.templates.vazoes import VazoesTemplate


class Vazoes(VazoesTemplate):
    def __init__(self):
        super().__init__()

        self._conteudo_ = None

    def ler(self, file_name: str, nr_postos: int) -> None:
        """
        Implementa o método para leitura do arquivo VAZOES.DAT que contem o histórico de
        às UHEs para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]

        # noinspection PyBroadException
        try:

            with open(file_name, 'rb') as f:  # type: IO[str]

                vazoes = np.fromfile(f, dtype=np.int32)
                # A principio o numero de anos seria ano corrente - 2, mas
                # o ons tem usado complementar o arquivo de vazoes com os
                # dados ate o mes anterior do ano corrente
                # Calcular o numero de anos dividindo o tamanho da variavel data / nreg / nmeses

                self.nr_postos = nr_postos
                #nr_postos = 600
                num_anos = int(vazoes.shape[0] / nr_postos / 12)
                self.vaz_nat = vazoes.reshape(num_anos, 12, int(nr_postos))

        except Exception as err:
            print(self.linha)
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._conteudo_ = None
            else:
                raise

        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o arquivo VAZOES.DAT que contem o o historico de vazoes das UHEs para execucao do Newave

        :param file_out: caminho completo para o arquivo
        """

        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        try:
            with open(file_out, 'wb') as f:  # type: IO[bytes]

                nanos = np.shape(self.vaz_nat)[0]
                npostos = np.shape(self.vaz_nat)[2]
                for iano in range(nanos):
                    for imes in range(12):
                        for iposto in range(npostos):
                            f.write(struct.pack('i', self.vaz_nat[iano][imes][iposto]))

        except Exception:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")
