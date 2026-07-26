import math
import unittest
from pathlib import Path
from types import SimpleNamespace

from PySDDP.newave.script.confhd import Confhd
from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.hidr import Hidr
from PySDDP.newave.script.vazoes import Vazoes


class TestFormulaEngolimento(unittest.TestCase):
    def test_expoente_por_tipo_de_turbina(self):
        casos = ((1, 0.5), (2, 0.2), (3, 0.5), (0, None), (4, None))
        for tipo_turbina, esperado in casos:
            with self.subTest(tipo_turbina=tipo_turbina):
                self.assertEqual(
                    Confhd._turbine_exponent(tipo_turbina), esperado
                )

    def test_queda_liquida_com_perda_percentual(self):
        self.assertEqual(
            Confhd._calcula_queda_liquida(100.0, 1, 3.0), 97.0
        )

    def test_queda_liquida_com_perda_absoluta(self):
        self.assertEqual(
            Confhd._calcula_queda_liquida(100.0, 2, 3.0), 97.0
        )

    def test_tipo_de_perda_invalido_e_controlado(self):
        with self.assertLogs(
                "PySDDP.newave.script.confhd", level="DEBUG"):
            resultado = Confhd._calcula_queda_liquida(100.0, 3, 3.0)
        self.assertIsNone(resultado)

    def test_queda_liquida_nao_positiva_e_invalida(self):
        for queda_bruta, tipo_perda, perda_hid in (
                (3.0, 2, 3.0),
                (2.0, 2, 3.0),
                (0.0, 1, 3.0)):
            with self.subTest(
                    queda_bruta=queda_bruta,
                    tipo_perda=tipo_perda,
                    perda_hid=perda_hid):
                resultado = Confhd._calcula_queda_liquida(
                    queda_bruta, tipo_perda, perda_hid
                )
                self.assertIsNone(resultado)

    def test_turbina_no_ponto_nominal(self):
        resultado = Confhd._calcula_engolimento_turbina(
            vazao_nominal=500.0,
            queda_liquida=40.0,
            altura_referencia=40.0,
            expoente=0.2
        )
        self.assertEqual(resultado, 500.0)

    def test_limite_do_gerador(self):
        resultado = Confhd._calcula_engolimento_gerador(
            potencia_nominal=62.5,
            prod_esp=0.008765,
            queda_liquida=38.5
        )
        self.assertAlmostEqual(resultado, 185.21125195397872)

    def test_conjunto_limitado_pela_turbina(self):
        resultado = Confhd._calcula_engolimento_conjunto(
            numero_maquinas=1,
            vazao_nominal=80.0,
            altura_referencia=100.0,
            potencia_nominal=1000.0,
            prod_esp=0.01,
            queda_liquida=100.0,
            expoente=0.5
        )
        self.assertEqual(resultado, 80.0)

    def test_conjunto_limitado_pelo_gerador(self):
        resultado = Confhd._calcula_engolimento_conjunto(
            numero_maquinas=1,
            vazao_nominal=80.0,
            altura_referencia=100.0,
            potencia_nominal=50.0,
            prod_esp=0.01,
            queda_liquida=100.0,
            expoente=0.5
        )
        self.assertEqual(resultado, 50.0)

    def test_numero_de_maquinas_aplicado_uma_vez(self):
        resultado = Confhd._calcula_engolimento_conjunto(
            numero_maquinas=4,
            vazao_nominal=100.0,
            altura_referencia=100.0,
            potencia_nominal=1000.0,
            prod_esp=0.01,
            queda_liquida=100.0,
            expoente=0.5
        )
        self.assertEqual(resultado, 400.0)

    def test_dados_ausentes_ou_nulos_sao_controlados(self):
        casos_turbina = (
            (0.0, 100.0, 100.0, 0.5),
            (100.0, 100.0, 0.0, 0.5),
        )
        for argumentos in casos_turbina:
            with self.subTest(funcao="turbina", argumentos=argumentos):
                self.assertIsNone(
                    Confhd._calcula_engolimento_turbina(*argumentos)
                )

        casos_gerador = (
            (0.0, 0.01, 100.0),
            (100.0, 0.0, 100.0),
        )
        for argumentos in casos_gerador:
            with self.subTest(funcao="gerador", argumentos=argumentos):
                self.assertIsNone(
                    Confhd._calcula_engolimento_gerador(*argumentos)
                )

        self.assertIsNone(Confhd._calcula_engolimento_conjunto(
            0, 100.0, 100.0, 100.0, 0.01, 100.0, 0.5
        ))

    def test_numero_de_conjuntos_limitado_ao_tamanho_dos_vetores(self):
        confhd = Confhd()
        dados = (
            ("_num_conj_maq", 5),
            ("_maq_por_conj", [4]),
            ("_pef_por_conj", [1000.0]),
            ("_alt_efet_conj", [100.0]),
            ("_vaz_efet_conj", [100.0]),
            ("_prod_esp", 0.01),
            ("_perda_hid", 0.0),
            ("_tipo_perda", 1),
            ("_tipo_turb", 1),
        )
        for atributo, valor in dados:
            getattr(confhd, atributo)["valor"].append(valor)

        self.assertEqual(confhd._calc_engol(100.0), 400.0)

    def test_media_ignora_condicao_com_queda_invalida(self):
        confhd = Confhd()
        dados = (
            ("_num_conj_maq", 1),
            ("_maq_por_conj", [1]),
            ("_pef_por_conj", [1000.0]),
            ("_alt_efet_conj", [1.0]),
            ("_vaz_efet_conj", [100.0]),
            ("_prod_esp", 0.01),
            ("_perda_hid", 0.0),
            ("_tipo_perda", 1),
            ("_tipo_turb", 1),
            ("_pol_cota_vol", [0.0, 1.0, 0.0, 0.0, 0.0]),
            ("_vol_min", 0.0),
            ("_vol_max", 4.0),
            ("_vol_util", 4.0),
            ("_cfmed", 1.0),
        )
        for atributo, valor in dados:
            getattr(confhd, atributo)["valor"].append(valor)

        valores_validos = [
            confhd._calc_engol(queda_bruta)
            for queda_bruta in (1.0, 1.6, 1.0, 3.0)
        ]
        confhd._calc_engol_maximo()

        self.assertAlmostEqual(
            confhd._engolimento["valor"][-1],
            sum(valores_validos) / len(valores_validos)
        )


