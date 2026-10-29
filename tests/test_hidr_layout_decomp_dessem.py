from contextlib import redirect_stdout
import hashlib
import io
import os
from pathlib import Path
import shutil
import struct
from tempfile import TemporaryDirectory
import unittest

from PySDDP.decomp.script.hidr import Hidr as HidrDecomp
from PySDDP.dessem.script.hidr import Hidr as HidrDessem
from PySDDP.hidr_layout import HidrFormatoError, REGISTRO_ANTIGO, REGISTRO_NOVO
# Modulo (e nao classes) importado para reaproveitar o montador de fixtures sem duplicar os testes NEWAVE
from tests import test_hidr_layout as base


def _caminhos(variavel):
    return [Path(p) for p in os.environ.get(variavel, "").split(os.pathsep) if p]


# HIDR.DAT reais opcionais e diretorios de decks reais opcionais, separados por os.pathsep
HIDR_REAIS = {"DECOMP": _caminhos("PYSDDP_HIDR_DECOMP"), "DESSEM": _caminhos("PYSDDP_HIDR_DESSEM")}
DECKS_REAIS = {"DECOMP": _caminhos("PYSDDP_DECKS_DECOMP"), "DESSEM": _caminhos("PYSDDP_DECKS_DESSEM")}

# 30 coeficientes distintos na regiao de pol_vaz_niv_jus (offset 548 no layout de 792 bytes): DECOMP e DESSEM
# agrupam em 5 polinomios de 6 coeficientes, ao contrario do NEWAVE (6 de 5)
VNJ = [float(k) + 0.5 for k in range(30)]


def montar_registro(tamanho, indice, **kwargs):
    reg = bytearray(base.montar_registro(tamanho, indice, **kwargs))
    struct.pack_into("<30f", reg, 548 + tamanho - REGISTRO_ANTIGO, *VNJ)
    return bytes(reg)


