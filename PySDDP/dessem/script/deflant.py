# -*- coding: utf-8 -*-
from typing import Optional, IO

import pandas as pd
import os

from PySDDP.dessem.script.templates.deflant import DeflAntTemplate

MNE = 'DEFANT'
COMENTARIO = '&'


class DeflAnt(DeflAntTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo DeflAnt do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.defluencias_uhe_anteriores = dict()
        self.defluencias_uhe_anteriores_df: pd.DataFrame()
        self._comentarios_: Optional[list] = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para leitura do arquivo de defluências das usinas hidroelétricas anteriores ao estudo

        Manual do Usuario III.15 Arquivo de Defluências das Usinas Hidroelétricas Anteriores ao Estudo para Consideração
        do Tempo de Viagem (DEFLANT.XXX)

        :param file_name: string com o caminho completo para o arquivo
        :return:
        """

        # dir_base = os.path.split(file_name)[0]
        self._comentarios_ = list()

        self.defluencias_uhe_anteriores['mne'] = list()
        self.defluencias_uhe_anteriores['numuhemon'] = list()
        self.defluencias_uhe_anteriores['numuhejus'] = list()
        self.defluencias_uhe_anteriores['ent'] = list()
        self.defluencias_uhe_anteriores['di'] = list()
        self.defluencias_uhe_anteriores['hi'] = list()
        self.defluencias_uhe_anteriores['mi'] = list()
        self.defluencias_uhe_anteriores['df'] = list()
        self.defluencias_uhe_anteriores['hf'] = list()
        self.defluencias_uhe_anteriores['mf'] = list()
        self.defluencias_uhe_anteriores['defluencia'] = list()

        # noinspection PyBroadException
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:

                    self.next_line(f)

                    linha = self.linha.strip()

                    # Se linha for comentario ou diferente do mneumônico, a leitura do arquivo deve ser encerrada
                    if linha[0] == COMENTARIO:
                        self._comentarios_.append(linha)
                        continue
                    else:
                        if linha[:6] != MNE:
                            self.dados['defluencias_uhe_anteriores']['valores'] = self.defluencias_uhe_anteriores
                            self.defluencias_uhe_anteriores_df = pd.DataFrame(self.defluencias_uhe_anteriores)
                            raise NotImplementedError(f"Mneumônico {linha[:6]} não implementado!")

                        # O ideal seria validarmos antes de carregar na estrutura
                        self.defluencias_uhe_anteriores['mne'].append(self.linha[:6])
                        self.defluencias_uhe_anteriores['numuhemon'].append(self.linha[7:12])
                        self.defluencias_uhe_anteriores['numuhejus'].append(self.linha[13:17])
                        self.defluencias_uhe_anteriores['ent'].append(self.linha[18:20])
                        self.defluencias_uhe_anteriores['di'].append(self.linha[21:26])
                        self.defluencias_uhe_anteriores['hi'].append(self.linha[27:29])
                        self.defluencias_uhe_anteriores['mi'].append(self.linha[30:31])
                        self.defluencias_uhe_anteriores['df'].append(self.linha[32:34])
                        self.defluencias_uhe_anteriores['hf'].append(self.linha[35:37])
                        self.defluencias_uhe_anteriores['mf'].append(self.linha[38:39])
                        self.defluencias_uhe_anteriores['defluencia'].append(self.linha[40:54])

        except Exception as err:
            if isinstance(err, StopIteration):
                # Verifica se atingiu o final do bloco
                if self.linha[0].upper() == COMENTARIO or self.linha[:6].upper() == MNE:
                    self.dados['defluencias_uhe_anteriores']['valores'] = self.defluencias_uhe_anteriores
                    self.defluencias_uhe_anteriores_df = pd.DataFrame(self.defluencias_uhe_anteriores)
                    print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                else:
                    raise
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Metodo para escrito do arquivo de defluencias das Usinas Hidroeletricas Anteriores ao Estudo para Consideracao
        do Tempo de Viagem

        :param file_out: conjunto de parametros obrigatorios
        :return:
        """
        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Descrição
                linha = self.dados['defluencias_uhe_anteriores']['descricao']
                f.write(linha)

                # Imprime Cabeçalho
                linha = self.dados['defluencias_uhe_anteriores']['cabecalho']
                f.write(linha)

                for idx, value in self.defluencias_uhe_anteriores_df.iterrows():
                    linha = self.dados['defluencias_uhe_anteriores']['formato'].format(**value)
                    f.write(linha)

        except Exception:
            raise
