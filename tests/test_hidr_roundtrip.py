from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from PySDDP.newave.script.hidr import Hidr


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"
HIDR_PATH = PMO / "HIDR.DAT"
RECORD_SIZE = 792


def read_hidr(path):
    hidr = Hidr()
    with redirect_stdout(io.StringIO()):
        hidr.ler(str(path))
    return hidr


def write_hidr(hidr, path):
    with redirect_stdout(io.StringIO()):
        hidr.escrever(str(path))


class TestHidrRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output_dir = Path(self.temp.name)

    def assert_loaded_count(self, hidr, expected):
        self.assertEqual(hidr.nr_usinas, expected)
        self.assertEqual(hidr._numero_registros_, expected)
        self.assertEqual(len(hidr._codigo["valor"]), expected)

    def test_round_trip_real_preserva_todos_os_registros_e_bytes(self):
        original_bytes = HIDR_PATH.read_bytes()
        expected_count = len(original_bytes) // RECORD_SIZE
        original = read_hidr(HIDR_PATH)
        original_records = [
            deepcopy(original.get(code))
            for code in range(1, expected_count + 1)
        ]
        last_code = original_records[-1]["codigo"]

        output_path = self.output_dir / "HIDR.DAT"
        write_hidr(original, output_path)
        reloaded = read_hidr(output_path)

        self.assert_loaded_count(original, expected_count)
        self.assert_loaded_count(reloaded, expected_count)
        self.assertEqual(output_path.stat().st_size,
                         expected_count * RECORD_SIZE)
        self.assertEqual(
            hashlib.sha256(output_path.read_bytes()).digest(),
            hashlib.sha256(original_bytes).digest(),
        )
        self.assertEqual(reloaded.get(last_code)["codigo"], last_code)
        for code, expected in enumerate(original_records, start=1):
            with self.subTest(code=code):
                self.assertEqual(reloaded.get(code), expected)

    def test_round_trip_de_um_e_dois_registros(self):
        original_bytes = HIDR_PATH.read_bytes()

        for expected_count in (1, 2):
            with self.subTest(expected_count=expected_count):
                fixture_path = (
                    self.output_dir / f"HIDR_{expected_count}_INPUT.DAT"
                )
                fixture_bytes = original_bytes[
                    :expected_count * RECORD_SIZE
                ]
                fixture_path.write_bytes(fixture_bytes)
                hidr = read_hidr(fixture_path)

                output_path = (
                    self.output_dir / f"HIDR_{expected_count}_OUTPUT.DAT"
                )
                write_hidr(hidr, output_path)
                reloaded = read_hidr(output_path)

                self.assert_loaded_count(hidr, expected_count)
                self.assert_loaded_count(reloaded, expected_count)
                self.assertEqual(output_path.read_bytes(), fixture_bytes)
                self.assertEqual(
                    reloaded.get(expected_count),
                    hidr.get(expected_count),
                )
                self.assertIsNone(reloaded.get(expected_count + 1))

    def test_put_persiste_primeira_intermediaria_e_ultima_uhe(self):
        expected_count = HIDR_PATH.stat().st_size // RECORD_SIZE
        codes = (1, expected_count // 2, expected_count)

        for code in codes:
            with self.subTest(code=code):
                hidr = read_hidr(HIDR_PATH)
                last_before = deepcopy(hidr.get(expected_count))
                updated = deepcopy(hidr.get(code))
                updated["posto"] += 1

                self.assertEqual(hidr.put(updated), "sucesso")
                output_path = self.output_dir / f"HIDR_PUT_{code}.DAT"
                write_hidr(hidr, output_path)
                reloaded = read_hidr(output_path)

                self.assert_loaded_count(reloaded, expected_count)
                self.assertEqual(output_path.stat().st_size,
                                 expected_count * RECORD_SIZE)
                self.assertEqual(reloaded.get(code), updated)
                self.assertEqual(reloaded.get(code)["codigo"], code)
                if code == expected_count:
                    self.assertEqual(reloaded.get(expected_count), updated)
                else:
                    self.assertEqual(
                        reloaded.get(expected_count),
                        last_before,
                    )


class TestHidrNewaveIntegration(unittest.TestCase):
    def test_deck_reabre_com_vazoes_compativeis(self):
        from PySDDP.Pen import Newave

        original_hash = hashlib.sha256(HIDR_PATH.read_bytes()).digest()

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))
            expected_count = newave.hidr.nr_usinas
            last_code = newave.hidr.get(expected_count)["codigo"]

            write_hidr(newave.hidr, deck_path / "HIDR.DAT")
            del newave

            with redirect_stdout(io.StringIO()):
                reloaded = Newave(str(deck_path))

            self.assertEqual(reloaded.hidr.nr_usinas, expected_count)
            self.assertEqual(
                reloaded.hidr._numero_registros_,
                expected_count,
            )
            self.assertEqual(
                reloaded.vazoes.vaz_nat.shape[2],
                expected_count,
            )
            self.assertEqual(
                reloaded.hidr.get(last_code)["codigo"],
                last_code,
            )

        self.assertEqual(
            hashlib.sha256(HIDR_PATH.read_bytes()).digest(),
            original_hash,
        )


if __name__ == "__main__":
    unittest.main()
