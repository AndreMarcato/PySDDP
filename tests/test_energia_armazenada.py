from types import SimpleNamespace
from contextlib import redirect_stdout
from pathlib import Path
import io
import unittest

import numpy as np
import pandas as pd

from PySDDP.Pen import Newave
from PySDDP.newave.energia_armazenada import (
    FATOR_NEWAVE_MWMES,
    calcular_energia_armazenada_inicial,
)
from PySDDP.newave.script.confhd import Confhd


def matriz(valor=0.0):
    return np.full((1, 12), valor, dtype=np.float64)


def uhe(codigo, ree, volume_util, vol_ini, ro_acum, status=2):
    produtividade = matriz(0.0)
    if np.isscalar(ro_acum):
        produtividade[:] = ro_acum
    else:
        produtividade[0, :] = ro_acum
    return {
        "codigo": codigo,
        "ree": ree,
        "vol_util": volume_util,
        "vol_ini": vol_ini,
        "status_vol_morto": matriz(status),
        "ro_acum": produtividade,
    }


class ConfhdFalso:
    def __init__(self, uhes):
        self.uhes = {registro["codigo"]: registro for registro in uhes}

    def lista_uhes(self):
        return list(self.uhes)

    def _get(self, codigo, copy_values=False):
        return self.uhes[codigo]


def montar_objetos(uhes, rees, sistemas, percentuais_dger, mes=1, flag=0):
    dger = SimpleNamespace(
        mesi_est={"valor": mes},
        ano_ini={"valor": 2026},
        flag_earm_inic={"valor": flag},
        vol_earm_inic={"valor": percentuais_dger},
    )
    ree = SimpleNamespace(
        bloco_ree={
            "df": pd.DataFrame(
                rees, columns=("codigo", "nome", "submercado")
            )
        }
    )
    sistema = SimpleNamespace(
        bloco_sistema={
            "df": pd.DataFrame(
                sistemas, columns=("codigo", "nome", "tipo")
            )
        }
    )
    return dger, ConfhdFalso(uhes), ree, sistema


def calcular(uhes, rees, sistemas, percentuais_dger, mes=1, flag=0):
    return calcular_energia_armazenada_inicial(
        *montar_objetos(
            uhes, rees, sistemas, percentuais_dger, mes=mes, flag=flag
        )
    )


