import os
from typing import IO
import pandas as pd
import numpy as np

from PySDDP.newave.script.templates.exph import ExphTemplate


class Exph(ExphTemplate):
    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_exps = None
        self.usina = dict()

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo EXPH.DAT que contem a expansão das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               confhd: classe contendo a configuracao de todas as usinas hidreletrica pertencentes ao estudo,
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_exps = 0

        # listas referentes ao dicionário USINA
        self.usina['codigo'] = list()
        self.usina['nome'] = list()
        self.usina['mesi_evm'] = list()
        self.usina['anoi_evm'] = list()
        self.usina['dura_evm'] = list()
        self.usina['perc_evm'] = list()
        self.usina['mesi_tur'] = list()
        self.usina['anoi_tur'] = list()
        self.usina['comentar'] = list()
        self.usina['nume_tur'] = list()
        self.usina['nume_cnj'] = list()

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho

                self.next_line(f)

                linha = self.linha

                continua = True

                while continua:
                    self.numero_exps += 1

                    codigo = int(linha[0:4])
                    nome = linha[5:17]

                    if linha[18:20] != '  ':
                        #
                        # Usina está enchendo o VM no início do estudo ou irá começar encher o VM no decorrer do estudo
                        #
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(int(linha[18:20]))
                        self.usina['anoi_evm'].append(int(linha[21:25]))
                        self.usina['dura_evm'].append(int(linha[31:33]))
                        self.usina['perc_evm'].append(float(linha[37:42]))
                        self.usina['mesi_tur'].append(None)
                        self.usina['anoi_tur'].append(None)
                        self.usina['comentar'].append(None)
                        self.usina['nume_tur'].append(None)
                        self.usina['nume_cnj'].append(None)
                    else:
                        #
                        # Usina já encheu o VM antes do início do estudo, mas receberá mais máquinas
                        #
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(None)
                        self.usina['anoi_evm'].append(None)
                        self.usina['dura_evm'].append(None)
                        self.usina['perc_evm'].append(None)
                        self.usina['mesi_tur'].append(int(linha[44:46]))
                        self.usina['anoi_tur'].append(int(linha[47:51]))
                        self.usina['comentar'].append(linha[52:59])
                        self.usina['nume_tur'].append(int(linha[60:62]))
                        self.usina['nume_cnj'].append(int(linha[63:65]))

                    self.next_line(f)
                    linha = self.linha

                    #
                    # Inserção de máquinas restantes
                    #
                    while linha[0:4] != '9999':
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(None)
                        self.usina['anoi_evm'].append(None)
                        self.usina['dura_evm'].append(None)
                        self.usina['perc_evm'].append(None)
                        self.usina['mesi_tur'].append(int(linha[44:46]))
                        self.usina['anoi_tur'].append(int(linha[47:51]))
                        self.usina['comentar'].append(linha[52:59])
                        self.usina['nume_tur'].append(int(linha[60:62]))
                        self.usina['nume_cnj'].append(int(linha[64:65]))
                        self.next_line(f)
                        linha = self.linha

                    #
                    # Passa para a próxima usina
                    #
                    self.next_line(f)
                    linha = self.linha

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_usina['df'] = pd.DataFrame(self.usina, columns = [ 'codigo',
                                                                              'nome',
                                                                              'mesi_evm',
                                                                              'anoi_evm',
                                                                              'dura_evm',
                                                                              'perc_evm',
                                                                              'mesi_tur',
                                                                              'anoi_tur',
                                                                              'comentar',
                                                                              'nume_tur',
                                                                              'nume_cnj'] )
                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso. (', self.numero_exps,
                      'Usinas Hidraulicas Expandidas )')
            else:
                raise

        return

    def escrever(self, file_out: str) -> None:

        df = self.bloco_usina['df']

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write("COD  NOME        ENCHIMENTO  VOLUME MORTO    DATA    POT.   MQ CJ\n" )
                f.write("                  INICIO    DUR.MESES  %    ENTRADA\n" )
                f.write("XXXX XXXXXXXXXXXX XX/XXXX      XX     XX.X  XX/XXXX XXXX.X\n")

                tamanho = df.shape
                tamanho = tamanho[0]

                linha = 0

                conta_usi = 0

                while linha < tamanho:

                    registro = df.iloc[linha].values
                    codigo = int(registro[0])
                    conta_usi += 1

                    #
                    # Cria dataframe apenas com a usina. Este procedimento é para manter a ordem do arquivo original
                    #

                    usinadf = df[df['codigo'] == codigo]
                    nr_reg = usinadf.shape
                    nr_reg = nr_reg[0]
                    reg = 0


                    if not np.isnan(registro[2]):
                        formato = "{codigo: >4} {nome: <12} {mesi_evm: >2}/{anoi_evm: <4}      {dura_evm: >2}     {perc_evm: >4.1f}\n"
                        row = dict(
                            codigo=int(registro[0]),
                            nome=registro[1],
                            mesi_evm=int(registro[2]),
                            anoi_evm=int(registro[3]),
                            dura_evm=int(registro[4]),
                            perc_evm=int(registro[5]),
                        )
                    else:
                        formato = "{codigo: >4} {nome: <12} {mesi_tur: >28}/{anoi_tur: <4} {comentar: >7} {nume_tur: >2} {nume_cnj: >2}\n"
                        row = dict(
                                    codigo=int(registro[0]),
                                    nome=registro[1],
                                    mesi_tur=int(registro[6]),
                                    anoi_tur=int(registro[7]),
                                    comentar=registro[8],
                                    nume_tur=int(registro[9]),
                                    nume_cnj=int(registro[10])
                                  )
                    f.write(formato.format(**row))
                    reg += 1

                    while reg < nr_reg:
                        registro = usinadf.iloc[reg].values
                        formato = "{codigo: >4} {nome: <12} {mesi_tur: >28}/{anoi_tur: <4} {comentar: >7} {nume_tur: >2} {nume_cnj: >2}\n"
                        row = dict(
                            codigo="    ",
                            nome="            ",
                            mesi_tur=int(registro[6]),
                            anoi_tur=int(registro[7]),
                            comentar=registro[8],
                            nume_tur=int(registro[9]),
                            nume_cnj=int(registro[10])
                        )
                        f.write(formato.format(**row))
                        reg += 1
                    f.write('9999\n')

                    #
                    # Pula para próxima usina
                    #
                    registro = df.iloc[linha].values
                    codigo = int(registro[0])
                    while codigo == int(registro[0]):
                        linha += 1
                        if linha == tamanho:
                            break
                        registro = df.iloc[linha].values

            print('OK! Escrita do', self.nome_arquivo ,'realizada com sucesso. (', conta_usi,
                  'Usinas Hidraulicas Modificadas )')

        except Exception:
            raise