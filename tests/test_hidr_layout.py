from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import os
from pathlib import Path
import shutil
import struct
from tempfile import TemporaryDirectory
import unittest

from PySDDP.newave.script.hidr import (
    Hidr,
    HidrFormatoError,
    REGISTRO_ANTIGO,
    REGISTRO_NOVO,
    detectar_tamanho_registro,
)


# Arquivos HIDR.DAT reais opcionais (ex.: decks NEWAVE ONS/CCEE de nov/2026), separados por os.pathsep.
# Os testes correspondentes sao ignorados quando a variavel nao esta definida.
HIDR_REAIS = [
    Path(p) for p in os.environ.get("PYSDDP_HIDR_REAIS", "").split(os.pathsep) if p
]
# Diretorios de decks NEWAVE completos opcionais, separados por os.pathsep.
DECKS_REAIS = [
    Path(p) for p in os.environ.get("PYSDDP_DECKS_NEWAVE", "").split(os.pathsep) if p
]

# Coeficientes que nao sao representaveis em float32: detectam rebaixamento de precisao.
POL_COTA_VOL = (893.0279, 0.06682515, -1.2345678901234e-4, 3.21e-7, -2.5e-10)
POL_COTA_AREA = (12.5313, -6.14375, 2.61067, 241.601, -0.942324)


def montar_registro(tamanho, indice, observ=b"", nome=None):
    """Monta um registro HIDR por offsets explicitos, independente do leitor testado."""
    desloc = tamanho - REGISTRO_ANTIGO
    fmt_pol = "<5d" if tamanho == REGISTRO_NOVO else "<5f"
    reg = bytearray(tamanho)
    struct.pack_into("12s", reg, 0, nome or f"USINA {indice:02d}".ljust(12).encode())
    struct.pack_into("<i", reg, 12, 100 + indice)
    struct.pack_into("8s", reg, 16, b"0       ")
    struct.pack_into("<4i", reg, 24, 1, 2, indice + 1, 0)
    struct.pack_into("<6f", reg, 40, 107.6, 743.74, 743.74, 0.0, 899.0, 913.0)
    struct.pack_into(fmt_pol, reg, 64, *(c * (indice + 1) for c in POL_COTA_VOL))
    struct.pack_into(fmt_pol, reg, 64 + struct.calcsize(fmt_pol), *POL_COTA_AREA)
    struct.pack_into("<12i", reg, 104 + desloc, *range(-3, 9))
    struct.pack_into("<i", reg, 152 + desloc, 2)
    struct.pack_into("<5i", reg, 156 + desloc, 6, 2, 0, 0, 0)
    struct.pack_into("<f", reg, 692 + desloc, 885.729 + indice)
    struct.pack_into("<i", reg, 732 + desloc, 2)
    struct.pack_into("8s", reg, 736 + desloc, b"29-09-26")
    struct.pack_into("43s", reg, 744 + desloc, observ.ljust(43))
    struct.pack_into("<f", reg, 787 + desloc, 743.74)
    struct.pack_into("c", reg, 791 + desloc, b"DMS"[indice % 3:indice % 3 + 1])
    return bytes(reg)


def montar_arquivo(tamanho, quantidade, **kwargs):
    return b"".join(montar_registro(tamanho, i, **kwargs) for i in range(quantidade))


def ler(path, **kwargs):
    hidr = Hidr()
    with redirect_stdout(io.StringIO()):
        hidr.ler(str(path), **kwargs)
    return hidr


