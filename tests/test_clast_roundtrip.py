from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PySDDP.newave.script.clast import Clast
from PySDDP.newave.script.dger import Dger


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"

CLASSE_FIELDS = (
    "numero_classe_termica",
    "nome_classe_termica",
    "tipo_combustivel",
    "custos",
)
ALTERACAO_FIELDS = (
    "numero_classe_termica",
    "novo_custo",
    "mes_inicio",
    "ano_inicio",
    "mes_fim",
    "ano_fim",
)


def carregar_dger():
    dger = Dger()
    dger.ler(str(PMO / "DGER.DAT"))
    return dger


def carregar_caso(clast_path=None, dger=None):
    dger = dger or carregar_dger()
    clast = Clast()
    clast.ler(str(clast_path or PMO / "CLAST.DAT"), dger)
    return clast


class TestClastLeitura(unittest.TestCase):
    def test_le_ambos_os_blocos_de_registros(self):
        clast = carregar_caso()
        self.assertEqual(clast.numero_classes, 132)
        self.assertEqual(clast.numero_alteracoes, 25)

    def test_sentinela_9999_nao_aparece_no_cadastro(self):
        clast = carregar_caso()
        self.assertNotIn(9999, clast._numero_classe_termica["valor"])

    def test_le_registro_tipo1_com_custos_de_varios_anos(self):
        clast = carregar_caso()
        angra1 = clast.get(1)
        self.assertEqual(angra1["numero_classe_termica"], 1)
        self.assertEqual(angra1["nome_classe_termica"], "ANGRA 1")
        self.assertEqual(angra1["tipo_combustivel"], "Nuclear")
        self.assertEqual(angra1["custos"], [29.13, 29.13, 29.13, 29.13, 29.13])
        self.assertEqual(len(angra1["custos"]), clast.nanos)

    def test_le_registro_tipo2_com_alteracao_completa(self):
        clast = carregar_caso()
        alteracao = clast.get_alteracao(0)
        self.assertEqual(
            {field: alteracao[field] for field in ALTERACAO_FIELDS},
            {
                "numero_classe_termica": 211,
                "novo_custo": 114.59,
                "mes_inicio": 1,
                "ano_inicio": 2018,
                "mes_fim": 2,
                "ano_fim": 2018,
            },
        )

    def test_get_aceita_codigo_nome_e_float_integral(self):
        clast = carregar_caso()
        self.assertEqual(clast.get(1)["numero_classe_termica"], 1)
        self.assertEqual(clast.get(1.0)["numero_classe_termica"], 1)
        self.assertEqual(clast.get("angra 1")["numero_classe_termica"], 1)
        self.assertIsNone(clast.get(999999))


