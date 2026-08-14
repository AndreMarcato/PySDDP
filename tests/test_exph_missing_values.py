from pathlib import Path
from tempfile import TemporaryDirectory
from types import MethodType, SimpleNamespace
import shutil
import unittest

import numpy as np
import pandas as pd

from PySDDP.Pen import Newave
from PySDDP.newave.script.confhd import Confhd
from PySDDP.newave.script.exph import Exph


ROOT = Path(__file__).resolve().parents[1]
PMO = ROOT / "PySDDP" / "pmo"
FIELDS = tuple(Exph._FIELD_MAP)


def volume_record(missing=None):
    return {
        "codigo": 101,
        "nome": "USINA TESTE ",
        "mesi_evm": 1,
        "anoi_evm": 2020,
        "dura_evm": 2,
        "perc_evm": 0.0,
        "mesi_tur": missing,
        "anoi_tur": missing,
        "comentar": missing,
        "nume_tur": missing,
        "nume_cnj": missing,
    }


def turbine_record(machine=1, missing=None):
    return {
        "codigo": 101,
        "nome": "USINA TESTE ",
        "mesi_evm": missing,
        "anoi_evm": missing,
        "dura_evm": missing,
        "perc_evm": missing,
        "mesi_tur": 3,
        "anoi_tur": 2020,
        "comentar": "50.0",
        "nume_tur": machine,
        "nume_cnj": 1,
    }


def exph_from_records(records):
    exph = Exph()
    exph.nome_arquivo = "EXPH.DAT"
    exph.bloco_usina["df"] = pd.DataFrame(records, columns=FIELDS)
    return exph


def assert_semantically_equal(test_case, expected, actual):
    test_case.assertEqual(len(expected), len(actual))
    for row_index, expected_row in expected.reset_index(drop=True).iterrows():
        actual_row = actual.iloc[row_index]
        for field in FIELDS:
            expected_value = expected_row[field]
            actual_value = actual_row[field]
            if pd.isna(expected_value):
                test_case.assertTrue(pd.isna(actual_value), field)
            elif field in ("nome", "comentar"):
                test_case.assertEqual(
                    str(actual_value).strip(), str(expected_value).strip(), field
                )
            else:
                test_case.assertEqual(actual_value, expected_value, field)


class TestExphMissingValues(unittest.TestCase):
    def test_writer_e_round_trip_dos_grupos_presentes_e_ausentes(self):
        scenarios = {
            "tipos_1_e_2": [volume_record(), turbine_record()],
            "somente_tipo_1": [volume_record()],
            "somente_tipo_2": [turbine_record(), turbine_record(machine=2)],
        }
        missing_values = {
            "None": None,
            "numpy.nan": np.nan,
            "pandas.NA": pd.NA,
        }

        with TemporaryDirectory() as temp_dir:
            for scenario, base_records in scenarios.items():
                for missing_name, missing in missing_values.items():
                    with self.subTest(
                        scenario=scenario, missing_value=missing_name
                    ):
                        records = []
                        for base in base_records:
                            if pd.isna(base["mesi_evm"]):
                                records.append(turbine_record(base["nume_tur"], missing))
                            else:
                                records.append(volume_record(missing))

                        exph = exph_from_records(records)
                        output = Path(temp_dir) / (
                            scenario + "_" + missing_name.replace(".", "_") + ".DAT"
                        )
                        exph.escrever(str(output))

                        text = output.read_text(encoding="latin-1")
                        self.assertNotIn("None", text)
                        self.assertNotIn("<NA>", text)
                        self.assertNotIn("nan", text.lower())

                        reloaded = Exph()
                        reloaded.ler(str(output))
                        assert_semantically_equal(
                            self, exph.bloco_usina["df"], reloaded.bloco_usina["df"]
                        )

    def test_put_normaliza_none_nan_e_pd_na_sem_mudar_contrato(self):
        for missing in (None, np.nan, pd.NA):
            with self.subTest(missing=repr(missing)):
                exph = exph_from_records([volume_record()])
                for field, (attribute, value_name) in exph._FIELD_MAP.items():
                    getattr(exph, attribute)[value_name] = list(
                        exph.bloco_usina["df"][field]
                    )

                record = exph.get(0)
                for field in exph._GRUPO_TURBINAMENTO:
                    record[field] = missing
                self.assertEqual(exph.put(record), "sucesso")
                for field in exph._GRUPO_TURBINAMENTO:
                    self.assertIsNone(exph.get(0)[field])


