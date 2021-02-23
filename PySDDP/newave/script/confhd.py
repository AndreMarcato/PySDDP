import os
from typing import IO

from PySDDP.newave.script.templates.confhd import ConfhdTemplate
from matplotlib import pyplot as plt
import numpy as np
from random import randint
from mpl_toolkits.mplot3d import Axes3D


class Confhd(ConfhdTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    def ler(self, file_name: str, hidr, vazoes, dger, modif, exph) -> None:
        """
        Implementa o método para leitura do arquivo HIDR.DAT que contem os dados cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               hidr: classe contendo o cadastro de todas as usinas hidreletrica,
               vazoes: classe contendo o historico de vazoes completo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._copiavazoes = vazoes.vaz_nat
        self._numero_registros_ = 0
        self.nuhe = 0

        nanos = dger.num_anos['valor']

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                contador = 1
                while continua:

                    self.next_line(f)

                    linha = self.linha

                    if contador >= 3:
                        if len(linha) > 5:
                            self._codigo["valor"].append(int(linha[1:5]))
                        else:
                            break
                        self._nome["valor"].append(linha[6:18])
                        self._posto["valor"].append(int(linha[19:23]))
                        self._jusante["valor"].append(int(linha[25:29]))
                        self._ree["valor"].append(int(linha[30:34]))
                        self._vol_ini["valor"].append(float(linha[35:41]))
                        self._status["valor"].append(linha[44:46])
                        self._modif["valor"].append(int(linha[49:53]))
                        self._ano_i["valor"].append(int(linha[58:62]))
                        self._ano_f["valor"].append(int(linha[67:71]))

                        # Preenche com dados cadastrais
                        uhe = hidr.get(self._codigo["valor"][-1])
                        self._bdh['valor'].append(uhe['bdh'])
                        self._sist['valor'].append(uhe['sist'])
                        self._empr['valor'].append(uhe['empr'])
                        self._desvio['valor'].append(uhe['desvio'])
                        self._vol_min['valor'].append(uhe['vol_min'])
                        self._vol_max['valor'].append(uhe['vol_max'])
                        self._vol_vert['valor'].append(uhe['vol_vert'])
                        self._vol_min_desv['valor'].append(uhe['vol_min_desv'])
                        self._cota_min['valor'].append(uhe['cota_min'])
                        self._cota_max['valor'].append(uhe['cota_max'])
                        self._pol_cota_vol['valor'].append(uhe['pol_cota_vol'])
                        self._pol_cota_area['valor'].append(uhe['pol_cota_area'])
                        self._coef_evap['valor'].append(uhe['coef_evap'])
                        self._num_conj_maq['valor'].append(uhe['num_conj_maq'])
                        self._maq_por_conj['valor'].append(uhe['maq_por_conj'])
                        self._pef_por_conj['valor'].append(uhe['pef_por_conj'])
                        self._cf_hbqt['valor'].append(uhe['cf_hbqt'])
                        self._cf_hbqt['valor_2'].append(uhe['cf_hbqt_2'])
                        self._cf_hbqt['valor_3'].append(uhe['cf_hbqt_3'])
                        self._cf_hbqt['valor_4'].append(uhe['cf_hbqt_4'])
                        self._cf_hbqt['valor_5'].append(uhe['cf_hbqt_5'])
                        self._cf_hbqg['valor'].append(uhe['cf_hbqg'])
                        self._cf_hbqg['valor_2'].append(uhe['cf_hbqg_2'])
                        self._cf_hbqg['valor_3'].append(uhe['cf_hbqg_3'])
                        self._cf_hbqg['valor_4'].append(uhe['cf_hbqg_4'])
                        self._cf_hbqg['valor_5'].append(uhe['cf_hbqg_5'])
                        self._cf_hbpt['valor'].append(uhe['cf_hbpt'])
                        self._cf_hbpt['valor_2'].append(uhe['cf_hbpt_2'])
                        self._cf_hbpt['valor_3'].append(uhe['cf_hbpt_3'])
                        self._cf_hbpt['valor_4'].append(uhe['cf_hbpt_4'])
                        self._cf_hbpt['valor_5'].append(uhe['cf_hbpt_5'])
                        self._alt_efet_conj['valor'].append(uhe['alt_efet_conj'])
                        self._vaz_efet_conj['valor'].append(uhe['vaz_efet_conj'])
                        self._prod_esp['valor'].append(uhe['prod_esp'])
                        self._perda_hid['valor'].append(uhe['perda_hid'])
                        self._num_pol_vnj['valor'].append(uhe['num_pol_vnj'])
                        self._pol_vaz_niv_jus['valor'].append(uhe['pol_vaz_niv_jus'])
                        self._pol_vaz_niv_jus['valor_2'].append(uhe['pol_vaz_niv_jus_2'])
                        self._pol_vaz_niv_jus['valor_3'].append(uhe['pol_vaz_niv_jus_3'])
                        self._pol_vaz_niv_jus['valor_4'].append(uhe['pol_vaz_niv_jus_4'])
                        self._pol_vaz_niv_jus['valor_5'].append(uhe['pol_vaz_niv_jus_5'])
                        self._cota_ref_nivel_jus['valor'].append(uhe['cota_ref_nivel_jus'])
                        self._cfmed['valor'].append(uhe['cfmed'])
                        self._inf_canal_fuga['valor'].append(uhe['inf_canal_fuga'])
                        self._fator_carga_max['valor'].append(uhe['fator_carga_max'])
                        self._fator_carga_min['valor'].append(uhe['fator_carga_min'])
                        self._vaz_min['valor'].append(uhe['vaz_min'])
                        self._unid_base['valor'].append(uhe['unid_base'])
                        self._tipo_turb['valor'].append(uhe['tipo_turb'])
                        self._repres_conj['valor'].append(uhe['repres_conj'])
                        self._teifh['valor'].append(uhe['teifh'])
                        self._ip['valor'].append(uhe['ip'])
                        self._tipo_perda['valor'].append(uhe['tipo_perda'])
                        self._data['valor'].append(uhe['data'])
                        self._observ['valor'].append(uhe['observ'])
                        self._vol_ref['valor'].append(uhe['vol_ref'])
                        self._tipo_reg['valor'].append(uhe['tipo_reg'])

                        # Inclui as vazoes naturais
                        vaz_nat = vazoes.vaz_nat.transpose()
                        vaz_nat = vaz_nat[self._posto["valor"][-1]-1]
                        vaz_nat = vaz_nat.transpose()
                        self._vazoes['valor'].append(vaz_nat)

                        # Se a usina for 'NE' ou 'EE' nao deve possuir maquinas
                        if self._status['valor'][-1] == 'NE' or self._status['valor'][-1] == 'EE':
                            for iconj in range(5):
                                self._maq_por_conj['valor'][-1][iconj] = 0

                        # Parametros Temporais controlados pelo MODIF.DAT
                        self._vol_mint['valor'].append(self._vol_min['valor'][-1]*np.ones((nanos, 12), 'f'))
                        self._vol_maxt['valor'].append(self._vol_max['valor'][-1]*np.ones((nanos, 12), 'f'))
                        self._vol_minp['valor'].append(self._vol_min['valor'][-1]*np.ones((nanos, 12), 'f'))
                        self._vaz_mint['valor'].append(self._vaz_min['valor'][-1]*np.ones((nanos, 12), 'f'))
                        self._cfugat['valor'].append(self._cfmed['valor'][-1]*np.ones((nanos, 12), 'f'))
                        self._cmont['valor'].append(self._cota_max['valor'][-1]*np.ones((nanos, 12), 'f'))

                        #
                        # Calcula Volume Útil
                        #
                        if self._tipo_reg['valor'][-1] == 'M':
                            self._vol_util['valor'].append(self._vol_max['valor'][-1] - self._vol_min['valor'][-1])
                        else:
                            self._vol_util['valor'].append(float(0))
                            self._vol_min['valor'][-1] = self._vol_max['valor'][-1]

                        # Incorpora Modificações do MODIF.DAT
                        usinadf = modif.bloco_usina['df'][modif.bloco_usina['df']['codigo'] == self._codigo['valor'][-1]]
                        self._acerta_modif(usinadf, dger)

                        # Calcula Parametros

                        #
                        # Re-Calcula Volume Útil
                        #
                        if self._tipo_reg['valor'][-1] == 'M':
                            self._vol_util['valor'][-1] = self._vol_max['valor'][-1] - self._vol_min['valor'][-1]
                        else:
                            self._vol_min['valor'][-1] = self._vol_max['valor'][-1]

                        self._calc_pot_efetiva()
                        self._calc_vaz_efetiva()
                        self._calc_produtibs(nanos)
                        self._calc_engol_maximo()

                        # Parametros Temporais calculados pelo EXPH.DAT
                        if self._status['valor'][-1] == 'EX':
                            self._status_vol_morto['valor'].append(2 * np.ones((nanos, 12), 'i'))
                            self._status_motoriz['valor'].append(2 * np.ones((nanos, 12), 'i'))
                            self._vol_morto_tempo['valor'].append(np.zeros((nanos, 12), 'f'))
                            self._engol_tempo['valor'].append(self._engolimento['valor'][-1] * np.ones((nanos, 12), 'f'))
                            self._potencia_tempo['valor'].append(self._pot_efet['valor'][-1] * np.ones((nanos, 12), 'f'))
                            self._unidades_tempo['valor'].append(sum(self._maq_por_conj['valor'][-1]) * np.ones((nanos, 12), 'f'))
                        else:
                            self._status_vol_morto['valor'].append(np.zeros((nanos, 12), 'i'))
                            self._status_motoriz['valor'].append(np.zeros((nanos, 12), 'i'))
                            self._vol_morto_tempo['valor'].append(np.zeros((nanos, 12), 'f'))
                            if self._status['valor'][-1] == 'EE':
                                self._engol_tempo['valor'].append(self._engolimento['valor'][-1] * np.ones((nanos, 12), 'f'))
                                self._potencia_tempo['valor'].append(self._pot_efet['valor'][-1] * np.ones((nanos, 12), 'f'))
                                self._unidades_tempo['valor'].append(sum(self._maq_por_conj['valor'][-1]) * np.ones((nanos, 12), 'f'))
                            else:
                                self._engol_tempo['valor'].append(np.zeros((nanos, 12), 'f'))
                                self._potencia_tempo['valor'].append(np.zeros((nanos, 12), 'f'))
                                self._unidades_tempo['valor'].append(np.zeros((nanos, 12), 'i'))

                        #
                        # Insere matrizes com nanos x 12 para cada tipo de produtibilidade acumulada
                        #

                        self._ro_acum_a_ree['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_b_ree['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_c_ree['valor'].append(np.zeros((nanos, 12), 'd'))

                        self._ro_acum_a_sist['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_b_sist['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_c_sist['valor'].append(np.zeros((nanos, 12), 'd'))

                        self._ro_acum['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_65['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_max['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_med['valor'].append(np.zeros((nanos, 12), 'd'))
                        self._ro_acum_min['valor'].append(np.zeros((nanos, 12), 'd'))

                        # Incorpora Modificações do EXPH.DAT
                        usinadf = exph.bloco_usina['df'][exph.bloco_usina['df']['codigo'] ==  self._codigo['valor'][-1]]
                        self._acerta_exph(usinadf, dger)

                        self.nuhe += 1

                    self._numero_registros_ += 1

                    contador += 1

        except Exception as err:
            if isinstance(err, StopIteration):
                maior = np.array(self._codigo['valor'], dtype=int)
                maior = np.max(maior)
                self._mapa = -np.ones(maior+1, dtype=int)
                for i, codigo in enumerate(self._codigo['valor']):
                    self._mapa[codigo]=int(i)
                # Acerta Produtibilidades Acumuladas
                self._prod_acum()
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Implementa o método para escrita do arquivo HIDR.DAT que contem os dados cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        self._numero_registros_ = 0

        formato = "{codigo: >5} {nome: <12} {posto: >4} {jusante: >5} {ree: >4} {vol_ini: >6} {status: >4} {modif: >6} {ano_i: >8} {ano_f: >8}\n"

        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        try:

            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                # Imprime Cabeçalho

                f.write(" NUM  NOME         POSTO JUS   REE V.INIC U.EXIS MODIF INIC.HIST FIM HIST\n")
                f.write(" XXXX XXXXXXXXXXXX XXXX  XXXX XXXX XXX.XX XXXX   XXXX     XXXX     XXXX  \n")

                for iusi in range(self.nuhe):
                    linha = dict(
                        codigo=self._codigo['valor'][iusi],
                        nome=self._nome['valor'][iusi],
                        posto=self._posto['valor'][iusi],
                        jusante=self._jusante['valor'][iusi],
                        ree=self._ree['valor'][iusi],
                        vol_ini=self._vol_ini['valor'][iusi],
                        status=self._status['valor'][iusi],
                        modif=self._modif['valor'][iusi],
                        ano_i=self._ano_i['valor'][iusi],
                        ano_f=self._ano_f['valor'][iusi]
                    )
                    f.write(formato.format(**linha))
                    self._numero_registros_ += 1

        except Exception as err:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def get(self, entrada):
        """
        Busca uma usina hidreletrica do arquivo CONFHD e retorna um dicionario de dados contendo todas as
        informacoes desta usina

        :param entrada: string com o nome da usina ou inteiro com o numero de referencia da usina

        """

        if (type(entrada) == float) or (type(entrada) == int):
            #for i, valor in enumerate(self._codigo["valor"]):
            #    if valor == int(entrada):
            #        posicao = i
            #        break

            if type(entrada) == float:
                entrada = int(entrada)

            posicao = int(self._mapa[entrada])

            if posicao == -1:
                return None

        if type(entrada) == str:
            posicao = None
            for i, valor in enumerate(self._nome["valor"]):
                if (valor.upper()).strip() == (entrada.upper()).strip():
                    posicao = i
                    break
            if posicao is None:
                return None

        uhe = {
            'codigo': self._codigo['valor'][posicao],
            'nome': self._nome['valor'][posicao],
            'posto': self._posto['valor'][posicao],
            'ree': self._ree["valor"][posicao],
            'vol_ini': self._vol_ini["valor"][posicao],
            'status': self._status["valor"][posicao],
            'modif': self._modif["valor"][posicao],
            'ano_i': self._ano_i["valor"][posicao],
            'ano_f': self._ano_f["valor"][posicao],
            'bdh': self._bdh['valor'][posicao],
            'sist': self._sist['valor'][posicao],
            'empr': self._empr['valor'][posicao],
            'jusante': self._jusante['valor'][posicao],
            'desvio': self._desvio['valor'][posicao],
            'vol_min': self._vol_min['valor'][posicao],
            'vol_max': self._vol_max['valor'][posicao],
            'vol_vert': self._vol_vert['valor'][posicao],
            'vol_min_desv': self._vol_min_desv['valor'][posicao],
            'cota_min': self._cota_min['valor'][posicao],
            'cota_max': self._cota_max['valor'][posicao],
            'pol_cota_vol': self._pol_cota_vol['valor'][posicao],
            'pol_cota_area': self._pol_cota_area['valor'][posicao],
            'coef_evap': self._coef_evap['valor'][posicao],
            'num_conj_maq': self._num_conj_maq['valor'][posicao],
            'maq_por_conj': self._maq_por_conj['valor'][posicao],
            'pef_por_conj': self._pef_por_conj['valor'][posicao],
            'cf_hbqt': self._cf_hbqt['valor'][posicao],
            'cf_hbqt_2': self._cf_hbqt['valor_2'][posicao],
            'cf_hbqt_3': self._cf_hbqt['valor_3'][posicao],
            'cf_hbqt_4': self._cf_hbqt['valor_4'][posicao],
            'cf_hbqt_5': self._cf_hbqt['valor_5'][posicao],
            'cf_hbqg': self._cf_hbqg['valor'][posicao],
            'cf_hbqg_2': self._cf_hbqg['valor_2'][posicao],
            'cf_hbqg_3': self._cf_hbqg['valor_3'][posicao],
            'cf_hbqg_4': self._cf_hbqg['valor_4'][posicao],
            'cf_hbqg_5': self._cf_hbqg['valor_5'][posicao],
            'cf_hbpt': self._cf_hbpt['valor'][posicao],
            'cf_hbpt_2': self._cf_hbpt['valor_2'][posicao],
            'cf_hbpt_3': self._cf_hbpt['valor_3'][posicao],
            'cf_hbpt_4': self._cf_hbpt['valor_4'][posicao],
            'cf_hbpt_5': self._cf_hbpt['valor_5'][posicao],
            'alt_efet_conj': self._alt_efet_conj['valor'][posicao],
            'vaz_efet_conj': self._vaz_efet_conj['valor'][posicao],
            'prod_esp': self._prod_esp['valor'][posicao],
            'perda_hid': self._perda_hid['valor'][posicao],
            'num_pol_vnj': self._num_pol_vnj['valor'][posicao],
            'pol_vaz_niv_jus': self._pol_vaz_niv_jus['valor'][posicao],
            'pol_vaz_niv_jus_2': self._pol_vaz_niv_jus['valor_2'][posicao],
            'pol_vaz_niv_jus_3': self._pol_vaz_niv_jus['valor_3'][posicao],
            'pol_vaz_niv_jus_4': self._pol_vaz_niv_jus['valor_4'][posicao],
            'pol_vaz_niv_jus_5': self._pol_vaz_niv_jus['valor_5'][posicao],
            'cota_ref_nivel_jus': self._cota_ref_nivel_jus['valor'][posicao],
            'cfmed': self._cfmed['valor'][posicao],
            'inf_canal_fuga': self._inf_canal_fuga['valor'][posicao],
            'fator_carga_max': self._fator_carga_max['valor'][posicao],
            'fator_carga_min': self._fator_carga_min['valor'][posicao],
            'vaz_min': self._vaz_min['valor'][posicao],
            'unid_base': self._unid_base['valor'][posicao],
            'tipo_turb': self._tipo_turb['valor'][posicao],
            'repres_conj': self._repres_conj['valor'][posicao],
            'teifh': self._teifh['valor'][posicao],
            'ip': self._ip['valor'][posicao],
            'tipo_perda': self._tipo_perda['valor'][posicao],
            'data': self._data['valor'][posicao],
            'observ': self._observ['valor'][posicao],
            'vol_ref': self._vol_ref['valor'][posicao],
            'tipo_reg': self._tipo_reg['valor'][posicao],
            'vazoes': self._vazoes['valor'][posicao],
            'vol_mint': self._vol_mint['valor'][posicao],
            'vol_maxt': self._vol_maxt['valor'][posicao],
            'vol_minp': self._vol_minp['valor'][posicao],
            'vaz_mint': self._vaz_mint['valor'][posicao],
            'cmont': self._cmont['valor'][posicao],
            'cfugat': self._cfugat['valor'][posicao],
            'vol_util': self._vol_util['valor'][posicao],
            'pot_efet': self._pot_efet['valor'][posicao],
            'vaz_efet': self._vaz_efet['valor'][posicao],
            'status_vol_morto': self._status_vol_morto['valor'][posicao],
            'status_motoriz': self._status_motoriz['valor'][posicao],
            'vol_morto_tempo': self._vol_morto_tempo['valor'][posicao],
            'engol_tempo': self._engol_tempo['valor'][posicao],
            'potencia_tempo': self._potencia_tempo['valor'][posicao],
            'unidades_tempo': self._unidades_tempo['valor'][posicao],
            'ro_65': self._ro_65['valor'][posicao],
            'ro_50': self._ro_50['valor'][posicao],
            'ro_equiv': self._ro_equiv['valor'][posicao],
            'ro_equiv65': self._ro_equiv65['valor'][posicao],
            'ro_min': self._ro_min['valor'][posicao],
            'ro_max': self._ro_max['valor'][posicao],
            'engolimento': self._engolimento['valor'][posicao],
            'ro_acum_a_ree': self._ro_acum_a_ree['valor'][posicao],
            'ro_acum_b_ree': self._ro_acum_b_ree['valor'][posicao],
            'ro_acum_c_ree': self._ro_acum_c_ree['valor'][posicao],
            'ro_acum_a_sist': self._ro_acum_a_sist['valor'][posicao],
            'ro_acum_b_sist': self._ro_acum_b_sist['valor'][posicao],
            'ro_acum_c_sist': self._ro_acum_c_sist['valor'][posicao],
            'ro_acum': self._ro_acum['valor'][posicao],
            'ro_acum_65': self._ro_acum_65['valor'][posicao],
            'ro_acum_max': self._ro_acum_max['valor'][posicao],
            'ro_acum_med': self._ro_acum_med['valor'][posicao],
            'ro_acum_med': self._ro_acum_min['valor'][posicao]
        }

        return uhe

    def put(self, uhe):
        """
        Atualiza os dados da usina com do CONFHD de acordo com o dicionario de dados fornecido na entrada.
        As chaves do dicionario de dados de entrada devem ser as mesmas do dicionario obtido atraves do
        comando get.

        :param uhe: dicionario de dados contendo informacoes da usina a ser atualizada.

        """

        posicao = None
        for i, valor in enumerate(self._codigo["valor"]):
            if valor == uhe['codigo']:
                posicao = i
                break
        if posicao is None:
            return None

        self._codigo['valor'][posicao] = uhe['codigo']
        self._nome['valor'][posicao] = uhe['nome']
        self._posto['valor'][posicao] = uhe['posto']
        self._bdh['valor'][posicao] = uhe['bdh']
        self._sist['valor'][posicao] = uhe['sist']
        self._empr['valor'][posicao] = uhe['empr']
        self._jusante['valor'][posicao] = uhe['jusante']
        self._desvio['valor'][posicao] = uhe['desvio']
        self._vol_min['valor'][posicao] = uhe['vol_min']
        self._vol_max['valor'][posicao] = uhe['vol_max']
        self._vol_vert['valor'][posicao] = uhe['vol_vert']
        self._vol_min_desv['valor'][posicao] = uhe['vol_min_desv']
        self._cota_min['valor'][posicao] = uhe['cota_min']
        self._cota_max['valor'][posicao] = uhe['cota_max']
        self._pol_cota_vol['valor'][posicao] = uhe['pol_cota_vol']
        self._pol_cota_area['valor'][posicao] = uhe['pol_cota_area']
        self._coef_evap['valor'][posicao] = uhe['coef_evap']
        self._num_conj_maq['valor'][posicao] = uhe['num_conj_maq']
        self._maq_por_conj['valor'][posicao] = uhe['maq_por_conj']
        self._pef_por_conj['valor'][posicao] = uhe['pef_por_conj']
        self._cf_hbqt['valor'][posicao] = uhe['cf_hbqt']
        self._cf_hbqt['valor_2'][posicao] = uhe['cf_hbqt_2']
        self._cf_hbqt['valor_3'][posicao] = uhe['cf_hbqt_3']
        self._cf_hbqt['valor_4'][posicao] = uhe['cf_hbqt_4']
        self._cf_hbqt['valor_5'][posicao] = uhe['cf_hbqt_5']
        self._cf_hbqg['valor'][posicao] = uhe['cf_hbqg']
        self._cf_hbqg['valor_2'][posicao] = uhe['cf_hbqg_2']
        self._cf_hbqg['valor_3'][posicao] = uhe['cf_hbqg_3']
        self._cf_hbqg['valor_4'][posicao] = uhe['cf_hbqg_4']
        self._cf_hbqg['valor_5'][posicao] = uhe['cf_hbqg_5']
        self._cf_hbpt['valor'][posicao] = uhe['cf_hbpt']
        self._cf_hbpt['valor_2'][posicao] = uhe['cf_hbpt_2']
        self._cf_hbpt['valor_3'][posicao] = uhe['cf_hbpt_3']
        self._cf_hbpt['valor_4'][posicao] = uhe['cf_hbpt_4']
        self._cf_hbpt['valor_5'][posicao] = uhe['cf_hbpt_5']
        self._alt_efet_conj['valor'][posicao] = uhe['alt_efet_conj']
        self._vaz_efet_conj['valor'][posicao] = uhe['vaz_efet_conj']
        self._prod_esp['valor'][posicao] = uhe['prod_esp']
        self._perda_hid['valor'][posicao] = uhe['perda_hid']
        self._num_pol_vnj['valor'][posicao] = uhe['num_pol_vnj']
        self._pol_vaz_niv_jus['valor'] = uhe['pol_vaz_niv_jus']
        self._pol_vaz_niv_jus['valor_2'][posicao] = uhe['pol_vaz_niv_jus_2']
        self._pol_vaz_niv_jus['valor_3'][posicao] = uhe['pol_vaz_niv_jus_3']
        self._pol_vaz_niv_jus['valor_4'][posicao] = uhe['pol_vaz_niv_jus_4']
        self._pol_vaz_niv_jus['valor_5'][posicao] = uhe['pol_vaz_niv_jus_5']
        self._cota_ref_nivel_jus['valor'][posicao] = uhe['cota_ref_nivel_jus']
        self._cfmed['valor'][posicao] = uhe['cfmed']
        self._inf_canal_fuga['valor'][posicao] = uhe['inf_canal_fuga']
        self._fator_carga_max['valor'][posicao] = uhe['fator_carga_max']
        self._fator_carga_min['valor'][posicao] = uhe['fator_carga_min']
        self._vaz_min['valor'][posicao] = uhe['vaz_min']
        self._unid_base['valor'][posicao] = uhe['unid_base']
        self._tipo_turb['valor'][posicao] = uhe['tipo_turb']
        self._repres_conj['valor'][posicao] = uhe['repres_conj']
        self._teifh['valor'][posicao] = uhe['teifh']
        self._ip['valor'][posicao] = uhe['ip']
        self._tipo_perda['valor'][posicao] = uhe['tipo_perda']
        self._data['valor'][posicao] = uhe['data']
        self._observ['valor'][posicao] = uhe['observ']
        self._vol_ref['valor'][posicao] = uhe['vol_ref']
        self._tipo_reg['valor'][posicao] = uhe['tipo_reg']
        self._vazoes['valor'][posicao] = uhe['vazoes']
        self._vol_mint['valor'][posicao] = uhe['vol_mint']
        self._vol_maxt['valor'][posicao] = uhe['vol_maxt']
        self._vol_minp['valor'][posicao] = uhe['vol_minp']
        self._vaz_mint['valor'][posicao] = uhe['vaz_mint']
        self._cfugat['valor'][posicao] = uhe['cfugat']
        self._vol_util['valor'][posicao] = uhe['vol_util']
        self._pot_efet['valor'][posicao] = uhe['pot_efet']
        self._vaz_efet['valor'][posicao] = uhe['vaz_efet']
        self._status_vol_morto['valor'][posicao] = uhe['status_vol_morto']
        self._status_motoriz['valor'][posicao] = uhe['status_motoriz']
        self._vol_morto_tempo['valor'][posicao] = uhe['vol_morto_tempo']
        self._engol_tempo['valor'][posicao] = uhe['engol_tempo']
        self._potencia_tempo['valor'][posicao] = uhe['potencia_tempo']
        self._unidades_tempo['valor'][posicao] = uhe['unidades_tempo']
        self._ro_65['valor'][posicao] = uhe['ro_65']
        self._ro_50['valor'][posicao] = uhe['ro_50']
        self._ro_equiv['valor'][posicao] = uhe['ro_equiv']
        self._ro_equiv65['valor'][posicao] = uhe['ro_equiv65']
        self._ro_min['valor'][posicao] = uhe['ro_min']
        self._ro_max['valor'][posicao] = uhe['ro_max']
        self._engolimento['valor'][posicao] = uhe['engolimento']

        print(np.shape(self._copiavazoes))
        for iano in range(np.shape(self._copiavazoes)[0]):
            for imes in range(12):
                self._copiavazoes[iano][imes][self._posto['valor'][posicao]-1] = self._vazoes['valor'][posicao][iano][imes]

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario de dados obtido pelo comando get.

        :param parametro: string contendo a chave do dicionario de dados cuja o detalhamento eh desejado

        """


        duvida = getattr(self, '_'+parametro)

        return duvida['descricao']


    # Calcula Vazao Incremental
    def vaz_inc(self, uhe, iano, imes):

        def Montante(uhe, iano, imes):
            for iusi in self.lista_uhes():
                usina = self.get(iusi)
                if usina['jusante'] == uhe['codigo']:
                    if usina['status_vol_morto'][iano][imes] == 2:
                        yield iusi
                    else:
                        yield from Montante(usina, iano, imes)

        # Inicia a vazão incremental da uhe com a sua vazão natural, depois abate as naturais de montante

        incremental = uhe['vazoes'][:,imes]

        if uhe['status_vol_morto'][iano][imes] != 2:
            print ('Erro: Tentativa de calculo de Incremental para usina (', uhe['nome'], ') fora de operacao no mes ', imes, ' e ano ', iano)
            return 0
        else:
            for iusina in Montante(uhe, iano, imes):
                usina = self.get(iusina)
                incremental = incremental - usina['vazoes'][:,imes]

        # Caso Alguma Incremental seja Menor que zero, força para zero
        codigos = np.where(incremental<0)
        incremental[codigos] = 0

        return incremental

    def vaz_inc_entre_res(self, codigo, ianoconf, imesconf):

        uhe = self.get(codigo)

        nanos_hist = len(uhe['vazoes'])

        def Montante(codigo, iano, imes):
            #for iusi in self.lista_uhes():
            #    usina = self.get(iusi)
            for iusi, jusante in enumerate(self._jusante['valor']):
                if jusante == codigo:
                    if self._status_vol_morto['valor'][iusi][iano][imes] == 2:
                        if self._vol_util['valor'][iusi] > 0:
                            yield iusi
                        else:
                            yield from Montante(self._codigo['valor'][iusi], iano, imes)
                    else:
                        yield from Montante(self._codigo['valor'][iusi], iano, imes)

        if uhe['status_vol_morto'][ianoconf][imesconf] != 2:
            print ('Erro: Tentativa de calculo de Incremental para usina (', uhe['nome'], ') fora de operacao no mes ', imesconf, ' e ano ', ianoconf)
            return 0
        else:
            incremental = np.zeros(nanos_hist)
            for ianoh in range(nanos_hist):
                incremental[ianoh] = uhe['vazoes'][ianoh][imesconf]
            for iusina in Montante(codigo, ianoconf, imesconf):
                for ianoh in range(nanos_hist):
                    incremental[ianoh] = incremental[ianoh] - self._vazoes['valor'][iusina][ianoh][imesconf]

        # Caso Alguma Incremental seja Menor que zero, força para zero
        codigos = np.where(incremental<0)
        incremental[codigos] = 0

        return incremental

    ##########################################################################################################
    # Calcula Parametros das Usinas
    ##########################################################################################################

    #def _calc_vol_util(self):     # Calcula Volume Util da Usina
    #    if self._tipo_reg['valor'][-1] == 'M':
    #        self._vol_util['valor'].append(self._vol_max['valor'][-1] - self._vol_min['valor'][-1])
    #    else:
    #        self._vol_util['valor'].append(float(0))
    #        self._vol_min['valor'][-1] = self._vol_max['valor'][-1]

    def _calc_pot_efetiva(self):     # Calcula Potencia Efetiva da Usina
        a = np.array(self._maq_por_conj["valor"][-1])
        b = np.array(self._pef_por_conj["valor"][-1])
        self._pot_efet['valor'].append(np.vdot(a, b))

    def _calc_vaz_efetiva(self):      # Calcula Vazao Efetiva da Usina
        a = np.array(self._maq_por_conj["valor"][-1])
        b = np.array(self._vaz_efet_conj["valor"][-1])
        self._vaz_efet['valor'].append(np.vdot(a, b))

    def _calc_produtibs(self, nanos):       # Calcula Produtibilidades Associadas aa diversos volumes
        self._ro_65['valor'].append(np.zeros( (nanos,12), 'd' ))
        self._ro_50['valor'].append(np.zeros( (nanos,12), 'd' ))
        self._ro_equiv['valor'].append(np.zeros( (nanos,12), 'd' ))
        self._ro_equiv65['valor'].append(np.zeros( (nanos,12), 'd' ))
        self._ro_min['valor'].append(np.zeros( (nanos,12), 'd' ))
        self._ro_max['valor'].append(np.zeros( (nanos,12), 'd' ))

        a = self._pol_cota_vol["valor"][-1][0]
        b = self._pol_cota_vol["valor"][-1][1]
        c = self._pol_cota_vol["valor"][-1][2]
        d = self._pol_cota_vol["valor"][-1][3]
        e = self._pol_cota_vol["valor"][-1][4]

        # Calcula Produtibilidade Associada a 65% do Volume Util
        volume = self._vol_min['valor'][-1] + 0.65*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self._cfugat['valor'][-1][iano][imes]
                if self._tipo_perda['valor'][-1] == 2:
                    self._ro_65['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga - self._perda_hid['valor'][-1])
                else:
                    self._ro_65['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga)*(1. - self._perda_hid['valor'][-1]/100)

        # Calcula Produtibilidade Associada a 50% do Volume Util
        volume = self._vol_min['valor'][-1] + 0.50*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self._cfugat['valor'][-1][iano][imes]
                if self._tipo_perda['valor'][-1] == 2:
                    self._ro_50['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga - self._perda_hid['valor'][-1])
                else:
                    self._ro_50['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga)*(1. - self._perda_hid['valor'][-1]/100)

        # Calcula Produtibilidade Associada ao Volume Maximo
        volume = self._vol_max['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self._cfugat['valor'][-1][iano][imes]
                if self._tipo_perda['valor'][-1] == 2:
                    self._ro_max['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga - self._perda_hid['valor'][-1])
                else:
                    self._ro_max['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga)*(1. - self._perda_hid['valor'][-1]/100)

        # Calcula Produtibilidade Associada ao Volume Minimo
        volume = self._vol_min['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self._cfugat['valor'][-1][iano][imes]
                if self._tipo_perda['valor'][-1] == 2:
                    self._ro_min['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga - self._perda_hid['valor'][-1])
                else:
                    self._ro_min['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota - cfuga)*(1. - self._perda_hid['valor'][-1]/100)

        # Calcula Produtibilidade Equivalente
        if ( self._vol_util['valor'][-1] > 0):
            cota = 0
            cota65 = 0
            Vol65 = self._vol_min['valor'][-1] + 0.65*self._vol_util['valor'][-1]
            for i in range(5):
                cota = cota + self._pol_cota_vol["valor"][-1][i] * (self._vol_max['valor'][-1]**(i+1)) / (i+1)
                cota = cota - self._pol_cota_vol["valor"][-1][i] * (self._vol_min['valor'][-1]**(i+1)) / (i+1)
                cota65 = cota65 + self._pol_cota_vol["valor"][-1][i] * (Vol65**(i+1)) / (i+1)
                cota65 = cota65 - self._pol_cota_vol["valor"][-1][i] * (self._vol_min['valor'][-1]**(i+1)) / (i+1)
            cota = cota / self._vol_util['valor'][-1]
            cota65 = cota65 / (Vol65 - self._vol_min['valor'][-1])
        else:
            cota65 = cota
        for iano in range(nanos):
            for imes in range(12):
                cfuga = self._cfugat['valor'][-1][iano][imes]
                if self._tipo_perda['valor'][-1] == 2:
                    self._ro_equiv['valor'][-1][iano][imes]   = self._prod_esp['valor'][-1] * (cota   - cfuga - self._perda_hid['valor'][-1])
                    self._ro_equiv65['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota65 - cfuga - self._perda_hid['valor'][-1])
                else:
                    self._ro_equiv['valor'][-1][iano][imes]   = self._prod_esp['valor'][-1] * (cota   - cfuga)*(1. - self._perda_hid['valor'][-1]/100)
                    self._ro_equiv65['valor'][-1][iano][imes] = self._prod_esp['valor'][-1] * (cota65 - cfuga)*(1. - self._perda_hid['valor'][-1]/100)
        return

    def _prod_acum(self):

        def cascata(confhd, codigo, iano,imes):
            current = confhd.get(codigo)
            if current['status_vol_morto'][iano][imes] == 2:
                yield current['codigo']
            while current['jusante'] != 0:
                current = confhd.get(current['jusante'])
                if current['status_vol_morto'][iano][imes] == 2:
                    yield current['codigo']

        #
        # Percorre todas as usinas do confhd para inserir produtibilidades acumuladas
        #

        for reg, codigo in enumerate(self._codigo['valor']):

            nanos = len(self._status_vol_morto['valor'][reg])

            #
            # As produtibilidades devem ser calculadas para cada mês/ano do histórico
            #

            for iano in range(nanos):
                for imes in range(12):
                    trocouRee = 0
                    trocouSist = 0
                    FioRee = True
                    FioSist = True

                    for iusina in cascata(self, codigo, iano, imes):
                        uhe = self.get(iusina)
                        produtib    = uhe['ro_equiv'][iano][imes]
                        produtib65  = uhe['ro_equiv65'][iano][imes]
                        produtibMax = uhe['ro_max'][iano][imes]
                        produtibMed = uhe['ro_65'][iano][imes]
                        produtibMin = uhe['ro_min'][iano][imes]
                        if uhe['status_motoriz'][iano][imes] == 2:
                            self._ro_acum['valor'][reg][iano][imes] += produtib
                            self._ro_acum_65['valor'][reg][iano][imes]  += produtib65
                            self._ro_acum_max['valor'][reg][iano][imes] += produtibMax
                            self._ro_acum_med['valor'][reg][iano][imes] +=  produtibMed
                            self._ro_acum_min['valor'][reg][iano][imes] +=  produtibMin
                        if uhe['sist'] != self._sist['valor'][reg]:
                            trocouSist = trocouSist + 1
                        if uhe['ree'] != self._ree['valor'][reg]:
                            trocouRee = trocouRee + 1

                        if trocouRee == 0:
                            if uhe['status_motoriz'][iano][imes] == 2:
                                self._ro_acum_a_ree['valor'][reg][iano][imes] += produtib
                        else:
                            if uhe['vol_util'] > 0:
                                FioRee = False
                            if FioRee:
                                if uhe['status_motoriz'][iano][imes] == 2:
                                    self._ro_acum_b_ree['valor'][reg][iano][imes] += produtib
                            else:
                                if uhe['status_motoriz'][iano][imes] == 2:
                                    self._ro_acum_c_ree['valor'][reg][iano][imes] += produtib

                        if trocouSist == 0:
                            if uhe['status_motoriz'][iano][imes] == 2:
                                self._ro_acum_a_sist['valor'][reg][iano][imes] += produtib
                        else:
                            if uhe['vol_util'] > 0:
                                FioSist = False
                            if FioSist:
                                if uhe['status_motoriz'][iano][imes] == 2:
                                    self._ro_acum_b_sist['valor'][reg][iano][imes] += produtib
                            else:
                                if uhe['status_motoriz'][iano][imes] == 2:
                                    self._ro_acum_c_sist['valor'][reg][iano][imes] += produtib

    def _prod_acum_entre_res_ree(self, uhe, iano, imes):

        if uhe['jusante'] == 0:
            return 0

        uhe_nova = self.get(uhe['jusante'])

        if uhe_nova['vol_util'] != 0:
            return 0.
        elif uhe_nova['ree'] != uhe['ree']:
            return 0.
        elif uhe_nova['status_motoriz'][iano][imes] == 2:
            return uhe_nova['ro_equiv'] + self._prod_acum_entre_res_ree(uhe_nova, iano, imes)
        else:
            return self._prod_acum_entre_res_ree(uhe_nova, iano, imes)
    #
    # def ProdAcumEntreResSist(self, iano, imes, usinas):
    #     if self.Jusante == 0:
    #         return 0
    #     for iusina in usinas:
    #         if iusina.Codigo == self.Jusante:
    #             if iusina.VolUtil != 0:
    #                 return 0.
    #             elif self.Sist != iusina.Sist:
    #                 return 0.
    #             elif iusina.StatusMotoriz[iano][imes] == 2:
    #                 return iusina.RoEquiv + iusina.ProdAcumEntreResSist(iano, imes, usinas)
    #             else:
    #                 return iusina.ProdAcumEntreResSist(iano, imes, usinas)
    #             break


    def _calc_engol(self, ql):
        engol = 0.
        for i in range(5):   # Varre Conjuntos de Maquinas
            if self._maq_por_conj['valor'][-1][i] > 0:
                if ql < self._alt_efet_conj['valor'][-1][i]:
                    if self._tipo_turb == 1 or self._tipo_turb == 3:
                        alpha = 0.5
                    else:
                        alpha = 0.2
                else:
                    alpha = -1
                if self._alt_efet_conj['valor'][-1][i] != 0:
                    engol = engol + self._maq_por_conj['valor'][-1][i]*self._vaz_efet_conj['valor'][-1][i]*((ql/self._alt_efet_conj['valor'][-1][i])**alpha)
        return engol

    def _calc_engol_maximo(self):    # Estima Engolimento Maximo da Usina

        a = self._pol_cota_vol['valor'][-1][0]
        b = self._pol_cota_vol['valor'][-1][1]
        c = self._pol_cota_vol['valor'][-1][2]
        d = self._pol_cota_vol['valor'][-1][3]
        e = self._pol_cota_vol['valor'][-1][4]

        # Calcula Engolimento a 65% do Volume Util
        volume = self._vol_min['valor'][-1] + 0.65*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda65 = cota - self._cfmed['valor'][-1]
        engol65 = self._calc_engol(queda65)

        # Calcula Engolimento a 50% do Volume Util
        volume = self._vol_min['valor'][-1] + 0.50*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda50 = cota - self._cfmed['valor'][-1]
        engol50 = self._calc_engol(queda50)

        # Calcula Engolimento Associada ao Volume Maximo
        volume = self._vol_max['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMax = cota - self._cfmed['valor'][-1]
        engolMax = self._calc_engol(quedaMax)

        # Calcula Engolimento Associada ao Volume Minimo
        volume = self._vol_min['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMin = cota - self._cfmed['valor'][-1]
        engolMin = self._calc_engol(quedaMin)

        # Calcula Engolimento Associado a Altura Equivalente
        if ( self._vol_util['valor'][-1] > 0):
            cota = 0
            for i in range(5):
                cota = cota + self._pol_cota_vol['valor'][-1][i] * (self._vol_max['valor'][-1]**(i+1)) / (i+1)
                cota = cota - self._pol_cota_vol['valor'][-1][i] * (self._vol_min['valor'][-1]**(i+1)) / (i+1)
            cota = cota / self._vol_util['valor'][-1]
        quedaEquiv = cota - self._cfmed['valor'][-1]
        engolEquiv = self._calc_engol(quedaEquiv)

        self._engolimento['valor'].append((engol50+engol65+engolEquiv+engolMax+engolMin)/5)

        return

    def lista_uhes(self):
        """
        Calcula um generator contendo todos os codigos de referencia das usinas pertencentes ao CONFHD.

        """

        for i in range(self.nuhe):
            yield self._codigo["valor"][i]

    def _acerta_modif(self, df, dger):
        tamanho = df.shape
        tamanho = tamanho[0]
        for linha in range(tamanho):
            registro = df.iloc[linha].values
            #
            # Palavras chaves tipo zero - somente atualiza valores
            #
            if registro[4].upper() == 'NUMCNJ':
                self._num_conj_maq['valor'][-1] = registro[5]
            if registro[4].upper() == 'PRODESP':
                self._prod_esp['valor'][-1] = registro[5]
            if registro[4].upper() == 'TEIF':
                self._teifh['valor'][-1] = registro[5]
            if registro[4].upper() == 'IP':
                self._ip['valor'][-1] = registro[5]
            if registro[4].upper() == 'PERDHID':
                self._perda_hid['valor'][-1] = registro[5]
            if registro[4].upper() == 'VAZMIN':
                self._vaz_min['valor'][-1] = registro[5]
            if registro[4].upper() == 'NUMBAS':
                self._unid_base['valor'][-1] = registro[5]
            #
            # Palavras chaves tipo um - dois campos
            #
            if registro[4].upper() == 'NUMMAQ':
                nr_conj = int(registro[6])
                self._maq_por_conj['valor'][-1][nr_conj-1] = int(registro[5])
            if registro[4].upper() == 'POTEFE':
                nr_conj = int(registro[6])
                self._pef_por_conj['valor'][-1][nr_conj-1] = registro[5]
            if registro[4].upper() == 'COEFEVAP':
                mes = int(registro[6])
                self._coef_evap['valor'][-1][mes-1] = registro[5]
            if registro[4].upper() == 'VOLMIN':
                if registro[6].find("%") == 1:
                    self._vol_min['valor'][-1] = self._vol_min['valor'][-1] + \
                                                 float(registro[5]) * self._vol_util['valor'][-1] / 100
                if registro[6].find("h") == 1:
                    self._vol_min['valor'][-1] = registro[5]
            if registro[4].upper() == 'VOLMAX':
                if registro[6].find("%") == 1:
                    self._vol_max['valor'][-1] = self._vol_min['valor'][-1] + \
                                                 float(registro[5]) * self._vol_util['valor'][-1] / 100
                if registro[6].find("h") == 1:
                    self._vol_max['valor'][-1] = registro[5]
            #
            # Palavras chaves tipo dois - coeficientes PCA e PCV
            #
            if registro[4].upper() == 'VOLCOTA':
                self._pol_cota_vol['valor'][-1] = registro[5]
            if registro[4].upper() == 'COTAREA':
                self._pol_cota_area['valor'][-1] = registro[5]
            #
            # Palavras chaves tipo 3 - Data e valor
            #
            if registro[4].upper() == 'CFUGA':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        self._cfugat['valor'][-1][ano][mes] = registro[5]
                        mes += 1
                    mes = 0
                    ano += 1
            if registro[4].upper() == 'VAZMINT':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        self._vaz_mint['valor'][-1][ano][mes] = registro[5]
                        mes += 1
                    mes = 0
                    ano += 1
            if registro[4].upper() == 'CMONT':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        self._cmont['valor'][-1][ano][mes] = registro[5]
                        mes += 1
                    mes = 0
                    ano += 1
            #
            # Palavras chaves tipo 4 - Data, valor e ('h' ou '%')
            #
            if registro[4].upper() == 'VMINP':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        if registro[6].find("h") == 1:
                            self._vol_minp['valor'][-1][ano][mes] = registro[5]
                        if registro[6].find("%") == 1:
                            self._vol_minp['valor'][-1][ano][mes] = self._vol_min['valor'][-1] + \
                                                                float(registro[5]) * self._vol_util['valor'][-1] / 100
                        mes += 1
                    mes = 0
                    ano += 1
            if registro[4].upper() == 'VMINT':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        if registro[6].find("h") == 1:
                            self._vol_mint['valor'][-1][ano][mes] = registro[5]
                        if registro[6].find("%") == 1:
                            self._vol_mint['valor'][-1][ano][mes] = self._vol_min['valor'][-1] + \
                                                                float(registro[5]) * self._vol_util['valor'][-1] / 100
                        mes += 1
                    mes = 0
                    ano += 1
            if registro[4].upper() == 'VMAXT':
                ano = int(registro[0]) - dger.ano_ini['valor']
                mes = int(registro[3]) - 1
                while ano < dger.num_anos['valor']:
                    while mes < 12:
                        if registro[6].find("h") == 1:
                            self._vol_maxt['valor'][-1][ano][mes] = registro[5]
                        if registro[6].find("%") == 1:
                            self._vol_maxt['valor'][-1][ano][mes] = self._vol_min['valor'][-1] + \
                                                                float(registro[5]) * self._vol_util['valor'][-1] / 100
                        mes += 1
                    mes = 0
                    ano += 1
        return

    def _acerta_exph(self, df, dger):
        tamanho = df.shape
        tamanho = tamanho[0]

        #
        # Organização do Registro
        #
        # registro[0] = 'codigo',
        # registro[1] = 'nome',
        # registro[2] = 'mesi_evm',
        # registro[3] = 'anoi_evm',
        # registro[4] = 'dura_evm',
        # registro[5] = 'perc_evm',
        # registro[6] = 'mesi_tur',
        # registro[7] = 'anoi_tur',
        # registro[8] = 'comentar',
        # registro[9] = 'nume_tur',
        # registro[10] = 'nume_cnj']

        if tamanho > 0:
            registro = df.iloc[0].values
            #
            # Trata Enchimento de Volume Morto
            #
            if not np.isnan(registro[2]):
                dur_vm = int(registro[4])
                mesinicial = int(registro[2])
                anoinicial = int(registro[3])
                volume = self._vol_min['valor'][-1] * float(registro[5]) / 100
                volume = (self._vol_min['valor'][-1] - volume) / dur_vm
                vol_frac = volume
                for iano in range(anoinicial - dger.ano_ini['valor'], dger.num_anos['valor']):
                    for imes in range(mesinicial - 1, 12):
                        if dur_vm > 0:
                            self._status_vol_morto['valor'][-1][iano][imes] = 1
                            self._vol_morto_tempo['valor'][-1][iano][imes] += volume
                            volume += vol_frac
                            dur_vm -= 1
                        else:
                            self._status_vol_morto['valor'][-1][iano][imes] = 2
                            self._vol_morto_tempo['valor'][-1][iano][imes] = 0.
                    mesinicial = 1
            else:
                self._status_vol_morto['valor'][-1] = 2 * np.ones((dger.num_anos['valor'], 12), 'i')

        for linha in range(tamanho):
            registro = df.iloc[linha].values

            if not np.isnan(registro[6]):

                #
                # Preenche evolução temporal do (1) Número de Unidades; (2) Engolimento; (3) Potência
                #
                mes_ent = int(registro[6])
                ano_ent = int(registro[7])
                pot_ent = float(registro[8])
                unidade = int(registro[9])
                conjunto = int(registro[10])

                if mes_ent > 0:
                    mesinicial = mes_ent
                    self._maq_por_conj['valor'][-1][conjunto - 1] = unidade
                    self._pef_por_conj['valor'][-1][conjunto - 1] = pot_ent
                    self._calc_pot_efetiva()
                    self._calc_engol_maximo()
                    for iano in range(ano_ent - dger.ano_ini['valor'], dger.num_anos['valor']):
                        for imes in range(mesinicial - 1, 12):
                            self._unidades_tempo['valor'][-1][iano][imes] += 1
                            self._engol_tempo['valor'][-1][iano][imes] = self._engolimento['valor'][-1]
                            self._potencia_tempo['valor'][-1][iano][imes] = self._pot_efet['valor'][-1]
                        mesinicial = 1

        #
        # Acerta Status da Motorização
        #
        for iano in range(dger.num_anos['valor']):
            for imes in range(12):
                if self._unidades_tempo['valor'][-1][iano][imes] >= self._unid_base['valor'][-1]:
                    self._status_motoriz['valor'][-1][iano][imes] = 2
                elif self._unidades_tempo['valor'][-1][iano][imes] > 0:
                    self._status_motoriz['valor'][-1][iano][imes] = 1
                else:
                    if self._status_motoriz['valor'][-1][iano][imes] == 2:
                        self._status_motoriz['valor'][-1][iano][imes] = 1
                    else:
                        self._status_motoriz['valor'][-1][iano][imes] = 0

    ##########################################################################################################
    # Plota Gráficos Diversos
    ##########################################################################################################

    def plota_volume(self, uhe):
        nanos = len(uhe['vol_mint'])

        fig = plt.figure()
        ax = plt.subplot(111)


        x_axis = np.arange(1,nanos*12+1)
        ax.plot(x_axis,uhe['vol_mint'].reshape(nanos*12),'g-.',lw=2, label = 'Vol.Min.Operat.')
        ax.plot(x_axis,uhe['vol_maxt'].reshape(nanos*12),'g-.',lw=2, label = 'Vol.Max.Operat.')
        ax.plot(x_axis,uhe['vol_max']*np.ones(nanos*12),'b-',lw=3,   label = 'Vol.Minimo Real')
        ax.plot(x_axis,uhe['vol_min']*np.ones(nanos*12),'b-',lw=3,   label = 'Vol.Maximo Real')
        ax.plot(x_axis,uhe['vol_minp'].reshape(nanos*12),'b-.',lw=2, label = 'Vol.Min.com Pen.')

        plt.fill_between(x_axis,uhe['vol_mint'].reshape(nanos*12), uhe['vol_maxt'].reshape(nanos*12), facecolor='g', alpha=0.1)

        titulo = 'Evolucao dos Volumes da Usina \n' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Volume em hm^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([ box.x0, box.y0, box.width*0.7, box.height] )

        ax.legend(loc='center left', shadow=True, fontsize=12, bbox_to_anchor=(1, 0.5))

        plt.show()

    def plota_vaz_min(self, uhe):
        nanos = len(uhe['vaz_mint'])

        fig = plt.figure()
        ax = plt.subplot(111)

        x_axis = np.arange(1,nanos*12+1)
        ax.plot(x_axis,uhe['vaz_mint'].reshape(nanos*12),'g-.',lw=2, label='Vaz.Min.Operat.')
        ax.plot(x_axis,uhe['vaz_min']*np.ones(nanos*12),'b-',lw=3,   label='Vaz.Min.Cadastro')

        titulo = 'Evolucao da Vazao Minima da Usina \n' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Vazao Minima em m^3', fontsize=16)

        box = ax.get_position()

        ax.set_position([ box.x0, box.y0, box.width*0.7, box.height] )

        ax.legend(loc='center left', shadow=True, fontsize=12, bbox_to_anchor=(1, 0.5))

        plt.show()

    def plota_volmorto(self, uhe):

        if uhe['status'] == 'EX':
            print('Grafico de Volume Morto nao impresso, pois ', uhe['nome'], 'e uma usina existente')
            return

        nanos = len(uhe['vol_morto_tempo'])

        nmeses = np.count_nonzero(uhe['vol_morto_tempo'])

        legenda = str(nmeses) + ' Meses'

        ax = plt.subplot(111)

        x_axis = np.arange(1,nanos*12+1)
        p1 = ax.plot(x_axis,uhe['vol_morto_tempo'].reshape(nanos*12),'g-.',lw=2, label = legenda )

        titulo = 'Enchimento do Volume Morto da Usina \n' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Volume Morto em hm^3', fontsize=16)

        plt.legend(fontsize=12)

        np.count_nonzero(uhe['vol_morto_tempo'])

        plt.show()

    def plota_potencia(self, uhe):

        nanos = len(uhe['potencia_tempo'])

        ax = plt.subplot(111)

        x_axis = np.arange(1, nanos * 12 + 1)
        p1 = ax.plot(x_axis, uhe['potencia_tempo'].reshape(nanos * 12), 'g-.', lw=2)

        titulo = 'Evolucao da Potencia Efetiva da Usina \n' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes de Estudo', fontsize=16)
        plt.ylabel('Potencia Efetiva em MW', fontsize=16)

        plt.show()

    def plot_vaz(self, uhe):
        """
        Plota as todas as series historicas anuais da usina cujo dicionario de dados eh fornecia na entrada.
        Em ciano estao as diversas series anuais.
        Em azul escuro esta a ultima serie anual.
        Em vermelho continuo esta a media mensal.
        Em vermelho pontilhado esta a media menos ou mais o desvio padrao.

        :param uhe: Dicionario de dados contendo informacoes de uma usina hidreletrica

        """

        vaz_nat = uhe['vazoes']
        x_axis = np.arange(1, 13)
        plt.plot(x_axis, vaz_nat.transpose(), 'c-')
        media = np.mean(vaz_nat, axis=0)
        plt.plot(x_axis, media, 'r-', lw=3)
        desvio = np.nanstd(vaz_nat, axis=0)
        plt.plot(x_axis, media + desvio, 'r-.', lw=2)
        plt.plot(x_axis, media - desvio, 'r-.', lw=2)
        ultimo = len(vaz_nat) - 1
        plt.plot(x_axis, vaz_nat[:][ultimo], 'b-')
        titulo = 'Historico de Vazoes da Usina ' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.xlabel('Mes do Ano', fontsize=16)
        plt.ylabel('Vazao', fontsize=16)
        plt.show()

        return

    # Plota Polinomio Cota-Volume
    def plot_pcv(self, uhe):
        """
        Plota polinimo Cota-Volume da usina hidreletrica especificada na entrada

        :param uhe: Dicionario de dados contendo informacoes da usina hidreletrica

        """

        if uhe["vol_min"] == 0:
            return

        a = uhe['pol_cota_vol'][0]
        b = uhe['pol_cota_vol'][1]
        c = uhe['pol_cota_vol'][2]
        d = uhe['pol_cota_vol'][3]
        e = uhe['pol_cota_vol'][4]

        if (uhe["vol_min"] == uhe["vol_max"]):
            volumes = np.linspace(uhe["vol_min"] - 1,uhe["vol_max"] + 1, 100)
            cota = a + b*uhe["vol_min"] + c*uhe["vol_min"]**2 + d*uhe["vol_min"]**3 + e*uhe["vol_min"]**4
            cota = cota*np.ones(100)
        else:
            volumes = np.linspace(uhe["vol_min"],uhe["vol_max"],100)
            cota = a + b*volumes + c*volumes**2 + d*volumes**3 + e*volumes**4
            cota.shape = volumes.shape

        plt.plot(volumes, cota, 'b-', lw=3)

        plt.xlabel('Volume do Reservatorio (hm^3)', fontsize=16)
        titulo = 'Polinomio Cota-Volume da Usina ' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.ylabel('Cota em Metros', fontsize=16)
        plt.xlim(volumes[0], volumes[99])
        if ( cota[0] == cota[99]):
            plt.ylim(cota[0]-1, cota[99]+1)
        else:
            plt.ylim(cota[0], cota[99])
        plt.show()

    # Plota Polinomio Cota-Area
    def plot_pca(self, uhe):
        """
        Plota polinimo cota-area da usina hidreletrica especificada na entrada

        :param uhe: Dicionario de dados contendo informacoes da usina hidreletrica

        """

        if uhe['vol_min'] == 0:
            return

        if (uhe['cota_min'] == uhe['cota_max']):
            cotas = np.linspace(uhe['cota_min'] - 1,uhe['cota_max'] + 1, 100)
        else:
            cotas = np.linspace(uhe['cota_min'],uhe['cota_max'],100)
        a = uhe['pol_cota_area'][0]
        b = uhe['pol_cota_area'][1]
        c = uhe['pol_cota_area'][2]
        d = uhe['pol_cota_area'][3]
        e = uhe['pol_cota_area'][4]
        areas = a + b*cotas + c*cotas**2 + d*cotas**3 + e*cotas**4
        areas.shape = cotas.shape
        plt.plot(cotas, areas, 'b-', lw=3)

        plt.xlabel('Cota do Reservatorio (em metros)', fontsize=16)
        titulo = 'Polinomio Cota-Area da Usina ' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.ylabel('Area Superficia em km^2', fontsize=16)
        plt.xlim(cotas[0], cotas[99])
        if ( areas[0] == areas[99]):
            plt.ylim(areas[0]-1, areas[99]+1)
        else:
            plt.ylim(areas[0], areas[99])
        plt.show()

    # Plota Produtibilidades Constantes da Usina
    def plota_produtibs(self, uhe, iano, imes):
        """
        Plota polinimo cota-area da usina hidreletrica especificada na entrada

        :param uhe: Dicionario de dados contendo informacoes da usina hidreletrica

        """

        x_axis = np.arange(1,7)
        y_axis = [ uhe['ro_equiv'][iano][imes], uhe['ro_equiv65'][iano][imes], uhe['ro_min'][iano][imes],
                   uhe['ro_50'][iano][imes], uhe['ro_65'][iano][imes], uhe['ro_max'][iano][imes] ]
        fig, ax = plt.subplots()
        a, b, c, d, e, f = plt.bar(x_axis, y_axis)
        a.set_facecolor('r')
        b.set_facecolor('g')
        c.set_facecolor('b')
        d.set_facecolor('y')
        e.set_facecolor('m')
        f.set_facecolor('c')
        ax.set_xticks(x_axis)
        ax.set_xticklabels(['Equiv', 'Equiv65', 'Min', '50%', '65%', 'Max'])
        titulo = 'Produtibilidades da Usina ' + uhe['nome'] + ' - Ano: ' + str(iano+1) + ' - Mês:' + str(imes+1)
        plt.title(titulo, fontsize=16)
        plt.xlabel('Tipo de Produtibilidade', fontsize=16)
        plt.ylabel('Produtibilidade', fontsize=16)
        plt.show()

    # Plota Variação de Produtibilidade
    def plot_var_prod(self, uhe):
        """
        Plota variacao da produtibilidade da usina hidreletrica especificada na entrada

        :param uhe: Dicionario de dados contendo informacoes da usina hidreletrica

        """

        if uhe['vol_min'] == 0:
            return
        a = uhe['pol_cota_vol'][0]
        b = uhe['pol_cota_vol'][1]
        c = uhe['pol_cota_vol'][2]
        d = uhe['pol_cota_vol'][3]
        e = uhe['pol_cota_vol'][4]

        if (uhe["vol_min"] == uhe["vol_max"]):
            volumes = np.linspace(uhe["vol_min"] - 1,uhe["vol_max"] + 1, 100)
            cotamont = a + b*uhe["vol_min"] + c*uhe["vol_min"]**2 + d*uhe["vol_min"]**3 + e*uhe["vol_min"]**4
            cotamont = cotamont*np.ones(100)
        else:
            volumes = np.linspace(uhe["vol_min"],uhe["vol_max"],100)
            cotamont = a + b*volumes + c*volumes**2 + d*volumes**3 + e*volumes**4
            cotamont.shape = volumes.shape

        qdef = np.linspace(uhe['vaz_min'], 2*uhe['engolimento'], 100)

        a = uhe['pol_vaz_niv_jus'][0]
        b = uhe['pol_vaz_niv_jus'][1]
        c = uhe['pol_vaz_niv_jus'][2]
        d = uhe['pol_vaz_niv_jus'][3]
        e = uhe['pol_vaz_niv_jus'][4]

        cotajus = a + b*qdef + c*qdef**2 + d*qdef**3 + e*qdef**4
        cotajus.shape = qdef.shape

        xGrid, yGrid = np.meshgrid(cotamont, cotajus)

        z = uhe['prod_esp'] * ( xGrid - yGrid )

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surf = ax.plot_surface(qdef, volumes,z, rcount=100, ccount = 100, cmap=plt.cm.coolwarm,
                       linewidth=0, antialiased=False)

        plt.xlabel('Vazão Defluente em m^3/s', fontsize=12)
        titulo = 'Produtibilidade da Usina ' + uhe['nome']
        plt.title(titulo, fontsize=16)
        plt.ylabel('Volume Armazenado em hm^3', fontsize=12)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()


    # Plota Usinas Não Existentes e Existentes em Expansao
    def plota_expansao(self):

        # Conta quantas usinas estao
        cont = 0
        nomes = []
        for iusi, status in enumerate(self._status['valor']):
            if status == 'EE' or status == 'NE':
                cont += 1
                nomes.append(self._nome['valor'][iusi])

        motorizada = np.zeros(cont)
        vazia = np.zeros(cont)
        enchendo = np.zeros(cont)
        submotorizada = np.zeros(cont)

        ind = np.arange(cont)
        cont = 0
        nanos = len(self._status_vol_morto['valor'][0])
        for iusi, status in enumerate(self._status['valor']):
            if status == 'EE' or status == 'NE':
                # Meses em que a usina esta motorizada
                motorizada[cont] = nanos * 12 - np.count_nonzero(self._status_motoriz['valor'][iusi] - 2)

                # Meses que a usina ainda nao iniciou o enchimento do volume morto
                vazia[cont] = nanos * 12 - np.count_nonzero(self._status_vol_morto['valor'][iusi])

                # Meses que a usina encontra-se enchendo o volume morto
                enchendo[cont] = nanos * 12 - np.count_nonzero(self._status_vol_morto['valor'][iusi] - 1)

                # Meses que a usina encontra-se motorizando
                submotorizada[cont] = nanos * 12 - np.count_nonzero(self._status_motoriz['valor'][iusi] - 1)

                cont += 1

        width = 0.35  # the width of the bars: can also be len(x) sequence

        ax = plt.axes()
        p1 = plt.barh(ind, vazia, width, color='w')
        p2 = plt.barh(ind, enchendo, width, color='lime', left=vazia)
        p3 = plt.barh(ind, submotorizada, width, color='sienna', left=vazia + enchendo)
        p4 = plt.barh(ind, motorizada, width, color='black', left=vazia + enchendo + submotorizada)

        plt.ylabel('Usinas', fontsize=16)
        plt.title('Usinas Hidreletricas em Expansao', fontsize=16)
        plt.yticks(ind, nomes, fontsize=12)
        plt.xticks(np.arange(0, nanos * 12 + 2, 12))
        # plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Nao Entrou', 'Enchendo Vol. Morto', 'Submotorizada', 'Motorizada'),
                   fontsize=12)
        plt.xlabel('Meses do Estudo', fontsize=16)
        ax.xaxis.grid()

        plt.show()


    def parp(self, uhe, ord_max):
        """
        Implementa o método para o calculo dos coeficentes do modelo PAR(p).

        :param uhe: dicionario de dados com informacoes da usina hidreletrica,
               ord_max: ord_max do modelo PAR(p)
        :returns ordem: Ordem do modelo Ar para cada mes,
                 coef_parp: Coeficientes do modelo AR para cada mes,
                 fac: Funcao de Auto-Correlacao,
                 facp: Funcao de Auto-Correlacao Parcial,
                 residuos: Matriz de residuos

        """


        vazoes = uhe['vazoes']

        nanos = len(vazoes)   # A serie historica do ultimo ano geralmente nao vem completa (despreze-a)

        media = np.mean(vazoes[1:(nanos-1)], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(vazoes[1:(nanos-1)], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)

        # Calcula vazao normalizada (nao precisa)
        #vaznorm = np.zeros((nanos,12),'d')
        #for iano in range(nanos):
        #    for imes in range(12):
        #        vaznorm[iano][imes] = (self.Vazoes[iano][imes] - media[imes])/desvio[imes]

        # Calcula funcao de auto-correlacao (uma para cada mes)
        fac = np.zeros( (12, ord_max+1), 'd')
        for ilag in range(ord_max+1):
            for imes in range(12):
                for iano in np.arange(1,nanos-1):
                     ano_ant = iano
                     mes_ant = imes - ilag
                     if mes_ant < 0:
                         ano_ant -= 1
                         mes_ant += 12
                     fac[imes][ilag] += (vazoes[iano][imes] - media[imes]) * (vazoes[ano_ant][mes_ant] - media[mes_ant])
                fac[imes][ilag] /= (nanos-2)
                fac[imes][ilag] /= (desvio[imes]*desvio[mes_ant])

        # Calcula funcao de auto-correlacao parcial (uma para cada mes)
        facp = np.zeros((12, ord_max+1), 'd')
        for ilag in np.arange(1,ord_max+1):
            for imes in range(12):
                A = np.eye(ilag)
                B = np.zeros(ilag)
                # Preenche matriz triangular superior
                for ilin in range(len(A)):
                    for icol in range( len(A) ):           # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                        if icol > ilin:
                            mes = imes - ilin - 1
                            if mes < 0:
                               mes = mes + 12
                            A[ilin][icol] = fac[mes][icol-ilin]
                    B[ilin] = fac[imes][ilin+1]
                # Preenche matriz triangular inferior
                for ilin in range(len(A)):
                    for icol in range( len(A) ):          # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                        if icol < ilin:
                            A[ilin][icol] = A[icol][ilin]
                phi = np.linalg.solve(A,B)
                facp[imes][ilag] = phi[ len(phi)-1 ]

        # Identificacao da ordem
        IC = 1.96/np.sqrt(nanos-2)
        ordem = np.zeros(12, 'i')
        for imes in range(12):
            ordem[imes] = 0
            for ilag in range(ord_max+1):
                if facp[imes][ilag] > IC or facp[imes][ilag] < -IC:
                    ordem[imes] = ilag

        # Calculo dos coeficientes
        coef_parp = np.zeros( (12,ord_max), 'd')
        for imes in range(12):
            ilag = ordem[imes]
            A = np.eye(ilag)
            B = np.zeros(ilag)
            # Preenche matriz triangular superior
            for ilin in range(len(A)):
                for icol in range( len(A) ):             # TODO: Aqui poderia ser np.arange(ilin+1,len(A)): Testar depois
                    if icol > ilin:
                        mes = imes - ilin - 1
                        if mes < 0:
                           mes = mes + 12
                        A[ilin][icol] = fac[mes][icol-ilin]
                B[ilin] = fac[imes][ilin+1]
            # Preenche matriz triangular inferior
            for ilin in range(len(A)):
                for icol in range( len(A) ):             # TODO: Aqui poderia ser np.arange(0, ilin): Testar depois
                    if icol < ilin:
                        A[ilin][icol] = A[icol][ilin]
            phi = np.linalg.solve(A,B)
            for iord in range ( len(phi) ):
                coef_parp[imes][iord ] = phi[ iord ]

            # Calculo dos Residuos Normalizados
            residuos = np.zeros( (nanos-1, 12) )
            for iano in np.arange(1,nanos-1):
                for imes in range(12):
                    residuos[iano][imes]= ( vazoes[iano][imes]-media[imes] ) / desvio[imes]
                    for ilag in range(ord_max):
                        ano_ant = iano
                        mes_ant = imes - ilag - 1
                        if mes_ant < 0:
                            ano_ant -= 1
                            mes_ant += 12
                        residuos[iano][imes] -= coef_parp[imes][ilag]*\
                                                (vazoes[ano_ant][mes_ant]-media[mes_ant])/desvio[mes_ant]


        return ordem, coef_parp, fac, facp, residuos

    def plota_parp(self, uhe, mes, ordmax):
        """
        Implementa o método para a impressao do grafico da fac e facp para a uhe cujo
        dicionário de dados é fornecido.

        :param uhe: dicionario de dados com informacoes da usina hidreletrica,
               mes: mes de 0 a 11 (jan a dez) a ser considerado,
               ord_max: ordem maxima do modelo PAR(p)
        """


        ordem, coef_parp, fac, facp, residuos = self.parp(uhe, ordmax)

        vazoes = uhe['vazoes']

        nanos = len(vazoes) - 1

        if mes == 0:
            str_mes = 'January'
        elif mes == 1:
            str_mes = 'Fevereiro'
        elif mes == 2:
            str_mes = 'Marco'
        elif mes == 3:
            str_mes = 'Abril'
        elif mes == 4:
            str_mes = 'Maio'
        elif mes == 5:
            str_mes = 'Junho'
        elif mes == 6:
            str_mes = 'Julho'
        elif mes == 7:
            str_mes = 'Agosto'
        elif mes == 8:
            str_mes = 'Setembro'
        elif mes == 9:
            str_mes = 'Outubro'
        elif mes == 10:
            str_mes = 'Novembro'
        else:
            str_mes = 'Dezembro'

        IC = 1.96/np.sqrt(nanos-1)

        cores = []
        limitesup = []
        limiteinf = []
        for elemento in facp[mes][1:ordmax+1]:
            limitesup.append(IC)
            limiteinf.append(-IC)
            if elemento > IC or elemento < -IC:
                cores.append('r')
            else:
                cores.append('b')

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        barWidth = 0.40

        titulo = 'FAC e FACP of ' + str_mes + ' - UHE ' + uhe['nome']
        f.canvas.set_window_title(titulo)

        ax1.bar(np.arange(1,ordmax+1), fac[mes][1:ordmax+1], barWidth, align='center')
        ax2.bar(np.arange(1,ordmax+1), facp[mes][1:ordmax+1], barWidth, align='center', color = cores)
        ax2.plot(np.arange(1,ordmax+1), limitesup, 'm--', lw=1)
        ax2.plot(np.arange(1,ordmax+1), limiteinf, 'm--', lw=1)

        ax1.set_xticks(np.arange(1,ordmax+1))
        ax2.set_xticks(np.arange(1,ordmax+1))
        tituloFAC =  'FAC - Month: ' + str_mes + '\n of UHE ' + uhe['nome']
        tituloFACP = 'FACP - Month ' + str_mes +  '\n of UHE ' + uhe['nome']
        ax1.set_title(tituloFAC,  fontsize = 13)
        ax2.set_title(tituloFACP, fontsize =13)
        #ax1.xlabel('Lag')
        #ax2.xlabel('Lag')
        #ax1.ylabel('Autocorrelacao e Autocorrelacao Parcial')

        plt.show()

    def gera_cen_sinteticos(self, uhe, ord_max, nr_cen):
        """
        Implementa o método para a geração de vazões natuarais sintéticas para a uhe cujo
        dicionário de dados é fornecido.

        :param uhe: dicionario de dados com informacoes da usina hidreletrica,
               ord_max: ord_max do modelo PAR(p),
               nr_cen: numero de series sinteticas geradas
        :returns sintetica_adit: array(nseries, nestagios) contendo cenários gerados

        """


        ordem, coef_parp, fac, facp, residuos = self.parp(uhe, ord_max)

        #
        # Pega Parâmetros Básicos
        #
        nanos_estudo = len(uhe['status_vol_morto'])
        nmeses_estudo = len(uhe['status_vol_morto'][0])
        nestagios = nanos_estudo*nmeses_estudo
        vazoes = uhe['vazoes']
        nanos = len(vazoes) - 1
        media = np.mean(vazoes[1:(nanos-1)], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)
        desvio = np.std(vazoes[1:(nanos-1)], 0)    # A primeira serie historica eh utilizada como tendencia (despreze-a)

        # Gera series sinteticas
        sintetica_adit = np.zeros((nr_cen,nestagios),'d')
        for iser in range(nr_cen):
            contador = -1
            for iano in range(nanos_estudo):
                for imes in range(nmeses_estudo):
                    contador += 1
                    serie = randint(1,nanos-2)
                    valor = media[imes] + desvio[imes]*residuos[serie][imes]
                    for ilag in range(ord_max):
                        mes_ant = imes - ilag - 1
                        ano_ant = iano
                        if mes_ant < 0:
                            mes_ant += 12
                            ano_ant -= 1
                        if ano_ant < 0:
                            vazant = media[mes_ant]
                        else:
                            vazant = sintetica_adit[iser][contador-1-ilag]
                        valor += desvio[imes]*coef_parp[imes][ilag]*(vazant-media[mes_ant])/desvio[mes_ant]
                    sintetica_adit[iser][contador] = valor

        x_axis = np.arange(1, nestagios+1)
        plt.plot(x_axis, sintetica_adit.transpose(), 'c-')
        plt.plot(x_axis, np.mean(sintetica_adit,0), 'r-', lw=3, label='Mean - Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit,0) + np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2, label='Std Synthetic Series')
        plt.plot(x_axis, np.mean(sintetica_adit,0) - np.nanstd(sintetica_adit, axis=0), 'r-.', lw=2)
        m = np.concatenate([ media, media, media, media, media])
        d = np.concatenate([ desvio, desvio, desvio, desvio, desvio])
        plt.plot(x_axis, m, 'mo', lw=3, label='Mean - Hystorical Series')
        plt.plot(x_axis, m + d, 'bo', lw=2, label='Std - Hystorical Series')
        plt.plot(x_axis, m - d, 'bo', lw=2)
        titulo = uhe['nome'].strip() + "'s Synthetic Series of Natural \n" " Inflows - Aditive Noise "
        plt.title(titulo, fontsize=16)
        plt.xlabel('Month', fontsize=16)
        plt.ylabel('Inflow (m^3/s', fontsize=16)
        plt.legend(fontsize=12)
        plt.show()

        return sintetica_adit
