import os
from typing import IO
import pandas as pd


from PySDDP.dessem.script.templates.operuh import OperuhTemplate

COMENTARIO = '&'

class Operuh (OperuhTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo OPERUH do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementação dos metodos de
    leitura e escrita
    """

    def __init__(self):
        super().__init__()

        self.restricoes_operativas = None

        self.rest = dict()
        self.elem = dict()
        self.lim =  dict()
        self.var = dict()
        self.rest_df: pd.DataFrame()
        self.elem_df: pd.DataFrame()
        self.lim_df: pd.DataFrame()
        self.var_df: pd.DataFrame()

        self._comentarios_ = None

    def ler(self,file_name: str) -> None:
        """
        Metodo para leitura do arquivo com as Restricoes Operativas para as Usinas Hidroeletricas

        Manual do Usuario III.2 Arquivo contendo informações sobre as restrições operativas para os reservatórios,
        geradores e vertedouros das usinas hidroelétricas, e para o bombeamento das usinas elevatórias (OPERUH.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        dir_base = os.path.split(file_name)[0]

        self.restricoes_operativas = list()

        # Listas referentes a operuh.rest
        self.rest['mneumo'] = list()
        self.rest['ind'] = list()
        self.rest['tipo'] = list()
        self.rest['flag_inclusao'] = list()
        self.rest['descricao'] = list()
        self.rest['vl'] = list()

        # Listas referentes a operuh.elem
        self.elem['mneumo'] = list()
        self.elem['ind'] = list()
        self.elem['num'] = list()
        self.elem['nome'] = list()
        self.elem['codigo'] = list()
        self.elem['fator'] = list()

        # Listas referentes a operuh.lim
        self.lim['mneumo'] = list()
        self.lim['ind'] = list()
        self.lim['di'] = list()
        self.lim['hi'] = list()
        self.lim['mi'] = list()
        self.lim['df'] = list()
        self.lim['hf'] = list()
        self.lim['mf'] = list()
        self.lim['vmin'] = list()
        self.lim['vmax'] = list()

        # Listas referentes a operuh.var
        self.var['mneumo'] = list()
        self.var['ind'] = list()
        self.var['di'] = list()
        self.var['hi'] = list()
        self.var['mi'] = list()
        self.var['df'] = list()
        self.var['hf'] = list()
        self.var['mf'] = list()
        self.var['vmin_rel'] = list()
        self.var['vmax_rel'] = list()
        self.var['vmin'] = list()
        self.var['vmax'] = list()

        self._comentarios_ = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]
                # Seguir o manual do usuario
                continua = True

                while continua:

                    self.next_line(f)

                    linha = self.linha.strip()
                    # Se a linha for comentario não faço nada e pula para proxima linha
                    if linha[0] == COMENTARIO:
                        self._comentarios_.append(linha)
                        self.restricoes_operativas.append(linha)

                        continue

                    mneumo = linha[:13].strip().lower()

                    self.restricoes_operativas.append(linha[:13])


                    # Leitura dos dados de acordo com o mneumo correspondente
                    if mneumo == 'operuh rest':
                        self.rest['mneumo'].append(self.linha[:13])
                        self.rest['ind'].append(self.linha[14:19])
                        self.rest['tipo'].append(self.linha[21:22])
                        self.rest['flag_inclusao'].append(self.linha[24:25])
                        self.rest['descricao'].append(self.linha[27:39])
                        self.rest['vl'].append(self.linha[40:50])

                        self.dados['operuh rest']['valores'] = self.rest
                        self.rest_df = pd.DataFrame(self.rest)

                        continue
                    if mneumo == 'operuh elem':
                        self.elem['mneumo'].append(self.linha[:13])
                        self.elem['ind'].append(self.linha[14:19])
                        self.elem['num'].append(self.linha[20:23])
                        self.elem['nome'].append(self.linha[25:37])
                        self.elem['codigo'].append(self.linha[40:42])
                        self.elem['fator'].append(self.linha[43:48])

                        self.dados['operuh elem']['valores'] = self.elem
                        self.elem_df = pd.DataFrame(self.elem)

                        continue
                    if mneumo == 'operuh lim':
                        self.lim['mneumo'].append(self.linha[:13])
                        self.lim['ind'].append(self.linha[14:19])
                        self.lim['di'].append(self.linha[20:22])
                        self.lim['hi'].append(self.linha[23:25])
                        self.lim['mi'].append(self.linha[26:27])
                        self.lim['df'].append(self.linha[28:30])
                        self.lim['hf'].append(self.linha[31:33])
                        self.lim['mf'].append(self.linha[34:35])
                        self.lim['vmin'].append(self.linha[38:48])
                        self.lim['vmax'].append(self.linha[48:58])

                        self.dados['operuh lim']['valores'] = self.lim
                        self.lim_df = pd.DataFrame(self.lim)

                        continue
                    if mneumo == 'operuh var':
                        self.var['mneumo'].append(self.linha[:13])
                        self.var['ind'].append(self.linha[14:19])
                        self.var['di'].append(self.linha[19:21])
                        self.var['hi'].append(self.linha[22:24])
                        self.var['mi'].append(self.linha[25:26])
                        self.var['df'].append(self.linha[27:29])
                        self.var['hf'].append(self.linha[30:32])
                        self.var['mf'].append(self.linha[33:34])
                        self.var['vmin_rel'].append(self.linha[37:47])
                        self.var['vmax_rel'].append(self.linha[47:57])
                        self.var['vmin'].append(self.linha[57:67])
                        self.var['vmax'].append(self.linha[67:77])

                        self.dados['operuh var']['valores'] = self.var
                        self.var_df = pd.DataFrame(self.var)

                        continue

        except Exception as err:
           if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, incluindo os comentários
                self.dados['operuh armazena']['valores'] = self.restricoes_operativas
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
           else:
                raise


    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de restricoes operativas

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding="latin-1") as f:  # type: IO[str]

                # Inicializa contadores para o loop
                num_linhas = len(self.restricoes_operativas)
                i_rest = 0
                i_elem = 0
                i_lim = 0
                i_var = 0

                for i in range(num_linhas):
                    # Verifica se a linha é um comentário
                    linha = self.restricoes_operativas[i]
                    verifica_comentario = linha[0] == COMENTARIO

                    if verifica_comentario:
                        f.write(self.restricoes_operativas[i])
                        f.write("\n")
                        continue

                    if linha == 'OPERUH REST  ':

                        for idx, value in self.rest_df.iterrows():
                            self.rest_df['vl'] = self.rest_df['vl'].str.replace('\n', '')
                            self.rest_df['descricao'] = self.rest_df['descricao'].str.replace('\n', '')
                            if idx == i_rest:
                                linha_rest = self.dados['operuh rest']['formato'].format(**value)
                                f.write(linha_rest)
                                continue

                        i_rest = i_rest + 1
                        continue

                    if linha == 'OPERUH ELEM  ':
                        for idx, value in self.elem_df.iterrows():
                            if idx == i_elem:
                                linha_elem = self.dados['operuh elem']['formato'].format(**value)
                                f.write(linha_elem)
                                continue
                        i_elem = i_elem + 1
                        continue

                    if linha == 'OPERUH LIM   ':
                        for idx, value in self.lim_df.iterrows():
                            self.lim_df['vmax'] = self.lim_df['vmax'].str.replace('\n', '')
                            if idx == i_lim:
                                linha_lim = self.dados['operuh lim']['formato'].format(**value)
                                f.write(linha_lim)
                                continue
                        i_lim = i_lim + 1
                        continue

                    if linha == 'OPERUH VAR   ':
                        for idx, value in self.var_df.iterrows():
                            if idx == i_var:
                                linha_var = self.dados['operuh var']['formato'].format(**value)
                                f.write(linha_var)
                                continue
                        i_var = i_var + 1
                        continue

        except Exception:
            raise