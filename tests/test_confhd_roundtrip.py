from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

import numpy as np

from PySDDP.newave.script.confhd import Confhd
from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.hidr import Hidr
from PySDDP.newave.script.vazoes import Vazoes


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"
CONFHD_FIELDS = (
    "codigo",
    "nome",
    "posto",
    "jusante",
    "ree",
    "vol_ini",
    "status",
    "modif",
    "ano_i",
    "ano_f",
)


class TabelaVazia:
    shape = (0, 0)

    def __getitem__(self, chave):
        return self

    def __eq__(self, outro):
        return self


def carregar_caso(confhd_path=None, vazoes_path=None):
    dger = Dger()
    dger.ler(str(PMO / "DGER.DAT"))
    hidr = Hidr()
    hidr.ler(str(PMO / "HIDR.DAT"))
    vazoes = Vazoes()
    vazoes.ler(str(vazoes_path or PMO / "VAZOES.DAT"), hidr.nr_usinas)
    sem_alteracoes = SimpleNamespace(
        bloco_usina={"df": TabelaVazia()}
    )
    confhd = Confhd()
    confhd.ler(
        str(confhd_path or PMO / "CONFHD.DAT"),
        hidr,
        vazoes,
        dger,
        sem_alteracoes,
        sem_alteracoes,
    )
    return confhd, vazoes


class TestConfhdRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def round_trip_field(self, field, value):
        confhd, _ = carregar_caso()
        uhe = deepcopy(confhd.get(4))
        uhe[field] = value
        self.assertEqual(confhd.put(uhe), "sucesso")

        confhd_out = self.saida / f"CONFHD_{field}.DAT"
        confhd.escrever(str(confhd_out))
        relido, _ = carregar_caso(confhd_path=confhd_out)
        return relido.get(4)[field]

    def test_campos_exclusivos_do_confhd_persistem_individualmente(self):
        alternativas = {
            "ree": 9,
            "vol_ini": 12.34,
            "status": "NC",
            "modif": 2,
            "ano_i": 1932,
            "ano_f": 2015,
        }
        for field, value in alternativas.items():
            with self.subTest(field=field):
                self.assertEqual(self.round_trip_field(field, value), value)

    def test_campos_comuns_persistem_individualmente(self):
        alternativas = {
            "nome": "FUNIL NOVA".ljust(12),
            "posto": 210,
            "jusante": 20,
        }
        for field, value in alternativas.items():
            with self.subTest(field=field):
                self.assertEqual(self.round_trip_field(field, value), value)

    def test_todos_os_campos_confhd_persistem_juntos(self):
        confhd, _ = carregar_caso()
        uhe = deepcopy(confhd.get(4))
        uhe.update({
            "nome": "FUNIL NOVA",
            "posto": np.int64(210),
            "jusante": np.int32(20),
            "ree": np.int64(9),
            "vol_ini": np.float64(12.34),
            "status": "nc",
            "modif": np.int32(2),
            "ano_i": np.int64(1932),
            "ano_f": np.int64(2015),
        })
        confhd.put(uhe)

        confhd_out = self.saida / "CONFHD.DAT"
        confhd.escrever(str(confhd_out))
        relido, _ = carregar_caso(confhd_path=confhd_out)
        atual = relido.get(4)

        esperado = {
            "codigo": 4,
            "nome": "FUNIL NOVA".ljust(12),
            "posto": 210,
            "jusante": 20,
            "ree": 9,
            "vol_ini": 12.34,
            "status": "NC",
            "modif": 2,
            "ano_i": 1932,
            "ano_f": 2015,
        }
        self.assertEqual(
            {field: atual[field] for field in CONFHD_FIELDS},
            esperado,
        )

    def test_codigo_original_impede_troca_de_identidade(self):
        confhd, _ = carregar_caso()
        uhe = deepcopy(confhd.get(4))
        outra_antes = confhd.get(20)
        uhe["codigo"] = 20

        with self.assertRaisesRegex(ValueError, "codigo"):
            confhd.put(uhe)

        outra_depois = confhd.get(20)
        for field in CONFHD_FIELDS:
            self.assertEqual(outra_depois[field], outra_antes[field])

    def test_get_aceita_codigo_nome_e_float_integral(self):
        confhd, _ = carregar_caso()
        self.assertEqual(confhd.get(4)["codigo"], 4)
        self.assertEqual(confhd.get(4.0)["codigo"], 4)
        self.assertEqual(confhd.get("funil-grande")["codigo"], 4)
        self.assertIsNone(confhd.get(9999))

    def test_get_devolve_copias_dos_arrays(self):
        confhd, vazoes = carregar_caso()
        posicao = confhd._mapa[4]
        posto = confhd.get(4)["posto"]
        uhe = confhd.get(4)
        vazao_original = int(vazoes.vaz_nat[0, 0, posto - 1])
        ro_original = float(
            confhd._ro_acum_med["valor"][posicao][0, 0]
        )

        uhe["vazoes"][0, 0] += 10
        uhe["ro_acum_med"][0, 0] += 10

        self.assertEqual(
            int(vazoes.vaz_nat[0, 0, posto - 1]), vazao_original
        )
        self.assertEqual(
            float(confhd._ro_acum_med["valor"][posicao][0, 0]),
            ro_original,
        )

    def test_put_trata_todas_as_chaves_expostas(self):
        confhd, _ = carregar_caso()
        uhe = confhd.get(4)
        self.assertEqual(
            set(uhe) - {"codigo_original"},
            set(Confhd._FIELD_MAP),
        )
        uhe["cmont"] = uhe["cmont"] + 1.0
        uhe["ro_acum_med"] = uhe["ro_acum_med"] + 2.0
        uhe["ro_acum_min"] = uhe["ro_acum_min"] + 3.0

        confhd.put(uhe)
        atual = confhd.get(4)

        np.testing.assert_array_equal(atual["cmont"], uhe["cmont"])
        np.testing.assert_array_equal(
            atual["ro_acum_med"], uhe["ro_acum_med"]
        )
        np.testing.assert_array_equal(
            atual["ro_acum_min"], uhe["ro_acum_min"]
        )

    def test_put_exige_dicionario_completo_e_rejeita_chave_desconhecida(self):
        confhd, _ = carregar_caso()
        incompleto = confhd.get(4)
        del incompleto["ree"]
        with self.assertRaisesRegex(KeyError, "ree"):
            confhd.put(incompleto)

        desconhecido = confhd.get(4)
        desconhecido["campo_inexistente"] = 1
        with self.assertRaisesRegex(KeyError, "campo_inexistente"):
            confhd.put(desconhecido)

    def test_validacoes_dos_campos_fixos(self):
        casos = (
            ("nome", "NOME GRANDE DEMAIS", ValueError),
            ("status", "XX", ValueError),
            ("vol_ini", 100.01, ValueError),
            ("posto", 0, ValueError),
            ("ree", 10000, ValueError),
            ("modif", "um", TypeError),
        )
        for field, value, error in casos:
            with self.subTest(field=field):
                confhd, _ = carregar_caso()
                uhe = confhd.get(4)
                uhe[field] = value
                with self.assertRaises(error):
                    confhd.put(uhe)

        confhd, _ = carregar_caso()
        uhe = confhd.get(4)
        uhe["ano_i"] = 2017
        uhe["ano_f"] = 2016
        with self.assertRaisesRegex(ValueError, "ano_i"):
            confhd.put(uhe)

    def test_round_trip_sem_edicao_preserva_arquivo_fisico_e_semantica(self):
        confhd, _ = carregar_caso()
        confhd_out = self.saida / "CONFHD.DAT"
        confhd.escrever(str(confhd_out))

        self.assertEqual(
            confhd_out.read_bytes(),
            (PMO / "CONFHD.DAT").read_bytes(),
        )

        relido, _ = carregar_caso(confhd_path=confhd_out)
        self.assertEqual(confhd.nuhe, relido.nuhe)
        for codigo in confhd.lista_uhes():
            original = confhd.get(codigo)
            atual = relido.get(codigo)
            for field in CONFHD_FIELDS:
                self.assertEqual(atual[field], original[field])

    def test_escrever_rejeita_estado_invalido_antes_de_criar_arquivo(self):
        confhd, _ = carregar_caso()
        confhd._status["valor"][0] = "XX"
        confhd_out = self.saida / "CONFHD_INVALIDO.DAT"

        with self.assertRaisesRegex(ValueError, "status"):
            confhd.escrever(str(confhd_out))

        self.assertFalse(confhd_out.exists())


