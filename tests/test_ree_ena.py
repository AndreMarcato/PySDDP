from contextlib import redirect_stdout
from pathlib import Path
import io
import unittest

import numpy as np

from PySDDP.Pen import Newave
from PySDDP.newave.script.ree import Ree


RAIZ = Path(__file__).resolve().parents[1]
PMO = RAIZ / "PySDDP" / "pmo"


def matriz_temporal(valor):
    return np.full((1, 12), valor)


class ConfhdFalso:
    def __init__(self):
        self._codigo = {"valor": [1, 2, 3, 4]}
        self._ree = {"valor": [10, 10, 10, 20]}
        self._vol_util = {"valor": [100.0, 0.0, 0.0, 0.0]}
        self._status_vol_morto = {
            "valor": [
                matriz_temporal(2),
                matriz_temporal(2),
                matriz_temporal(2),
                matriz_temporal(2),
            ]
        }
        self._status_motoriz = {
            "valor": [
                matriz_temporal(0),
                matriz_temporal(2),
                matriz_temporal(1),
                matriz_temporal(2),
            ]
        }
        self._ro_acum_med = {
            "valor": [
                matriz_temporal(3.0),
                matriz_temporal(0.0),
                matriz_temporal(0.0),
                matriz_temporal(0.0),
            ]
        }
        self._ro_equiv = {
            "valor": [
                matriz_temporal(0.0),
                matriz_temporal(0.5),
                matriz_temporal(100.0),
                matriz_temporal(50.0),
            ]
        }
        self._vazoes = {
            "valor": [np.zeros((2, 12), dtype=np.int32) for _ in range(4)]
        }
        self.incrementais = {
            1: np.array([10.0, 20.0]),
            2: np.array([4.0, 8.0]),
            3: np.array([7.0, 9.0]),
            4: np.array([100.0, 200.0]),
        }

    def vaz_inc_entre_res(self, codigo, iano, imes):
        return self.incrementais[codigo]


class TestCalculoEnaRee(unittest.TestCase):
    def test_calcula_parcelas_diretamente_em_float64(self):
        ena, ec, efio = Ree()._calc_ena(ConfhdFalso(), 10)

        self.assertEqual(ena.dtype, np.float64)
        self.assertEqual(ec.dtype, np.float64)
        self.assertEqual(efio.dtype, np.float64)
        np.testing.assert_array_equal(ec[0, 0], [30.0, 60.0])
        np.testing.assert_array_equal(efio[0, 0], [2.0, 4.0])
        np.testing.assert_array_equal(ena[0, 0], [32.0, 64.0])
        np.testing.assert_array_equal(ena, ec + efio)

    def test_fio_dagua_nao_motorizada_nao_contribui(self):
        confhd = ConfhdFalso()
        confhd._status_motoriz["valor"][1][:] = 1

        ena, ec, efio = Ree()._calc_ena(confhd, 10)

        np.testing.assert_array_equal(efio, np.zeros_like(efio))
        np.testing.assert_array_equal(ena, ec)

    def test_usina_com_volume_morto_incompleto_nao_contribui(self):
        confhd = ConfhdFalso()
        confhd._status_vol_morto["valor"][0][:] = 1
        confhd._status_vol_morto["valor"][1][:] = 1

        ena, ec, efio = Ree()._calc_ena(confhd, 10)

        np.testing.assert_array_equal(ec, np.zeros_like(ec))
        np.testing.assert_array_equal(efio, np.zeros_like(efio))
        np.testing.assert_array_equal(ena, np.zeros_like(ena))

    def test_nao_mistura_usinas_de_outro_ree_na_efio(self):
        ena, ec, efio = Ree()._calc_ena(ConfhdFalso(), 10)

        self.assertLess(float(efio.max()), 50.0)
        np.testing.assert_array_equal(ena, ec + efio)


class TestRegressaoDeckPmo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.newave = Newave(str(PMO))

    def test_parana_e_paranapanema_sem_efio_negativa(self):
        for codigo in (10, 12):
            with self.subTest(codigo=codigo):
                ree = self.newave.ree.get(codigo)
                self.assertGreaterEqual(float(ree["efio_bruta"].min()), 0.0)
                self.assertGreater(float(ree["efio_bruta"].max()), 0.0)

    def test_identidade_ena_em_todos_os_rees(self):
        for _, registro in self.newave.ree.bloco_ree["df"].iterrows():
            with self.subTest(codigo=registro["codigo"]):
                np.testing.assert_array_equal(
                    registro["ena_bruta"],
                    registro["ec"] + registro["efio_bruta"],
                )
                self.assertGreaterEqual(
                    float(registro["efio_bruta"].min()), 0.0
                )


if __name__ == "__main__":
    unittest.main()
