import os
import logging
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO

from PySDDP.newave.script.templates.confhd import ConfhdTemplate
from matplotlib import pyplot as plt
import numpy as np
from random import randint
from mpl_toolkits.mplot3d import Axes3D


logger = logging.getLogger(__name__)


class Confhd(ConfhdTemplate):
    # Mapa único das chaves públicas de get()/put() para as estruturas
    # internas. Os dados de CONFHD, HIDR, MODIF e EXPH e os valores
    # calculados continuam expostos por compatibilidade com a API histórica.
    _FIELD_MAP = {
        'codigo': ('_codigo', 'valor'),
        'nome': ('_nome', 'valor'),
        'posto': ('_posto', 'valor'),
        'ree': ('_ree', 'valor'),
        'vol_ini': ('_vol_ini', 'valor'),
        'status': ('_status', 'valor'),
        'modif': ('_modif', 'valor'),
        'ano_i': ('_ano_i', 'valor'),
        'ano_f': ('_ano_f', 'valor'),
        'bdh': ('_bdh', 'valor'),
        'sist': ('_sist', 'valor'),
        'empr': ('_empr', 'valor'),
        'jusante': ('_jusante', 'valor'),
        'desvio': ('_desvio', 'valor'),
        'vol_min': ('_vol_min', 'valor'),
        'vol_max': ('_vol_max', 'valor'),
        'vol_vert': ('_vol_vert', 'valor'),
        'vol_min_desv': ('_vol_min_desv', 'valor'),
        'cota_min': ('_cota_min', 'valor'),
        'cota_max': ('_cota_max', 'valor'),
        'pol_cota_vol': ('_pol_cota_vol', 'valor'),
        'pol_cota_area': ('_pol_cota_area', 'valor'),
        'coef_evap': ('_coef_evap', 'valor'),
        'num_conj_maq': ('_num_conj_maq', 'valor'),
        'maq_por_conj': ('_maq_por_conj', 'valor'),
        'pef_por_conj': ('_pef_por_conj', 'valor'),
        'cf_hbqt': ('_cf_hbqt', 'valor'),
        'cf_hbqt_2': ('_cf_hbqt', 'valor_2'),
        'cf_hbqt_3': ('_cf_hbqt', 'valor_3'),
        'cf_hbqt_4': ('_cf_hbqt', 'valor_4'),
        'cf_hbqt_5': ('_cf_hbqt', 'valor_5'),
        'cf_hbqg': ('_cf_hbqg', 'valor'),
        'cf_hbqg_2': ('_cf_hbqg', 'valor_2'),
        'cf_hbqg_3': ('_cf_hbqg', 'valor_3'),
        'cf_hbqg_4': ('_cf_hbqg', 'valor_4'),
        'cf_hbqg_5': ('_cf_hbqg', 'valor_5'),
        'cf_hbpt': ('_cf_hbpt', 'valor'),
        'cf_hbpt_2': ('_cf_hbpt', 'valor_2'),
        'cf_hbpt_3': ('_cf_hbpt', 'valor_3'),
        'cf_hbpt_4': ('_cf_hbpt', 'valor_4'),
        'cf_hbpt_5': ('_cf_hbpt', 'valor_5'),
        'alt_efet_conj': ('_alt_efet_conj', 'valor'),
        'vaz_efet_conj': ('_vaz_efet_conj', 'valor'),
        'prod_esp': ('_prod_esp', 'valor'),
        'perda_hid': ('_perda_hid', 'valor'),
        'num_pol_vnj': ('_num_pol_vnj', 'valor'),
        'pol_vaz_niv_jus': ('_pol_vaz_niv_jus', 'valor'),
        'pol_vaz_niv_jus_2': ('_pol_vaz_niv_jus', 'valor_2'),
        'pol_vaz_niv_jus_3': ('_pol_vaz_niv_jus', 'valor_3'),
        'pol_vaz_niv_jus_4': ('_pol_vaz_niv_jus', 'valor_4'),
        'pol_vaz_niv_jus_5': ('_pol_vaz_niv_jus', 'valor_5'),
        'pol_vaz_niv_jus_6': ('_pol_vaz_niv_jus', 'valor_6'),
        'cota_ref_nivel_jus': ('_cota_ref_nivel_jus', 'valor'),
        'cfmed': ('_cfmed', 'valor'),
        'inf_canal_fuga': ('_inf_canal_fuga', 'valor'),
        'fator_carga_max': ('_fator_carga_max', 'valor'),
        'fator_carga_min': ('_fator_carga_min', 'valor'),
        'vaz_min': ('_vaz_min', 'valor'),
        'unid_base': ('_unid_base', 'valor'),
        'tipo_turb': ('_tipo_turb', 'valor'),
        'repres_conj': ('_repres_conj', 'valor'),
        'teifh': ('_teifh', 'valor'),
        'ip': ('_ip', 'valor'),
        'tipo_perda': ('_tipo_perda', 'valor'),
        'data': ('_data', 'valor'),
        'observ': ('_observ', 'valor'),
        'vol_ref': ('_vol_ref', 'valor'),
        'tipo_reg': ('_tipo_reg', 'valor'),
        'vazoes': ('_vazoes', 'valor'),
        'vol_mint': ('_vol_mint', 'valor'),
        'vol_maxt': ('_vol_maxt', 'valor'),
        'vol_minp': ('_vol_minp', 'valor'),
        'vaz_mint': ('_vaz_mint', 'valor'),
        'cmont': ('_cmont', 'valor'),
        'cfugat': ('_cfugat', 'valor'),
        'vol_util': ('_vol_util', 'valor'),
        'pot_efet': ('_pot_efet', 'valor'),
        'vaz_efet': ('_vaz_efet', 'valor'),
        'status_vol_morto': ('_status_vol_morto', 'valor'),
        'status_motoriz': ('_status_motoriz', 'valor'),
        'vol_morto_tempo': ('_vol_morto_tempo', 'valor'),
        'engol_tempo': ('_engol_tempo', 'valor'),
        'potencia_tempo': ('_potencia_tempo', 'valor'),
        'unidades_tempo': ('_unidades_tempo', 'valor'),
        'ro_65': ('_ro_65', 'valor'),
        'ro_50': ('_ro_50', 'valor'),
        'ro_equiv': ('_ro_equiv', 'valor'),
        'ro_equiv65': ('_ro_equiv65', 'valor'),
        'ro_min': ('_ro_min', 'valor'),
        'ro_max': ('_ro_max', 'valor'),
        'engolimento': ('_engolimento', 'valor'),
        'ro_acum_a_ree': ('_ro_acum_a_ree', 'valor'),
        'ro_acum_b_ree': ('_ro_acum_b_ree', 'valor'),
        'ro_acum_c_ree': ('_ro_acum_c_ree', 'valor'),
        'ro_acum_a_sist': ('_ro_acum_a_sist', 'valor'),
        'ro_acum_b_sist': ('_ro_acum_b_sist', 'valor'),
        'ro_acum_c_sist': ('_ro_acum_c_sist', 'valor'),
        'ro_acum': ('_ro_acum', 'valor'),
        'ro_acum_65': ('_ro_acum_65', 'valor'),
        'ro_acum_max': ('_ro_acum_max', 'valor'),
        'ro_acum_med': ('_ro_acum_med', 'valor'),
        'ro_acum_min': ('_ro_acum_min', 'valor'),
    }
    _CONFHD_FIELDS = (
        'codigo', 'nome', 'posto', 'jusante', 'ree', 'vol_ini',
        'status', 'modif', 'ano_i', 'ano_f',
    )
    _STATUS_VALUES = frozenset(('EX', 'EE', 'NE', 'NC'))

    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    @staticmethod
    def _as_int(field, value, minimum, maximum):
        """Converte escalares inteiros Python/NumPy sem truncamento."""
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, bool):
            raise TypeError(f"{field} deve ser inteiro")
        if isinstance(value, Integral):
            result = int(value)
        elif isinstance(value, Real):
            numeric = float(value)
            if not math.isfinite(numeric) or not numeric.is_integer():
                raise ValueError(f"{field} deve ser um inteiro exato")
            result = int(numeric)
        else:
            raise TypeError(f"{field} deve ser inteiro")
        if result < minimum or result > maximum:
            raise ValueError(
                f"{field} deve estar entre {minimum} e {maximum}"
            )
        return result

    @staticmethod
    def _as_float(field, value, minimum, maximum, decimals=None):
        """Converte escalares reais Python/NumPy e verifica finitude."""
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{field} deve ser numerico")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{field} deve ser finito")
        if result < minimum or result > maximum:
            raise ValueError(
                f"{field} deve estar entre {minimum} e {maximum}"
            )
        if decimals is not None:
            result = float(f"{result:.{decimals}f}")
        return result

    def _position_for_code(self, codigo):
        """Retorna a posição de um código existente sem indexar fora do mapa."""
        if codigo < 0 or codigo >= len(self._mapa):
            return None
        posicao = int(self._mapa[codigo])
        if posicao < 0:
            return None
        return posicao

    def _normalize_confhd_fields(self, values):
        """Valida e normaliza os dez campos físicos de um registro CONFHD."""
        nome = values['nome']
        if not isinstance(nome, str):
            raise TypeError("nome deve ser string")
        try:
            nome.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError("nome deve ser representavel em latin-1") from err
        if len(nome) > 12:
            raise ValueError("nome deve possuir no maximo 12 caracteres")

        status = values['status']
        if not isinstance(status, str):
            raise TypeError("status deve ser string")
        status = status.strip().upper()
        if status not in self._STATUS_VALUES:
            permitidos = ", ".join(sorted(self._STATUS_VALUES))
            raise ValueError(f"status deve ser um de: {permitidos}")

        posto_maximo = int(np.shape(self._copiavazoes)[2])
        normalized = {
            'codigo': self._as_int('codigo', values['codigo'], 1, 9999),
            'nome': nome.ljust(12),
            'posto': self._as_int(
                'posto', values['posto'], 1, min(9999, posto_maximo)
            ),
            'jusante': self._as_int(
                'jusante', values['jusante'], 0, 9999
            ),
            'ree': self._as_int('ree', values['ree'], 0, 9999),
            'vol_ini': self._as_float(
                'vol_ini', values['vol_ini'], 0.0, 100.0, decimals=2
            ),
            'status': status,
            'modif': self._as_int('modif', values['modif'], 0, 9999),
            'ano_i': self._as_int('ano_i', values['ano_i'], 0, 9999),
            'ano_f': self._as_int('ano_f', values['ano_f'], 0, 9999),
        }
        if normalized['ano_i'] > normalized['ano_f']:
            raise ValueError("ano_i nao pode ser posterior a ano_f")
        return normalized

    def _normalize_vazoes(self, values):
        """Valida a série (anos, 12) e converte-a sem perda para int32."""
        try:
            vazoes = np.asarray(values)
        except (TypeError, ValueError) as err:
            raise TypeError("vazoes deve ser uma matriz numerica") from err

        expected_shape = tuple(np.shape(self._copiavazoes)[:2])
        if vazoes.shape != expected_shape:
            raise ValueError(
                f"vazoes deve possuir dimensao {expected_shape}, "
                f"recebida {vazoes.shape}"
            )
        is_integer = np.issubdtype(vazoes.dtype, np.integer)
        is_floating = np.issubdtype(vazoes.dtype, np.floating)
        if not (is_integer or is_floating):
            raise TypeError("vazoes deve conter valores numericos")
        if not np.all(np.isfinite(vazoes)):
            raise ValueError("vazoes deve conter apenas valores finitos")
        if not np.all(vazoes == np.trunc(vazoes)):
            raise ValueError("vazoes deve conter apenas valores inteiros")

        limits = np.iinfo(np.int32)
        if np.any(vazoes < limits.min) or np.any(vazoes > limits.max):
            raise ValueError("vazoes excede os limites de int32")
        return vazoes.astype(np.int32, copy=True)

    def ler(self, file_name: str, hidr, vazoes, dger, modif, exph) -> None:
        """
        Lê o CONFHD.DAT e incorpora os dados cadastrais, temporais e de
        vazões necessários à configuração hidrelétrica do NEWAVE.

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
                        self._pol_vaz_niv_jus['valor_6'].append(uhe['pol_vaz_niv_jus_6'])
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
        Escreve todos os registros físicos do CONFHD.DAT.

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        self._numero_registros_ = 0

        formato = (
            "{codigo: >5d} {nome: <12} {posto: >4d} {jusante: >5d} "
            "{ree: >4d} {vol_ini: >6.2f} {status: >4} {modif: >6d} "
            "{ano_i: >8d} {ano_f: >8d}\n"
        )

        diretorio = os.path.split(file_out)[0]
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        registros = []
        for iusi in range(len(self._codigo['valor'])):
            linha = {
                field: getattr(self, self._FIELD_MAP[field][0])[
                    self._FIELD_MAP[field][1]
                ][iusi]
                for field in self._CONFHD_FIELDS
            }
            registros.append(self._normalize_confhd_fields(linha))

        with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
            f.write(
                " NUM  NOME         POSTO JUS   REE V.INIC U.EXIS MODIF "
                "INIC.HIST FIM HIST\n"
            )
            f.write(
                " XXXX XXXXXXXXXXXX XXXX  XXXX XXXX XXX.XX XXXX   XXXX"
                "     XXXX     XXXX\n"
            )

            for linha in registros:
                f.write(formato.format(**linha))
                self._numero_registros_ += 1

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def _get(self, entrada, copy_values):
        """
        Busca uma usina hidreletrica do arquivo CONFHD e retorna um dicionario de dados contendo todas as
        informacoes desta usina

        :param entrada: string com o nome da usina ou inteiro com o numero de referencia da usina

        """

        if isinstance(entrada, np.generic):
            entrada = entrada.item()

        if isinstance(entrada, bool):
            raise TypeError("entrada deve ser codigo numerico ou nome")
        if isinstance(entrada, Integral):
            codigo = int(entrada)
            posicao = self._position_for_code(codigo)
            if posicao is None:
                return None
        elif isinstance(entrada, Real):
            numeric = float(entrada)
            if not math.isfinite(numeric) or not numeric.is_integer():
                raise ValueError("codigo numerico deve ser um inteiro exato")
            posicao = self._position_for_code(int(numeric))
            if posicao is None:
                return None
        elif isinstance(entrada, str):
            posicao = None
            for i, valor in enumerate(self._nome["valor"]):
                if (valor.upper()).strip() == (entrada.upper()).strip():
                    posicao = i
                    break
            if posicao is None:
                return None
        else:
            raise TypeError("entrada deve ser codigo numerico ou nome")

        uhe = {
            field: getattr(self, attr_name)[value_name][posicao]
            for field, (attr_name, value_name) in self._FIELD_MAP.items()
        }

        if copy_values:
            # O metadado permite que put() detecte uma tentativa de trocar a
            # identidade mesmo depois de deepcopy(), sem alterar codigo.
            uhe['codigo_original'] = uhe['codigo']
            return deepcopy(uhe)
        return uhe

    def get(self, entrada):
        """
        Retorna o dicionário completo e independente de uma UHE.

        ``entrada`` aceita o código (inteiro ou real integral) ou o nome. Os
        arrays retornados são cópias: alterações só atingem o objeto após
        :meth:`put`. A chave ``codigo_original`` preserva a identidade através
        de ``deepcopy`` e não deve ser modificada.
        """
        return self._get(entrada, copy_values=True)

    def put(self, uhe):
        """
        Atualiza uma UHE a partir do dicionário completo retornado por get().

        ``codigo`` identifica o registro e não é editável. Todas as demais
        chaves públicas são reincorporadas às estruturas internas. Os dez
        campos físicos do CONFHD são validados contra suas larguras; ``vazoes``
        atualiza a coluna do posto na matriz compartilhada com Vazoes.

        :param uhe: dicionário completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        :raises TypeError: para dicionário ou tipos incompatíveis
        :raises KeyError: para chaves ausentes ou desconhecidas
        :raises ValueError: para identidade ou valores inválidos
        """
        if not isinstance(uhe, dict):
            raise TypeError("uhe deve ser um dicionario completo")

        required = set(self._FIELD_MAP)
        received = set(uhe)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        allowed = required | {'codigo_original'}
        unknown = sorted(received - allowed)
        if unknown:
            raise KeyError(
                "chaves desconhecidas: " + ", ".join(unknown)
            )

        normalized = self._normalize_confhd_fields(uhe)
        codigo = normalized['codigo']
        codigo_original = self._as_int(
            'codigo_original',
            uhe.get('codigo_original', codigo),
            1,
            9999,
        )
        if codigo != codigo_original:
            raise ValueError(
                "codigo identifica a UHE e nao pode ser alterado"
            )
        posicao = self._position_for_code(codigo_original)
        if posicao is None:
            raise ValueError(
                f"codigo {codigo_original} nao corresponde a uma UHE existente"
            )

        vazoes = self._normalize_vazoes(uhe['vazoes'])
        updates = {
            field: deepcopy(value)
            for field, value in uhe.items()
            if field in self._FIELD_MAP
            and field not in ('codigo', 'vazoes')
        }
        updates.update(normalized)
        updates.pop('codigo')

        # Prepara todas as cópias antes de modificar o objeto, evitando uma
        # atualização parcial em caso de entrada não copiável.
        for field, value in updates.items():
            attr_name, value_name = self._FIELD_MAP[field]
            getattr(self, attr_name)[value_name][posicao] = value

        posto = normalized['posto']
        self._copiavazoes[:, :, posto - 1] = vazoes

        # Cada série permanece uma visão da coluna de seu posto. Assim, UHEs
        # que compartilham posto observam a mesma série, como exige o formato.
        for iusi, posto_uhe in enumerate(self._posto['valor']):
            self._vazoes['valor'][iusi] = (
                self._copiavazoes[:, :, int(posto_uhe) - 1]
            )

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario de dados obtido pelo comando get.

        :param parametro: string contendo a chave do dicionario de dados cuja o detalhamento eh desejado

        """

        if parametro == 'codigo_original':
            return (
                'Identidade original da UHE; metadado somente leitura usado '
                'por put para impedir alteracao de codigo'
            )

        duvida = getattr(self, '_'+parametro)

        return duvida['descricao']


    # Calcula Vazao Incremental
    def vaz_inc(self, uhe, iano, imes):

        def Montante(uhe, iano, imes):
            for iusi in self.lista_uhes():
                usina = self._get(iusi, copy_values=False)
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
                usina = self._get(iusina, copy_values=False)
                incremental = incremental - usina['vazoes'][:,imes]

        # Caso Alguma Incremental seja Menor que zero, força para zero
        codigos = np.where(incremental<0)
        incremental[codigos] = 0

        return incremental

    def vaz_inc_entre_res(self, codigo, ianoconf, imesconf):

        uhe = self._get(codigo, copy_values=False)

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
            current = confhd._get(codigo, copy_values=False)
            if current['status_vol_morto'][iano][imes] == 2:
                yield current['codigo']
            while current['jusante'] != 0:
                current = confhd._get(
                    current['jusante'], copy_values=False
                )
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
                        uhe = self._get(iusina, copy_values=False)
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

        uhe_nova = self._get(uhe['jusante'], copy_values=False)

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


    @staticmethod
    def _turbine_exponent(tipo_turbina):
        """Retorna o expoente da curva de engolimento para o tipo de turbina."""
        if tipo_turbina in (1, 3):  # Francis e Pelton
            return 0.5
        if tipo_turbina == 2:       # Kaplan
            return 0.2
        return None

    @staticmethod
    def _calcula_queda_liquida(queda_bruta, tipo_perda, perda_hid):
        """Converte queda bruta em liquida conforme o cadastro do HIDR.DAT."""
        try:
            queda_bruta = float(queda_bruta)
            perda_hid = float(perda_hid)
        except (TypeError, ValueError):
            return None

        if not math.isfinite(queda_bruta) or not math.isfinite(perda_hid):
            return None

        if tipo_perda == 1:      # Perda percentual
            queda_liquida = queda_bruta * (1.0 - perda_hid / 100.0)
        elif tipo_perda == 2:    # Perda absoluta, em metros
            queda_liquida = queda_bruta - perda_hid
        else:
            logger.debug("Tipo de perda hidraulica invalido: %r", tipo_perda)
            return None

        if not math.isfinite(queda_liquida) or queda_liquida <= 0.0:
            return None
        return queda_liquida

    @staticmethod
    def _calcula_engolimento_turbina(
            vazao_nominal, queda_liquida, altura_referencia, expoente):
        """Calcula o limite de vazao por maquina imposto pela turbina."""
        try:
            vazao_nominal = float(vazao_nominal)
            queda_liquida = float(queda_liquida)
            altura_referencia = float(altura_referencia)
            expoente = float(expoente)
        except (TypeError, ValueError):
            return None

        valores = (
            vazao_nominal, queda_liquida, altura_referencia, expoente
        )
        if (
                not all(math.isfinite(valor) for valor in valores)
                or vazao_nominal <= 0.0
                or queda_liquida <= 0.0
                or altura_referencia <= 0.0):
            return None

        resultado = vazao_nominal * (
            queda_liquida / altura_referencia
        ) ** expoente
        return resultado if math.isfinite(resultado) else None

    @staticmethod
    def _calcula_engolimento_gerador(
            potencia_nominal, prod_esp, queda_liquida):
        """Calcula o limite de vazao por maquina imposto pelo gerador."""
        try:
            potencia_nominal = float(potencia_nominal)
            prod_esp = float(prod_esp)
            queda_liquida = float(queda_liquida)
        except (TypeError, ValueError):
            return None

        valores = (potencia_nominal, prod_esp, queda_liquida)
        if (
                not all(math.isfinite(valor) for valor in valores)
                or potencia_nominal <= 0.0
                or prod_esp <= 0.0
                or queda_liquida <= 0.0):
            return None

        resultado = potencia_nominal / (prod_esp * queda_liquida)
        return resultado if math.isfinite(resultado) else None

    @classmethod
    def _calcula_engolimento_conjunto(
            cls, numero_maquinas, vazao_nominal, altura_referencia,
            potencia_nominal, prod_esp, queda_liquida, expoente):
        """Soma as maquinas usando o menor limite entre turbina e gerador."""
        try:
            numero_maquinas = float(numero_maquinas)
        except (TypeError, ValueError):
            return None
        if (
                not math.isfinite(numero_maquinas)
                or numero_maquinas <= 0.0):
            return None

        engol_turbina = cls._calcula_engolimento_turbina(
            vazao_nominal, queda_liquida, altura_referencia, expoente
        )
        engol_gerador = cls._calcula_engolimento_gerador(
            potencia_nominal, prod_esp, queda_liquida
        )
        if engol_turbina is None or engol_gerador is None:
            return None

        resultado = numero_maquinas * min(engol_turbina, engol_gerador)
        return resultado if math.isfinite(resultado) else None

    def _calc_engol(self, queda_bruta):
        # O campo interno e publico chama-se perda_hid; ql usa a perda cadastrada.
        queda_liquida = self._calcula_queda_liquida(
            queda_bruta,
            self._tipo_perda['valor'][-1],
            self._perda_hid['valor'][-1]
        )
        if queda_liquida is None:
            return None

        # Usa o valor da usina atual, e nao o dicionario que armazena a serie.
        expoente = self._turbine_exponent(
            self._tipo_turb['valor'][-1]
        )
        if expoente is None:
            logger.debug(
                "Tipo de turbina invalido: %r",
                self._tipo_turb['valor'][-1]
            )
            return None

        try:
            numero_conjuntos = max(
                0, min(int(self._num_conj_maq['valor'][-1]), 5)
            )
            vetores = (
                self._maq_por_conj['valor'][-1],
                self._vaz_efet_conj['valor'][-1],
                self._alt_efet_conj['valor'][-1],
                self._pef_por_conj['valor'][-1]
            )
            numero_conjuntos = min(
                numero_conjuntos, *(len(vetor) for vetor in vetores)
            )
        except (TypeError, ValueError):
            return 0.0

        engolimento = 0.0
        for i in range(numero_conjuntos):
            engolimento_conjunto = self._calcula_engolimento_conjunto(
                self._maq_por_conj['valor'][-1][i],
                self._vaz_efet_conj['valor'][-1][i],
                self._alt_efet_conj['valor'][-1][i],
                self._pef_por_conj['valor'][-1][i],
                self._prod_esp['valor'][-1],
                queda_liquida,
                expoente
            )
            if engolimento_conjunto is not None:
                engolimento += engolimento_conjunto
        return engolimento

    def _calc_engol_maximo(self):    # Estima Engolimento Maximo da Usina

        a = self._pol_cota_vol['valor'][-1][0]
        b = self._pol_cota_vol['valor'][-1][1]
        c = self._pol_cota_vol['valor'][-1][2]
        d = self._pol_cota_vol['valor'][-1][3]
        e = self._pol_cota_vol['valor'][-1][4]

        # Mantem as cinco condicoes historicas: 50%, 65%, equivalente,
        # volume maximo e volume minimo.
        # A jusante continua aproximada por cfmed: nao ha rotina iterativa
        # consolidada nesta classe para acoplar vazao e nivel de jusante.
        volume = self._vol_min['valor'][-1] + 0.65*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda65 = cota - self._cfmed['valor'][-1]
        engol65 = self._calc_engol(queda65)

        volume = self._vol_min['valor'][-1] + 0.50*self._vol_util['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        queda50 = cota - self._cfmed['valor'][-1]
        engol50 = self._calc_engol(queda50)

        volume = self._vol_max['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMax = cota - self._cfmed['valor'][-1]
        engolMax = self._calc_engol(quedaMax)

        volume = self._vol_min['valor'][-1]
        cota = a + b*volume + c*volume**2 + d*volume**3 + e*volume**4
        quedaMin = cota - self._cfmed['valor'][-1]
        engolMin = self._calc_engol(quedaMin)

        if ( self._vol_util['valor'][-1] > 0):
            cota = 0
            for i in range(5):
                cota = cota + self._pol_cota_vol['valor'][-1][i] * (self._vol_max['valor'][-1]**(i+1)) / (i+1)
                cota = cota - self._pol_cota_vol['valor'][-1][i] * (self._vol_min['valor'][-1]**(i+1)) / (i+1)
            cota = cota / self._vol_util['valor'][-1]
        quedaEquiv = cota - self._cfmed['valor'][-1]
        engolEquiv = self._calc_engol(quedaEquiv)

        # engolimento permanece a media das condicoes validas, em m3/s.
        valores_validos = [
            valor for valor in (
                engol50, engol65, engolEquiv, engolMax, engolMin
            )
            if valor is not None and math.isfinite(valor)
        ]
        self._engolimento['valor'].append(
            sum(valores_validos) / len(valores_validos)
            if valores_validos else 0.0
        )

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
