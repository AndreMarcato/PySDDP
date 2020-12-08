from PySDDP.dessem.script.templates.areacont import AreacontTemplate

import pandas as pd
from typing import IO
import os

COMENTARIO = '&'


class Areacont(AreacontTemplate):

    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Areacont do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.comentarios = list()
        self.area = dict()
        self.usina = dict()

    def ler(self, file_name: str) -> None:

        self.area_comentario = list()
        self.usina_comentario = list()
        # listas referentes ao dicionário AREA
        self.area['area'] = list()
        self.area['nome_area'] = list()

        # listas referentes ao dicionário USINA
        self.usina['area'] = list()
        self.usina['conjunto'] = list()
        self.usina['tipo'] = list()
        self.usina['usina'] = list()
        self.usina['nome_usina'] = list()

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:

                    self.next_line(f)
                    linha = self.linha

                    if linha[:1] == COMENTARIO:
                        self.comentarios.append(linha)

                    if linha[:4] == 'AREA':
                        self.next_line(f)
                        linha = self.linha
                        while linha[:3] != 'FIM':

                            if linha[:1] == COMENTARIO:
                                self.comentarios.append(linha)
                                self.area_comentario.append(linha)
                                self.next_line(f)
                                linha = self.linha
                            else:
                                self.area['area'].append(linha[:3])
                                self.area['nome_area'].append(linha[9:49].strip())
                                self.area_comentario.append(linha)
                                self.next_line(f)
                                linha = self.linha

                    if linha[:5] == 'USINA':
                        self.next_line(f)
                        linha = self.linha
                        while linha[:3] != 'FIM':

                            if linha[:1] == COMENTARIO:
                                self.comentarios.append(linha)
                                self.usina_comentario.append(linha)
                                self.next_line(f)
                                linha = self.linha
                            else:
                                self.usina['area'].append(linha[:3])
                                self.usina['conjunto'].append(linha[4])
                                self.usina['tipo'].append(linha[7])
                                self.usina['usina'].append(linha[9:12])
                                self.usina['nome_usina'].append(linha[14:54].strip())
                                self.usina_comentario.append(linha)
                                self.next_line(f)
                                linha = self.linha

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_area['df'] = pd.DataFrame(self.area)
                self.bloco_usina['df'] = pd.DataFrame(self.usina)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                num_linhas_area = len(self.area_comentario)
                i_area = 0
                num_linhas_usina = len(self.usina_comentario)
                i_usina  = 0
                f.write('AREA\n')
                for i in range(num_linhas_area):
                    # Verifica comentário
                    linha = self.area_comentario[i]
                    self.area_comentario[i] = self.area_comentario[i].replace('\n', '')
                    verifica_comentario = linha[0] == COMENTARIO
                    if verifica_comentario:
                        f.write(self.area_comentario[i])
                        f.write("\n")

                    else:
                        for idx, value in self.bloco_area['df'].iterrows():
                            if idx == i_area:
                                linha = self.bloco_area['formato'].format(**value)
                                f.write(linha)
                        i_area = i_area + 1
                f.write('FIM\n&\n')

                f.write('USINA\n')
                for i in range(num_linhas_usina):
                    # Verifica comentário
                    linha = self.usina_comentario[i]
                    self.usina_comentario[i] = self.usina_comentario[i].replace('\n','')
                    verifica_comentario = linha[0] == COMENTARIO
                    if verifica_comentario:
                        f.write(self.usina_comentario[i])
                        f.write("\n")

                    else:
                        for idx, value in self.bloco_usina['df'].iterrows():
                            if idx == i_usina:
                                linha = self.bloco_usina['formato'].format(**value)
                                f.write(linha)
                        i_usina = i_usina + 1
                f.write('FIM\n9999')

        except Exception:
            raise