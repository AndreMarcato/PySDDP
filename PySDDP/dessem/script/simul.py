from PySDDP.dessem.script.templates.simul import SimulTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'


class Simul(SimulTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Simul do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.comentarios = list()
        self.periodo = dict()
        self.disc = dict()
        self.voli = dict()
        self.oper = dict()

    def ler(self, file_name: str) -> None:
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:

                    self.next_line(f)
                    linha = self.linha

                    self.periodo['dia'].append(linha[4:6])
                    self.periodo['hora'].append(linha[7:9])
                    self.periodo['meiahora'].append(linha[11])
                    self.periodo['mes'].append(linha[13:15])
                    self.periodo['ano'].append(linha[17:21])
                    self.periodo['flag_restr'].append(linha[23])

                    if linha[:1] == COMENTARIO:
                        self.comentarios.append(linha)

                    if linha[:4] == 'DISC':

                        while linha[:3] != 'FIM':

                            if linha[:1] == COMENTARIO:
                                self.comentarios.append(linha)
                                self.next_line(f)
                                linha = self.linha

                            else:
                                self.disc['mneumo'].append(linha[0:3])
                                self.disc['dia'].append(linha[4:6])
                                self.disc['hora'].append(linha[7:9])
                                self.disc['meiahora'].append(linha[10])
                                self.disc['duracao'].append(linha[14:19])
                                self.disc['flag_restr'].append(linha[20])
                                self.next_line(f)
                                linha = self.linha

                    if linha[:4] == 'VOLI':

                        while linha[:3] != 'FIM':

                            if linha[:1] == COMENTARIO:
                                self.comentarios.append(linha)
                                self.next_line(f)
                                linha = self.linha
                            else:
                                self.voli['mneumo'].append(linha[:4])
                                self.voli['usina'].append(linha[4:7])
                                self.voli['nome'].append(linha[9:21])
                                self.voli['volume'].append(linha[24:34])
                                self.next_line(f)
                                linha = self.linha

                    if linha[:4] == 'OPER':

                        while linha[:3] != 'FIM':

                            if linha[:1] == COMENTARIO:
                                self.comentarios.append(linha)
                                self.next_line(f)
                                linha = self.linha
                            else:
                                self.oper['mneumo'].append(linha[:4])
                                self.oper['usina'].append(linha[4:7])
                                self.oper['tipo'].append(linha[7])
                                self.oper['nome'].append(linha[9:22])
                                self.oper['dia_inicio'].append(linha[23:25])
                                self.oper['hora_inicio'].append(linha[26:28])
                                self.oper['meiahora_inicio'].append(linha[29])
                                self.oper['dia_final'].append(linha[31:33])
                                self.oper['hora_final'].append(linha[34:36])
                                self.oper['meiahora_final'].append(linha[37])
                                self.oper['tipo_vazao'].append(linha[39])
                                self.oper['vazao'].append(linha[41:51])
                                self.oper['id_tipovazao'].append(linha[52])
                                self.oper['vazao_retirada'].append(linha[54:64])
                                self.oper['geracao'].append(linha[64:74])

                                self.next_line(f)
                                linha = self.linha

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_periodo['df'] = pd.DataFrame(self.periodo)
                self.bloco_voli['df'] = pd.DataFrame(self.voli)
                self.bloco_disc['df'] = pd.DataFrame(self.disc)
                self.bloco_oper['df'] = pd.DataFrame(self.oper)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                for idx, value in self.bloco_periodo['df'].iterrows():
                    linha = self.bloco_periodo['formato'].format(**value)
                    f.write(linha)
                f.write('FIM\n')

                for idx, value in self.bloco_disc['df'].iterrows():
                    linha = self.bloco_disc['formato'].format(**value)
                    f.write(linha)
                f.write('FIM\n')

                for idx, value in self.bloco_voli['df'].iterrows():
                    linha = self.bloco_voli['formato'].format(**value)
                    f.write(linha)
                f.write('FIM\n')

                for idx, value in self.bloco_oper['df'].iterrows():
                    linha = self.bloco_oper['formato'].format(**value)
                    f.write(linha)
                f.write('FIM\n')

        except Exception:
            raise