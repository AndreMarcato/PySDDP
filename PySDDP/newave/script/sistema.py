import os
from typing import IO
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from PySDDP.newave.script.templates.sistema import SistemaTemplate


class Sistema(SistemaTemplate):

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_sistemas = None
        self.sistema = dict()
        self.interc = dict()
        self.usinsim = dict()
        self.mercado = dict()
        self.num_anos = None

    def ler(self, file_name: str, dger) -> None:
        """
        Implementa o método para leitura do arquivo SISTEMA.DAT que contem o detalhamento dos submercados
        que são utilizados para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               dger: classe contendo os dados gerais
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_sistemas = 0
        self.numero_intercambios = 0
        self.num_anos = dger.num_anos['valor']

        # Listas referente ao dicionário bloco_sistema['df']
        self.sistema['codigo'] = list()
        self.sistema['nome'] = list()
        self.sistema['tipo'] = list()
        self.sistema['cdef_1'] = list()
        self.sistema['cdef_2'] = list()
        self.sistema['cdef_3'] = list()
        self.sistema['cdef_4'] = list()
        self.sistema['prof_1'] = list()
        self.sistema['prof_2'] = list()
        self.sistema['prof_3'] = list()
        self.sistema['prof_4'] = list()

        # Listas Referentes ao dicionario bloco_intercambio['df']
        self.interc['de']  = list()
        self.interc['para']  = list()
        self.interc['flag_tipo_interc'] = list()
        self.interc['flag_penal_interc']  = list()
        self.interc[ 'intercambio'] = list()

        # Listas Referentes ao dicionario bloco_mercado['df']
        self.mercado['codigo'] = list()
        self.mercado['pre'] = list()
        self.mercado['estudo'] = list()
        self.mercado['pos'] = list()

        # Lista Referentes ao dicionario bloco_nao_simuladas['df']
        self.usinsim['codigo'] = list()
        self.usinsim['nume_bloco'] = list()
        self.usinsim['desc_bloco'] = list()
        self.usinsim['nume_tecno'] = list()
        self.usinsim['geracao'] = list()

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                #
                # Lê bloco 1 - Patamares de Déficit
                #
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)
                linha = self.linha

                self.bloco_patamar_deficit['nr_pat_def'] = int(linha[1:4])

                #
                # Lê bloco 2 - Submercados
                #
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)
                linha = self.linha

                while linha[1:4] != '999':
                    #
                    # Incrementa contador de reservatórios equivalentes
                    #
                    self.numero_sistemas += 1

                    # Le_conteudo da linha
                    self.sistema['codigo'].append(int(linha[1:4]))
                    self.sistema['nome'].append(linha[5:15])
                    self.sistema['tipo'].append(int(linha[17:18]))
                    if len(linha.strip()) >= 18:
                        self.sistema['cdef_1'].append(float(linha[19:26]))
                        self.sistema['cdef_2'].append(float(linha[27:34]))
                        self.sistema['cdef_3'].append(float(linha[35:42]))
                        self.sistema['cdef_4'].append(float(linha[43:50]))
                        self.sistema['prof_1'].append(float(linha[51:56]))
                        self.sistema['prof_2'].append(float(linha[57:62]))
                        self.sistema['prof_3'].append(float(linha[63:68]))
                        self.sistema['prof_4'].append(float(linha[69:74]))
                    else:
                        self.sistema['cdef_1'].append(0.0)
                        self.sistema['cdef_2'].append(0.0)
                        self.sistema['cdef_3'].append(0.0)
                        self.sistema['cdef_4'].append(0.0)
                        self.sistema['prof_1'].append(0.0)
                        self.sistema['prof_2'].append(0.0)
                        self.sistema['prof_3'].append(0.0)
                        self.sistema['prof_4'].append(0.0)

                    #
                    # Lê próxima linha
                    #
                    self.next_line(f)
                    linha = self.linha

                #
                #  Lê bloco 3 - Limites de Intercâmbio ou Intercâmbio Mínimo
                #
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)
                linha = self.linha

                while linha[1:4] != '999':
                    #
                    # Incrementa contador de limites de intercâmbio
                    #
                    self.numero_intercambios += 1

                    de = int(linha[1:4])
                    para = int(linha[5:8])
                    flag_tipo_int = int(linha[23:24])
                    if len(linha.strip()) >= 31:
                        flag_penal_int = int(linha[31:32])
                    else:
                        flag_penal_int = 0

                    intercambio = np.zeros((dger.num_anos['valor'],12))
                    for iano in range(dger.num_anos['valor']):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                intercambio[iano][imes] = float(linha[7+imes*8:14+imes*8])

                    self.interc['de'].append(de)
                    self.interc['para'].append(para)
                    self.interc['flag_tipo_interc'].append(flag_tipo_int)
                    self.interc['flag_penal_interc'].append(flag_penal_int)
                    self.interc['intercambio'].append(intercambio)

                    self.next_line(f) # Pula Linha em branco

                    intercambio = ( np.zeros((dger.num_anos['valor'],12)))
                    for iano in range(dger.num_anos['valor']):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                intercambio[iano][imes] = float(linha[7+imes*8:14+imes*8])

                    self.interc['de'].append(para)
                    self.interc['para'].append(de)
                    self.interc['flag_tipo_interc'].append(flag_tipo_int)
                    self.interc['flag_penal_interc'].append(flag_penal_int)
                    self.interc['intercambio'].append(intercambio)

                    #
                    # Lê próxima linha
                    #
                    self.next_line(f)
                    linha = self.linha

                #
                #  Lê bloco 4 - Mercado de Energia
                #
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)
                linha = self.linha

                while linha[1:4] != '999':
                    #
                    # Incrementa contador de limites de intercâmbio
                    #

                    codigo = int(linha[1:4])

                    pre = np.zeros((1, 12))
                    if (dger.anos_pre['valor'] > 0):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                pre[0][imes] = float(linha[7+imes*8:14+imes*8])
                    estudo = np.zeros((dger.num_anos['valor'],12))
                    for iano in range(dger.num_anos['valor']):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                estudo[iano][imes] = float(linha[7+imes*8:14+imes*8])
                    pos = np.zeros((1,12))
                    if (dger.anos_pos['valor'] > 0):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                pos[0][imes] = float(linha[7+imes*8:14+imes*8])

                    self.mercado['codigo'].append(codigo)
                    self.mercado['pre'].append(pre)
                    self.mercado['estudo'].append(estudo)
                    self.mercado['pos'].append(pos)

                    self.next_line(f)
                    linha = self.linha

                #
                #  Lê bloco 5 - Usinas Não Simuladas
                #

                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)
                linha = self.linha

                while linha[1:4] != '999':

                    codigo = int(linha[1:4])
                    if len(linha.strip()) >= 9:
                        nume_bloco = int(linha[6:9])
                        desc_bloco = linha[11:31].rstrip("\n")
                    else:
                        nume_bloco = 0
                        desc_bloco = 'unico'
                    if len(linha.strip()) >= 36:
                        nume_tecno = int(linha[33:66])
                    else:
                        nume_tecno = 0

                    geracao = np.zeros((dger.num_anos['valor'],12))
                    for iano in range(dger.num_anos['valor']):
                        self.next_line(f)
                        linha = self.linha
                        for imes in range(12):
                            if len(linha[7+imes*8:14+imes*8].strip()) > 0:
                                geracao[iano][imes] = float(linha[7+imes*8:14+imes*8])

                    self.usinsim['codigo'].append(codigo)
                    self.usinsim['nume_bloco'].append(nume_bloco)
                    self.usinsim['desc_bloco'].append(desc_bloco)
                    self.usinsim['nume_tecno'].append(nume_tecno)
                    self.usinsim['geracao'].append(geracao)

                    self.next_line(f)
                    linha = self.linha

                #
                # Força erro de leitura para provocar exception
                #

                continua = True

                while continua:
                    self.next_line(f)

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_sistema['df'] = pd.DataFrame(self.sistema, columns = [ 'codigo',
                                                                                  'nome',
                                                                                  'tipo',
                                                                                  'cdef_1',
                                                                                  'cdef_2',
                                                                                  'cdef_3',
                                                                                  'cdef_4',
                                                                                  'prof_1',
                                                                                  'prof_2',
                                                                                  'prof_3',
                                                                                  'prof_4' ] )

                self.bloco_intercambio['df'] = pd.DataFrame(self.interc, columns = [ 'de',
                                                                                    'para',
                                                                                    'flag_tipo_interc',
                                                                                    'flat_penal_interc',
                                                                                    'intercambio' ] )

                self.bloco_mercado['df'] = pd.DataFrame(self.mercado, columns = [ 'codigo',
                                                                                  'pre',
                                                                                  'estudo',
                                                                                  'pos' ] )

                self.bloco_nao_simuladas['df'] = pd.DataFrame(self.usinsim, columns = [ 'codigo',
                                                                                        'nume_bloco',
                                                                                        'desc_bloco',
                                                                                        'nume_tecno',
                                                                                        'geracao'])

                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso.')
            else:
                raise

        return

    def escrever(self, file_out: str, dger) -> None:
        """
        Implementa o método para escrita do arquivo SISTEMA.DAT que contem o detalhamento dos submercados
        que são utilizados para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               dger: classe contendo os dados gerais
        """


        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                #
                # Escreve bloco 1 - Patamares de Déficit
                #

                f.write(" PATAMAR DE DEFICIT\n" )
                f.write(" NUMERO DE PATAMARES DE DEFICIT\n" )
                f.write(" XXX\n")

                f.write(f" {self.bloco_patamar_deficit['nr_pat_def']:3d}\n")

                #
                # Escreve bloco 2 - Submercados
                #

                f.write(" CUSTO DO DEFICIT\n" )
                f.write(" NUM|NOME SSIS.|    CUSTO DE DEFICIT POR PATAMAR  | P.U. CORTE POR PATAMAR|\n" )
                f.write(" XXX|XXXXXXXXXX| F|XXXX.XX XXXX.XX XXXX.XX XXXX.XX|X.XXX X.XXX X.XXX X.XXX\n")

                df = self.bloco_sistema['df']

                tamanho = df.shape
                tamanho = tamanho[0]

                for linha in range(tamanho):

                    registro = df.iloc[linha].values

                    if registro[3] > 0:
                        row = dict( codigo = registro[0],
                                    nome = registro[1],
                                    tipo = registro[2],
                                    cdef_1 = registro[3],
                                    cdef_2 = registro[4],
                                    cdef_3 = registro[5],
                                    cdef_4 = registro[6],
                                    prof_1 = registro[7],
                                    prof_2 = registro[8],
                                    prof_3 = registro[9],
                                    prof_4 = registro[10] )
                        formato = ' {codigo: <3} {nome: <10} {tipo: >2} {cdef_1: >7.2f} {cdef_2: >7.2f} {cdef_3: >7.2f} {cdef_4: >7.2f} {prof_1: >5.3f} {prof_2: >5.3f} {prof_3: >5.3f} {prof_4: >5.3f}\n'
                    else:
                        row = dict( codigo = registro[0],
                                    nome = registro[1],
                                    tipo = registro[2] )
                        formato = " {codigo: <3} {nome: <10} {tipo: >2} \n"

                    f.write(formato.format(**row))
                f.write(' 999\n')

                #
                # Escreve bloco 3 - Intercâmbios
                #

                f.write(" LIMITES DE INTERCAMBIO\n" )
                f.write(" A   B   A->B    B->A\n" )
                f.write(" XXX XXX XJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN. XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")

                df = self.bloco_intercambio['df']

                tamanho = df.shape
                tamanho = tamanho[0]

                linha = 0
                while linha < tamanho:
                    registro = df.iloc[linha].values

                    de = registro[0]
                    para = registro[1]
                    flag_tipo_interc = registro[2]
                    flag_penal_interc = registro[3]
                    intercambio = registro[4]

                    f.write(f" {de:3d} {para: 3d} {flag_tipo_interc: 15d}")

                    if flag_penal_interc > 0:
                        f.write(f"{flag_penal_interc: 7d}\n")
                    else:
                        f.write(f"\n")

                    for iano in range(dger.num_anos['valor']):
                        f.write(f"{dger.ano_ini['valor']+iano}  ")
                        for imes in range(12):
                            if intercambio[iano][imes] > 0:
                                f.write(f" {intercambio[iano][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")

                    f.write("\n")

                    linha += 1

                    registro = df.iloc[linha].values

                    intercambio = registro[4]
                    for iano in range(dger.num_anos['valor']):
                        f.write(f"{dger.ano_ini['valor']+iano}  ")
                        for imes in range(12):
                            if intercambio[iano][imes] > 0:
                                f.write(f" {intercambio[iano][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")

                    linha += 1
                f.write(' 999\n')

                #
                # Escreve bloco 4 - Mercado
                #

                f.write(" MERCADO DE ENERGIA TOTAL\n" )
                f.write(" XXX\n" )
                f.write("       XXXJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN. XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")

                df = self.bloco_mercado['df']

                tamanho = df.shape
                tamanho = tamanho[0]

                for linha in range(tamanho):
                    registro = df.iloc[linha].values

                    codigo = registro[0]
                    pre = registro[1]
                    estudo = registro[2]
                    pos = registro[3]

                    f.write(f" {codigo:3d}\n")

                    if (dger.anos_pre['valor'] > 0):
                        f.write(f"PRE   ")
                        for imes in range(12):
                            if pre[0][imes] > 0:
                                f.write(f" {pre[0][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")

                    for iano in range(dger.num_anos['valor']):
                        f.write(f"{dger.ano_ini['valor']+iano}  ")
                        for imes in range(12):
                            if estudo[iano][imes] > 0:
                                f.write(f" {estudo[iano][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")

                    if (dger.anos_pos['valor'] > 0):
                        f.write(f"POS   ")
                        for imes in range(12):
                            if pos[0][imes] > 0:
                                f.write(f" {pos[0][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")

                    linha += 1

                f.write(' 999\n')

                #
                # Escreve bloco 5 - Usinas Não Simuladas
                #

                f.write(" GERACAO DE USINAS NAO SIMULADAS\n" )
                f.write(" XXX  XBL  XXXXXXXXXXXXXXXXXXXX  XTE\n" )
                f.write("       XXXJAN. XXXFEV. XXXMAR. XXXABR. XXXMAI. XXXJUN. XXXJUL. XXXAGO. XXXSET. XXXOUT. XXXNOV. XXXDEZ.\n")

                df = self.bloco_nao_simuladas['df']

                tamanho = df.shape
                tamanho = tamanho[0]

                for linha in range(tamanho):
                    registro = df.iloc[linha].values

                    codigo = registro[0]
                    nume_bloco = registro[1]
                    desc_bloco = registro[2]
                    nume_tecno = registro[3]
                    geracao = registro[4]

                    if nume_tecno == 0:
                        f.write(f" {codigo:3d}  {nume_bloco:3d}  {desc_bloco:20s}\n")
                    else:
                        f.write(f" {codigo:3d}  {nume_bloco:3d}  {desc_bloco:20s}  {nume_tecno:3d}\n")

                    for iano in range(dger.num_anos['valor']):
                        f.write(f"{dger.ano_ini['valor']+iano}  ")
                        for imes in range(12):
                            if geracao[iano][imes] > 0:
                                f.write(f" {geracao[iano][imes]:6.0f}.")
                            else:
                                f.write("        ")
                        f.write("\n")
                f.write(' 999\n')

            print('OK! Escrita do', self.nome_arquivo ,'realizada com sucesso.')

        except Exception:
            raise

    def get(self, nr_sist):
        """
        Implementa o método para externar os dados de um submercado do arquivo SISTEMA.DAT

        :param nr_sist: número de sistema para o qual os dados serão alternados
        """


        if (type(nr_sist) == float) or (type(nr_sist) == int):

            sist_df = self.bloco_sistema['df'][self.bloco_sistema['df']['codigo'] == nr_sist]

            tamanho = sist_df.shape
            tamanho = tamanho[0]

            if tamanho == 0:
                return None
        else:
            return None

        registro = sist_df.iloc[0].values

        #
        # Carrega dados gerais do sistema (codigo, nome, custo/profundidade déficit
        #

        sist = dict()
        sist['codigo'] = registro[0]
        sist['nome'] = registro[1]
        sist['tipo'] = registro[2]
        sist['cdef'] = list()
        sist['cdef'].append(registro[3])
        sist['cdef'].append(registro[4])
        sist['cdef'].append(registro[5])
        sist['cdef'].append(registro[6])
        sist['prof'] = list()
        sist['prof'].append(registro[7])
        sist['prof'].append(registro[8])
        sist['prof'].append(registro[9])
        sist['prof'].append(registro[10])

        #
        # Carrega Dados do Mercado (pré, estudo e pós estudo)
        #

        sist_df = self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == nr_sist]
        registro = sist_df.iloc[0].values
        sist['mercado_pre'] = registro[1]
        sist['mercado_estudo'] = registro[2]
        sist['mercado_pos'] = registro[3]

        #
        # Carrega os Dados de Usinas Não Simuladas
        #

        sist_df = self.bloco_nao_simuladas['df'][self.bloco_nao_simuladas['df']['codigo'] == nr_sist]

        tamanho = sist_df.shape
        tamanho = tamanho[0]

        sist['nao_simuladas'] = list()

        for i in range(tamanho):
            registro = sist_df.iloc[i].values
            nao_sim = dict()
            nao_sim['nume_bloco'] = registro[1]
            nao_sim['desc_bloco'] = registro[2]
            nao_sim['nume_tecno'] = registro[3]
            nao_sim['geracao'] = registro[4]
            sist['nao_simuladas'].append(nao_sim)

        return sist


    def put(self, sist):
        """
        Implementa o método para alterar os dados de um submercado do arquivo SISTEMA.DAT

        :param sist: dicionário de dados contendo os dados a serem externados. Observação: a estrutura do dicionários de
                     dados deve ser a mesma que a obtida através do comando get.
        """


        sist_df = self.bloco_sistema['df'][self.bloco_sistema['df']['codigo'] == sist['codigo']]

        tamanho = sist_df.shape
        tamanho = tamanho[0]

        if tamanho == 0:
            return None

        #
        # Carrega dados gerais do sistema (codigo, nome, custo/profundidade déficit
        #


        self.bloco_sistema['df'][self.bloco_sistema['df']['codigo'] == sist['codigo']] = [ sist['codigo'],
                                                                                           sist['nome'].ljust(10),
                                                                                           sist['tipo'],
                                                                                           sist['cdef'][0],
                                                                                           sist['cdef'][1],
                                                                                           sist['cdef'][2],
                                                                                           sist['cdef'][3],
                                                                                           sist['prof'][0],
                                                                                           sist['prof'][1],
                                                                                           sist['prof'][2],
                                                                                           sist['prof'][3] ]

        #
        # Carrega Dados do Mercado (pré, estudo e pós estudo)
        #

        serie_pre = self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == sist['codigo']]['pre'].values
        serie_est = self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == sist['codigo']]['estudo'].values
        serie_pos = self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == sist['codigo']]['pos'].values

        serie_pre[0] = sist['mercado_pre']
        serie_est[0] = sist['mercado_estudo']
        serie_pos[0] = sist['mercado_pos']

        self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == sist['codigo']] = [ sist['codigo'],
                                                                                           serie_pre,
                                                                                           serie_est,
                                                                                           serie_pos ]

        #
        # Carrega os Dados de Usinas Não Simuladas
        #

        for nao_sim in sist['nao_simuladas']:

            serie = self.bloco_nao_simuladas['df'][(self.bloco_nao_simuladas['df']['codigo'] == sist['codigo']) &
                                           (self.bloco_nao_simuladas['df']['nume_bloco'] == nao_sim['nume_bloco'])]['geracao'].values

            serie[0] = nao_sim['geracao']

            self.bloco_nao_simuladas['df'][(self.bloco_nao_simuladas['df']['codigo'] == sist['codigo']) &
                                           (self.bloco_nao_simuladas['df']['nume_bloco'] == nao_sim['nume_bloco'])] = \
                                                        [ sist['codigo'],
                                                          nao_sim['nume_bloco'],
                                                          nao_sim['desc_bloco'],
                                                          nao_sim['nume_tecno'],
                                                          serie
                                                        ]

        return

    def get_interc(self, de, para):
        """
        Implementa o método para externar os dados de um elo de transmissão obtido no arquivo SISTEMA.DAT

        :param de: sistema de origem para a transmissão do bloco de energia
               para: sistema destino para o qual será enviado o bloco de energia.
        """


        if (type(de) == float) or (type(de) == int) and (type(para) == float) or (type(para) == int):

            interc_df = self.bloco_intercambio['df'][(self.bloco_intercambio['df']['de'] == de) &
                                                     (self.bloco_intercambio['df']['para'] == para)]

            tamanho = interc_df.shape
            tamanho = tamanho[0]

            if tamanho == 0:
                return None
        else:
            return None

        registro = interc_df.iloc[0].values

        #
        # Carrega dados gerais do intercambio
        #

        interc = dict()
        interc['de'] = registro[0]
        interc['para'] = registro[1]
        interc['flag_tipo_interc'] = registro[2]
        interc['flag_penal_interc'] = registro[3]
        interc['valor'] = registro[4]

        return interc

    def put_interc(self, interc):
        """
        Implementa o método para alterar os dados de um elo de transmissão no arquivo SISTEMA.DAT

        :param interc: dicionário de dados contento as informação sobre o link de transmissão. ATENÇÃO: deve estar
                       com a mesma estrutura do dicionário externado pelo comando get_interc
        """


        interc_df = self.bloco_intercambio['df'][(self.bloco_intercambio['df']['de'] == interc['de']) &
                                                 (self.bloco_intercambio['df']['para'] == interc['para'])]

        tamanho = interc_df.shape
        tamanho = tamanho[0]

        if tamanho == 0:
            return None

        serie = self.bloco_intercambio['df'][(self.bloco_intercambio['df']['de'] == interc['de']) &
                                             (self.bloco_intercambio['df']['para'] == interc['para'])]['intercambio'].values

        serie[0] =  interc['valor']

        self.bloco_intercambio['df'][(self.bloco_intercambio['df']['de'] == interc['de']) &
                                     (self.bloco_intercambio['df']['para'] == interc['para'])] = [ interc['de'],
                                                                                                   interc['para'],
                                                                                                   interc['flag_tipo_interc'],
                                                                                                   interc['flag_penal_interc'],
                                                                                                   serie ]
        return

    def plota_mercado(self,sistema):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(sistema['mercado_estudo'])
        nr_col = len(sistema['mercado_estudo'][0])

        if sistema['tipo'] == 0:
            carga = sistema['mercado_estudo'][0:nr_lin][0:nr_col]
            ax.plot(np.arange(1, nr_lin * nr_col + 1), carga.reshape(nr_lin * nr_col, ), 'r-', lw=3,
                    label='Mercado Total')
            for nao_sim in sistema['nao_simuladas']:
                pq = nao_sim['geracao']
                ax.plot(np.arange(1, nr_lin * nr_col + 1), pq.reshape(nr_lin * nr_col, ), '--', lw=2,
                        label=nao_sim['desc_bloco'])

            titulo = 'Evolucao do Mercado Total do ' + sistema['nome']
            f.canvas.set_window_title(titulo)

            ax.set_title(titulo, fontsize=16)
            ax.set_xlabel('Meses de Estudo', fontsize=14)
            ax.set_ylabel('Demanda de Energia (MWmes)', fontsize=14)
            ax.legend(fontsize=12)

            plt.show()


    # Plota Mercado de Todos os Submercados
    def plota_sistema(self):

        f, (ax) = plt.subplots(1, 1)

        sist_df = self.bloco_sistema['df'][self.bloco_sistema['df']['tipo'] == 0 ]

        nr_lin = len(sist_df['nome'].values)
        nr_lin = len(self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == 1]['estudo'].values[0])
        nr_col = len(self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == 1]['estudo'].values[0][0])
        total = np.zeros((nr_lin, nr_col), 'd')

        nomes = sist_df['nome'].values
        codigos = sist_df['codigo'].values

        for i, mercado in enumerate(codigos):
            if mercado == 1:
                cor = 'lime'
                linha = '--'
                LineWidth = 2
            elif mercado == 2:
                cor = 'blue'
                linha = '--'
                LineWidth = 2
            elif mercado == 3:
                cor = 'chocolate'
                linha = '--'
                LineWidth = 2
            elif mercado == 4:
                cor = 'black'
                linha = '-'
                LineWidth = 3
            else:
                cor = 'orange'
                linha = '-'
                LineWidth = 3
            y = self.bloco_mercado['df'][self.bloco_mercado['df']['codigo'] == mercado]['estudo'].values[0]
            ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                    lw=LineWidth, label=nomes[i])
            ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                            (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
            total += y

        titulo = 'Evolucao da Demanda Total do Sistema'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Demanda de Energia (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()





