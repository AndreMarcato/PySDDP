from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PySDDP.newave.script.manutt import Manutt
from PySDDP.newave.script.expt import Expt


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"

MANUTT_FIELDS = (
    "codigo_usina",
    "dia_inicio",
    "mes_inicio",
    "ano_inicio",
    "duracao",
    "potencia",
)

EXPT_FIELDS = (
    "codigo_usina",
    "tipo_modificacao",
    "novo_valor",
    "mes_inicio",
    "ano_inicio",
    "mes_fim",
    "ano_fim",
    "comentario",
)


def carregar_manutt(manutt_path=None):
    manutt = Manutt()
    manutt.ler(str(manutt_path or PMO / "MANUTT.DAT"))
    return manutt


def carregar_expt(expt_path=None):
    expt = Expt()
    expt.ler(str(expt_path or PMO / "EXPT.DAT"))
    return expt


class TestManuttLeitura(unittest.TestCase):
    def test_le_pelo_menos_dois_registros(self):
        manutt = carregar_manutt()
        self.assertGreaterEqual(manutt.numero_manutencoes, 2)

    def test_le_os_seis_campos_do_primeiro_registro(self):
        manutt = carregar_manutt()
        primeiro = manutt.get(0)
        self.assertEqual(
            {field: primeiro[field] for field in MANUTT_FIELDS},
            {
                "codigo_usina": 1,
                "dia_inicio": 10,
                "mes_inicio": 10,
                "ano_inicio": 2018,
                "duracao": 36,
                "potencia": 640.00,
            },
        )

    def test_tipos_python_dos_campos(self):
        manutt = carregar_manutt()
        registro = manutt.get(0)
        self.assertIsInstance(registro["codigo_usina"], int)
        self.assertIsInstance(registro["dia_inicio"], int)
        self.assertIsInstance(registro["mes_inicio"], int)
        self.assertIsInstance(registro["ano_inicio"], int)
        self.assertIsInstance(registro["duracao"], int)
        self.assertIsInstance(registro["potencia"], float)

    def test_segundo_registro_usina_diferente(self):
        manutt = carregar_manutt()
        segundo = manutt.get(1)
        self.assertEqual(segundo["codigo_usina"], 13)
        self.assertEqual(segundo["dia_inicio"], 17)
        self.assertEqual(segundo["mes_inicio"], 2)
        self.assertEqual(segundo["ano_inicio"], 2018)
        self.assertEqual(segundo["duracao"], 32)
        self.assertEqual(segundo["potencia"], 1350.00)


class TestExptLeitura(unittest.TestCase):
    def test_le_pelo_menos_dois_registros(self):
        expt = carregar_expt()
        self.assertGreaterEqual(expt.numero_expansoes, 2)

    def test_le_os_sete_campos_tipo_potef(self):
        expt = carregar_expt()
        primeiro = expt.get(0)
        self.assertEqual(
            {field: primeiro[field] for field in EXPT_FIELDS},
            {
                "codigo_usina": 7,
                "tipo_modificacao": "POTEF",
                "novo_valor": 36.00,
                "mes_inicio": 1,
                "ano_inicio": 2018,
                "mes_fim": None,
                "ano_fim": None,
                "comentario": "CARIOBA",
            },
        )

    def test_le_tipo_distinto_fcmax(self):
        expt = carregar_expt()
        segundo = expt.get(1)
        self.assertEqual(segundo["tipo_modificacao"], "FCMAX")
        self.assertEqual(segundo["codigo_usina"], 7)
        self.assertEqual(segundo["novo_valor"], 0.0)
        # registro sem comentario no deck real
        self.assertEqual(segundo["comentario"], "")

    def test_le_registro_com_mes_fim_e_ano_fim_preenchidos(self):
        expt = carregar_expt()
        # codigo 219, POTEF, com vigencia mes_fim/ano_fim preenchidos
        encontrado = None
        for indice in expt.lista_expansoes():
            registro = expt.get(indice)
            if registro["codigo_usina"] == 219 and registro["tipo_modificacao"] == "POTEF":
                encontrado = registro
                break
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado["mes_fim"], 12)
        self.assertEqual(encontrado["ano_fim"], 2019)

    def test_todos_os_cinco_tipos_de_modificacao_sao_lidos(self):
        expt = carregar_expt()
        tipos = {expt.get(i)["tipo_modificacao"] for i in expt.lista_expansoes()}
        self.assertEqual(
            tipos, {"GTMIN", "POTEF", "FCMAX", "IPTER", "TEIFT"}
        )

    def test_tipos_python_dos_campos(self):
        expt = carregar_expt()
        registro = expt.get(0)
        self.assertIsInstance(registro["codigo_usina"], int)
        self.assertIsInstance(registro["tipo_modificacao"], str)
        self.assertIsInstance(registro["novo_valor"], float)
        self.assertIsInstance(registro["mes_inicio"], int)
        self.assertIsInstance(registro["ano_inicio"], int)
        self.assertIsNone(registro["mes_fim"])
        self.assertIsNone(registro["ano_fim"])
        self.assertIsInstance(registro["comentario"], str)

    def test_le_comentario_com_12_caracteres_sem_truncar(self):
        expt = carregar_expt()
        encontrado = None
        for indice in expt.lista_expansoes():
            registro = expt.get(indice)
            if registro["comentario"] == "DO ATLAN_CSA":
                encontrado = registro
                break
        self.assertIsNotNone(encontrado)
        self.assertEqual(len(encontrado["comentario"]), 12)


class TestManuttRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def test_round_trip_sem_edicao_e_byte_a_byte(self):
        manutt = carregar_manutt()
        manutt_out = self.saida / "MANUTT.DAT"
        manutt.escrever(str(manutt_out))

        original = (PMO / "MANUTT.DAT").read_bytes()
        gerado = manutt_out.read_bytes()
        self.assertEqual(gerado, original)

    def test_round_trip_preserva_todos_os_campos(self):
        manutt = carregar_manutt()
        manutt_out = self.saida / "MANUTT2.DAT"
        manutt.escrever(str(manutt_out))

        relido = carregar_manutt(manutt_out)
        self.assertEqual(manutt.numero_manutencoes, relido.numero_manutencoes)
        for indice in manutt.lista_manutencoes():
            original = manutt.get(indice)
            atual = relido.get(indice)
            for field in MANUTT_FIELDS:
                self.assertEqual(atual[field], original[field], field)

    def test_put_seguido_de_escrita_e_releitura(self):
        manutt = carregar_manutt()
        registro = deepcopy(manutt.get(0))
        registro["potencia"] = 123.45
        registro["duracao"] = 7
        self.assertEqual(manutt.put(registro), "sucesso")

        manutt_out = self.saida / "MANUTT_PUT.DAT"
        manutt.escrever(str(manutt_out))
        relido = carregar_manutt(manutt_out)
        atualizado = relido.get(0)

        self.assertEqual(atualizado["potencia"], 123.45)
        self.assertEqual(atualizado["duracao"], 7)
        # campos nao alterados continuam iguais
        self.assertEqual(atualizado["codigo_usina"], 1)
        self.assertEqual(atualizado["dia_inicio"], 10)

    def test_indice_original_impede_troca_de_identidade_por_posicao_invalida(self):
        manutt = carregar_manutt()
        registro = deepcopy(manutt.get(0))
        registro["indice_original"] = manutt.numero_manutencoes + 10

        with self.assertRaises(ValueError):
            manutt.put(registro)

    def test_put_exige_dicionario_completo_e_rejeita_chave_desconhecida(self):
        manutt = carregar_manutt()
        incompleto = manutt.get(0)
        del incompleto["duracao"]
        with self.assertRaisesRegex(KeyError, "duracao"):
            manutt.put(incompleto)

        desconhecido = manutt.get(0)
        desconhecido["campo_inexistente"] = 1
        with self.assertRaisesRegex(KeyError, "campo_inexistente"):
            manutt.put(desconhecido)

    def test_validacoes_dos_campos(self):
        casos = (
            ("codigo_usina", 0, ValueError),
            ("dia_inicio", 32, ValueError),
            ("mes_inicio", 13, ValueError),
            ("potencia", "muito", TypeError),
        )
        for field, value, error in casos:
            with self.subTest(field=field):
                manutt = carregar_manutt()
                registro = manutt.get(0)
                registro[field] = value
                with self.assertRaises(error):
                    manutt.put(registro)


class TestExptRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def test_round_trip_sem_edicao_e_byte_a_byte(self):
        expt = carregar_expt()
        expt_out = self.saida / "EXPT.DAT"
        expt.escrever(str(expt_out))

        original = (PMO / "EXPT.DAT").read_bytes()
        gerado = expt_out.read_bytes()
        self.assertEqual(gerado, original)

    def test_round_trip_preserva_todos_os_campos(self):
        expt = carregar_expt()
        expt_out = self.saida / "EXPT2.DAT"
        expt.escrever(str(expt_out))

        relido = carregar_expt(expt_out)
        self.assertEqual(expt.numero_expansoes, relido.numero_expansoes)
        for indice in expt.lista_expansoes():
            original = expt.get(indice)
            atual = relido.get(indice)
            for field in EXPT_FIELDS:
                self.assertEqual(atual[field], original[field], field)

    def test_put_seguido_de_escrita_e_releitura_preserva_comentario(self):
        expt = carregar_expt()
        registro = deepcopy(expt.get(0))
        registro["novo_valor"] = 99.99
        self.assertEqual(expt.put(registro), "sucesso")

        expt_out = self.saida / "EXPT_PUT.DAT"
        expt.escrever(str(expt_out))
        relido = carregar_expt(expt_out)
        atualizado = relido.get(0)

        self.assertEqual(atualizado["novo_valor"], 99.99)
        self.assertEqual(atualizado["codigo_usina"], 7)
        self.assertEqual(atualizado["tipo_modificacao"], "POTEF")
        # comentario nao foi alterado no put, deve continuar o mesmo
        self.assertEqual(atualizado["comentario"], "CARIOBA")

    def test_put_altera_comentario_e_preserva_apos_escrita(self):
        expt = carregar_expt()
        registro = deepcopy(expt.get(0))
        registro["comentario"] = "USINA NOVA"
        self.assertEqual(expt.put(registro), "sucesso")

        expt_out = self.saida / "EXPT_COMENTARIO.DAT"
        expt.escrever(str(expt_out))
        relido = carregar_expt(expt_out)
        self.assertEqual(relido.get(0)["comentario"], "USINA NOVA")

    def test_put_remove_comentario(self):
        expt = carregar_expt()
        registro = deepcopy(expt.get(0))
        self.assertEqual(registro["comentario"], "CARIOBA")
        registro["comentario"] = ""
        self.assertEqual(expt.put(registro), "sucesso")

        expt_out = self.saida / "EXPT_SEM_COMENTARIO.DAT"
        expt.escrever(str(expt_out))
        relido = carregar_expt(expt_out)
        self.assertEqual(relido.get(0)["comentario"], "")

    def test_comentario_maior_que_12_caracteres_e_rejeitado(self):
        expt = carregar_expt()
        registro = expt.get(0)
        registro["comentario"] = "NOME MUITO GRANDE DEMAIS"
        with self.assertRaisesRegex(ValueError, "comentario"):
            expt.put(registro)

    def test_put_com_mes_fim_ano_fim_preenchidos(self):
        expt = carregar_expt()
        registro = deepcopy(expt.get(0))
        registro["mes_fim"] = 6
        registro["ano_fim"] = 2019
        self.assertEqual(expt.put(registro), "sucesso")

        expt_out = self.saida / "EXPT_FIM.DAT"
        expt.escrever(str(expt_out))
        relido = carregar_expt(expt_out)
        atualizado = relido.get(0)
        self.assertEqual(atualizado["mes_fim"], 6)
        self.assertEqual(atualizado["ano_fim"], 2019)

    def test_put_exige_dicionario_completo_e_rejeita_chave_desconhecida(self):
        expt = carregar_expt()
        incompleto = expt.get(0)
        del incompleto["novo_valor"]
        with self.assertRaisesRegex(KeyError, "novo_valor"):
            expt.put(incompleto)

        desconhecido = expt.get(0)
        desconhecido["campo_inexistente"] = 1
        with self.assertRaisesRegex(KeyError, "campo_inexistente"):
            expt.put(desconhecido)

    def test_validacoes_dos_campos(self):
        casos = (
            ("tipo_modificacao", "XXXXX", ValueError),
            ("codigo_usina", 0, ValueError),
            ("mes_inicio", 13, ValueError),
            ("novo_valor", "muito", TypeError),
        )
        for field, value, error in casos:
            with self.subTest(field=field):
                expt = carregar_expt()
                registro = expt.get(0)
                registro[field] = value
                with self.assertRaises(error):
                    expt.put(registro)

    def test_mes_fim_e_ano_fim_devem_estar_ambos_preenchidos_ou_ambos_em_branco(self):
        expt = carregar_expt()
        registro = expt.get(0)
        registro["mes_fim"] = 6
        registro["ano_fim"] = None
        with self.assertRaises(ValueError):
            expt.put(registro)


if __name__ == "__main__":
    unittest.main()
