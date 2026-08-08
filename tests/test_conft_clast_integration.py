import io
import shutil
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"


class TestConftClastNewaveIntegration(unittest.TestCase):
    def test_newave_carrega_conft_e_clast_do_deck(self):
        from PySDDP.Pen import Newave

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))

            self.assertTrue(hasattr(newave, "conft"))
            self.assertTrue(hasattr(newave, "clast"))

            self.assertGreater(newave.conft.numero_usinas, 0)
            self.assertGreater(newave.clast.numero_classes, 0)
            self.assertGreater(newave.clast.numero_alteracoes, 0)

            # Os objetos devem estar acessiveis e consultaveis via get()
            primeira_usina = next(newave.conft.lista_usinas())
            self.assertIsNotNone(newave.conft.get(primeira_usina))

            primeira_classe = next(newave.clast.lista_classes())
            self.assertIsNotNone(newave.clast.get(primeira_classe))
            self.assertIsNotNone(newave.clast.get_alteracao(0))

    def test_conft_e_clast_escrevem_arquivos_independentes(self):
        from PySDDP.Pen import Newave

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))

            saida = Path(temp) / "saida"
            saida.mkdir()
            with redirect_stdout(io.StringIO()):
                newave.conft.escrever(str(saida / newave.arquivos.conft))
                newave.clast.escrever(str(saida / newave.arquivos.clast))

            self.assertTrue((saida / "CONFT.DAT").exists())
            self.assertTrue((saida / "CLAST.DAT").exists())


if __name__ == "__main__":
    unittest.main()