class TestConfhdMissingExphGroups(unittest.TestCase):
    @staticmethod
    def configured_confhd():
        confhd = Confhd()
        for attribute, value in (
            ("_vol_min", 100.0),
            ("_unid_base", 2),
            ("_maq_por_conj", [0]),
            ("_pef_por_conj", [0.0]),
            ("_pot_efet", 0.0),
            ("_engolimento", 0.0),
            ("_status_vol_morto", np.zeros((1, 12), dtype=int)),
            ("_status_motoriz", np.zeros((1, 12), dtype=int)),
            ("_vol_morto_tempo", np.zeros((1, 12), dtype=float)),
            ("_potencia_tempo", np.zeros((1, 12), dtype=float)),
            ("_unidades_tempo", np.zeros((1, 12), dtype=float)),
            ("_engol_tempo", np.zeros((1, 12), dtype=float)),
        ):
            getattr(confhd, attribute)["valor"].append(value)

        def calc_power(self):
            self._pot_efet["valor"][-1] = 50.0

        def calc_flow(self):
            self._engolimento["valor"][-1] = 25.0

        confhd._calc_pot_efetiva = MethodType(calc_power, confhd)
        confhd._calc_engol_maximo = MethodType(calc_flow, confhd)
        return confhd

    def test_recalculo_sem_tipo_1_sem_tipo_2_e_normal(self):
        dger = SimpleNamespace(
            ano_ini={"valor": 2020}, num_anos={"valor": 1}
        )

        for missing in (None, np.nan, pd.NA):
            scenarios = {
                "sem_tipo_1": [turbine_record(missing=missing)],
                "sem_tipo_2": [volume_record(missing=missing)],
                "normal": [
                    volume_record(missing=missing),
                    turbine_record(missing=missing),
                ],
            }
            for scenario, records in scenarios.items():
                with self.subTest(scenario=scenario, missing=repr(missing)):
                    confhd = self.configured_confhd()
                    frame = pd.DataFrame(records, columns=FIELDS)
                    confhd._acerta_exph(frame, dger)

                    volume = confhd._vol_morto_tempo["valor"][-1]
                    power = confhd._potencia_tempo["valor"][-1]
                    units = confhd._unidades_tempo["valor"][-1]
                    flow = confhd._engol_tempo["valor"][-1]

                    if scenario == "sem_tipo_1":
                        np.testing.assert_array_equal(volume, np.zeros((1, 12)))
                        np.testing.assert_array_equal(
                            confhd._status_vol_morto["valor"][-1],
                            2 * np.ones((1, 12), dtype=int),
                        )
                    else:
                        self.assertEqual(volume[0, 0], 50.0)
                        self.assertEqual(volume[0, 1], 100.0)

                    if scenario == "sem_tipo_2":
                        np.testing.assert_array_equal(power, np.zeros((1, 12)))
                        np.testing.assert_array_equal(units, np.zeros((1, 12)))
                        np.testing.assert_array_equal(flow, np.zeros((1, 12)))
                    else:
                        np.testing.assert_array_equal(power[0, 2:], 50.0)
                        np.testing.assert_array_equal(units[0, 2:], 1.0)
                        np.testing.assert_array_equal(flow[0, 2:], 25.0)


class TestNewaveDegenerateExphIntegration(unittest.TestCase):
    def test_deck_real_sem_registros_tipo_1_reabre_e_recalcula_confhd(self):
        with TemporaryDirectory() as temp_dir:
            deck = Path(temp_dir) / "deck"
            shutil.copytree(PMO, deck)

            case = Newave(str(deck))
            frame = case.exph.bloco_usina["df"]
            frame = frame[frame["mesi_evm"].isna()].copy().reset_index(drop=True)
            for field in case.exph._GRUPO_ENCHIMENTO:
                frame[field] = pd.Series([None] * len(frame), dtype=object)
            case.exph.bloco_usina["df"] = frame
            case.exph.escrever(str(deck / case.arquivos.exph))
            del case

            reloaded = Newave(str(deck))
            self.assertEqual(reloaded.exph.bloco_usina["df"]["mesi_evm"].dtype, object)
            plant = reloaded.confhd.get(288)
            for field in (
                "vol_morto_tempo",
                "potencia_tempo",
                "unidades_tempo",
                "engol_tempo",
            ):
                self.assertIsInstance(plant[field], np.ndarray)
                self.assertEqual(plant[field].shape, (reloaded.dger.num_anos["valor"], 12))


if __name__ == "__main__":
    unittest.main()
