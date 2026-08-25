from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import io
import unittest

import numpy as np
import pandas as pd

from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.sistema import Sistema


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"


def carregar_sistema():
    dger = Dger()
    sistema = Sistema()
    with redirect_stdout(io.StringIO()):
        dger.ler(str(PMO / "DGER.DAT"))
        sistema.ler(str(PMO / "SISTEMA.DAT"), dger)
    return sistema, dger


def reler(sistema, dger, pasta):
    saida = pasta / "SISTEMA.DAT"
    with redirect_stdout(io.StringIO()):
        sistema.escrever(str(saida), dger)
    novo = Sistema()
    with redirect_stdout(io.StringIO()):
        novo.ler(str(saida), dger)
    return novo, saida


def registro_copiado(sistema, codigo):
    registro = sistema.get(codigo)
    registro["cdef"] = list(registro["cdef"])
    registro["prof"] = list(registro["prof"])
    for campo in ("mercado_pre", "mercado_estudo", "mercado_pos"):
        registro[campo] = np.array(registro[campo], copy=True)
    registro["nao_simuladas"] = [
        {
            **nao_sim,
            "geracao": np.array(nao_sim["geracao"], copy=True),
        }
        for nao_sim in registro["nao_simuladas"]
    ]
    return registro


def criar_sistema_com_fontes(pasta, dger, fontes):
    linhas = (PMO / "SISTEMA.DAT").read_text(encoding="latin-1").splitlines()
    inicio = linhas.index(" GERACAO DE USINAS NAO SIMULADAS")
    linhas = linhas[:inicio + 3]

    for fonte in fontes:
        linhas.append(
            f" {fonte['codigo']:3d}  {fonte['bloco']:3d}  "
            f"{fonte['descricao']:20s}  {fonte['tecnologia']:3d}"
        )
        for iano, valores in enumerate(fonte["geracao"]):
            if fonte["precisao"] == 2:
                campos = "".join(f" {valor:7.2f}" for valor in valores)
            else:
                campos = "".join(f" {valor:7.0f}" for valor in valores)
            linhas.append(f"{dger.ano_ini['valor'] + iano}  {campos}")

    linhas.append(" 999")
    entrada = pasta / "SISTEMA_ENTRADA.DAT"
    entrada.write_text("\n".join(linhas) + "\n", encoding="latin-1")
    sistema = Sistema()
    with redirect_stdout(io.StringIO()):
        sistema.ler(str(entrada), dger)
    return sistema


def fonte(codigo, bloco, precisao, primeiros):
    geracao = np.full((5, 12), 90.0)
    geracao[0, :len(primeiros)] = primeiros
    return {
        "codigo": codigo,
        "bloco": bloco,
        "descricao": f"FONTE {bloco}",
        "tecnologia": bloco,
        "precisao": precisao,
        "geracao": geracao,
    }


def primeira_linha_ano(saida, descricao):
    linhas = saida.read_text(encoding="latin-1").splitlines()
    indice = next(i for i, linha in enumerate(linhas) if descricao in linha)
    return linhas[indice + 1]


class TestSistemaPutRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)
        self.sistema, self.dger = carregar_sistema()

    def test_put_nao_escreve_em_array_read_only_do_pandas(self):
        filtro = self.sistema.bloco_mercado["df"]["codigo"] == 1
        valores = self.sistema.bloco_mercado["df"].loc[filtro, "estudo"].values
        if pd.__version__.split(".", 1)[0] == "3":
            self.assertFalse(valores.flags.writeable)

        registro = registro_copiado(self.sistema, 1)
        self.sistema.put(registro)
        np.testing.assert_array_equal(
            self.sistema.get(1)["mercado_estudo"], registro["mercado_estudo"]
        )

    def test_round_trip_de_escalar_mercado_e_geracao_nao_simulada(self):
        registro = registro_copiado(self.sistema, 1)
        registro["nome"] = "SE-EDIT"
        registro["cdef"][0] = 4321.25
        registro["mercado_estudo"][0, 0] = 54321.0
        registro["nao_simuladas"][0]["geracao"][0, 0] = 3456.0

        self.sistema.put(registro)
        relido, _ = reler(self.sistema, self.dger, self.pasta)
        atual = relido.get(1)

        self.assertEqual(atual["nome"].strip(), "SE-EDIT")
        self.assertEqual(atual["cdef"][0], 4321.25)
        self.assertEqual(atual["mercado_estudo"][0, 0], 54321.0)
        self.assertEqual(atual["nao_simuladas"][0]["geracao"][0, 0], 3456.0)

    def test_alteracao_de_um_sistema_preserva_os_demais(self):
        codigos = (2, 3, 4)
        antes = {codigo: registro_copiado(self.sistema, codigo) for codigo in codigos}
        alterado = registro_copiado(self.sistema, 1)
        alterado["mercado_estudo"][2, 5] += 123.0
        self.sistema.put(alterado)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        for codigo in codigos:
            atual = relido.get(codigo)
            esperado = antes[codigo]
            self.assertEqual(atual["nome"], esperado["nome"])
            self.assertEqual(atual["cdef"], esperado["cdef"])
            self.assertEqual(atual["prof"], esperado["prof"])
            np.testing.assert_array_equal(
                atual["mercado_estudo"], esperado["mercado_estudo"]
            )
            np.testing.assert_array_equal(atual["mercado_pos"], esperado["mercado_pos"])

    def test_put_de_estudo_preserva_blocos_pre_e_pos(self):
        self.dger.anos_pre["valor"] = 1
        registro = registro_copiado(self.sistema, 1)
        registro["mercado_pre"][0] = np.arange(100, 112)
        registro["mercado_pos"][0] = np.arange(200, 212)
        self.sistema.put(registro)

        somente_estudo = registro_copiado(self.sistema, 1)
        somente_estudo["mercado_estudo"][1, 1] = 45678.0
        self.sistema.put(somente_estudo)
        relido, _ = reler(self.sistema, self.dger, self.pasta)

        np.testing.assert_array_equal(relido.get(1)["mercado_pre"], registro["mercado_pre"])
        np.testing.assert_array_equal(relido.get(1)["mercado_pos"], registro["mercado_pos"])
        self.assertEqual(relido.get(1)["mercado_estudo"][1, 1], 45678.0)

    def test_mercado_zero_e_escrito_e_formato_f7_0_arredonda(self):
        registro = registro_copiado(self.sistema, 1)
        registro["mercado_estudo"][0, 0] = 0.0
        registro["mercado_estudo"][0, 1] = 1234.6
        self.sistema.put(registro)

        relido, saida = reler(self.sistema, self.dger, self.pasta)
        mercado = relido.get(1)["mercado_estudo"]
        self.assertEqual(mercado[0, 0], 0.0)
        self.assertEqual(mercado[0, 1], 1235.0)

        linhas = saida.read_text(encoding="latin-1").splitlines()
        inicio = linhas.index(" MERCADO DE ENERGIA TOTAL")
        linha_2018 = next(linha for linha in linhas[inicio:] if linha.startswith("2018"))
        self.assertRegex(linha_2018, r"^2018\s+0\.\s+1235\.")

    def test_deficit_e_escrito_para_nao_ficticio_mesmo_com_cdef_1_zero(self):
        registro = registro_copiado(self.sistema, 1)
        registro["cdef"] = [0.0, 2222.25, 333.5, 44.75]
        registro["prof"] = [0.1, 0.2, 0.3, 0.4]
        self.sistema.put(registro)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        self.assertEqual(relido.get(1)["cdef"], registro["cdef"])
        self.assertEqual(relido.get(1)["prof"], registro["prof"])

    def test_put_interc_compativel_com_copy_on_write(self):
        intercambio = self.sistema.get_interc(1, 2)
        intercambio["valor"] = np.array(intercambio["valor"], copy=True)
        intercambio["valor"][0, 0] = 8123.0
        self.sistema.put_interc(intercambio)

        relido, _ = reler(self.sistema, self.dger, self.pasta)
        self.assertEqual(relido.get_interc(1, 2)["valor"][0, 0], 8123.0)


