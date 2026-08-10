from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from PySDDP.newave.script.conft import Conft
from PySDDP.newave.script.dger import Dger
from PySDDP.newave.script.term import Term
from PySDDP.newave.script.expt import Expt
from PySDDP.newave.script.manutt import Manutt


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


def _carregar_dger_term_expt_manutt():
    dger = Dger()
    dger.ler(str(PMO / "DGER.DAT"))
    term = Term()
    term.ler(str(PMO / "TERM.DAT"))
    expt = Expt()
    expt.ler(str(PMO / "EXPT.DAT"))
    manutt = Manutt()
    manutt.ler(str(PMO / "MANUTT.DAT"))
    return dger, term, expt, manutt


def carregar_caso(conft_path=None, dger=None, term=None, expt=None, manutt=None):
    if dger is None or term is None or expt is None or manutt is None:
        dger, term, expt, manutt = _carregar_dger_term_expt_manutt()
    conft = Conft()
    conft.ler(str(conft_path or PMO / "CONFT.DAT"), dger, term, expt, manutt)
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


TEMPO_FIELDS = ("gtmin_tempo", "pot_tempo", "fcmax_tempo", "ip_tempo", "teif_tempo")


class TestConftTempoArrays(unittest.TestCase):
    """
    Testa as matrizes de evolucao temporal (nanos x 12) construidas por
    Conft._acerta_expt a partir do cadastro de Term e das modificacoes
    temporais de Expt, a exemplo de Confhd.engol_tempo.
    """

    def test_formato_e_tipo_das_matrizes(self):
        conft = carregar_caso()
        usina = conft.get(1)
        for field in TEMPO_FIELDS:
            self.assertEqual(usina[field].shape, (conft.nanos, 12), field)

    def test_usina_sem_modificacao_reflete_apenas_o_cadastro_term(self):
        dger, term, expt, manutt = _carregar_dger_term_expt_manutt()
        expt_codigos = {expt._codigo_usina["valor"][i] for i in range(expt.numero_expansoes)}
        manutt_codigos = {manutt._codigo_usina["valor"][i] for i in range(manutt.numero_manutencoes)}

        conft = carregar_caso(dger=dger, term=term, expt=expt, manutt=manutt)

        # usina sem nenhuma modificacao em EXPT.DAT nem manutencao em MANUTT.DAT
        codigo = next(
            c for c in conft.lista_usinas()
            if c not in expt_codigos and c not in manutt_codigos
        )
        usina = conft.get(codigo)
        i_term = term._codigo["valor"].index(codigo)

        gtmin_cadastro = term._gtmin["valor"][i_term]
        # dtype 'f' (float32), a exemplo de engol_tempo, entao comparamos com tolerancia
        self.assertTrue(
            (abs(usina["gtmin_tempo"][0] - gtmin_cadastro[0:12]) < 1e-2).all()
        )
        for iano in range(1, conft.nanos):
            self.assertTrue(
                (abs(usina["gtmin_tempo"][iano] - gtmin_cadastro[12]) < 1e-2).all()
            )

        self.assertTrue((usina["pot_tempo"] == term._pot["valor"][i_term]).all())
        self.assertTrue((usina["fcmax_tempo"] == term._fcmax["valor"][i_term]).all())
        self.assertTrue((usina["ip_tempo"] == term._ip["valor"][i_term]).all())
        self.assertTrue((usina["teif_tempo"] == term._teif["valor"][i_term]).all())

    def test_gtmin_tempo_usina_219_estende_padrao_para_segundo_ano(self):
        # codigo 219 (CCBS_L1): as modificacoes GTMIN do EXPT.DAT cobrem
        # jan/2018 a dez/2019 repetindo o padrao mensal do cadastro Term,
        # em vez do valor "D+ anos" (15.72) que valeria sem a modificacao
        conft = carregar_caso()
        usina = conft.get(219)
        esperado_ano0 = [62.87, 62.87, 38.62, 29.92, 62.87, 62.87,
                          62.87, 62.87, 62.87, 62.87, 62.87, 62.87]
        self.assertTrue(
            (abs(usina["gtmin_tempo"][0] - esperado_ano0) < 1e-3).all()
        )
        # ano_ini=2018, logo indice 1 = 2019
        self.assertTrue(
            (abs(usina["gtmin_tempo"][1] - 62.87) < 1e-3).all()
        )

    def test_pot_e_gtmin_tempo_usina_97_aplicados_a_partir_de_2020(self):
        # codigo 97 (CCBS): cadastro Term e zero; POTEF=216.00 e GTMIN=86.40
        # passam a valer a partir de jan/2020 (sem mes_fim/ano_fim, ou
        # seja, ate o fim do horizonte)
        conft = carregar_caso()
        usina = conft.get(97)

        # ano_ini=2018 -> indices 0 e 1 sao 2018 e 2019 (antes da modificacao)
        for iano in (0, 1):
            self.assertTrue((usina["pot_tempo"][iano] == 0.0).all())
            self.assertTrue((usina["gtmin_tempo"][iano] == 0.0).all())

        # indices 2..nanos-1 sao 2020 em diante (modificacao em vigor)
        for iano in range(2, conft.nanos):
            self.assertTrue((usina["pot_tempo"][iano] == 216.0).all())
            self.assertTrue((usina["gtmin_tempo"][iano] == 86.4).all())

    def test_fcmax_tempo_usina_7_modificacao_desde_o_inicio_do_horizonte(self):
        # codigo 7 (CARIOBA): cadastro Term tem fcmax=100, mas o EXPT.DAT
        # define FCMAX=0.00 a partir de jan/2018 (inicio do horizonte),
        # entao toda a matriz passa a ser 0.00
        conft = carregar_caso()
        usina = conft.get(7)
        self.assertTrue((usina["fcmax_tempo"] == 0.0).all())

    def test_put_preserva_matrizes_tempo_nao_alteradas(self):
        conft = carregar_caso()
        usina = deepcopy(conft.get(219))
        usina["status"] = "ex"
        self.assertEqual(conft.put(usina), "sucesso")

        atualizado = conft.get(219)
        self.assertTrue(
            (atualizado["gtmin_tempo"] == usina["gtmin_tempo"]).all()
        )

    def test_pot_tempo_usina_1_abatido_pela_manutencao_programada(self):
        # codigo 1 (ANGRA 1): MANUTT.DAT tem um evento com
        # dia_inicio=10, mes_inicio=10, ano_inicio=2018, duracao=36,
        # potencia=640.00 -> cobre 10/out/2018 a 14/nov/2018
        # (22 dias em outubro, 14 dias em novembro), sem nenhuma
        # modificacao POTEF em EXPT.DAT (cadastro Term=640 MW)
        conft = carregar_caso()
        usina = conft.get(1)

        base = 640.0
        esperado_out = base - (22 / 31) * base
        esperado_nov = base - (14 / 30) * base

        # ano_ini=2018 -> indice 0; outubro=indice9, novembro=indice10 (0-based)
        self.assertAlmostEqual(usina["pot_tempo"][0][9], esperado_out, places=2)
        self.assertAlmostEqual(usina["pot_tempo"][0][10], esperado_nov, places=2)

        # meses nao tocados pela manutencao permanecem no valor de cadastro
        for imes in range(9):
            self.assertAlmostEqual(usina["pot_tempo"][0][imes], base, places=2)
        self.assertAlmostEqual(usina["pot_tempo"][0][11], base, places=2)
        for iano in range(1, conft.nanos):
            self.assertTrue((abs(usina["pot_tempo"][iano] - base) < 1e-2).all())


