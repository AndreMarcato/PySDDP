import os
from typing import IO
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from PySDDP.newave.script.templates.term import TermTemplate


class Term(TermTemplate):

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_terms = None
        self.term = dict()

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo TERM.DAT que contem as usinas térmicas de cadastro utilizados para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_terms = 0

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho

                self.next_line(f)

                linha = self.linha

                while linha != '':
                    #
                    # Incrementa contador de térmicas
                    #
                    self.numero_terms += 1

                    # Le_conteudo das linhas
                    codigo = int(linha[1:4])
                    nome = linha[5:17]
                    pot = float(linha[19:24])
                    fcmax = float(linha[25:29])
                    teif = float(linha[31:37])
                    ip = float(linha[38:44])
                    gtmin = list()
                    for i in range(13):
                        gtmin.append(float(linha[45+(i*7):51+(i*7)]))
                    #
                    # Acrescenta dados lidos no banco de dados
                    #
                    self._codigo['valor'].append(codigo)
                    self._term['codigo'].append(codigo)
                    self._nome['valor'].append(nome)
                    self._term['nome'].append(nome)
                    self._pot['valor'].append(pot)
                    self._term['pot'].append(pot)
                    self._fcmax['valor'].append(fcmax)
                    self._term['fcmax'].append(fcmax)
                    self._teif['valor'].append(teif)
                    self._term['teif'].append(teif)
                    self._ip['valor'].append(ip)
                    self._term['ip'].append(ip)
                    self._gtmin['valor'].append(gtmin)
                    self._term['gtmin'].append(gtmin)

                    #
                    # Lê próxima linha
                    #
                    self.next_line(f)
                    linha = self.linha

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_term['df'] = pd.DataFrame(self._term, columns = [ 'codigo',
                                                                          'nome',
                                                                          'pot',
                                                                          'fcmax',
                                                                          'teif',
                                                                          'ip',
                                                                          'gtmin'] )

                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso. (', self.numero_terms,
                      'Usinas Térmicas Foram Lidas )')
            else:
                raise

        return

    def escrever(self, file_out: str) -> None:
        """
        Implementa o método para escrita do arquivo TERM.DAT que contem os dados cadastrais das usinas
         termelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        formato = "{codigo: >4} {nome: <12} {pot: >5.0f}. {fcmax: >3.0f}. {teif: >7.2f} {ip: >6.2f} " + \
                  "{gtmin0: >6.2f} {gtmin1: >6.2f} {gtmin2: >6.2f} {gtmin3: >6.2f} {gtmin4: >6.2f} " + \
                  "{gtmin5: >6.2f} {gtmin6: >6.2f} {gtmin7: >6.2f} {gtmin8: >6.2f} {gtmin9: >6.2f} " + \
                  "{gtmin10: >6.2f} {gtmin11: >6.2f} {gtmin12: >6.2f}\n"

        formato2 = "{codigo: >4} {nome: <12} {pot: >5.0f}. {fcmax: >3.0f}. {teif: >7.2f} {ip: >6.2f} " + \
                  "{gtmin0: >6.1f} {gtmin1: >6.1f} {gtmin2: >6.1f} {gtmin3: >6.1f} {gtmin4: >6.1f} " + \
                  "{gtmin5: >6.1f} {gtmin6: >6.1f} {gtmin7: >6.1f} {gtmin8: >6.1f} {gtmin9: >6.1f} " + \
                  "{gtmin10: >6.1f} {gtmin11: >6.1f} {gtmin12: >6.1f}\n"


        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        try:

            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Cabeçalho

                f.write(" NUM NOME          POT  FCMX    TEIF   IP    <-------------------- GTMIN PARA O PRIMEIRO ANO DE ESTUDO ------------------------|D+ ANOS\n")
                f.write(" XXX XXXXXXXXXXXX  XXXX. XXX.  XXX.XX XXX.XX JAN.XX FEV.XX MAR.XX ABR.XX MAI.XX JUN.XX JUL.XX AGO.XX SET.XX OUT.XX NOV.XX DEZ.XX XXX.XX\n")

                for iusi in range(self.numero_terms):
                    linha = dict(
                        codigo=self._codigo['valor'][iusi],
                        nome=self._nome['valor'][iusi],
                        pot=self._pot['valor'][iusi],
                        fcmax=self._fcmax['valor'][iusi],
                        teif=self._teif['valor'][iusi],
                        ip=self._ip['valor'][iusi],
                        gtmin0=self._gtmin['valor'][iusi][0],
                        gtmin1=self._gtmin['valor'][iusi][1],
                        gtmin2=self._gtmin['valor'][iusi][2],
                        gtmin3=self._gtmin['valor'][iusi][3],
                        gtmin4=self._gtmin['valor'][iusi][4],
                        gtmin5=self._gtmin['valor'][iusi][5],
                        gtmin6=self._gtmin['valor'][iusi][6],
                        gtmin7=self._gtmin['valor'][iusi][7],
                        gtmin8=self._gtmin['valor'][iusi][8],
                        gtmin9=self._gtmin['valor'][iusi][9],
                        gtmin10=self._gtmin['valor'][iusi][10],
                        gtmin11=self._gtmin['valor'][iusi][11],
                        gtmin12=self._gtmin['valor'][iusi][12],
                    )
                    if len(formato.format(**linha)) <= 136:
                        f.write(formato.format(**linha))
                    else:
                        f.write(formato2.format(**linha))

        except Exception as err:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

        return