def montar_arquivo(tamanho, quantidade, **kwargs):
    return b"".join(montar_registro(tamanho, i, **kwargs) for i in range(quantidade))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class _HidrModeloBase:
    """Testes comuns aos leitores DECOMP e DESSEM; as subclasses definem modelo, classe e nomes de atributos."""
    modelo = None
    classe = None
    campo_sist = None
    contador = None
    layout = None

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def gravar(self, nome, conteudo):
        path = self.dir / nome
        path.write_bytes(conteudo)
        return path

    def ler(self, path, **kwargs):
        hidr = self.classe()
        with redirect_stdout(io.StringIO()):
            hidr.ler(str(path), **kwargs)
        return hidr

    def escrever(self, hidr, path, **kwargs):
        with redirect_stdout(io.StringIO()):
            hidr.escrever(str(path), **kwargs)

    def test_le_layout_antigo_com_varios_registros(self):
        hidr = self.ler(self.gravar("HIDR.DAT", montar_arquivo(REGISTRO_ANTIGO, 4, observ=b"OBS TESTE")))

        self.assertEqual(getattr(hidr, self.layout), REGISTRO_ANTIGO)
        self.assertEqual(getattr(hidr, self.contador), 5)
        self.assertEqual(hidr.codigo["valor"], [1, 2, 3, 4])
        for i in range(4):
            self.assertEqual(hidr.nome["valor"][i], f"USINA {i:02d}".ljust(12))
            self.assertEqual(hidr.posto["valor"][i], 100 + i)
            self.assertEqual(getattr(hidr, self.campo_sist)["valor"][i], 1)
            self.assertEqual(hidr.coef_evap["valor"][i], list(range(-3, 9)))
            esperado = [c * (i + 1) for c in base.POL_COTA_VOL]
            self.assertEqual(hidr.pol_cota_vol["valor"][i],
                             list(struct.unpack("<5f", struct.pack("<5f", *esperado))))
            self.assertEqual(hidr.pol_vaz_niv_jus["valor"][i], VNJ[0:6])
            self.assertEqual(hidr.pol_vaz_niv_jus["valor_5"][i], VNJ[24:30])
            self.assertAlmostEqual(hidr.cfmed["valor"][i], 885.729 + i, places=3)
            self.assertEqual(hidr.data["valor"][i], "29-09-26")
            self.assertEqual(hidr.observ["valor"][i], "OBS TESTE".ljust(43))
            self.assertEqual(hidr.tipo_reg["valor"][i], b"DMS"[i % 3:i % 3 + 1])

    def test_round_trip_layout_antigo_sha_identico(self):
        entrada = self.gravar("IN.DAT", montar_arquivo(REGISTRO_ANTIGO, 5))
        saida = self.dir / "OUT.DAT"
        self.escrever(self.ler(entrada), saida)

        self.assertEqual(saida.stat().st_size, 5 * REGISTRO_ANTIGO)
        self.assertEqual(sha256(saida), sha256(entrada))

    def test_layout_novo_exige_pedido_explicito(self):
        path = self.gravar("NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 3))

        with self.assertRaises(HidrFormatoError) as ctx:
            self.ler(path)
        self.assertIn(self.modelo, str(ctx.exception))
        self.assertIn(f"tamanho_registro={REGISTRO_NOVO}", str(ctx.exception))

    def test_layout_novo_forcado_le_e_preserva_double(self):
        entrada = self.gravar("NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 3))
        saida = self.dir / "NOVO_OUT.DAT"
        hidr = self.ler(entrada, tamanho_registro=REGISTRO_NOVO)

        self.assertEqual(getattr(hidr, self.layout), REGISTRO_NOVO)
        self.assertEqual(hidr.pol_cota_vol["valor"][0], list(base.POL_COTA_VOL))
        self.assertEqual(hidr.pol_cota_area["valor"][2], list(base.POL_COTA_AREA))
        self.assertEqual(hidr.pol_vaz_niv_jus["valor_2"][1], VNJ[6:12])
        self.assertEqual(hidr.data["valor"][2], "29-09-26")
        self.escrever(hidr, saida)
        self.assertEqual(sha256(saida), sha256(entrada))
        self.assertEqual(saida.read_bytes()[64:104], struct.pack("<5d", *base.POL_COTA_VOL))

    def test_edicao_controlada_preserva_demais_bytes(self):
        original = montar_arquivo(REGISTRO_ANTIGO, 3)
        hidr = self.ler(self.gravar("EDIT.DAT", original))
        hidr.posto["valor"][1] = 999
        hidr.pol_cota_vol["valor"][1] = [1.0, 2.0, 3.0, 4.0, 5.0]
        hidr.observ["valor"][1] = "EDITADO"
        saida = self.dir / "EDIT_OUT.DAT"
        self.escrever(hidr, saida)

        esperado = bytearray(original)
        struct.pack_into("<i", esperado, REGISTRO_ANTIGO + 12, 999)
        struct.pack_into("<5f", esperado, REGISTRO_ANTIGO + 64, 1.0, 2.0, 3.0, 4.0, 5.0)
        struct.pack_into("43s", esperado, REGISTRO_ANTIGO + 744, b"EDITADO")
        self.assertEqual(saida.read_bytes(), bytes(esperado))
        self.assertEqual(getattr(self.ler(saida), self.layout), REGISTRO_ANTIGO)

    def test_escrita_com_layout_explicito_e_invalido(self):
        hidr = self.ler(self.gravar("ANTIGO.DAT", montar_arquivo(REGISTRO_ANTIGO, 2)))
        convertido = self.dir / "CONVERTIDO.DAT"
        self.escrever(hidr, convertido, tamanho_registro=REGISTRO_NOVO)

        self.assertEqual(convertido.stat().st_size, 2 * REGISTRO_NOVO)
        relido = self.ler(convertido, tamanho_registro=REGISTRO_NOVO)
        self.assertEqual(relido.pol_cota_vol["valor"], hidr.pol_cota_vol["valor"])
        self.assertEqual(relido.pol_vaz_niv_jus["valor_3"], hidr.pol_vaz_niv_jus["valor_3"])
        self.assertEqual(relido.tipo_reg["valor"], hidr.tipo_reg["valor"])
        with self.assertRaises(HidrFormatoError):
            self.escrever(hidr, self.dir / "INVALIDO.DAT", tamanho_registro=800)
        self.assertIsNone(getattr(self.classe(), self.layout))

    def test_erros_de_arquivo(self):
        casos = {
            "vazio": b"",
            "truncado": montar_arquivo(REGISTRO_ANTIGO, 3)[:-1],
            "nao_multiplo": b"\x00" * 1000,
        }
        for nome, conteudo in casos.items():
            with self.subTest(caso=nome):
                with self.assertRaises(HidrFormatoError) as ctx:
                    self.ler(self.gravar(f"{nome}.DAT", conteudo))
                self.assertIn(self.modelo, str(ctx.exception))

        with self.assertRaises(FileNotFoundError):
            self.ler(self.dir / "INEXISTENTE.DAT")
        with self.assertRaises(HidrFormatoError):
            self.ler(self.gravar("FORCADO.DAT", montar_arquivo(REGISTRO_ANTIGO, 2)), tamanho_registro=800)

    def test_texto_ilegivel_gera_erro_diagnostico(self):
        conteudo = montar_arquivo(REGISTRO_ANTIGO, 1) + montar_registro(
            REGISTRO_ANTIGO, 1, observ="CONSTRUÇÃO".encode("latin-1"))
        with self.assertRaises(HidrFormatoError) as ctx:
            self.ler(self.gravar("OBS.DAT", conteudo))
        mensagem = str(ctx.exception)
        self.assertIn(self.modelo, mensagem)
        self.assertIn("registro 2, campo observ", mensagem)
        self.assertIn(f"offset absoluto {REGISTRO_ANTIGO + 744}", mensagem)

    def test_tamanho_ambiguo(self):
        # 104 registros de 792 bytes = 99 registros de 832 bytes = 82368 bytes
        antigo = self.ler(self.gravar("AMB_ANTIGO.DAT", montar_arquivo(REGISTRO_ANTIGO, 104)))
        self.assertEqual(getattr(antigo, self.layout), REGISTRO_ANTIGO)
        self.assertEqual(len(antigo.nome["valor"]), 104)

        with self.assertRaises(HidrFormatoError) as ctx:
            self.ler(self.gravar("AMB_ZEROS.DAT", b"\x00" * 82368))
        self.assertIn("tamanho_registro", str(ctx.exception))
        with self.assertRaises(HidrFormatoError):
            self.ler(self.gravar("AMB_NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 99)))
        novo = self.ler(self.dir / "AMB_NOVO.DAT", tamanho_registro=REGISTRO_NOVO)
        self.assertEqual(len(novo.nome["valor"]), 99)

    def test_arquivos_reais_opcionais(self):
        arquivos = HIDR_REAIS[self.modelo]
        if not arquivos:
            self.skipTest(f"defina PYSDDP_HIDR_{self.modelo} com caminhos de hidr.dat reais")
        for path in arquivos:
            with self.subTest(path=str(path)):
                hash_original = sha256(path)
                with TemporaryDirectory() as temp:
                    saida = Path(temp) / "hidr.dat"
                    self.escrever(self.ler(path), saida)
                    self.assertEqual(sha256(saida), hash_original)
                self.assertEqual(sha256(path), hash_original)

    def test_decks_reais_opcionais(self):
        decks = DECKS_REAIS[self.modelo]
        if not decks:
            self.skipTest(f"defina PYSDDP_DECKS_{self.modelo} com diretorios de decks reais")
        for deck in decks:
            with self.subTest(deck=str(deck)):
                hash_original = sha256(deck / "hidr.dat")
                with TemporaryDirectory() as temp:
                    copia = Path(temp) / "deck"
                    shutil.copytree(deck, copia)
                    with redirect_stdout(io.StringIO()):
                        objeto = self.carregar_deck(copia)
                    self.assertGreater(len(objeto.hidr.nome["valor"]), 0)
                    self.escrever(objeto.hidr, copia / "hidr_out.dat")
                    self.assertEqual(sha256(copia / "hidr_out.dat"), hash_original)
                self.assertEqual(sha256(deck / "hidr.dat"), hash_original)


class TestHidrDecomp(_HidrModeloBase, unittest.TestCase):
    modelo = "DECOMP"
    classe = HidrDecomp
    campo_sist = "submercado"
    contador = "_numero_registros"
    layout = "_tamanho_registro"

    @staticmethod
    def carregar_deck(caminho):
        from PySDDP.Pmo import Decomp
        return Decomp(str(caminho))


class TestHidrDessem(_HidrModeloBase, unittest.TestCase):
    modelo = "DESSEM"
    classe = HidrDessem
    campo_sist = "sist"
    contador = "_numero_registros_"
    layout = "_tamanho_registro_"

    @staticmethod
    def carregar_deck(caminho):
        from PySDDP.Pde import Dessem
        return Dessem(str(caminho), "dessem.arq")


if __name__ == "__main__":
    unittest.main()
