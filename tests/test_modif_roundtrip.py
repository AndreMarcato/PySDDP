from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stdout
import io
import shutil
import unittest

from PySDDP.newave.script.modif import Modif


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"
FIELDS = ("codigo", "comentario", "palavra_chave", "valorA", "valorB", "mes", "ano")


def escrever_fixture(path, registros):
    linhas = [
        " P.CHAVE  MODIFICACOES E INDICES\n",
        " XXXXXXXX XXXXXXXXXXXXXXXXXXXXX\n",
        " USINA    101                               TESTE A\n",
    ]
    linhas.extend(f" {registro}\n" for registro in registros)
    linhas.extend([
        " USINA    202                               TESTE B\n",
        " VAZMIN       7\n",
    ])
    path.write_text("".join(linhas), encoding="latin-1")


def round_trip(registros, pasta):
    entrada = pasta / "MODIF.DAT"
    saida = pasta / "MODIF_OUT.DAT"
    escrever_fixture(entrada, registros)

    original = Modif()
    original.ler(str(entrada))
    original.escrever(str(saida))
    relido = Modif()
    relido.ler(str(saida))
    return original, relido, saida


class TestModifNovasPalavrasRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)

    def assert_registro_igual(self, original, relido, indice=0):
        esperado = original.get(indice)
        atual = relido.get(indice)
        for campo in FIELDS:
            self.assertEqual(atual[campo], esperado[campo], campo)

    def test_turbmaxt_com_um_valor(self):
        original, relido, _ = round_trip(["TURBMAXT  1 2026 123.456"], self.pasta)
        self.assertEqual(original.get(0)["valorA"], [123.456])
        self.assert_registro_igual(original, relido)

    def test_turbmaxt_com_multiplos_valores(self):
        original, relido, _ = round_trip(
            ["TURBMAXT  2 2027 1.25 2.5 3.75 4.125"], self.pasta
        )
        self.assertEqual(original.get(0)["valorA"], [1.25, 2.5, 3.75, 4.125])
        self.assert_registro_igual(original, relido)

    def test_turbmint_com_um_e_multiplos_valores(self):
        original, relido, _ = round_trip([
            "TURBMINT  3 2028 10.5",
            "TURBMINT  4 2028 10.5 20.25 30.125",
        ], self.pasta)
        self.assertEqual(original.get(0)["valorA"], [10.5])
        self.assertEqual(original.get(1)["valorA"], [10.5, 20.25, 30.125])
        self.assert_registro_igual(original, relido, 0)
        self.assert_registro_igual(original, relido, 1)

    def test_vazmaxt_com_um_e_multiplos_valores(self):
        original, relido, _ = round_trip([
            "VAZMAXT   5 2029 99.875",
            "VAZMAXT   6 2029 99.875 100.0625",
        ], self.pasta)
        self.assertEqual(original.get(0)["valorA"], [99.875])
        self.assertEqual(original.get(1)["valorA"], [99.875, 100.0625])
        self.assert_registro_igual(original, relido, 0)
        self.assert_registro_igual(original, relido, 1)

    def test_cdesvio_apenas_com_codigo(self):
        original, relido, saida = round_trip(["CDESVIO      303"], self.pasta)
        self.assertEqual(original.get(0)["valorA"], 303)
        self.assertIsNone(original.get(0)["valorB"])
        self.assert_registro_igual(original, relido)
        self.assertRegex(saida.read_text(encoding="latin-1"), r"CDESVIO\s+303\n")

    def test_cdesvio_com_codigo_e_vazao(self):
        original, relido, _ = round_trip(["CDESVIO      303 456.7891"], self.pasta)
        self.assertEqual(original.get(0)["valorA"], 303)
        self.assertEqual(original.get(0)["valorB"], 456.7891)
        self.assert_registro_igual(original, relido)

    def test_variantes_minusculas_das_novas_palavras(self):
        registros = [
            "turbmaxt  1 2026 1.0 2.0",
            "turbmint  2 2026 3.0",
            "vazmaxt   3 2026 4.0 5.0 6.0",
            "cdesvio      303 7.5",
        ]
        original, relido, saida = round_trip(registros, self.pasta)
        self.assertEqual(
            [original.get(i)["palavra_chave"] for i in range(4)],
            ["turbmaxt", "turbmint", "vazmaxt", "cdesvio"],
        )
        for indice in range(4):
            self.assert_registro_igual(original, relido, indice)
        texto = saida.read_text(encoding="latin-1")
        for palavra in ("turbmaxt", "turbmint", "vazmaxt", "cdesvio"):
            self.assertIn(palavra, texto)

    def test_put_edita_novas_representacoes(self):
        original, _, _ = round_trip([
            "TURBMAXT  1 2026 1.0",
            "CDESVIO      303",
        ], self.pasta)
        temporal = original.get(0)
        temporal["valorA"] = [7, 8.5, 9.125]
        original.put(temporal)
        desvio = original.get(1)
        desvio["valorA"] = 404
        desvio["valorB"] = 123.4567
        original.put(desvio)

        saida = self.pasta / "MODIF_EDITADO.DAT"
        original.escrever(str(saida))
        relido = Modif()
        relido.ler(str(saida))
        self.assertEqual(relido.get(0)["valorA"], [7.0, 8.5, 9.125])
        self.assertEqual(relido.get(1)["valorA"], 404)
        self.assertEqual(relido.get(1)["valorB"], 123.4567)


class TestModifVazmintRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)

    def test_vazmint_com_ano_numerico(self):
        original, relido, _ = round_trip(["VAZMINT   1 2030 12.75"], self.pasta)
        self.assertEqual(original.get(0)["ano"], 2030)
        self.assertEqual(relido.get(0)["ano"], 2030)
        self.assertEqual(relido.get(0)["valorA"], 12.75)

    def test_vazmint_pre(self):
        original, relido, saida = round_trip(["VAZMINT   2 PRE 13.25"], self.pasta)
        self.assertEqual(original.get(0)["ano"], "PRE")
        self.assertEqual(relido.get(0)["ano"], "PRE")
        self.assertIn(" PRE ", saida.read_text(encoding="latin-1"))

    def test_vazmint_pos(self):
        original, relido, saida = round_trip(["VAZMINT   3 POS 14.5"], self.pasta)
        self.assertEqual(original.get(0)["ano"], "POS")
        self.assertEqual(relido.get(0)["ano"], "POS")
        self.assertIn(" POS ", saida.read_text(encoding="latin-1"))

    def test_put_aceita_pre_pos_e_normaliza_caixa(self):
        original, _, _ = round_trip(["VAZMINT   1 2030 12.75"], self.pasta)
        registro = original.get(0)
        registro["ano"] = "pre"
        original.put(registro)
        self.assertEqual(original.get(0)["ano"], "PRE")


class TestModifCompatibilidadeDeck(unittest.TestCase):
    def test_round_trip_do_modif_real_preserva_registros_suportados(self):
        original = Modif()
        original.ler(str(PMO / "MODIF.DAT"))
        with TemporaryDirectory(dir=ROOT / "tests") as temp:
            saida = Path(temp) / "MODIF.DAT"
            original.escrever(str(saida))
            relido = Modif()
            relido.ler(str(saida))

        self.assertEqual(list(original.lista_registros()), list(relido.lista_registros()))
        for indice in original.lista_registros():
            esperado = original.get(indice)
            atual = relido.get(indice)
            for campo in FIELDS:
                self.assertEqual(atual[campo], esperado[campo], (indice, campo))

    def test_fluxo_newave_escreve_e_rele_todos_os_novos_formatos(self):
        from PySDDP.Pen import Newave

        novos_registros = [
            " TURBMAXT  1 2026 1.0 2.0 3.0\n",
            " TURBMINT  2 2026 4.0\n",
            " VAZMAXT   3 2026 5.0 6.0\n",
            " CDESVIO      202\n",
            " CDESVIO      202 77.75\n",
            " VAZMINT   1 PRE 8.0\n",
            " VAZMINT   2 POS 9.0\n",
        ]
        with TemporaryDirectory() as temp:
            deck = Path(temp) / "deck"
            shutil.copytree(PMO, deck)
            modif_path = deck / "MODIF.DAT"
            linhas = modif_path.read_text(encoding="latin-1").splitlines(keepends=True)
            linhas[3:3] = novos_registros
            modif_path.write_text("".join(linhas), encoding="latin-1")

            with redirect_stdout(io.StringIO()):
                caso = Newave(str(deck))
            encontrados = [
                caso.modif.get(i) for i in caso.modif.lista_registros()
                if caso.modif.get(i)["codigo"] == 1 and
                caso.modif.get(i)["palavra_chave"].upper() in {
                    "TURBMAXT", "TURBMINT", "VAZMAXT", "CDESVIO", "VAZMINT"
                }
            ]
            self.assertTrue(any(r["ano"] == "PRE" for r in encontrados))
            self.assertTrue(any(r["ano"] == "POS" for r in encontrados))

            with redirect_stdout(io.StringIO()):
                caso.modif.escrever(str(modif_path))
            del caso
            with redirect_stdout(io.StringIO()):
                caso = Newave(str(deck))

            relidos = [
                caso.modif.get(i) for i in caso.modif.lista_registros()
                if caso.modif.get(i)["codigo"] == 1 and
                caso.modif.get(i)["palavra_chave"].upper() in {
                    "TURBMAXT", "TURBMINT", "VAZMAXT", "CDESVIO", "VAZMINT"
                }
            ]
            for esperado in novos_registros:
                palavra = esperado.split()[0]
                self.assertTrue(
                    any(r["palavra_chave"].upper() == palavra for r in relidos),
                    palavra,
                )
            self.assertTrue(any(r["ano"] == "PRE" for r in relidos))
            self.assertTrue(any(r["ano"] == "POS" for r in relidos))


if __name__ == "__main__":
    unittest.main()
