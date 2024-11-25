# -*- coding: utf-8 -*-
from typing import IO

import math
import os

import numpy as np
import pandas as pd

from PySDDP.decomp.script.templates.vazoes import VazoesTemplate


class Vazoes(VazoesTemplate):
    """
    Classe que contém todos os elementos comuns a qualquer versão do arquivo Vazoes do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nível de especificação
    dentro da fábrica. Além disso, esta classe deve passar adiante a responsabilidade da implementação dos métodos de
    leitura e escrita.
    """

    def __init__(self, nreg: int):
        super().__init__()

        self.nreg: int = nreg

    def ler(self, file_name: str) -> None:
        """
        Método para a leitura do arquivo vazoes.xxx.
        Manual do Usuário 30.1: Arquivo vazoes.xxx. Este arquivo contém os dados de afluência (vazão incremental para
        cada aproveitamento) que compõem a previsão do mês inicial e os cenários de vazões para cada estágio de
        planejamento. É um arquivo de acesso direto, não formatado, gerado pelo modelo GEVAZP.
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        # TODO: O metodo está preparado para ler somente 1 mes de vazoes sintéticas

        with open(file_name, 'rb') as f:
            # Leitura do Registro 1
            self.__reg1__ = np.fromfile(f, dtype=np.dtype('i4'), count=self.nreg)
            self.numero_postos = self.__reg1__[0]
            self.numero_estagios = self.__reg1__[1]

            fim = np.where(self.__reg1__ == 0)[0][0]
            self.numero_aberturas = self.__reg1__[2:fim]
            self.total_aberturas = np.sum(self.numero_aberturas)

            # Leitura do Registro 2
            self.__reg2__ = np.fromfile(f, dtype=np.dtype('i4'), count=self.nreg)
            self.codigo_uhes = self.__reg2__

            # Leitura do Registro 3
            self.__reg3__ = np.fromfile(f, dtype=np.dtype('i4'), count=self.nreg)
            self.numero_semanas_completas = self.__reg3__[0]
            self.numero_dias_excluidos = self.__reg3__[1]
            self.mes_inicial_estudo = self.__reg3__[2]
            self.ano_inicial_estudo = self.__reg3__[3]

            # Leitura do Registro 4
            nrows = int(math.ceil(self.total_aberturas / self.nreg))
            self.__reg4__ = np.zeros([nrows * self.nreg], dtype='f4')

            fim = 0
            for i in range(nrows):
                ini = fim
                fim = ini + self.nreg
                self.__reg4__[ini:fim] = np.fromfile(f, dtype=np.dtype('f4'), count=self.nreg)

            ini = 0
            fim = np.sum(self.numero_aberturas)
            self.probabilidade_no = self.__reg4__[ini:fim]

            # Leitura do Registro 5
            self.__reg5__ = np.fromfile(f, dtype=np.dtype('i4'))
            len_reg_5 = len(self.__reg5__)
            nrows = int(len_reg_5 / self.nreg)

            self.__reg5__ = self.__reg5__.reshape(nrows, self.nreg)
            self.vazao_incremental = self.__reg5__[:self.total_aberturas, :]
            self.vazao_incremental_art = self.__reg5__[self.total_aberturas:, :]

    def escrever(self, *args):
        raise NotImplementedError(
            f"Método de escrita não implementado para Vazoes nessa versão!"
        )

    def get_ano_ini_estudo(self) -> int:
        """
        Retorna o ano inicial do estudo
        :return: Ano inicial do estudo
        """

        return self.ano_inicial_estudo

    def get_mes_ini_estudo(self) -> int:
        """
        Retorna o mes inicial do estudo
        :return: Mes inicial do estudo
        """

        return self.mes_inicial_estudo

    def get_numero_estagios(self) -> int:
        """
        Retorna o número de estágios do estudo
        :return: Número de estágios
        """

        return self.numero_estagios

    def get_numero_semanas_completas(self) -> int:
        """
        Retorna o número semanas completas do estágio inicial do estudo
        :return: Número semanas completas
        """

        return self.numero_semanas_completas

    def get_numero_dias_excluidos(self) -> int:
        """
        Retorna o Número de dias a serem excluídos do mês seguinte ao mes inicial dividido em semanas
        :return: Número semanas completas
        """

        return self.numero_dias_excluidos