def escrever(hidr, path, **kwargs):
    with redirect_stdout(io.StringIO()):
        hidr.escrever(str(path), **kwargs)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class TestHidrLayout(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def gravar(self, nome, conteudo):
        path = self.dir / nome
        path.write_bytes(conteudo)
        return path

    def test_detecta_layout_antigo_e_novo(self):
        antigo = self.gravar("ANTIGO.DAT", montar_arquivo(REGISTRO_ANTIGO, 3))
        novo = self.gravar("NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 3))

        self.assertEqual(detectar_tamanho_registro(str(antigo)), REGISTRO_ANTIGO)
        self.assertEqual(detectar_tamanho_registro(str(novo)), REGISTRO_NOVO)
        self.assertEqual(ler(antigo)._tamanho_registro_, REGISTRO_ANTIGO)
        self.assertEqual(ler(novo)._tamanho_registro_, REGISTRO_NOVO)

    def test_le_varios_registros_nos_dois_layouts_sem_deslocamento(self):
        for tamanho in (REGISTRO_ANTIGO, REGISTRO_NOVO):
            with self.subTest(tamanho=tamanho):
                path = self.gravar(f"HIDR_{tamanho}.DAT", montar_arquivo(tamanho, 4, observ=b"OBS TESTE"))
                hidr = ler(path)

                self.assertEqual(hidr.nr_usinas, 4)
                self.assertEqual(hidr._numero_registros_, 4)
                for i in range(4):
                    uhe = hidr.get(i + 1)
                    self.assertEqual(uhe["nome"], f"USINA {i:02d}".ljust(12))
                    self.assertEqual(uhe["posto"], 100 + i)
                    self.assertEqual(uhe["jusante"], i + 1)
                    self.assertEqual(uhe["coef_evap"], list(range(-3, 9)))
                    self.assertEqual(uhe["num_conj_maq"], 2)
                    self.assertEqual(uhe["maq_por_conj"], [6, 2, 0, 0, 0])
                    self.assertAlmostEqual(uhe["cfmed"], 885.729 + i, places=3)
                    self.assertEqual(uhe["tipo_perda"], 2)
                    self.assertEqual(uhe["data"], "29-09-26")
                    self.assertEqual(uhe["observ"], "OBS TESTE".ljust(43))
                    self.assertAlmostEqual(uhe["vol_ref"], 743.74, places=3)
                    self.assertEqual(uhe["tipo_reg"], "DMS"[i % 3])
                    esperado = [c * (i + 1) for c in POL_COTA_VOL]
                    if tamanho == REGISTRO_NOVO:
                        self.assertEqual(uhe["pol_cota_vol"], esperado)
                        self.assertEqual(uhe["pol_cota_area"], list(POL_COTA_AREA))
                    else:
                        esperado32 = list(struct.unpack("<5f", struct.pack("<5f", *esperado)))
                        self.assertEqual(uhe["pol_cota_vol"], esperado32)

    def test_round_trip_preserva_layout_e_bytes(self):
        for tamanho in (REGISTRO_ANTIGO, REGISTRO_NOVO):
            with self.subTest(tamanho=tamanho):
                entrada = self.gravar(f"IN_{tamanho}.DAT", montar_arquivo(tamanho, 5))
                saida = self.dir / f"OUT_{tamanho}.DAT"
                hidr = ler(entrada)
                escrever(hidr, saida)

                self.assertEqual(saida.stat().st_size, 5 * tamanho)
                self.assertEqual(sha256(saida), sha256(entrada))
                self.assertEqual(ler(saida)._tamanho_registro_, tamanho)

    def test_layout_novo_nao_rebaixa_coeficientes_double(self):
        entrada = self.gravar("NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 2))
        saida = self.dir / "NOVO_OUT.DAT"
        hidr = ler(entrada)
        escrever(hidr, saida)
        conteudo = saida.read_bytes()

        self.assertEqual(conteudo[64:104], struct.pack("<5d", *POL_COTA_VOL))
        self.assertEqual(conteudo[104:144], struct.pack("<5d", *POL_COTA_AREA))
        self.assertEqual(ler(saida).get(1)["pol_cota_vol"], list(POL_COTA_VOL))
        self.assertNotEqual(
            list(struct.unpack("<5f", struct.pack("<5f", *POL_COTA_VOL))),
            list(POL_COTA_VOL),
        )

    def test_edicao_controlada_preserva_layout_e_demais_campos(self):
        for tamanho in (REGISTRO_ANTIGO, REGISTRO_NOVO):
            with self.subTest(tamanho=tamanho):
                original = montar_arquivo(tamanho, 3)
                entrada = self.gravar(f"EDIT_IN_{tamanho}.DAT", original)
                saida = self.dir / f"EDIT_OUT_{tamanho}.DAT"
                hidr = ler(entrada)
                uhe = deepcopy(hidr.get(2))
                uhe["posto"] = 999
                uhe["pol_cota_vol"] = [1.0, 2.0, 3.0, 4.0, 5.0]
                uhe["observ"] = "EDITADO"
                self.assertEqual(hidr.put(uhe), "sucesso")
                escrever(hidr, saida)

                gravado = saida.read_bytes()
                fmt_pol = "<5d" if tamanho == REGISTRO_NOVO else "<5f"
                tam_pol = struct.calcsize(fmt_pol)
                obs = 744 + tamanho - REGISTRO_ANTIGO
                inicio = tamanho
                esperado = bytearray(original)
                struct.pack_into("<i", esperado, inicio + 12, 999)
                struct.pack_into(fmt_pol, esperado, inicio + 64, 1.0, 2.0, 3.0, 4.0, 5.0)
                struct.pack_into("43s", esperado, inicio + obs, b"EDITADO")

                self.assertEqual(len(gravado), 3 * tamanho)
                self.assertEqual(gravado, bytes(esperado))
                self.assertEqual(tam_pol, 40 if tamanho == REGISTRO_NOVO else 20)
                relido = ler(saida)
                self.assertEqual(relido._tamanho_registro_, tamanho)
                self.assertEqual(relido.get(2)["posto"], 999)
                self.assertEqual(relido.get(1), hidr.get(1))
                self.assertEqual(relido.get(3), hidr.get(3))

    def test_instancia_sem_origem_e_conversao_explicita(self):
        entrada = self.gravar("ANTIGO.DAT", montar_arquivo(REGISTRO_ANTIGO, 2))
        hidr = ler(entrada)

        vazio = Hidr()
        self.assertIsNone(vazio._tamanho_registro_)
        vazio._numero_registros_ = 0
        escrever(vazio, self.dir / "VAZIO.DAT")
        self.assertEqual((self.dir / "VAZIO.DAT").stat().st_size, 0)

        convertido = self.dir / "CONVERTIDO.DAT"
        escrever(hidr, convertido, tamanho_registro=REGISTRO_NOVO)
        self.assertEqual(convertido.stat().st_size, 2 * REGISTRO_NOVO)
        self.assertEqual(hidr._tamanho_registro_, REGISTRO_ANTIGO)
        relido = ler(convertido)
        self.assertEqual(relido._tamanho_registro_, REGISTRO_NOVO)
        self.assertEqual(relido.get(2)["pol_cota_vol"], hidr.get(2)["pol_cota_vol"])
        self.assertEqual(relido.get(2)["data"], "29-09-26")

        with self.assertRaises(HidrFormatoError):
            escrever(hidr, self.dir / "INVALIDO.DAT", tamanho_registro=800)

    def test_preserva_bytes_nao_utf8_da_observacao(self):
        observ = "USINA EM CONSTRUÇÃO".encode("latin-1")
        entrada = self.gravar("OBS.DAT", montar_arquivo(REGISTRO_NOVO, 2, observ=observ))
        saida = self.dir / "OBS_OUT.DAT"
        hidr = ler(entrada)
        escrever(hidr, saida)

        self.assertEqual(hidr.get(1)["observ"], "USINA EM CONSTRUO".ljust(43 - 2))
        self.assertEqual(sha256(saida), sha256(entrada))

    def test_texto_nao_utf8_em_campo_estrito_gera_erro_diagnostico(self):
        conteudo = montar_arquivo(REGISTRO_ANTIGO, 2)
        conteudo = conteudo[:REGISTRO_ANTIGO] + montar_registro(
            REGISTRO_ANTIGO, 1, nome="SÃO JOÃO".encode("latin-1").ljust(12))
        path = self.gravar("NOME.DAT", conteudo)

        with self.assertRaises(HidrFormatoError) as ctx:
            ler(path)
        mensagem = str(ctx.exception)
        self.assertIn("registro 2", mensagem)
        self.assertIn("campo nome", mensagem)
        self.assertIn(f"offset absoluto {REGISTRO_ANTIGO}", mensagem)
        self.assertIsInstance(ctx.exception, ValueError)

    def test_erros_de_tamanho(self):
        casos = {
            "vazio": b"",
            "truncado_novo": montar_arquivo(REGISTRO_NOVO, 3)[:-1],
            "truncado_antigo": montar_arquivo(REGISTRO_ANTIGO, 3)[:-10],
            "nao_multiplo": b"\x00" * 1000,
        }
        for nome, conteudo in casos.items():
            with self.subTest(caso=nome):
                path = self.gravar(f"{nome}.DAT", conteudo)
                with self.assertRaises(HidrFormatoError):
                    ler(path)

        with self.assertRaises(FileNotFoundError):
            ler(self.dir / "INEXISTENTE.DAT")

        path = self.gravar("FORCADO.DAT", montar_arquivo(REGISTRO_NOVO, 2))
        with self.assertRaises(HidrFormatoError):
            ler(path, tamanho_registro=REGISTRO_ANTIGO)
        with self.assertRaises(HidrFormatoError):
            ler(path, tamanho_registro=800)

    def test_tamanho_ambiguo(self):
        # 104 registros de 792 bytes = 99 registros de 832 bytes = 82368 bytes
        antigo = self.gravar("AMB_ANTIGO.DAT", montar_arquivo(REGISTRO_ANTIGO, 104))
        novo = self.gravar("AMB_NOVO.DAT", montar_arquivo(REGISTRO_NOVO, 99))
        zeros = self.gravar("AMB_ZEROS.DAT", b"\x00" * 82368)

        self.assertEqual(detectar_tamanho_registro(str(antigo)), REGISTRO_ANTIGO)
        self.assertEqual(detectar_tamanho_registro(str(novo)), REGISTRO_NOVO)
        with self.assertRaises(HidrFormatoError) as ctx:
            detectar_tamanho_registro(str(zeros))
        self.assertIn("tamanho_registro", str(ctx.exception))

        forcado = ler(zeros, tamanho_registro=REGISTRO_NOVO)
        self.assertEqual(forcado.nr_usinas, 99)


@unittest.skipUnless(HIDR_REAIS, "defina PYSDDP_HIDR_REAIS com caminhos de HIDR.DAT reais")
class TestHidrArquivosReais(unittest.TestCase):
    def test_round_trip_binario_sem_alterar_original(self):
        for path in HIDR_REAIS:
            with self.subTest(path=str(path)):
                hash_original = sha256(path)
                hidr = ler(path)
                self.assertEqual(path.stat().st_size, hidr.nr_usinas * hidr._tamanho_registro_)
                with TemporaryDirectory() as temp:
                    saida = Path(temp) / "HIDR.DAT"
                    escrever(hidr, saida)
                    self.assertEqual(sha256(saida), hash_original)
                self.assertEqual(sha256(path), hash_original)


@unittest.skipUnless(DECKS_REAIS, "defina PYSDDP_DECKS_NEWAVE com diretorios de decks NEWAVE reais")
class TestHidrDecksReais(unittest.TestCase):
    def test_pen_newave_em_copia_do_deck(self):
        from PySDDP.Pen import Newave

        for deck in DECKS_REAIS:
            with self.subTest(deck=str(deck)):
                hash_original = sha256(deck / "HIDR.DAT")
                with TemporaryDirectory() as temp:
                    copia = Path(temp) / "deck"
                    shutil.copytree(deck, copia)
                    with redirect_stdout(io.StringIO()):
                        newave = Newave(str(copia))
                    self.assertEqual(newave.vazoes.vaz_nat.shape[2], newave.hidr.nr_usinas)
                    # A carga completa aplica o MODIF.DAT sobre os dados do Hidr (comportamento pre-existente),
                    # por isso aqui se verifica apenas a preservacao do layout; o round-trip binario do
                    # HIDR isolado e coberto por TestHidrArquivosReais.
                    escrever(newave.hidr, copia / "HIDR_OUT.DAT")
                    self.assertEqual((copia / "HIDR_OUT.DAT").stat().st_size, (deck / "HIDR.DAT").stat().st_size)
                    relido = ler(copia / "HIDR_OUT.DAT")
                    self.assertEqual(relido._tamanho_registro_, newave.hidr._tamanho_registro_)
                    self.assertEqual(relido.nr_usinas, newave.hidr.nr_usinas)
                self.assertEqual(sha256(deck / "HIDR.DAT"), hash_original)


if __name__ == "__main__":
    unittest.main()