class TestEnergiaArmazenada(unittest.TestCase):
    def test_caso_a_um_ree_um_reservatorio(self):
        resultado = calcular(
            [uhe(1, 7, 263.0, 25.0, 10.0)],
            [(7, "REE 7", 3)],
            [(3, "SIST 3", 0)],
            [40.0],
        )
        linha = resultado["por_ree"].iloc[0]
        self.assertEqual(FATOR_NEWAVE_MWMES, 2.63)
        self.assertAlmostEqual(linha.earm_max_mwmes, 1000.0)
        self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 250.0)
        self.assertAlmostEqual(linha.percentual_confhd, 25.0)
        self.assertAlmostEqual(linha.ear_inicial_dger_mwmes, 400.0)
        self.assertAlmostEqual(linha.percentual_dger, 40.0)

    def test_caso_b_cada_reservatorio_usa_seu_ro_acum(self):
        resultado = calcular(
            [
                uhe(1, 1, 263.0, 50.0, 10.0),
                uhe(2, 1, 526.0, 50.0, 5.0),
            ],
            [(1, "R1", 1)],
            [(1, "S1", 0)],
            [50.0],
        )
        linha = resultado["por_ree"].iloc[0]
        self.assertAlmostEqual(linha.earm_max_mwmes, 2000.0)
        self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 1000.0)

    def test_caso_c_percentuais_individuais_nao_usam_media_simples(self):
        resultado = calcular(
            [
                uhe(1, 1, 263.0, 0.0, 10.0),
                uhe(2, 1, 526.0, 100.0, 10.0),
            ],
            [(1, "R1", 1)],
            [(1, "S1", 0)],
            [50.0],
        )
        linha = resultado["por_ree"].iloc[0]
        media_simples_vezes_earm = 0.5 * linha.earm_max_mwmes
        self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 2000.0)
        self.assertNotAlmostEqual(
            linha.ear_inicial_confhd_mwmes, media_simples_vezes_earm
        )

    def test_caso_d_fio_dagua_nao_armazena_mas_pdtarm_inclui_jusante(self):
        resultado = calcular(
            [
                uhe(1, 1, 263.0, 100.0, 15.0),
                uhe(2, 1, 0.0, 100.0, 5.0),
            ],
            [(1, "R1", 1)],
            [(1, "S1", 0)],
            [100.0],
        )
        linha = resultado["por_ree"].iloc[0]
        self.assertAlmostEqual(linha.earm_max_mwmes, 1500.0)
        self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 1500.0)

    def test_caso_e_rees_independentes(self):
        resultado = calcular(
            [uhe(1, 10, 263.0, 20.0, 10.0), uhe(2, 20, 263.0, 80.0, 5.0)],
            [(10, "R10", 1), (20, "R20", 2)],
            [(1, "S1", 0), (2, "S2", 0)],
            [30.0, 60.0],
        )
        por_codigo = resultado["por_ree"].set_index("codigo_ree")
        self.assertAlmostEqual(por_codigo.loc[10, "earm_max_mwmes"], 1000.0)
        self.assertAlmostEqual(por_codigo.loc[20, "earm_max_mwmes"], 500.0)

    def test_caso_f_acoplamento_fica_no_ree_de_origem(self):
        resultado = calcular(
            [uhe(1, 1, 263.0, 100.0, 15.0), uhe(2, 2, 263.0, 100.0, 5.0)],
            [(1, "MONT", 1), (2, "JUS", 2)],
            [(1, "SM1", 0), (2, "SM2", 0)],
            [100.0, 100.0],
        )
        por_codigo = resultado["por_ree"].set_index("codigo_ree")
        self.assertAlmostEqual(por_codigo.loc[1, "earm_max_mwmes"], 1500.0)
        self.assertAlmostEqual(por_codigo.loc[2, "earm_max_mwmes"], 500.0)

    def test_caso_g_agregacao_mesmo_sistema_usa_razao_das_somas(self):
        resultado = calcular(
            [uhe(1, 1, 263.0, 0.0, 10.0), uhe(2, 2, 526.0, 100.0, 10.0)],
            [(1, "R1", 9), (2, "R2", 9)],
            [(9, "S9", 0)],
            [0.0, 100.0],
        )
        linha = resultado["por_submercado"].iloc[0]
        self.assertEqual(linha.codigos_rees, [1, 2])
        self.assertAlmostEqual(linha.earm_max_mwmes, 3000.0)
        self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 2000.0)
        self.assertAlmostEqual(linha.percentual_confhd, 200.0 / 3.0)

    def test_caso_h_acoplamento_entre_sistemas_nao_transfere_estoque(self):
        resultado = calcular(
            [uhe(1, 1, 263.0, 100.0, 15.0), uhe(2, 2, 263.0, 100.0, 5.0)],
            [(1, "MONT", 100), (2, "JUS", 300)],
            [(100, "ORIGEM", 0), (300, "DESTINO", 0)],
            [100.0, 100.0],
        )
        por_codigo = resultado["por_submercado"].set_index("codigo_submercado")
        self.assertAlmostEqual(por_codigo.loc[100, "earm_max_mwmes"], 1500.0)
        self.assertAlmostEqual(por_codigo.loc[300, "earm_max_mwmes"], 500.0)

    def test_caso_i_codigos_nao_sequenciais_e_sistema_ficticio(self):
        resultado = calcular(
            [uhe(1, 42, 263.0, 50.0, 10.0)],
            [(42, "R42", 99)],
            [(99, "REAL", 0), (501, "FICT", 1)],
            [50.0],
        )
        sistemas = resultado["por_submercado"].set_index("codigo_submercado")
        self.assertEqual(sistemas.loc[99, "codigos_rees"], [42])
        self.assertFalse(bool(sistemas.loc[99, "ficticio"]))
        self.assertTrue(bool(sistemas.loc[501, "ficticio"]))
        self.assertTrue(np.isnan(sistemas.loc[501, "percentual_confhd"]))

    def test_caso_j_respeita_mesi_est(self):
        produtividades = np.ones(12)
        produtividades[3] = 10.0
        resultado = calcular(
            [uhe(1, 1, 263.0, 100.0, produtividades)],
            [(1, "R1", 1)],
            [(1, "S1", 0)],
            [100.0],
            mes=4,
        )
        self.assertAlmostEqual(
            resultado["por_ree"].iloc[0].earm_max_mwmes, 1000.0
        )
        self.assertEqual(resultado["metadados"]["mes_inicial"], 4)

    def test_caso_k_limites_zero_e_validacoes(self):
        resultado = calcular(
            [uhe(1, 1, 263.0, 0.0, 10.0)],
            [(1, "R1", 1), (2, "VAZIO", 1)],
            [(1, "S1", 0)],
            [0.0, 100.0],
        )
        por_codigo = resultado["por_ree"].set_index("codigo_ree")
        self.assertEqual(por_codigo.loc[1, "ear_inicial_confhd_mwmes"], 0.0)
        self.assertEqual(por_codigo.loc[2, "earm_max_mwmes"], 0.0)
        self.assertTrue(np.isnan(por_codigo.loc[2, "percentual_confhd"]))

        for invalido in (None, np.nan, -1.0, 101.0, "texto"):
            with self.subTest(vol_ini=invalido), self.assertRaises(ValueError):
                calcular(
                    [uhe(1, 1, 263.0, invalido, 10.0)],
                    [(1, "R1", 1)],
                    [(1, "S1", 0)],
                    [50.0],
                )

        with self.assertRaisesRegex(ValueError, "submercado inexistente"):
            calcular(
                [uhe(1, 1, 263.0, 50.0, 10.0)],
                [(1, "R1", 999)],
                [(1, "S1", 0)],
                [50.0],
            )

    def test_dger_incompleto_retorna_diagnostico_sem_eliminar_confhd(self):
        resultado = calcular(
            [uhe(1, 1, 263.0, 50.0, 10.0), uhe(2, 2, 263.0, 50.0, 5.0)],
            [(1, "R1", 1), (2, "R2", 1)],
            [(1, "S1", 0)],
            [25.0],
            flag=1,
        )
        self.assertFalse(resultado["metadados"]["dger_disponivel"])
        self.assertTrue(resultado["metadados"]["diagnosticos"])
        self.assertTrue(resultado["por_ree"]["percentual_dger"].isna().all())
        self.assertTrue(
            np.isfinite(resultado["por_ree"]["ear_inicial_confhd_mwmes"]).all()
        )

    def test_dger_rejeita_percentuais_invalidos_quando_vetor_e_completo(self):
        for invalido in (None, np.nan, -1.0, 101.0, "texto"):
            with self.subTest(percentual_dger=invalido), self.assertRaises(ValueError):
                calcular(
                    [uhe(1, 1, 263.0, 50.0, 10.0)],
                    [(1, "R1", 1)],
                    [(1, "S1", 0)],
                    [invalido],
                )

    def test_periodo_inicial_invalido_e_rejeitado(self):
        for mes in (0, 13, 1.5, None):
            with self.subTest(mes=mes), self.assertRaises(ValueError):
                calcular(
                    [uhe(1, 1, 263.0, 50.0, 10.0)],
                    [(1, "R1", 1)],
                    [(1, "S1", 0)],
                    [50.0],
                    mes=mes,
                )

    def test_flag_e_apenas_metadado_e_as_duas_fontes_sao_calculadas(self):
        resultados = []
        for flag in (0, 1):
            resultados.append(
                calcular(
                    [uhe(1, 1, 263.0, 25.0, 10.0)],
                    [(1, "R1", 1)],
                    [(1, "S1", 0)],
                    [75.0],
                    flag=flag,
                )
            )
        for flag, resultado in enumerate(resultados):
            linha = resultado["por_ree"].iloc[0]
            self.assertAlmostEqual(linha.ear_inicial_confhd_mwmes, 250.0)
            self.assertAlmostEqual(linha.ear_inicial_dger_mwmes, 750.0)
            self.assertEqual(resultado["metadados"]["flag_earm_inic"], flag)

    def test_nova_api_retorna_float64_e_fachada_newave_delega(self):
        objetos = montar_objetos(
            [uhe(1, 1, 263.0, 25.0, 10.0)],
            [(1, "R1", 1)],
            [(1, "S1", 0)],
            [75.0],
        )
        newave = Newave.__new__(Newave)
        newave.dger, newave.confhd, newave.ree, newave.sistema = objetos
        resultado = newave.calcular_energia_armazenada_inicial()
        for tabela in (resultado["por_ree"], resultado["por_submercado"]):
            self.assertEqual(tabela["earm_max_mwmes"].dtype, np.dtype("float64"))

    def test_regressao_earm_nova_igual_calculo_existente_no_deck_pmo(self):
        raiz = Path(__file__).resolve().parents[1]
        with redirect_stdout(io.StringIO()):
            newave = Newave(str(raiz / "PySDDP" / "pmo"))
        resultado = newave.calcular_energia_armazenada_inicial()
        imes = resultado["metadados"]["mes_inicial"] - 1
        existente = np.asarray(
            [
                np.asarray(earm, dtype=np.float64)[0, imes]
                for earm in newave.ree.bloco_ree["df"]["earmax"]
            ],
            dtype=np.float64,
        )
        np.testing.assert_allclose(
            resultado["por_ree"]["earm_max_mwmes"].to_numpy(),
            existente,
            rtol=0.0,
            atol=1.0e-10,
        )