class TestVazoesViaConfhd(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def test_series_de_multiplas_uhes_persistem_sem_afetar_outra(self):
        confhd, vazoes = carregar_caso()
        uhe_4 = confhd.get(4)
        uhe_20 = confhd.get(20)
        controle = confhd.get(21)
        serie_controle = controle["vazoes"].copy()
        serie_4 = uhe_4["vazoes"] + 1
        serie_20 = uhe_20["vazoes"] + 2
        uhe_4["vazoes"] = serie_4
        uhe_20["vazoes"] = serie_20

        confhd.put(uhe_4)
        confhd.put(uhe_20)

        confhd_out = self.saida / "CONFHD.DAT"
        vazoes_out = self.saida / "VAZOES.DAT"
        confhd.escrever(str(confhd_out))
        vazoes.escrever(str(vazoes_out))
        relido, _ = carregar_caso(
            confhd_path=confhd_out,
            vazoes_path=vazoes_out,
        )

        np.testing.assert_array_equal(relido.get(4)["vazoes"], serie_4)
        np.testing.assert_array_equal(relido.get(20)["vazoes"], serie_20)
        np.testing.assert_array_equal(
            relido.get(21)["vazoes"], serie_controle
        )
        self.assertEqual(relido.get(4)["vazoes"].dtype, np.dtype(np.int32))

    def test_round_trip_de_vazoes_sem_edicao_preserva_arquivo(self):
        _, vazoes = carregar_caso()
        vazoes_out = self.saida / "VAZOES.DAT"

        vazoes.escrever(str(vazoes_out))

        self.assertEqual(
            vazoes_out.read_bytes(),
            (PMO / "VAZOES.DAT").read_bytes(),
        )

    def test_posto_compartilhado_compartilha_a_mesma_serie(self):
        confhd, _ = carregar_caso()
        self.assertEqual(confhd.get(155)["posto"], confhd.get(308)["posto"])
        uhe = confhd.get(155)
        serie = uhe["vazoes"] + 1
        uhe["vazoes"] = serie

        confhd.put(uhe)

        np.testing.assert_array_equal(confhd.get(308)["vazoes"], serie)

    def test_alterar_posto_associa_serie_ao_novo_posto(self):
        confhd, vazoes = carregar_caso()
        uhe = confhd.get(4)
        serie = uhe["vazoes"] + 3
        uhe["posto"] = 210
        uhe["vazoes"] = serie

        confhd.put(uhe)
        confhd_out = self.saida / "CONFHD.DAT"
        vazoes_out = self.saida / "VAZOES.DAT"
        confhd.escrever(str(confhd_out))
        vazoes.escrever(str(vazoes_out))
        relido, _ = carregar_caso(
            confhd_path=confhd_out,
            vazoes_path=vazoes_out,
        )

        self.assertEqual(relido.get(4)["posto"], 210)
        np.testing.assert_array_equal(relido.get(4)["vazoes"], serie)

    def test_vazoes_invalidas_sao_rejeitadas(self):
        confhd, _ = carregar_caso()
        casos = (
            np.zeros((1, 12), dtype=np.int32),
            np.full(confhd.get(4)["vazoes"].shape, 1.5),
            np.full(confhd.get(4)["vazoes"].shape, np.nan),
            np.full(confhd.get(4)["vazoes"].shape, 1 + 2j),
            np.full(
                confhd.get(4)["vazoes"].shape,
                np.iinfo(np.int32).max + 1,
                dtype=np.int64,
            ),
        )
        for serie in casos:
            with self.subTest(shape=serie.shape, dtype=serie.dtype):
                uhe = confhd.get(4)
                uhe["vazoes"] = serie
                with self.assertRaises((TypeError, ValueError)):
                    confhd.put(uhe)


if __name__ == "__main__":
    unittest.main()