class TestAbateManutt(unittest.TestCase):
    """Testes unitarios de Conft._abate_manutt (rateio de dias por mes)."""

    def _matriz(self, nanos=3, base=640.0):
        return base * np.ones((nanos, 12), "f")

    def test_manutencao_dentro_de_um_unico_mes(self):
        matriz = self._matriz()
        registro = {
            "dia_inicio": 5, "mes_inicio": 6, "ano_inicio": 2018,
            "duracao": 10, "potencia": 100.0,
        }
        Conft._abate_manutt(matriz, registro, ano_ini_estudo=2018, nanos=3)
        # junho tem 30 dias; dias 5-14 = 10 dias sobrepostos
        self.assertAlmostEqual(float(matriz[0][5]), 640.0 - (10 / 30) * 100.0, places=3)
        # demais meses inalterados
        self.assertTrue((matriz[0][:5] == 640.0).all())
        self.assertTrue((matriz[0][6:] == 640.0).all())

    def test_manutencao_estende_para_o_exemplo_do_usuario(self):
        # Exemplo ilustrativo: inicio 05/09/2026, duracao 65 dias corridos
        # (05/set a 08/nov/2026, inclusive): 26 dias em setembro
        # (30 - 5 + 1), 31 dias em outubro (mes inteiro) e 8 dias em
        # novembro (65 - 26 - 31), pelo calendario padrao (dia_inicio
        # contado como o 1o dia da manutencao).
        matriz = self._matriz(nanos=1, base=640.0)
        registro = {
            "dia_inicio": 5, "mes_inicio": 9, "ano_inicio": 2026,
            "duracao": 65, "potencia": 640.0,
        }
        Conft._abate_manutt(matriz, registro, ano_ini_estudo=2026, nanos=1)
        self.assertAlmostEqual(float(matriz[0][8]), 640.0 - (26 / 30) * 640.0, places=2)  # set
        self.assertAlmostEqual(float(matriz[0][9]), 640.0 - (31 / 31) * 640.0, places=2)  # out
        self.assertAlmostEqual(float(matriz[0][10]), 640.0 - (8 / 30) * 640.0, places=2)  # nov

    def test_eventos_de_manutencao_sao_cumulativos(self):
        # duas manutencoes da mesma usina no mesmo mes abatem em conjunto
        matriz = self._matriz(nanos=1, base=640.0)
        r1 = {"dia_inicio": 1, "mes_inicio": 3, "ano_inicio": 2018, "duracao": 10, "potencia": 100.0}
        r2 = {"dia_inicio": 11, "mes_inicio": 3, "ano_inicio": 2018, "duracao": 10, "potencia": 50.0}
        Conft._abate_manutt(matriz, r1, ano_ini_estudo=2018, nanos=1)
        Conft._abate_manutt(matriz, r2, ano_ini_estudo=2018, nanos=1)
        esperado = 640.0 - (10 / 31) * 100.0 - (10 / 31) * 50.0
        self.assertAlmostEqual(float(matriz[0][2]), esperado, places=3)

    def test_manutencao_fora_do_horizonte_e_ignorada(self):
        matriz = self._matriz(nanos=2, base=640.0)
        registro = {
            "dia_inicio": 1, "mes_inicio": 1, "ano_inicio": 2010,
            "duracao": 30, "potencia": 100.0,
        }
        Conft._abate_manutt(matriz, registro, ano_ini_estudo=2018, nanos=2)
        self.assertTrue((matriz == 640.0).all())