class TestSistemaNaoSimuladasPrecisao(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pasta = Path(self.temp.name)
        _, self.dger = carregar_sistema()

    def test_leitura_e_escrita_f7_0(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 0, [2744, 90])]
        )
        geracao = sistema.get(1)["nao_simuladas"][0]["geracao"]
        self.assertEqual(geracao[0, 0], 2744.0)
        self.assertEqual(geracao[0, 1], 90.0)

        _, saida = reler(sistema, self.dger, self.pasta)
        linha = primeira_linha_ano(saida, "FONTE 1")
        self.assertEqual(linha[7:14], "  2744.")
        self.assertEqual(linha[15:22], "    90.")

    def test_leitura_f7_2(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 2, [0.00, 3.41, 0.02, 565.64])]
        )
        geracao = sistema.get(1)["nao_simuladas"][0]["geracao"]
        np.testing.assert_array_equal(geracao[0, :4], [0.00, 3.41, 0.02, 565.64])

    def test_round_trip_f7_2_preserva_valores_e_formato(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 2, [3.41, 0.02, 565.64])]
        )
        relido, saida = reler(sistema, self.dger, self.pasta)
        geracao = relido.get(1)["nao_simuladas"][0]["geracao"]
        np.testing.assert_array_equal(geracao[0, :3], [3.41, 0.02, 565.64])
        linha = primeira_linha_ano(saida, "FONTE 1")
        self.assertEqual(linha[7:14], "   3.41")
        self.assertEqual(linha[15:22], "   0.02")
        self.assertEqual(linha[23:30], " 565.64")

    def test_zero_decimal_permanece_explicito(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 2, [0.00])]
        )
        _, saida = reler(sistema, self.dger, self.pasta)
        self.assertEqual(primeira_linha_ano(saida, "FONTE 1")[7:14], "   0.00")

    def test_inteiro_em_conjunto_decimal_mantem_duas_casas(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 2, [3.41, 4.00, 5.25])]
        )
        _, saida = reler(sistema, self.dger, self.pasta)
        linha = primeira_linha_ano(saida, "FONTE 1")
        self.assertEqual(linha[15:22], "   4.00")

    def test_f7_0_editado_com_fracao_e_promovido_para_f7_2(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 0, [90])]
        )
        registro = registro_copiado(sistema, 1)
        registro["nao_simuladas"][0]["geracao"][0, 0] = 90.25
        sistema.put(registro)

        relido, saida = reler(sistema, self.dger, self.pasta)
        self.assertEqual(
            relido.get(1)["nao_simuladas"][0]["geracao"][0, 0], 90.25
        )
        self.assertEqual(primeira_linha_ano(saida, "FONTE 1")[7:14], "  90.25")

    def test_fontes_com_precisoes_diferentes(self):
        sistema = criar_sistema_com_fontes(
            self.pasta,
            self.dger,
            [fonte(1, 1, 0, [90]), fonte(1, 2, 2, [3.41])],
        )
        _, saida = reler(sistema, self.dger, self.pasta)
        self.assertEqual(primeira_linha_ano(saida, "FONTE 1")[7:14], "    90.")
        self.assertEqual(primeira_linha_ano(saida, "FONTE 2")[7:14], "   3.41")

    def test_campos_f7_2_permanecem_nas_posicoes_fixas(self):
        sistema = criar_sistema_com_fontes(
            self.pasta, self.dger, [fonte(1, 1, 2, [0.00, 3.41, 565.64])]
        )
        _, saida = reler(sistema, self.dger, self.pasta)
        linha = primeira_linha_ano(saida, "FONTE 1")
        self.assertEqual(linha[:4], str(self.dger.ano_ini["valor"]))
        self.assertEqual(len(linha), 102)
        self.assertTrue(all(linha[6 + 8 * imes] == " " for imes in range(12)))
        self.assertEqual(
            [linha[7 + 8 * imes:14 + 8 * imes] for imes in range(3)],
            ["   0.00", "   3.41", " 565.64"],
        )


if __name__ == "__main__":
    unittest.main()
