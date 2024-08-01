# -*- coding: utf-8 -*-
import os
from typing import IO

import pandas as pd

from PySDDP.decomp.script.templates.indice import IndiceTemplate


class Indice(IndiceTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Indice do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):

        super().__init__()

        self.indice = dict()
        self.num_arquivos = 6

    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo indice.dat.
        Manual do Usuario 30.1: Arquivo indice.dat. Este arquivo contem o indice dos arquivos de dados de entrada sob
        gerenciamento do usuario.
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.indice['arquivo'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                for _ in range(self.num_arquivos):

                    line = self.next_line(f)

                    # Leitura do campo:
                    line = line.replace("\n", "")
                    self.indice['arquivo'].append(line.strip())

                # Armazena dados no DataFrame correspondente:
                self.bloco_indice['df'] = pd.DataFrame(self.indice)

        except Exception as err:
            if isinstance(err, StopIteration):
                # Armazena dados no DataFrame correspondente:
                self.bloco_indice['df'] = pd.DataFrame(self.indice)
            else:
                raise

        print(f'OK! Leitura do {os.path.split(file_name)[1]} realizada com sucesso.')

    def escrever(self, file_out: str) -> None:
        """
        Metodo para a escrita do arquivo caso.dat.
        :param file_out: Conjunto de parametros obrigatorios.
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for idx, value in self.bloco_indice['df'].iterrows():
                    line = self.bloco_indice['formato'].format(**value)
                    f.write(line)
        except Exception:
            raise