class ConfhdAcoplamentoSintetico(Confhd):
    CAMPOS_ACUMULADOS = (
        "_ro_acum",
        "_ro_acum_65",
        "_ro_acum_max",
        "_ro_acum_med",
        "_ro_acum_min",
        "_ro_acum_a_ree",
        "_ro_acum_b_ree",
        "_ro_acum_c_ree",
        "_ro_acum_a_sist",
        "_ro_acum_b_sist",
        "_ro_acum_c_sist",
    )

    def __init__(self, produtividades, volumes, rees, sistemas):
        super().__init__()
        codigos = list(range(1, len(produtividades) + 1))
        self._codigo["valor"] = codigos
        self._ree["valor"] = list(rees)
        self._sist["valor"] = list(sistemas)
        self._status_vol_morto["valor"] = [matriz(2) for _ in codigos]
        for campo in self.CAMPOS_ACUMULADOS:
            getattr(self, campo)["valor"] = [matriz(0.0) for _ in codigos]
        self._usinas = {}
        for indice, codigo in enumerate(codigos):
            jusante = codigos[indice + 1] if indice + 1 < len(codigos) else 0
            produtividade = matriz(produtividades[indice])
            self._usinas[codigo] = {
                "codigo": codigo,
                "jusante": jusante,
                "ree": rees[indice],
                "sist": sistemas[indice],
                "vol_util": volumes[indice],
                "status_vol_morto": matriz(2),
                "status_motoriz": matriz(2),
                "ro_equiv": produtividade,
                "ro_equiv65": produtividade,
                "ro_max": produtividade,
                "ro_65": produtividade,
                "ro_min": produtividade,
            }

    def _get(self, codigo, copy_values=False):
        return self._usinas[codigo]


