# -*- coding: utf-8 -*-
from abc import ABC
from typing import Optional, IO

import pandas as pd
import os

from PySDDP.dessem.script.templates.dessopc import DessopcTemplate

COMENTARIO = '& OPCOES DE EXECUCAO\n'


class Dessopc(DessopcTemplate):

    def __init__(self):

        """
        Classe que contem todos os elementos comuns a qualquer versao do arquivo Dessopc do Dessem.
        Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
        dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
        leitura e escrita
        """

        super().__init__()

        self.ativas: Optional[list] = None
        self.inativas: Optional[list] = None

        self._flags = dict()
        self._comentarios: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de opcoes de execucao

        Manual do Usuario III.10 Arquivo de Opções de Execução (DESSOPC.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # Listas de Comentários:
        self._comentarios = None

        self.peninte['peninte'] = None
        self.peninte['fator'] = None

        self.deficit['deficit'] = None
        self.deficit['valor'] = None

        self.tolerilh['tolerilh'] = None
        self.tolerilh['valor'] = None

        self.trata_inviab_ilha['trata_inviab_ilha'] = None
        self.trata_inviab_ilha['valor'] = None

        self.regranptv['regranptv'] = None
        self.regranptv['regra'] = None
        self.regranptv['flag'] = None
        self.regranptv['numpon'] = None

        self.engolimento['engolimento'] = None
        self.engolimento['flag'] = None

        self.solvertd['solvertd'] = None

        self.zeralimuh['zeralimuh'] = None

        self.fphadessem['fphadessem'] = None

        self.ucterm['ucterm'] = None
        self.ucterm['metodologia'] = None

        self.flgucterm['flgucterm'] = None

        self.constdados['constdados'] = None
        self.constdados['flag'] = None

        self.flgtitul['flgtitul'] = None

        self.ajustefcf['ajustefcf'] = None
        self.ajustefcf['regra_1'] = None
        self.ajustefcf['regra_2'] = None
        self.ajustefcf['regra_3'] = None

        self.milpin['milpin'] = None

        self.pint['pint'] = None

        self.uctbusloc['uctbusloc'] = None

        self.prsvlplfinal['prsvlplfinal'] = None

        self.crossover['crossover'] = None
        self.crossover['campo_1'] = None
        self.crossover['campo_2'] = None
        self.crossover['campo_3'] = None
        self.crossover['campo_4'] = None
        self.crossover['campo_5'] = None

        self.uctheurfp['uctheurfp'] = None
        self.uctheurfp['numrel'] = None
        self.uctheurfp['numvar'] = None

        self.cpxpreslv['cpxpreslv'] = None

        self.uctser['uctser'] = None

        self.uctpar['uctpar'] = None
        self.uctpar['numnuc'] = None

        self.avlcmo['avlcmo'] = None
        self.avlcmo['flag'] = None

        self.cplexlog['cplexlog'] = None

        self.impavl['impavl'] = None
        self.impavl['flag'] = None

        self.ativas = list()
        self.inativas = list()

        # noinspection PyBroadException
        try:
            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:
                    self.next_line(f)
                    line = self.linha.strip()

                    for idx, value in enumerate(self.flags.keys()):
                        if value.upper() in line:

                            if line[0] == "&":
                                self.inativas.append(line)
                            else:
                                self.ativas.append(line)

                        else:
                            pass

                    continue

        except Exception as err:
            if isinstance(err, StopIteration):
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def ativa_to_inativa(self, flag: str):
        """
        Metodo para transformar flag ativa em inativa
        """

        for idx, value in enumerate(self.ativas):

            if flag.upper() in value:
                self.inativas.append("&" + value + "\n")
                del self.ativas[idx]

            else:
                pass

    def inativa_to_ativa(self, flag: str):
        """
        Metodo para transformar flag inativa em ativa
        """

        for idx, value in enumerate(self.inativas):

            if flag.upper() in value:
                self.ativas.append(value[1:])
                del self.inativas[idx]

            else:
                pass

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrita do arquivo de opcoes de execucao

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write(COMENTARIO)
                f.write("&\n")
                for line in self.ativas:
                    f.write(line + "\n")

                f.write("&\n")
                f.write("&Flags Inativos\n")

                for line in self.inativas:
                    f.write(line + "\n")

        except Exception:
            raise
