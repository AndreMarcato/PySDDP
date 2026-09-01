from contextlib import redirect_stdout
from pathlib import Path
from tempfile import NamedTemporaryFile
import io
import unittest

import pandas as pd

from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.patamar import Patamar


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"


def _arquivo_temporario(conteudo):
    arquivo = NamedTemporaryFile(
        mode="w", encoding="latin-1", suffix=".DAT", dir=ROOT, delete=False
    )
    arquivo.write(conteudo)
    arquivo.close()
    return Path(arquivo.name)


class TestCompatibilidadeDgerPatamar(unittest.TestCase):
    def test_dger_ignora_padding_de_espacos(self):
        linhas = (PMO / "DGER.DAT").read_text(encoding="latin-1").splitlines()
        caminho = _arquivo_temporario(
            "\n".join(linha.ljust(500) for linha in linhas) + "\n"
        )
        self.addCleanup(caminho.unlink, missing_ok=True)

        dger = Dger()
        with redirect_stdout(io.StringIO()):
            dger.ler(str(caminho))

        self.assertEqual(dger.vol_earm_inic["valor"], [0.0] * 5)
        self.assertIsNone(dger.iter_inic_zinf["valor"])
        self.assertIsNone(dger.aini_sim_fin["valor"])
        self.assertEqual(dger.vini_ree_sim_fin["valor"], [])

    def test_patamar_aceita_meses_anteriores_ao_inicio_em_branco(self):
        dger = Dger()
        with redirect_stdout(io.StringIO()):
            dger.ler(str(PMO / "DGER.DAT"))

        linhas = (PMO / "PATAMAR.DAT").read_text(
            encoding="latin-1"
        ).splitlines()
        for indice in (26, 27, 28):
            linhas[indice] = linhas[indice][:8] + " " * 56 + linhas[indice][64:]
        caminho = _arquivo_temporario("\n".join(linhas) + "\n")
        self.addCleanup(caminho.unlink, missing_ok=True)

        patamar = Patamar()
        with redirect_stdout(io.StringIO()):
            patamar.ler(str(caminho), dger)

        primeiro_ano = patamar.bloco_mercado["df"].query(
            "sistema == 1 and ano == 2018"
        )
        self.assertEqual(primeiro_ano["fator"].isna().sum(), 24)
        self.assertFalse(
            pd.isna(
                primeiro_ano.query("mes == 9 and patamar == 1").iloc[0]["fator"]
            )
        )

        saida = caminho.with_name(caminho.stem + "_OUT.DAT")
        self.addCleanup(saida.unlink, missing_ok=True)
        with redirect_stdout(io.StringIO()):
            patamar.escrever(str(saida))
        self.assertTrue(saida.read_text(encoding="latin-1").splitlines()[26][8:64].isspace())


if __name__ == "__main__":
    unittest.main()
