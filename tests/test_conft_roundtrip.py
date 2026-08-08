from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PySDDP.newave.script.conft import Conft


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"

CONFT_FIELDS = (
    "codigo_usina",
    "nome_usina",
    "codigo_submercado",
    "status",
    "codigo_classe_termica",
    "codigo_tecnologia",
    "codigo_classe_gas",
)


def carregar_caso(conft_path=None):
    conft = Conft()
    conft.ler(str(conft_path or PMO / "CONFT.DAT"))
    return conft


class TestConftLeitura(unittest.TestCase):
    def test_le_todos_os_registros_ignorando_comentarios_iniciais(self):
        conft = carregar_caso()
        self.assertEqual(conft.numero_usinas, 132)
        # Nenhum registro de comentario/cabecalho deve aparecer nos dados
        self.assertNotIn(9999999, conft._codigo_usina["valor"])

    def test_le_os_sete_campos_de_um_registro(self):
        conft = carregar_caso()
        angra1 = conft.get(1)
        self.assertEqual(
            {field: angra1[field] for field in CONFT_FIELDS},
            {
                "codigo_usina": 1,
                "nome_usina": "ANGRA 1",
                "codigo_submercado": 1,
                "status": "EX",
                "codigo_classe_termica": 1,
                "codigo_tecnologia": None,
                "codigo_classe_gas": None,
            },
        )

    def test_status_ex_ee_ne_estao_presentes_no_deck_real(self):
        conft = carregar_caso()
        self.assertEqual(
            set(conft._status["valor"]) & {"EX", "EE", "NE", "NC"},
            {"EX", "EE", "NE"},
        )

    def test_campos_numericos_opcionais_em_branco_viram_none(self):
        conft = carregar_caso()
        usina = conft.get(1)
        self.assertIsNone(usina["codigo_tecnologia"])
        self.assertIsNone(usina["codigo_classe_gas"])

    def test_get_aceita_codigo_nome_e_float_integral(self):
        conft = carregar_caso()
        self.assertEqual(conft.get(1)["codigo_usina"], 1)
        self.assertEqual(conft.get(1.0)["codigo_usina"], 1)
        self.assertEqual(conft.get("angra 1")["codigo_usina"], 1)
        self.assertIsNone(conft.get(999999))


class TestConftRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def test_round_trip_sem_edicao_preserva_semantica(self):
        conft = carregar_caso()
        conft_out = self.saida / "CONFT.DAT"
        conft.escrever(str(conft_out))

        relido = carregar_caso(conft_out)
        self.assertEqual(conft.numero_usinas, relido.numero_usinas)
        for codigo in conft.lista_usinas():
            original = conft.get(codigo)
            atual = relido.get(codigo)
            for field in CONFT_FIELDS:
                self.assertEqual(atual[field], original[field], field)

    def test_status_com_expansao_ee_ne_sao_preservados(self):
        conft = carregar_caso()
        # 7 CARIOBA e EE; 97 CCBS e NE no deck real
        self.assertEqual(conft.get(7)["status"], "EE")
        self.assertEqual(conft.get(97)["status"], "NE")

        conft_out = self.saida / "CONFT_STATUS.DAT"
        conft.escrever(str(conft_out))
        relido = carregar_caso(conft_out)
        self.assertEqual(relido.get(7)["status"], "EE")
        self.assertEqual(relido.get(97)["status"], "NE")

    def test_put_seguido_de_escrita_e_releitura(self):
        conft = carregar_caso()
        usina = deepcopy(conft.get(1))
        usina["status"] = "nc"
        usina["codigo_tecnologia"] = 5
        usina["codigo_classe_gas"] = 12
        self.assertEqual(conft.put(usina), "sucesso")

        conft_out = self.saida / "CONFT_PUT.DAT"
        conft.escrever(str(conft_out))
        relido = carregar_caso(conft_out)
        atualizado = relido.get(1)

        self.assertEqual(atualizado["status"], "NC")
        self.assertEqual(atualizado["codigo_tecnologia"], 5)
        self.assertEqual(atualizado["codigo_classe_gas"], 12)

    def test_campos_opcionais_em_branco_continuam_em_branco_apos_escrita(self):
        conft = carregar_caso()
        conft_out = self.saida / "CONFT_BRANCO.DAT"
        conft.escrever(str(conft_out))
        relido = carregar_caso(conft_out)
        usina = relido.get(1)
        self.assertIsNone(usina["codigo_tecnologia"])
        self.assertIsNone(usina["codigo_classe_gas"])

    def test_codigo_usina_original_impede_troca_de_identidade(self):
        conft = carregar_caso()
        usina = deepcopy(conft.get(1))
        outra_antes = conft.get(7)
        usina["codigo_usina"] = 7

        with self.assertRaisesRegex(ValueError, "codigo_usina"):
            conft.put(usina)

        outra_depois = conft.get(7)
        for field in CONFT_FIELDS:
            self.assertEqual(outra_depois[field], outra_antes[field])

    def test_put_exige_dicionario_completo_e_rejeita_chave_desconhecida(self):
        conft = carregar_caso()
        incompleto = conft.get(1)
        del incompleto["status"]
        with self.assertRaisesRegex(KeyError, "status"):
            conft.put(incompleto)

        desconhecido = conft.get(1)
        desconhecido["campo_inexistente"] = 1
        with self.assertRaisesRegex(KeyError, "campo_inexistente"):
            conft.put(desconhecido)

    def test_validacoes_dos_campos(self):
        casos = (
            ("nome_usina", "NOME MUITO GRANDE DEMAIS", ValueError),
            ("status", "XX", ValueError),
            ("codigo_submercado", -1, ValueError),
            ("codigo_tecnologia", "cinco", TypeError),
        )
        for field, value, error in casos:
            with self.subTest(field=field):
                conft = carregar_caso()
                usina = conft.get(1)
                usina[field] = value
                with self.assertRaises(error):
                    conft.put(usina)

    def test_escrever_rejeita_estado_invalido_antes_de_criar_arquivo(self):
        conft = carregar_caso()
        conft._status["valor"][0] = "XX"
        conft_out = self.saida / "CONFT_INVALIDO.DAT"

        with self.assertRaisesRegex(ValueError, "status"):
            conft.escrever(str(conft_out))

        self.assertFalse(conft_out.exists())


if __name__ == "__main__":
    unittest.main()