class TestParcelasAcoplamento(unittest.TestCase):
    def assert_invariantes(self, confhd, produtividades):
        for indice in range(len(produtividades)):
            total_esperado = sum(produtividades[indice:])
            total = confhd._ro_acum["valor"][indice][0, 0]
            ree = sum(
                getattr(confhd, campo)["valor"][indice][0, 0]
                for campo in ("_ro_acum_a_ree", "_ro_acum_b_ree", "_ro_acum_c_ree")
            )
            sistema = sum(
                getattr(confhd, campo)["valor"][indice][0, 0]
                for campo in ("_ro_acum_a_sist", "_ro_acum_b_sist", "_ro_acum_c_sist")
            )
            self.assertAlmostEqual(total, total_esperado)
            self.assertAlmostEqual(total, ree)
            self.assertAlmostEqual(total, sistema)

    def test_fronteira_fio_dagua_reservatorio_corrige_b_c_ree_e_sistema(self):
        # reservatorio origem -> dois fios d'agua -> reservatorio -> usina
        produtividades = [1.0, 2.0, 3.0, 4.0, 5.0]
        confhd = ConfhdAcoplamentoSintetico(
            produtividades,
            volumes=[100.0, 0.0, 0.0, 100.0, 0.0],
            rees=[1, 2, 2, 2, 2],
            sistemas=[10, 20, 20, 20, 20],
        )
        confhd._prod_acum()
        self.assertAlmostEqual(confhd._ro_acum_a_ree["valor"][0][0, 0], 1.0)
        self.assertAlmostEqual(confhd._ro_acum_c_ree["valor"][0][0, 0], 5.0)
        self.assertAlmostEqual(confhd._ro_acum_b_ree["valor"][0][0, 0], 9.0)
        self.assertAlmostEqual(confhd._ro_acum_a_sist["valor"][0][0, 0], 1.0)
        self.assertAlmostEqual(confhd._ro_acum_c_sist["valor"][0][0, 0], 5.0)
        self.assertAlmostEqual(confhd._ro_acum_b_sist["valor"][0][0, 0], 9.0)
        self.assert_invariantes(confhd, produtividades)

    def test_fronteira_sem_fio_intermediario_tem_c_zero(self):
        produtividades = [1.0, 4.0, 5.0]
        confhd = ConfhdAcoplamentoSintetico(
            produtividades,
            volumes=[100.0, 100.0, 0.0],
            rees=[1, 2, 2],
            sistemas=[10, 20, 20],
        )
        confhd._prod_acum()
        self.assertAlmostEqual(confhd._ro_acum_c_ree["valor"][0][0, 0], 0.0)
        self.assertAlmostEqual(confhd._ro_acum_b_ree["valor"][0][0, 0], 9.0)
        self.assertAlmostEqual(confhd._ro_acum_c_sist["valor"][0][0, 0], 0.0)
        self.assertAlmostEqual(confhd._ro_acum_b_sist["valor"][0][0, 0], 9.0)
        self.assert_invariantes(confhd, produtividades)


if __name__ == "__main__":
    unittest.main()
