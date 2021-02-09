import os
from typing import IO
import pandas as pd

from PySDDP.newave.script.templates.modif import ModifTemplate


class Modif(ModifTemplate):
    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_modifs = None
        self.usina = dict()

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo MODIF.DAT que contem as modificacoes cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               confhd: classe contendo a configuracao de todas as usinas hidreletrica pertencentes ao estudo,
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_modifs = 0

        # listas referentes ao dicionário USINA
        self.usina['codigo'] = list()
        self.usina['comentario'] = list()
        self.usina['palavra_chave'] = list()
        self.usina['valorA'] = list()
        self.usina['valorB'] = list()
        self.usina['mes'] = list()
        self.usina['ano'] = list()

        lista0 = ( 'NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'VAZMIN', 'NUMBAS',
                   'numcnj', 'prodesp', 'teif', 'ip', 'perdhidr', 'vazmin', 'numbas')

        lista1 = ( 'NUMMAQ', 'POTEFE', 'COEFEVAP', 'VOLMIN', 'VOLMAX',
                   'nummaq', 'potefe', 'coefevap', 'volmin', 'volmax')

        lista2 = ( 'COTAREA', 'VOLCOTA', 'cotaarea', 'volcota')

        lista3 = ( 'CFUGA', 'VAZMINT', 'CMONT',
                   'cfuga', 'vazmint', 'cmont')

        lista4 = ( 'VMINP', 'VMINT', 'VMAXT', 'vminp', 'vmint', 'vmaxt')

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)
                self.next_line(f)
                self.next_line(f)

                linha = self.linha

                continua = True

                while continua:
                    self.numero_modifs += 1
                    codigo = int(linha[10:30])
                    comentario = linha[30:]
                    self.next_line(f)
                    linha = self.linha
                    pal_chave = linha[1:9]
                    pal_chave = pal_chave.strip()
                    while pal_chave.upper() != 'USINA':
                        if pal_chave in lista0:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[0]))
                            self.usina['valorB'].append(None)
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista1:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[0]))
                            self.usina['valorB'].append(linha[9:].strip().split()[1])
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista2:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            polinomio = []
                            polinomio.append(float(linha[9:].strip().split()[0]))
                            polinomio.append(float(linha[9:].strip().split()[1]))
                            polinomio.append(float(linha[9:].strip().split()[2]))
                            polinomio.append(float(linha[9:].strip().split()[3]))
                            polinomio.append(float(linha[9:].strip().split()[4]))
                            self.usina['valorA'].append(polinomio)
                            self.usina['valorB'].append(None)
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista3:
                            pal_chave.split()[0]
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[2]))
                            self.usina['valorB'].append(None)
                            mes = linha[9:].strip().split()[0]
                            mes = int(mes)
                            self.usina['mes'].append(mes)
                            ano = linha[9:].strip().split()[1]
                            ano = int(ano)
                            self.usina['ano'].append(ano)
                        elif pal_chave in lista4:
                            pal_chave.split()[0]
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[2]))
                            self.usina['valorB'].append(linha[9:].strip().split()[3])
                            mes = linha[9:].strip().split()[0]
                            mes = int(mes)
                            self.usina['mes'].append(mes)
                            ano = linha[9:].strip().split()[1]
                            ano = int(ano)
                            self.usina['ano'].append(ano)
                        self.next_line(f)
                        linha = self.linha
                        pal_chave = linha[1:9]
                        pal_chave = pal_chave.strip()


        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_usina['df'] = pd.DataFrame(self.usina, columns = [ 'ano', 'codigo', 'comentario',
                                                                                'mes', 'palavra_chave',
                                                                                'valorA', 'valorB'] )

                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso. (', self.numero_modifs,
                      'Usinas Hidraulicas Modificadas )')
            else:
                raise

        return

    def escrever(self, file_out: str) -> None:

        lista0 = ( 'NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'VAZMIN', 'NUMBAS',
                   'numcnj', 'prodesp', 'teif', 'ip', 'perdhidr', 'vazmin', 'numbas')

        lista1 = ( 'NUMMAQ', 'POTEFE', 'COEFEVAP', 'VOLMIN', 'VOLMAX',
                   'nummaq', 'potefe', 'coefevap', 'volmin', 'volmax')

        lista2 = ( 'COTAREA', 'VOLCOTA', 'cotaarea', 'volcota')

        lista3 = ( 'CFUGA', 'VAZMINT', 'CMONT',
                   'cfuga', 'vazmint', 'cmont')

        lista4 = ( 'VMINP', 'VMINT', 'VMAXT', 'vminp', 'vmint', 'vmaxt')

        df = self.bloco_usina['df']

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write(" P.CHAVE  MODIFICACOES E INDICES \n" )
                f.write(" XXXXXXXX XXXXXXXXXXXXXXXXXXXXX \n" )

                tamanho = df.shape
                tamanho = tamanho[0]

                linha = 0

                conta_usi = 0

                while linha < tamanho:

                    registro = df.iloc[linha].values
                    codigo = int(registro[1])
                    comentario = registro[2]
                    conta_usi += 1

                    #
                    # Cria dataframe apenas com a usina. Este procedimento é para manter a ordem do arquivo original
                    #

                    usinadf = df[df['codigo'] == codigo]
                    nr_reg = usinadf.shape
                    nr_reg = nr_reg[0]
                    reg = 0

                    formato = " {key: <8} {codigo: <33} {comentarios: <40}\n"

                    row = dict(
                        key='USINA',
                        codigo=codigo,
                        comentarios=comentario
                    )
                    f.write(formato.format(**row))

                    while reg < nr_reg:
                        registro = usinadf.iloc[reg].values

                        if registro[4] in lista0:
                            if ( registro[4].upper() == 'NUMCNJ' or
                                 registro[4].upper() == 'VAZMIN' or
                                 registro[4].upper() == 'NUMBAS'):
                                formato = " {key: <8} {valor: >6d}\n"
                            elif ( registro[4].upper() == 'PRODESP' ):
                                formato = " {key: <8} {valor: >12.8f}\n"
                            else:
                                formato = " {key: <8} {valor: >6.3f}\n"
                            row = dict(
                                        key=registro[4],
                                        valor=int(registro[5])
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista1:
                            if ( registro[4].upper() == 'NUMMAQ' or registro[4].upper() == 'COEFEVAP' ):
                                formato = " {key: <8} {valor: >6d} {valorb: <3d}\n"
                                row = dict(
                                            key=registro[4],
                                            valor=int(registro[5]),
                                            valorb=int(registro[6])
                                          )
                            elif ( registro[4].upper() == 'VOLMIN' or registro[4].upper() == 'VOLMAX' ):
                                formato = " {key: <8} {valor: >10.3f} {valorb: <3}\n"
                                row = dict(
                                    key=registro[4],
                                    valor=registro[5],
                                    valorb=registro[6]
                                )
                            else:
                                formato = " {key: <8} {valor: >10.4f} {valorb: <2d}\n"
                                row = dict(
                                            key=registro[4],
                                            valor=registro[5],
                                            valorb=int(registro[6])
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista2:
                            formato = " {key: <8} {a: >10} {b: <10} {c: >10} {d: >10} {e: >10}\n"
                            row = dict(
                                        key=registro[4],
                                        a=registro[5][0],
                                        b=registro[5][1],
                                        c=registro[5][2],
                                        d=registro[5][3],
                                        e=registro[5][4],
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista3:
                            formato = " {key: <8} {mes:>2} {ano:>4} {valor: >7.3f}\n"
                            row = dict(
                                        key=registro[4],
                                        ano=registro[0],
                                        mes=registro[3],
                                        valor=registro[5]
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista4:
                            formato = " {key: <8} {mes:>2} {ano:>4} {valor: >7.3f} {valorb: <3}\n"
                            row = dict(
                                        key=registro[4],
                                        ano=registro[0],
                                        mes=registro[3],
                                        valor=registro[5],
                                        valorb=registro[6]
                                      )
                            f.write(formato.format(**row))
                        reg += 1
                    #
                    # Pula para próxima usina
                    #
                    registro = df.iloc[linha].values
                    codigo = int(registro[1])
                    while codigo == int(registro[1]):
                        linha += 1
                        if linha == tamanho:
                            break
                        registro = df.iloc[linha].values

            print('OK! Escrita do', os.path.split(file_out)[1] ,'realizada com sucesso. (', conta_usi,
                  'Usinas Hidraulicas Modificadas )')

        except Exception:
            raise