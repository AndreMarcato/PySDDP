import io
import shutil
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"


class TestManuttExptNewaveIntegration(unittest.TestCase):
    def test_newave_carrega_manutt_e_expt_do_deck(self):
        from PySDDP.Pen import Newave

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))

            self.assertTrue(hasattr(newave, "manutt"))
            self.assertTrue(hasattr(newave, "expt"))

            self.assertGreater(newave.manutt.numero_manutencoes, 0)
            self.assertGreater(newave.expt.numero_expansoes, 0)

            primeira_manutencao = next(newave.manutt.lista_manutencoes())
            self.assertIsNotNone(newave.manutt.get(primeira_manutencao))

            primeira_expansao = next(newave.expt.lista_expansoes())
            self.assertIsNotNone(newave.expt.get(primeira_expansao))

    def test_manutt_e_expt_escrevem_arquivos_independentes(self):
        from PySDDP.Pen import Newave

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))

            saida = Path(temp) / "saida"
            saida.mkdir()
            with redirect_stdout(io.StringIO()):
                newave.manutt.escrever(str(saida / newave.arquivos.manutt))
                newave.expt.escrever(str(saida / newave.arquivos.expt))

            self.assertTrue((saida / "MANUTT.DAT").exists())
            self.assertTrue((saida / "EXPT.DAT").exists())

    def test_nome_fisico_alternativo_declarado_em_arquivos_dat_e_usado(self):
        """
        Confirma que Newave resolve o nome fisico do MANUTT.DAT (e nao um
        nome fixo hard-coded) a partir do que estiver declarado em
        ARQUIVOS.DAT, do mesmo modo que confhd/exph/conft/clast.
        """
        from PySDDP.Pen import Newave

        with TemporaryDirectory() as temp:
            deck_path = Path(temp) / "deck"
            shutil.copytree(PMO, deck_path)

            # Renomeia o arquivo fisico de manutencao programada
            novo_nome = "MANUTPROG_ALT.DAT"
            (deck_path / "MANUTT.DAT").rename(deck_path / novo_nome)

            # Atualiza somente o nome fisico na linha do MANUTT em
            # ARQUIVOS.DAT (a descricao/mneumonico, colunas 0-29,
            # permanece intacta; o nome fisico comeca na coluna 30 -
            # ver Arquivos.ler, `nome = linha[30:].strip()`)
            arquivos_dat = deck_path / "ARQUIVOS.DAT"
            linhas = arquivos_dat.read_text(encoding="latin-1").splitlines()
            indice_manutt = next(
                i for i, linha in enumerate(linhas) if linha[30:].strip() == "MANUTT.DAT"
            )
            linhas[indice_manutt] = linhas[indice_manutt][:30] + novo_nome
            arquivos_dat.write_text(
                "\n".join(linhas) + "\n", encoding="latin-1"
            )

            with redirect_stdout(io.StringIO()):
                newave = Newave(str(deck_path))

            self.assertEqual(newave.arquivos.manutt, novo_nome)
            self.assertGreater(newave.manutt.numero_manutencoes, 0)


if __name__ == "__main__":
    unittest.main()
