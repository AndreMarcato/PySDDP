"""Calculo da energia armazenada inicial na representacao equivalente NEWAVE.

O calculo reutiliza a produtividade acumulada ``ro_acum`` (PDTARM) produzida
por :class:`Confhd`. Nao ha uma segunda travessia da cascata hidraulica neste
modulo.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


# Conversao NEWAVE de hm3 x MW/(m3/s) para MWmes. A convencao e fixa e nao
# depende da quantidade de dias do mes civil.
FATOR_NEWAVE_MWMES: float = 2.63

_TOLERANCIA_ENERGIA = 1.0e-12

COLUNAS_POR_REE = [
    "codigo_ree",
    "nome_ree",
    "codigo_submercado",
    "nome_submercado",
    "earm_max_mwmes",
    "ear_inicial_confhd_mwmes",
    "percentual_confhd",
    "ear_inicial_dger_mwmes",
    "percentual_dger",
]

COLUNAS_POR_SUBMERCADO = [
    "codigo_submercado",
    "nome_submercado",
    "codigos_rees",
    "earm_max_mwmes",
    "ear_inicial_confhd_mwmes",
    "percentual_confhd",
    "ear_inicial_dger_mwmes",
    "percentual_dger",
    "ficticio",
]


def _valor_campo(objeto: Any, nome: str) -> Any:
    campo = getattr(objeto, nome, None)
    if not isinstance(campo, dict) or "valor" not in campo:
        raise ValueError("Campo DGER ausente ou invalido: {}".format(nome))
    return campo["valor"]


def _numero_finito(valor: Any, campo: str) -> float:
    if valor is None or isinstance(valor, (str, bytes)):
        raise ValueError("{} deve ser numerico e finito".format(campo))
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ValueError("{} deve ser numerico e finito".format(campo))
    if not np.isfinite(numero):
        raise ValueError("{} deve ser numerico e finito".format(campo))
    return numero


def _percentual(valor: Any, campo: str) -> float:
    numero = _numero_finito(valor, campo)
    if numero < 0.0 or numero > 100.0:
        raise ValueError("{} deve estar no intervalo [0, 100]".format(campo))
    return numero


def _percentual_energia(energia: float, earm_max: float) -> float:
    if earm_max <= _TOLERANCIA_ENERGIA:
        return np.nan
    return float(100.0 * energia / earm_max)


def _periodo_inicial(dger: Any) -> Tuple[int, int, int]:
    mes = _valor_campo(dger, "mesi_est")
    ano = _valor_campo(dger, "ano_ini")
    if isinstance(mes, bool) or not isinstance(mes, (int, np.integer)):
        raise ValueError("DGER.mesi_est deve ser um inteiro entre 1 e 12")
    if mes < 1 or mes > 12:
        raise ValueError("DGER.mesi_est deve estar no intervalo [1, 12]")
    if isinstance(ano, bool) or not isinstance(ano, (int, np.integer)):
        raise ValueError("DGER.ano_ini deve ser um inteiro")
    return 0, int(mes) - 1, int(ano)


def _tabela(objeto: Any, bloco: str, descricao: str) -> pd.DataFrame:
    valor = getattr(objeto, bloco, None)
    if not isinstance(valor, dict) or not isinstance(valor.get("df"), pd.DataFrame):
        raise ValueError("Tabela {} nao esta disponivel".format(descricao))
    return valor["df"]


def _validar_colunas(df: pd.DataFrame, colunas: Sequence[str], descricao: str) -> None:
    ausentes = [coluna for coluna in colunas if coluna not in df.columns]
    if ausentes:
        raise ValueError(
            "Tabela {} sem as colunas obrigatorias: {}".format(
                descricao, ", ".join(ausentes)
            )
        )


def _sistemas_por_codigo(sistema_df: pd.DataFrame) -> Dict[int, Dict[str, Any]]:
    _validar_colunas(sistema_df, ("codigo", "nome", "tipo"), "SISTEMA")
    if sistema_df["codigo"].duplicated().any():
        raise ValueError("SISTEMA possui codigos duplicados")
    sistemas = {}
    for _, registro in sistema_df.iterrows():
        codigo = int(registro["codigo"])
        sistemas[codigo] = {
            "nome": str(registro["nome"]).strip(),
            "ficticio": bool(int(registro["tipo"]) == 1),
        }
    return sistemas


def _percentuais_dger(
    dger: Any, quantidade_rees: int
) -> Tuple[Optional[np.ndarray], List[str]]:
    campo = getattr(dger, "vol_earm_inic", None)
    valores = campo.get("valor") if isinstance(campo, dict) else None
    if valores is None:
        return None, ["DGER.vol_earm_inic nao esta disponivel"]
    try:
        quantidade = len(valores)
    except TypeError:
        raise ValueError("DGER.vol_earm_inic deve ser uma sequencia")
    if quantidade == 0:
        return None, ["DGER.vol_earm_inic nao esta disponivel"]
    if quantidade != quantidade_rees:
        return None, [
            "DGER.vol_earm_inic possui {} percentuais para {} REEs; "
            "a fonte DGER nao foi calculada".format(quantidade, quantidade_rees)
        ]
    percentuais = np.asarray(
        [
            _percentual(valor, "DGER.vol_earm_inic[{}]".format(indice))
            for indice, valor in enumerate(valores)
        ],
        dtype=np.float64,
    )
    return percentuais, []


def _valor_matriz(uhe: Dict[str, Any], campo: str, iano: int, imes: int) -> float:
    try:
        valor = uhe[campo][iano][imes]
    except (KeyError, IndexError, TypeError):
        raise ValueError(
            "UHE {} sem {} para o primeiro periodo do estudo".format(
                uhe.get("codigo", "?"), campo
            )
        )
    return _numero_finito(valor, "UHE {}.{}".format(uhe.get("codigo", "?"), campo))


def calcular_energia_armazenada_inicial(
    dger: Any, confhd: Any, ree: Any, sistema: Any
) -> Dict[str, Any]:
    """Calcula EARMX e as duas fontes de EAR inicial por REE e submercado.

    ``CONFHD.vol_ini`` e ``DGER.vol_earm_inic`` sao avaliados em paralelo. A
    ``flag_earm_inic`` e retornada apenas como metadado e nao seleciona fonte.
    Os percentuais DGER sao associados posicionalmente aos REEs na ordem de
    ``REE.DAT``, conforme o registro do arquivo.
    """

    iano, imes, ano_inicial = _periodo_inicial(dger)
    ree_df = _tabela(ree, "bloco_ree", "REE")
    sistema_df = _tabela(sistema, "bloco_sistema", "SISTEMA")
    _validar_colunas(ree_df, ("codigo", "nome", "submercado"), "REE")
    if ree_df["codigo"].duplicated().any():
        raise ValueError("REE possui codigos duplicados")

    sistemas = _sistemas_por_codigo(sistema_df)
    for _, registro in ree_df.iterrows():
        codigo_submercado = int(registro["submercado"])
        if codigo_submercado not in sistemas:
            raise ValueError(
                "REE {} associado ao submercado inexistente {}".format(
                    int(registro["codigo"]), codigo_submercado
                )
            )

    percentuais_dger, diagnosticos = _percentuais_dger(dger, len(ree_df))

    uhes = []
    for codigo_uhe in confhd.lista_uhes():
        uhe = confhd._get(codigo_uhe, copy_values=False)
        percentual_confhd = _percentual(
            uhe.get("vol_ini"), "CONFHD.vol_ini da UHE {}".format(codigo_uhe)
        )
        volume_util = _numero_finito(
            uhe.get("vol_util"), "CONFHD.vol_util da UHE {}".format(codigo_uhe)
        )
        if volume_util < 0.0:
            raise ValueError(
                "CONFHD.vol_util da UHE {} nao pode ser negativo".format(
                    codigo_uhe
                )
            )
        codigo_ree_uhe = _numero_finito(
            uhe.get("ree"), "CONFHD.ree da UHE {}".format(codigo_uhe)
        )
        if not codigo_ree_uhe.is_integer():
            raise ValueError(
                "CONFHD.ree da UHE {} deve ser um codigo inteiro".format(codigo_uhe)
            )
        uhes.append((uhe, int(codigo_ree_uhe), percentual_confhd, volume_util))

    linhas_ree = []
    for posicao, (_, registro) in enumerate(ree_df.iterrows()):
        codigo_ree = int(registro["codigo"])
        codigo_submercado = int(registro["submercado"])
        earm_max = np.float64(0.0)
        ear_confhd = np.float64(0.0)

        for uhe, codigo_ree_uhe, percentual_confhd, volume_util in uhes:
            if codigo_ree_uhe != codigo_ree or volume_util <= 0.0:
                continue
            status = _valor_matriz(uhe, "status_vol_morto", iano, imes)
            if status != 2.0:
                continue
            ro_acum = _valor_matriz(uhe, "ro_acum", iano, imes)
            contribuicao = np.float64(
                volume_util * ro_acum / FATOR_NEWAVE_MWMES
            )
            earm_max += contribuicao
            ear_confhd += np.float64(percentual_confhd / 100.0) * contribuicao

        if percentuais_dger is None:
            percentual_dger = np.nan
            ear_dger = np.nan
        else:
            percentual_dger = np.float64(percentuais_dger[posicao])
            ear_dger = np.float64(percentual_dger / 100.0) * earm_max

        linhas_ree.append(
            {
                "codigo_ree": codigo_ree,
                "nome_ree": str(registro["nome"]).strip(),
                "codigo_submercado": codigo_submercado,
                "nome_submercado": sistemas[codigo_submercado]["nome"],
                "earm_max_mwmes": np.float64(earm_max),
                "ear_inicial_confhd_mwmes": np.float64(ear_confhd),
                "percentual_confhd": np.float64(
                    _percentual_energia(ear_confhd, earm_max)
                ),
                "ear_inicial_dger_mwmes": np.float64(ear_dger),
                "percentual_dger": np.float64(percentual_dger),
            }
        )

    por_ree = pd.DataFrame(linhas_ree, columns=COLUNAS_POR_REE)
    for coluna in (
        "earm_max_mwmes",
        "ear_inicial_confhd_mwmes",
        "percentual_confhd",
        "ear_inicial_dger_mwmes",
        "percentual_dger",
    ):
        por_ree[coluna] = por_ree[coluna].astype(np.float64)

    linhas_submercado = []
    for codigo_submercado, dados_sistema in sistemas.items():
        grupo = por_ree[por_ree["codigo_submercado"] == codigo_submercado]
        earm_max = np.float64(grupo["earm_max_mwmes"].sum())
        ear_confhd = np.float64(grupo["ear_inicial_confhd_mwmes"].sum())
        if percentuais_dger is None:
            ear_dger = np.nan
        else:
            ear_dger = np.float64(grupo["ear_inicial_dger_mwmes"].sum())
        linhas_submercado.append(
            {
                "codigo_submercado": codigo_submercado,
                "nome_submercado": dados_sistema["nome"],
                "codigos_rees": grupo["codigo_ree"].astype(int).tolist(),
                "earm_max_mwmes": earm_max,
                "ear_inicial_confhd_mwmes": ear_confhd,
                "percentual_confhd": np.float64(
                    _percentual_energia(ear_confhd, earm_max)
                ),
                "ear_inicial_dger_mwmes": np.float64(ear_dger),
                "percentual_dger": np.float64(
                    _percentual_energia(ear_dger, earm_max)
                    if np.isfinite(ear_dger)
                    else np.nan
                ),
                "ficticio": dados_sistema["ficticio"],
            }
        )

    por_submercado = pd.DataFrame(
        linhas_submercado, columns=COLUNAS_POR_SUBMERCADO
    )
    for coluna in (
        "earm_max_mwmes",
        "ear_inicial_confhd_mwmes",
        "percentual_confhd",
        "ear_inicial_dger_mwmes",
        "percentual_dger",
    ):
        por_submercado[coluna] = por_submercado[coluna].astype(np.float64)

    flag = getattr(dger, "flag_earm_inic", None)
    flag_valor = flag.get("valor") if isinstance(flag, dict) else None
    return {
        "por_ree": por_ree,
        "por_submercado": por_submercado,
        "metadados": {
            "unidade": "MWmes",
            "fator_conversao": FATOR_NEWAVE_MWMES,
            "mes_inicial": imes + 1,
            "ano_inicial": ano_inicial,
            "flag_earm_inic": flag_valor,
            "observacao_flag": (
                "informativa; a selecao da fonte sera aplicada apenas na futura "
                "execucao da otimizacao"
            ),
            "dger_disponivel": percentuais_dger is not None,
            "diagnosticos": diagnosticos,
            "escopo_produtibilidade": "cascata_configurada",
        },
    }
