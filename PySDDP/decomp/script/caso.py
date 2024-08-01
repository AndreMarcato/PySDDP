# -*- coding: utf-8 -*-
import os
from typing import IO

import pandas as pd

from PySDDP.decomp.script.templates.caso import CasoTemplate


class Caso(CasoTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Caso do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementação dos metodos de
    leitura e escrita.
    """

    def __init__(self):

        super().__init__()

        self.caso = dict()

    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo caso.dat.
        Manual do Usuario 30.1: Arquivo caso.dat. Este arquivo contem um unico registro, contendo o nome do arquivo
        indice.
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.caso['nome_arq'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                line = self.next_line(f)

                # Leitura do campo:
                line = line.replace("\n", "")
                self.caso['nome_arq'].append(line.strip())

                # Armazena dados no DataFrame correspondente:
                self.bloco_caso['df'] = pd.DataFrame(self.caso)

        except Exception as err:
            if isinstance(err, StopIteration):
                # Armazena dados no DataFrame correspondente:
                self.bloco_caso['df'] = pd.DataFrame(self.caso)
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

                for idx, value in self.bloco_caso['df'].iterrows():
                    line = self.bloco_caso['formato'].format(**value)
                    f.write(line)
        except Exception:
            raise
