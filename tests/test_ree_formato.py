from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

import numpy as np

from PySDDP.newave.script.ree import Ree


class ConfhdVazio:
    def __init__(self):
        self._status_vol_morto = {"valor": [np.zeros((1, 12))]}
        self._vazoes = {"valor": [np.zeros((2, 12))]}
        self._ree = {"valor": []}

    def lista_uhes(self):
        return []


class TestFormatoRee(unittest.TestCase):
    CABECALHO = (
        " REES X SUBMERCADOS\n"
        " NUM|NOME REES.| SUBM\n"
        " XXX|XXXXXXXXXX|  XXX\n"
    )

    def ler(self, caminho):
        ree = Ree()
        with redirect_stdout(io.StringIO()):
            ree.ler(str(caminho), ConfhdVazio())
        return ree

    def test_round_trip_preserva_campos_e_flag_modificados(self):
        conteudo = (
            self.CABECALHO
            + "   1 SUDESTE        1   3 2027\n"
            + "  12 PRNPANEMA      2  11 2031\n"
            + " 999\n"
            + "                        1\n"
        )

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as diretorio:
            origem = Path(diretorio) / "REE.DAT"
            destino = Path(diretorio) / "REE_OUT.DAT"
            origem.write_text(conteudo, encoding="latin-1")

            ree = self.ler(origem)
            self.assertEqual(ree.numero_rees, 2)
            self.assertEqual(ree.bloco_ree["df"]["mes"].tolist(), [3, 11])
            self.assertEqual(ree.bloco_ree["df"]["ano"].tolist(), [2027, 2031])
            self.assertEqual(ree.flag_ficticias["valor"], 1)

            ree.bloco_ree["df"].loc[0, "mes"] = 8
            ree.bloco_ree["df"].loc[0, "ano"] = 2035
            ree.flag_ficticias["valor"] = 0
            with redirect_stdout(io.StringIO()):
                ree.escrever(str(destino))

            linhas = destino.read_text(encoding="latin-1").splitlines()
            self.assertEqual(linhas[3][1:4], "  1")
            self.assertEqual(linhas[3][5:15], "SUDESTE   ")
            self.assertEqual(linhas[3][18:21], "  1")
            self.assertEqual(linhas[3][23:25], " 8")
            self.assertEqual(linhas[3][26:30], "2035")
            self.assertEqual(linhas[5], " 999")
            self.assertEqual(linhas[6][21:25], "   0")

            relido = self.ler(destino)
            self.assertEqual(relido.numero_rees, 2)
            self.assertEqual(relido.bloco_ree["df"]["codigo"].tolist(), [1, 12])
            self.assertEqual(
                relido.bloco_ree["df"]["nome"].str.rstrip().tolist(),
                ["SUDESTE", "PRNPANEMA"],
            )
            self.assertEqual(
                relido.bloco_ree["df"]["submercado"].tolist(), [1, 2]
            )
            self.assertEqual(relido.bloco_ree["df"]["mes"].tolist(), [8, 11])
            self.assertEqual(
                relido.bloco_ree["df"]["ano"].tolist(), [2035, 2031]
            )
            self.assertEqual(relido.flag_ficticias["valor"], 0)

    def test_deck_antigo_sem_segundo_bloco_assume_zero(self):
        conteudo = self.CABECALHO + "   1 SUDESTE        1\n" + " 999\n"

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as diretorio:
            origem = Path(diretorio) / "REE.DAT"
            destino = Path(diretorio) / "REE_OUT.DAT"
            origem.write_text(conteudo, encoding="latin-1")

            ree = self.ler(origem)
            self.assertEqual(ree.bloco_ree["df"].loc[0, "mes"], 0)
            self.assertEqual(ree.bloco_ree["df"].loc[0, "ano"], 0)
            self.assertEqual(ree.flag_ficticias["valor"], 0)

            with redirect_stdout(io.StringIO()):
                ree.escrever(str(destino))

            linhas = destino.read_text(encoding="latin-1").splitlines()
            self.assertEqual(linhas[-2], " 999")
            self.assertEqual(linhas[-1][21:25], "   0")

    def test_fim_antes_do_terminador_nao_e_mascarado(self):
        conteudo = self.CABECALHO + "   1 SUDESTE        1   3 2027\n"

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as diretorio:
            origem = Path(diretorio) / "REE.DAT"
            origem.write_text(conteudo, encoding="latin-1")

            with self.assertRaisesRegex(ValueError, "terminador 999"):
                self.ler(origem)


if __name__ == "__main__":
    unittest.main()