class TestRegressaoEngolimento(unittest.TestCase):
    RESULTADOS_ESPERADOS = {
        66: 13122.728144278604,   # Itaipu: alta queda, Francis, percentual
        285: 24178.513343825154,  # Jirau: baixa queda, Kaplan, metros
        287: 25719.00569049692,   # Santo Antonio: baixa queda, Kaplan
    }

    @classmethod
    def setUpClass(cls):
        class TabelaVazia:
            shape = (0, 0)

            def __getitem__(self, chave):
                return self

            def __eq__(self, outro):
                return self

        diretorio = Path(__file__).resolve().parents[1] / "PySDDP" / "pmo"
        dger = Dger()
        dger.ler(str(diretorio / "DGER.DAT"))
        hidr = Hidr()
        hidr.ler(str(diretorio / "HIDR.DAT"))
        vazoes = Vazoes()
        vazoes.ler(str(diretorio / "VAZOES.DAT"), hidr.nr_usinas)

        sem_alteracoes = SimpleNamespace(
            bloco_usina={"df": TabelaVazia()}
        )
        cls.confhd = Confhd()
        cls.confhd.ler(
            str(diretorio / "CONFHD.DAT"),
            hidr,
            vazoes,
            dger,
            sem_alteracoes,
            sem_alteracoes
        )

    def test_casos_reais_de_baixa_e_alta_queda(self):
        for codigo, esperado in self.RESULTADOS_ESPERADOS.items():
            with self.subTest(codigo=codigo):
                uhe = self.confhd.get(codigo)
                resultado = uhe["engolimento"]
                vazao_nominal = sum(
                    float(numero) * float(vazao)
                    for numero, vazao in zip(
                        uhe["maq_por_conj"], uhe["vaz_efet_conj"]
                    )
                )

                self.assertIsInstance(resultado, float)
                self.assertTrue(math.isfinite(resultado))
                self.assertGreater(resultado, 0.0)
                self.assertAlmostEqual(resultado, esperado, places=6)
                self.assertGreater(resultado / vazao_nominal, 0.0)


if __name__ == "__main__":
    unittest.main()
