import os
import math
from numbers import Integral, Real
from typing import IO

import pandas as pd

from PySDDP.newave.script.templates.agrint import AgrintTemplate


class Agrint(AgrintTemplate):
    """Le composicao e limites dos agrupamentos livres de interligacoes."""

    _SENTINEL = "999"

    def __init__(self):
        super().__init__()
        self._numero_registros_ = 0
        self._linhas_composicao = {}
        self._linhas_limites = {}
        self._sentinela_composicao = None
        self._sentinela_limites = None

    def _next(self, arquivo: IO[str], contexto: str) -> str:
        try:
            linha = self.next_line(arquivo)
        except StopIteration as err:
            raise ValueError(
                f"Fim inesperado de {self.nome_arquivo} ao ler {contexto}"
            ) from err
        self._numero_registros_ += 1
        return linha.rstrip("\r\n")

    def _skip(self, arquivo: IO[str], quantidade: int, contexto: str):
        return [self._next(arquivo, contexto) for _ in range(quantidade)]

    @staticmethod
    def _substituir(linha: str, inicio: int, largura: int, valor: str) -> str:
        if len(valor) != largura:
            raise ValueError(
                f"Campo com largura {len(valor)}, esperado {largura}: {valor!r}"
            )
        if len(linha) < inicio + largura:
            linha = linha.ljust(inicio + largura)
        return linha[:inicio] + valor + linha[inicio + largura:]

    @staticmethod
    def _ausente(valor) -> bool:
        try:
            return bool(pd.isna(valor))
        except (TypeError, ValueError):
            return False

    @classmethod
    def _inteiro_saida(
        cls, valor, largura: int, contexto: str, opcional: bool = False
    ) -> str:
        if cls._ausente(valor):
            if opcional:
                return " " * largura
            raise ValueError(f"Inteiro ausente em {contexto}")
        if isinstance(valor, bool) or not isinstance(valor, Integral):
            if isinstance(valor, Real) and math.isfinite(float(valor)):
                if float(valor).is_integer():
                    valor = int(valor)
                else:
                    raise ValueError(f"Inteiro inexato em {contexto}: {valor}")
            else:
                raise ValueError(f"Inteiro invalido em {contexto}: {valor}")
        texto = f"{int(valor):>{largura}d}"
        if len(texto) != largura:
            raise ValueError(f"Inteiro fora do campo em {contexto}: {valor}")
        return texto

    @classmethod
    def _decimal_saida(
        cls,
        valor,
        largura: int,
        casas: int,
        contexto: str,
        opcional: bool = False,
        original: str = "",
    ) -> str:
        if cls._ausente(valor):
            if opcional:
                return " " * largura
            raise ValueError(f"Decimal ausente em {contexto}")
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise ValueError(f"Decimal invalido em {contexto}: {valor}")
        numero = float(valor)
        if not math.isfinite(numero):
            raise ValueError(f"Decimal nao finito em {contexto}: {valor}")
        if casas == 0 and original.strip().endswith("."):
            texto = f"{numero:>{largura - 1}.0f}."
        else:
            texto = f"{numero:>{largura}.{casas}f}"
        if len(texto) != largura:
            raise ValueError(f"Decimal fora do campo em {contexto}: {valor}")
        return texto

    @staticmethod
    def _int(campo: str, contexto: str, opcional: bool = False):
        texto = campo.strip()
        if not texto and opcional:
            return None
        if not texto:
            raise ValueError(f"Campo inteiro vazio em {contexto}")
        try:
            return int(texto)
        except ValueError as err:
            raise ValueError(f"Inteiro invalido em {contexto}: {campo!r}") from err

    @staticmethod
    def _float(campo: str, contexto: str, opcional: bool = False):
        texto = campo.strip()
        if not texto and opcional:
            return None
        if not texto:
            raise ValueError(f"Campo decimal vazio em {contexto}")
        try:
            return float(texto)
        except ValueError as err:
            raise ValueError(f"Decimal invalido em {contexto}: {campo!r}") from err

    @staticmethod
    def _eh_fim(linha: str) -> bool:
        return linha[1:4].strip() == Agrint._SENTINEL

    def ler(self, file_name: str, numero_patamares=None) -> None:
        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.cont = 0
        self._numero_registros_ = 0
        composicao = []
        limites = []
        self._linhas_composicao = {}
        self._linhas_limites = {}
        self._sentinela_composicao = None
        self._sentinela_limites = None
        self.bloco_composicao["cabecalho"] = []
        self.bloco_limites["cabecalho"] = []

        with open(file_name, "r", encoding="latin-1") as arquivo:
            self.bloco_composicao["cabecalho"] = self._skip(
                arquivo, 3, "comentarios do bloco 1"
            )
            while True:
                linha = self._next(arquivo, "bloco 1")
                if self._eh_fim(linha):
                    self._sentinela_composicao = linha
                    break
                indice = len(composicao)
                self._linhas_composicao[indice] = linha
                composicao.append(
                    {
                        "agrupamento": self._int(linha[1:4], "agrupamento"),
                        "origem": self._int(linha[5:8], "origem"),
                        "destino": self._int(linha[9:12], "destino"),
                        "coeficiente": self._float(linha[13:20], "coeficiente"),
                    }
                )

            comentarios_limites = [
                self._next(arquivo, "comentarios do bloco 2") for _ in range(3)
            ]
            self.bloco_limites["cabecalho"] = comentarios_limites
            if numero_patamares is None:
                cabecalho = " ".join(comentarios_limites).upper()
                declarados = [
                    patamar
                    for patamar in range(1, 6)
                    if f"LIM_P{patamar}" in cabecalho
                ]
                numero_patamares = max(declarados) if declarados else 5
            numero_patamares = int(numero_patamares)
            if numero_patamares < 1 or numero_patamares > 5:
                raise ValueError(
                    "numero_patamares do AGRINT deve estar entre 1 e 5"
                )
            self.numero_patamares = numero_patamares
            inicio_texto_livre = 29 + (numero_patamares - 1) * 8
            while True:
                linha = self._next(arquivo, "bloco 2")
                if self._eh_fim(linha):
                    self._sentinela_limites = linha
                    break
                indice = len(limites)
                self._linhas_limites[indice] = linha
                limites.append(
                    {
                        "agrupamento": self._int(linha[1:4], "agrupamento"),
                        "mes_inicio": self._int(
                            linha[6:8], "mes inicial", opcional=True
                        ),
                        "ano_inicio": self._int(
                            linha[9:13], "ano inicial", opcional=True
                        ),
                        "mes_fim": self._int(
                            linha[14:16], "mes final", opcional=True
                        ),
                        "ano_fim": self._int(
                            linha[17:21], "ano final", opcional=True
                        ),
                        "limite_1": (
                            self._float(
                                linha[22:29],
                                "limite do patamar 1",
                                opcional=True,
                            )
                            if numero_patamares >= 1
                            else None
                        ),
                        "limite_2": (
                            self._float(
                                linha[30:37],
                                "limite do patamar 2",
                                opcional=True,
                            )
                            if numero_patamares >= 2
                            else None
                        ),
                        "limite_3": (
                            self._float(
                                linha[38:45],
                                "limite do patamar 3",
                                opcional=True,
                            )
                            if numero_patamares >= 3
                            else None
                        ),
                        "limite_4": (
                            self._float(
                                linha[46:53],
                                "limite do patamar 4",
                                opcional=True,
                            )
                            if numero_patamares >= 4
                            else None
                        ),
                        "limite_5": (
                            self._float(
                                linha[54:61],
                                "limite do patamar 5",
                                opcional=True,
                            )
                            if numero_patamares >= 5
                            else None
                        ),
                        "texto_livre": linha[inicio_texto_livre:],
                    }
                )

        self.bloco_composicao["df"] = pd.DataFrame(
            composicao,
            columns=["agrupamento", "origem", "destino", "coeficiente"],
        )
        self.bloco_limites["df"] = pd.DataFrame(
            limites,
            columns=[
                "agrupamento",
                "mes_inicio",
                "ano_inicio",
                "mes_fim",
                "ano_fim",
                "limite_1",
                "limite_2",
                "limite_3",
                "limite_4",
                "limite_5",
                "texto_livre",
            ],
        )
        for coluna in (
            "agrupamento",
            "mes_inicio",
            "ano_inicio",
            "mes_fim",
            "ano_fim",
        ):
            self.bloco_limites["df"][coluna] = self.bloco_limites["df"][
                coluna
            ].astype("Int64")

        self.numero_registros_composicao = len(composicao)
        self.numero_registros_limites = len(limites)
        print("OK! Leitura do", self.nome_arquivo, "realizada com sucesso.")

    def _linha_composicao_saida(self, indice, dado) -> str:
        linha = self._linhas_composicao.get(indice, " " * 20)
        linha = self._substituir(
            linha,
            1,
            3,
            self._inteiro_saida(dado["agrupamento"], 3, "agrupamento"),
        )
        linha = self._substituir(
            linha,
            5,
            3,
            self._inteiro_saida(dado["origem"], 3, "origem"),
        )
        linha = self._substituir(
            linha,
            9,
            3,
            self._inteiro_saida(dado["destino"], 3, "destino"),
        )
        return self._substituir(
            linha,
            13,
            7,
            self._decimal_saida(
                dado["coeficiente"],
                7,
                4,
                "coeficiente",
                original=linha[13:20],
            ),
        )

    def _linha_limite_saida(self, indice, dado) -> str:
        linha = self._linhas_limites.get(indice, " " * 61)
        campos_inteiros = (
            ("agrupamento", 1, 3, False),
            ("mes_inicio", 6, 2, True),
            ("ano_inicio", 9, 4, True),
            ("mes_fim", 14, 2, True),
            ("ano_fim", 17, 4, True),
        )
        for nome, inicio, largura, opcional in campos_inteiros:
            linha = self._substituir(
                linha,
                inicio,
                largura,
                self._inteiro_saida(
                    dado[nome], largura, nome, opcional=opcional
                ),
            )

        for patamar in range(1, self.numero_patamares + 1):
            inicio = 22 + (patamar - 1) * 8
            linha = self._substituir(
                linha,
                inicio,
                7,
                self._decimal_saida(
                    dado[f"limite_{patamar}"],
                    7,
                    0,
                    f"limite do patamar {patamar}",
                    opcional=True,
                    original=linha[inicio:inicio + 7],
                ),
            )

        inicio_texto_livre = 29 + (self.numero_patamares - 1) * 8
        texto_livre = dado.get("texto_livre", "")
        if self._ausente(texto_livre):
            texto_livre = ""
        texto_livre = str(texto_livre)
        if len(linha) < inicio_texto_livre:
            linha = linha.ljust(inicio_texto_livre)
        return linha[:inicio_texto_livre] + texto_livre

    def escrever(self, file_out: str) -> None:
        """Escreve composicao e limites preservando os textos fisicos lidos."""

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]
        if self.dir_base:
            os.makedirs(self.dir_base, exist_ok=True)
        if self.numero_patamares is None:
            raise ValueError("AGRINT deve ser lido antes da escrita")

        with open(file_out, "w", encoding="latin-1") as arquivo:
            for linha in self.bloco_composicao["cabecalho"]:
                arquivo.write(linha + "\n")
            for indice, dado in self.bloco_composicao["df"].iterrows():
                arquivo.write(
                    self._linha_composicao_saida(indice, dado) + "\n"
                )
            arquivo.write((self._sentinela_composicao or " 999") + "\n")

            for linha in self.bloco_limites["cabecalho"]:
                arquivo.write(linha + "\n")
            for indice, dado in self.bloco_limites["df"].iterrows():
                arquivo.write(self._linha_limite_saida(indice, dado) + "\n")
            arquivo.write((self._sentinela_limites or " 999") + "\n")

        print(
            "OK! Escrita do",
            os.path.split(file_out)[1],
            "realizada com sucesso.",
        )
