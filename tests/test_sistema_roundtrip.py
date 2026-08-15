from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import io
import unittest

import numpy as np
import pandas as pd

from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.sistema import Sistema


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"


def carregar_sistema():
    dger = Dger()
    sistema = Sistema()
    with redirect_stdout(io.StringIO()):
        dger.ler(str(PMO / "DGER.DAT"))
        sistema.ler(str(PMO / "SISTEMA.DAT"), dger)
    return sistema, dger


def reler(sistema, dger, pasta):
    saida = pasta / "SISTEMA.DAT"
    with redirect_stdout(io.StringIO()):
        sistema.escrever(str(saida), dger)
    novo = Sistema()
    with redirect_stdout(io.StringIO()):
        novo.ler(str(saida), dger)
    return novo, saida


def registro_copiado(sistema, codigo):
    registro = sistema.get(codigo)
    registro["cdef"] = list(registro["cdef"])
    registro["prof"] = list(registro["prof"])
    for campo in ("mercado_pre", "mercado_estudo", "mercado_pos"):
        registro[campo] = np.array(registro[campo], copy=True)
    registro["nao_simuladas"] = [
        {
            **nao_sim,
            "geracao": np.array(nao_sim["geracao"], copy=True),
        }
        for nao_sim in registro["nao_simuladas"]
    ]
    return registro


class TestSistemaPutRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)
        self.sistema, self.dger = carregar_sistema()

    def test_put_nao_escreve_em_array_read_only_do_pandas(self):
        filtro = self.sistema.bloco_mercado["df"]["codigo"] == 1
        valores = self.sistema.bloco_mercado["df"].loc[filtro, "estudo"].values
        if pd.__version__.split(".", 1)[0] == "3":
            self.assertFalse(valores.flags.writeable)

        registro = registro_copiado(self.sistema, 1)
        self.sistema.put(registro)
        np.testing.assert_array_equal(
            self.sistema.get(1)["mercado_estudo"], registro["mercado_estudo"]
        )

    def test_round_trip_de_escalar_mercado_e_geracao_nao_simulada(self):
        registro = registro_copiado(self.sistema, 1)
        registro["nome"] = "SE-EDIT"
        registro["cdef"][0] = 4321.25
        registro["mercado_estudo"][0, 0] = 54321.0
        registro["nao_simuladas"][0]["geracao"][0, 0] = 3456.0

        self.sistema.put(registro)
        relido, _ = reler(self.sistema, self.dger, self.pasta)
        atual = relido.get(1)

        self.assertEqual(atual["nome"].strip(), "SE-EDIT")
        self.assertEqual(atual["cdef"][0], 4321.25)
        self.assertEqual(atual["mercado_estudo"][0, 0], 54321.0)
        self.assertEqual(atual["nao_simuladas"][0]["geracao"][0, 0], 3456.0)

    def test_alteracao_de_um_sistema_preserva_os_demais(self):
        codigos = (2, 3, 4)
        antes = {codigo: registro_copiado(self.sistema, codigo) for codigo in codigos}
        alterado = registro_copiado(self.sistema, 1)
        alterado["mercado_estudo"][2, 5] += 123.0
        self.sistema.put(alterado)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        for codigo in codigos:
            atual = relido.get(codigo)
            esperado = antes[codigo]
            self.assertEqual(atual["nome"], esperado["nome"])
            self.assertEqual(atual["cdef"], esperado["cdef"])
            self.assertEqual(atual["prof"], esperado["prof"])
            np.testing.assert_array_equal(
                atual["mercado_estudo"], esperado["mercado_estudo"]
            )
            np.testing.assert_array_equal(atual["mercado_pos"], esperado["mercado_pos"])

    def test_put_de_estudo_preserva_blocos_pre_e_pos(self):
        self.dger.anos_pre["valor"] = 1
        registro = registro_copiado(self.sistema, 1)
        registro["mercado_pre"][0] = np.arange(100, 112)
        registro["mercado_pos"][0] = np.arange(200, 212)
        self.sistema.put(registro)

        somente_estudo = registro_copiado(self.sistema, 1)
        somente_estudo["mercado_estudo"][1, 1] = 45678.0
        self.sistema.put(somente_estudo)
        relido, _ = reler(self.sistema, self.dger, self.pasta)

        np.testing.assert_array_equal(relido.get(1)["mercado_pre"], registro["mercado_pre"])
        np.testing.assert_array_equal(relido.get(1)["mercado_pos"], registro["mercado_pos"])
        self.assertEqual(relido.get(1)["mercado_estudo"][1, 1], 45678.0)

    def test_mercado_zero_e_escrito_e_formato_f7_0_arredonda(self):
        registro = registro_copiado(self.sistema, 1)
        registro["mercado_estudo"][0, 0] = 0.0
        registro["mercado_estudo"][0, 1] = 1234.6
        self.sistema.put(registro)

        relido, saida = reler(self.sistema, self.dger, self.pasta)
        mercado = relido.get(1)["mercado_estudo"]
        self.assertEqual(mercado[0, 0], 0.0)
        self.assertEqual(mercado[0, 1], 1235.0)

        linhas = saida.read_text(encoding="latin-1").splitlines()
        inicio = linhas.index(" MERCADO DE ENERGIA TOTAL")
        linha_2018 = next(linha for linha in linhas[inicio:] if linha.startswith("2018"))
        self.assertRegex(linha_2018, r"^2018\s+0\.\s+1235\.")

    def test_deficit_e_escrito_para_nao_ficticio_mesmo_com_cdef_1_zero(self):
        registro = registro_copiado(self.sistema, 1)
        registro["cdef"] = [0.0, 2222.25, 333.5, 44.75]
        registro["prof"] = [0.1, 0.2, 0.3, 0.4]
        self.sistema.put(registro)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        self.assertEqual(relido.get(1)["cdef"], registro["cdef"])
        self.assertEqual(relido.get(1)["prof"], registro["prof"])

    def test_put_interc_compativel_com_copy_on_write(self):
        intercambio = self.sistema.get_interc(1, 2)
        intercambio["valor"] = np.array(intercambio["valor"], copy=True)
        intercambio["valor"][0, 0] = 8123.0
        self.sistema.put_interc(intercambio)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        self.assertEqual(relido.get_interc(1, 2)["valor"][0, 0], 8123.0)


if __name__ == "__main__":
    unittest.main()