class TestClastRoundTrip(unittest.TestCase):
    def setUp(self):
        self.dger = carregar_dger()
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.saida = Path(self.temp.name)

    def test_round_trip_sem_edicao_preserva_semantica(self):
        clast = carregar_caso(dger=self.dger)
        clast_out = self.saida / "CLAST.DAT"
        clast.escrever(str(clast_out))

        relido = carregar_caso(clast_out, dger=self.dger)
        self.assertEqual(clast.numero_classes, relido.numero_classes)
        self.assertEqual(clast.numero_alteracoes, relido.numero_alteracoes)

        for codigo in clast.lista_classes():
            original = clast.get(codigo)
            atual = relido.get(codigo)
            for field in CLASSE_FIELDS:
                self.assertEqual(atual[field], original[field], field)

        for i in range(clast.numero_alteracoes):
            original = clast.get_alteracao(i)
            atual = relido.get_alteracao(i)
            for field in ALTERACAO_FIELDS:
                self.assertEqual(atual[field], original[field], field)

    def test_sentinela_reaparece_corretamente_na_escrita(self):
        clast = carregar_caso(dger=self.dger)
        clast_out = self.saida / "CLAST_SENTINELA.DAT"
        clast.escrever(str(clast_out))

        conteudo = clast_out.read_text(encoding="latin-1")
        linhas = [l for l in conteudo.splitlines() if l.strip() == "9999"]
        self.assertEqual(len(linhas), 1)

    def test_put_classe_seguido_de_escrita_e_releitura(self):
        clast = carregar_caso(dger=self.dger)
        classe = deepcopy(clast.get(1))
        classe["custos"] = [10.0, 20.0, 30.0, 40.0, 50.0]
        classe["tipo_combustivel"] = "Gas"
        self.assertEqual(clast.put(classe), "sucesso")

        clast_out = self.saida / "CLAST_PUT.DAT"
        clast.escrever(str(clast_out))
        relido = carregar_caso(clast_out, dger=self.dger)
        atualizado = relido.get(1)

        self.assertEqual(atualizado["custos"], [10.0, 20.0, 30.0, 40.0, 50.0])
        self.assertEqual(atualizado["tipo_combustivel"], "Gas")

    def test_put_alteracao_seguido_de_escrita_e_releitura(self):
        clast = carregar_caso(dger=self.dger)
        alteracao = deepcopy(clast.get_alteracao(0))
        alteracao["novo_custo"] = 555.55
        self.assertEqual(clast.put_alteracao(alteracao), "sucesso")

        clast_out = self.saida / "CLAST_PUT_ALT.DAT"
        clast.escrever(str(clast_out))
        relido = carregar_caso(clast_out, dger=self.dger)

        self.assertEqual(relido.get_alteracao(0)["novo_custo"], 555.55)

    def test_alteracao_sem_mes_ano_fim_permanece_valida_ate_fim_do_horizonte(self):
        clast = carregar_caso(dger=self.dger)
        alteracao = deepcopy(clast.get_alteracao(0))
        alteracao["mes_fim"] = None
        alteracao["ano_fim"] = None
        self.assertEqual(clast.put_alteracao(alteracao), "sucesso")

        clast_out = self.saida / "CLAST_SEM_FIM.DAT"
        clast.escrever(str(clast_out))
        relido = carregar_caso(clast_out, dger=self.dger)

        atualizada = relido.get_alteracao(0)
        self.assertIsNotNone(atualizada["mes_inicio"])
        self.assertIsNotNone(atualizada["ano_inicio"])
        self.assertIsNone(atualizada["mes_fim"])
        self.assertIsNone(atualizada["ano_fim"])

    def test_alteracao_so_com_novo_custo_vale_apenas_primeiro_mes(self):
        clast = carregar_caso(dger=self.dger)
        alteracao = deepcopy(clast.get_alteracao(0))
        alteracao["mes_inicio"] = None
        alteracao["ano_inicio"] = None
        alteracao["mes_fim"] = None
        alteracao["ano_fim"] = None
        self.assertEqual(clast.put_alteracao(alteracao), "sucesso")

        clast_out = self.saida / "CLAST_SO_CUSTO.DAT"
        clast.escrever(str(clast_out))
        relido = carregar_caso(clast_out, dger=self.dger)

        atualizada = relido.get_alteracao(0)
        for field in ("mes_inicio", "ano_inicio", "mes_fim", "ano_fim"):
            self.assertIsNone(atualizada[field])

    def test_numero_classe_termica_original_impede_troca_de_identidade(self):
        clast = carregar_caso(dger=self.dger)
        classe = deepcopy(clast.get(1))
        outra_antes = clast.get(13)
        classe["numero_classe_termica"] = 13

        with self.assertRaisesRegex(ValueError, "numero_classe_termica"):
            clast.put(classe)

        outra_depois = clast.get(13)
        for field in CLASSE_FIELDS:
            self.assertEqual(outra_depois[field], outra_antes[field])

    def test_get_alteracao_indice_fora_do_intervalo_retorna_erro(self):
        clast = carregar_caso(dger=self.dger)
        with self.assertRaises(ValueError):
            clast.get_alteracao(clast.numero_alteracoes)
        with self.assertRaises(ValueError):
            clast.get_alteracao(-1)

    def test_put_alteracao_rejeita_chave_desconhecida_ou_ausente(self):
        clast = carregar_caso(dger=self.dger)
        incompleta = clast.get_alteracao(0)
        del incompleta["novo_custo"]
        with self.assertRaisesRegex(KeyError, "novo_custo"):
            clast.put_alteracao(incompleta)

        desconhecida = clast.get_alteracao(0)
        desconhecida["campo_inexistente"] = 1
        with self.assertRaisesRegex(KeyError, "campo_inexistente"):
            clast.put_alteracao(desconhecida)

    def test_put_classe_rejeita_quantidade_errada_de_custos(self):
        clast = carregar_caso(dger=self.dger)
        classe = clast.get(1)
        classe["custos"] = [1.0, 2.0]
        with self.assertRaises(ValueError):
            clast.put(classe)

    def test_escrever_rejeita_estado_invalido_antes_de_criar_arquivo(self):
        clast = carregar_caso(dger=self.dger)
        clast._nome_classe_termica["valor"][0] = "NOME MUITO GRANDE DEMAIS"
        clast_out = self.saida / "CLAST_INVALIDO.DAT"

        with self.assertRaises(ValueError):
            clast.escrever(str(clast_out))

        self.assertFalse(clast_out.exists())


if __name__ == "__main__":
    unittest.main()
