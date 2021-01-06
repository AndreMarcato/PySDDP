import os
from typing import IO

from PySDDP.newave.script.templates.confhd import ConfhdTemplate
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Confhd(ConfhdTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    def ler(self, file_name: str, hidr, vazoes) -> None:
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

        nanos = 5  # (TO DO: ALTERAR ISSO DEPOIS DE LER O DGER.DAT)

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
                        self._jusante['valor'].append(uhe['jusante'])
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

                        # Calcula Parametros
                        self._calc_vol_util()
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
                            self._unidades_tempo['valor'].append(np.zeros((nanos, 12), 'i'))
                            if self._status['valor'][-1] == 'EE':
                                self._engol_tempo['valor'].append(self._engolimento['valor'][-1] * np.ones((nanos, 12), 'f'))
                                self._potencia_tempo['valor'].append(self._pot_efet['valor'][-1] * np.ones((nanos, 12), 'f'))
                            else:
                                self._engol_tempo['valor'].append(np.zeros((nanos, 12), 'f'))
                                self._potencia_tempo['valor'].append(np.zeros((nanos, 12), 'f'))

                        self.nuhe += 1

                    self._numero_registros_ += 1

                    contador += 1

        except Exception as err:
            if isinstance(err, StopIteration):
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Implementa o método para leitura do arquivo HIDR.DAT que contem os dados cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo

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
        posicao = None
        if (type(entrada) == float) or (type(entrada) == int):
            for i, valor in enumerate(self._codigo["valor"]):
                if valor == int(entrada):
                    posicao = i
                    break
            if posicao is None:
                return None

        if type(entrada) == str:
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
            'engolimento': self._engolimento['valor'][posicao]
        }

        return uhe

    def put(self, uhe):
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

        duvida = getattr(self, '_'+parametro)

        return duvida['descricao']

    def plot_vaz(self, uhe):
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

    # Plota Variação de Produtibilidade
    def plot_var_prod(self, uhe):
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

    # Calcula Vazao Incremental
    def QInc(self, usinas, iano, imes):

        nanos_hist = len(self.Vazoes)

        def Montante(usinas, usina, iano, imes):
            for iusi in usinas:
                if iusi.Jusante == usina.Codigo:
                    if iusi.StatusVolMorto[iano][imes] == 2:
                        yield iusi
                    else:
                        yield from Montante(usinas, iusi, iano, imes)

        if self.StatusVolMorto[iano][imes] != 2:
            print ('Erro: Tentativa de calculo de Incremental para usina (', self.Nome, ') fora de operacao no mes ', imes, ' e ano ', iano)
            return 0
        else:
            Incremental = self.Vazoes[0:nanos_hist,imes]
            for iusina in Montante(usinas, self, iano, imes):
                Incremental = Incremental - iusina.Vazoes[0:nanos_hist,imes]

        if np.min(Incremental) < 0:
            contador = 0
            for i in range(nanos_hist):
                if Incremental[i] < 0:
                    Incremental[i] = 0
                    contador = contador + 1
            return Incremental
        else:
            return Incremental

    ##########################################################################################################
    # Calcula Parametros das Usinas
    ##########################################################################################################

    def _calc_vol_util(self):     # Calcula Volume Util da Usina
        if self._tipo_reg['valor'][-1] == 'M':
            self._vol_util['valor'].append(self._vol_max['valor'][-1] - self._vol_min['valor'][-1])
        else:
            self._vol_util['valor'].append(float(0))
            self._vol_min['valor'][-1] = self._vol_max['valor'][-1]

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