class TestAplicaJanelaExpt(unittest.TestCase):
    """Testes unitarios de Conft._aplica_janela_expt (clamping de janela)."""

    class _DgerFake:
        def __init__(self, ano_ini):
            self.ano_ini = {"valor": ano_ini}

    def _matriz(self, nanos=5, base=1.0):
        import numpy as np
        return base * np.ones((nanos, 12), "f")

    def test_janela_totalmente_dentro_do_horizonte(self):
        matriz = self._matriz(nanos=5)
        registro = {
            "novo_valor": 9.0, "mes_inicio": 3, "ano_inicio": 2019,
            "mes_fim": 6, "ano_fim": 2019,
        }
        Conft._aplica_janela_expt(matriz, registro, self._DgerFake(2018))
        self.assertTrue((matriz[1, 2:6] == 9.0).all())
        self.assertTrue((matriz[1, :2] == 1.0).all())
        self.assertTrue((matriz[1, 6:] == 1.0).all())
        self.assertTrue((matriz[0] == 1.0).all())
        self.assertTrue((matriz[2:] == 1.0).all())

    def test_janela_sem_fim_vale_ate_o_horizonte(self):
        matriz = self._matriz(nanos=3)
        registro = {
            "novo_valor": 9.0, "mes_inicio": 6, "ano_inicio": 2019,
            "mes_fim": None, "ano_fim": None,
        }
        Conft._aplica_janela_expt(matriz, registro, self._DgerFake(2018))
        self.assertTrue((matriz[1, 5:] == 9.0).all())
        self.assertTrue((matriz[1, :5] == 1.0).all())
        self.assertTrue((matriz[2] == 9.0).all())
        self.assertTrue((matriz[0] == 1.0).all())

    def test_janela_iniciada_antes_do_horizonte_e_recortada(self):
        matriz = self._matriz(nanos=3)
        registro = {
            "novo_valor": 9.0, "mes_inicio": 6, "ano_inicio": 2016,
            "mes_fim": 3, "ano_fim": 2018,
        }
        Conft._aplica_janela_expt(matriz, registro, self._DgerFake(2018))
        self.assertTrue((matriz[0, :3] == 9.0).all())
        self.assertTrue((matriz[0, 3:] == 1.0).all())

    def test_janela_totalmente_antes_do_horizonte_e_ignorada(self):
        matriz = self._matriz(nanos=3)
        registro = {
            "novo_valor": 9.0, "mes_inicio": 1, "ano_inicio": 2010,
            "mes_fim": 12, "ano_fim": 2016,
        }
        Conft._aplica_janela_expt(matriz, registro, self._DgerFake(2018))
        self.assertTrue((matriz == 1.0).all())

    def test_janela_totalmente_apos_o_horizonte_e_ignorada(self):
        matriz = self._matriz(nanos=3)
        registro = {
            "novo_valor": 9.0, "mes_inicio": 1, "ano_inicio": 2025,
            "mes_fim": 12, "ano_fim": 2030,
        }
        Conft._aplica_janela_expt(matriz, registro, self._DgerFake(2018))
        self.assertTrue((matriz == 1.0).all())


class TestMesiEstZeroing(unittest.TestCase):
    def test_meses_antes_do_mes_inicial_de_estudo_ficam_zerados(self):
        dger, term, expt, manutt = _carregar_dger_term_expt_manutt()
        dger.mesi_est["valor"] = 4  # estudo comeca em abril

        conft = carregar_caso(dger=dger, term=term, expt=expt, manutt=manutt)

        # codigo 1 (ANGRA 1): cadastro Term nao-nulo em todos os campos
        usina = conft.get(1)

        for field in TEMPO_FIELDS:
            self.assertTrue((usina[field][0, :3] == 0.0).all(), field)
            self.assertFalse((usina[field][0, 3:] == 0.0).all(), field)
            # anos seguintes nao sao afetados pelo mes inicial de estudo
            self.assertFalse((usina[field][1, :3] == 0.0).all(), field)


if __name__ == "__main__":
    unittest.main()
