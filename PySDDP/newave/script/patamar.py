import os
import math
from numbers import Integral, Real
from typing import IO, List, Optional

import pandas as pd

from PySDDP.newave.script.templates.patamar import PatamarTemplate


class Patamar(PatamarTemplate):
    """Le os cinco blocos do arquivo de patamares de mercado do NEWAVE."""

    _SENTINEL = "9999"
    _MESES = tuple(range(1, 13))

    def __init__(self):
        super().__init__()
        self._numero_registros_ = 0
        self._linha_numero_patamares = None
        self._estrutura_duracao = []
        self._estrutura_blocos = {3: None, 4: None, 5: None}

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

    def _next_or_none(self, arquivo: IO[str]):
        try:
            linha = self.next_line(arquivo)
        except StopIteration:
            return None
        self._numero_registros_ += 1
        return linha.rstrip("\r\n")

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
    def _inteiro_saida(valor, largura: int, contexto: str) -> str:
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

    @staticmethod
    def _decimal_saida(valor, largura: int, casas: int, contexto: str) -> str:
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise ValueError(f"Decimal invalido em {contexto}: {valor}")
        numero = float(valor)
        if not math.isfinite(numero):
            raise ValueError(f"Decimal nao finito em {contexto}: {valor}")
        texto = f"{numero:>{largura}.{casas}f}"
        if len(texto) != largura:
            raise ValueError(f"Decimal fora do campo em {contexto}: {valor}")
        return texto

    @staticmethod
    def _linhas_fisicas(df, indices, contexto: str):
        try:
            linhas = df.loc[indices]
        except KeyError as err:
            raise ValueError(
                f"Estrutura do DataFrame alterada em {contexto}"
            ) from err
        if len(linhas) != 12 or list(linhas["mes"]) != list(range(1, 13)):
            raise ValueError(f"Meses incompletos ou fora de ordem em {contexto}")
        return linhas

    @staticmethod
    def _int(campo: str, contexto: str) -> int:
        texto = campo.strip()
        if not texto:
            raise ValueError(f"Campo inteiro vazio em {contexto}")
        try:
            return int(texto)
        except ValueError as err:
            raise ValueError(f"Inteiro invalido em {contexto}: {campo!r}") from err

    @staticmethod
    def _float(campo: str, contexto: str) -> float:
        texto = campo.strip()
        if not texto:
            raise ValueError(f"Campo decimal vazio em {contexto}")
        try:
            return float(texto)
        except ValueError as err:
            raise ValueError(f"Decimal invalido em {contexto}: {campo!r}") from err

    def _valores_mensais(
        self,
        linha: str,
        inicio: int,
        passo: int,
        contexto: str,
        permitir_vazio: bool = False,
    ) -> List[Optional[float]]:
        valores = []
        for mes in range(12):
            campo = linha[inicio + mes * passo:inicio + mes * passo + 6]
            if permitir_vazio and not campo.strip():
                valores.append(None)
            else:
                valores.append(
                    self._float(campo, f"{contexto}, mes {mes + 1}")
                )
        return valores

    @staticmethod
    def _novo_df(linhas, colunas):
        return pd.DataFrame(linhas, columns=colunas)

    def _ler_duracao(self, arquivo: IO[str], numero_anos: int):
        linhas = []
        self._estrutura_duracao = []
        if self.tipo == 1:
            for mes in self._MESES:
                linha = self._next(arquivo, "bloco 2 tipo 1")
                nome_mes = linha[1:4].strip()
                inicio_registro = len(linhas)
                for patamar in range(1, self.numero_patamares + 1):
                    inicio = 6 + (patamar - 1) * 8
                    linhas.append(
                        {
                            "tipo": 1,
                            "ano": None,
                            "mes": mes,
                            "nome_mes": nome_mes,
                            "patamar": patamar,
                            "duracao": self._float(
                                linha[inicio:inicio + 6],
                                f"bloco 2 tipo 1, mes {mes}, patamar {patamar}",
                            ),
                        }
                    )
                self._estrutura_duracao.append(
                    {
                        "linha": linha,
                        "indices": list(range(inicio_registro, len(linhas))),
                        "ano_explicito": False,
                    }
                )
        else:
            for _ in range(numero_anos):
                ano = None
                for patamar in range(1, self.numero_patamares + 1):
                    linha = self._next(arquivo, "bloco 2 tipo 2")
                    inicio_registro = len(linhas)
                    if patamar == 1:
                        ano = self._int(linha[0:4], "ano do bloco 2 tipo 2")
                    valores = self._valores_mensais(
                        linha, 6, 8, f"bloco 2, ano {ano}, patamar {patamar}"
                    )
                    for mes, valor in zip(self._MESES, valores):
                        linhas.append(
                            {
                                "tipo": 2,
                                "ano": ano,
                                "mes": mes,
                                "nome_mes": None,
                                "patamar": patamar,
                                "duracao": valor,
                            }
                        )
                    self._estrutura_duracao.append(
                        {
                            "linha": linha,
                            "indices": list(range(inicio_registro, len(linhas))),
                            "ano_explicito": patamar == 1,
                        }
                    )
        return linhas

    def _ler_fatores(
        self,
        arquivo: IO[str],
        numero_anos: int,
        bloco: int,
        identificadores,
        linhas_cabecalho,
        eof_permitido: bool = False,
    ):
        linhas = []
        estrutura = {
            "grupos": [],
            "sentinela": None,
            "terminado": False,
        }
        primeiro_cabecalho = True
        while True:
            cabecalho = self._next_or_none(arquivo)
            if cabecalho is None:
                if eof_permitido:
                    self._estrutura_blocos[bloco] = estrutura
                    return linhas, False
                raise ValueError(
                    f"Fim inesperado de {self.nome_arquivo} no bloco {bloco}"
                )
            campo_identificador = cabecalho[0:4].strip()
            if primeiro_cabecalho and not campo_identificador.isdigit():
                # Alguns decks antigos possuem uma linha de mascara adicional
                # aos comentarios obrigatorios descritos no manual.
                linhas_cabecalho.append(cabecalho)
                continue
            primeiro_cabecalho = False
            if cabecalho[0:5].strip() == self._SENTINEL:
                estrutura["sentinela"] = cabecalho
                estrutura["terminado"] = True
                self._estrutura_blocos[bloco] = estrutura
                return linhas, True

            ids = identificadores(cabecalho)
            grupo = {"linha": cabecalho, "registros": []}
            if self.tipo == 1:
                for patamar in range(1, self.numero_patamares + 1):
                    linha = self._next(arquivo, f"bloco {bloco} tipo 1")
                    inicio_registro = len(linhas)
                    valores = self._valores_mensais(
                        linha, 1, 7, f"bloco {bloco}, patamar {patamar}"
                    )
                    for mes, valor in zip(self._MESES, valores):
                        linhas.append(
                            {
                                "tipo": 1,
                                **ids,
                                "ano": None,
                                "mes": mes,
                                "patamar": patamar,
                                "fator": valor,
                            }
                        )
                    grupo["registros"].append(
                        {
                            "linha": linha,
                            "indices": list(range(inicio_registro, len(linhas))),
                            "ano_explicito": False,
                        }
                    )
            else:
                for _ in range(numero_anos):
                    ano = None
                    for patamar in range(1, self.numero_patamares + 1):
                        linha = self._next(arquivo, f"bloco {bloco} tipo 2")
                        inicio_registro = len(linhas)
                        if patamar == 1:
                            ano = self._int(
                                linha[3:7], f"ano do bloco {bloco} tipo 2"
                            )
                        valores = self._valores_mensais(
                            linha,
                            8,
                            7,
                            f"bloco {bloco}, ano {ano}, patamar {patamar}",
                            permitir_vazio=True,
                        )
                        for mes, valor in zip(self._MESES, valores):
                            linhas.append(
                                {
                                    "tipo": 2,
                                    **ids,
                                    "ano": ano,
                                    "mes": mes,
                                    "patamar": patamar,
                                    "fator": valor,
                                }
                            )
                        grupo["registros"].append(
                            {
                                "linha": linha,
                                "indices": list(
                                    range(inicio_registro, len(linhas))
                                ),
                                "ano_explicito": patamar == 1,
                            }
                        )
            estrutura["grupos"].append(grupo)

    def _ids_mercado(self, linha: str):
        return {"sistema": self._int(linha[1:4], "sistema do bloco 3")}

    def _ids_intercambio(self, linha: str):
        return {
            "de": self._int(linha[1:4], "origem do bloco 4"),
            "para": self._int(linha[5:8], "destino do bloco 4"),
        }

    def _ids_nao_simuladas(self, linha: str):
        return {
            "sistema": self._int(linha[1:4], "sistema do bloco 5"),
            "bloco": self._int(linha[5:8], "bloco nao simulado do bloco 5"),
        }

    def _finalizar_dataframes(self, duracao, mercado, intercambio, nao_simuladas):
        self.bloco_duracao["df"] = self._novo_df(
            duracao, ["tipo", "ano", "mes", "nome_mes", "patamar", "duracao"]
        )
        self.bloco_mercado["df"] = self._novo_df(
            mercado, ["tipo", "sistema", "ano", "mes", "patamar", "fator"]
        )
        self.bloco_intercambio["df"] = self._novo_df(
            intercambio,
            ["tipo", "de", "para", "ano", "mes", "patamar", "fator"],
        )
        self.bloco_nao_simuladas["df"] = self._novo_df(
            nao_simuladas,
            ["tipo", "sistema", "bloco", "ano", "mes", "patamar", "fator"],
        )
        for bloco in (
            self.bloco_duracao,
            self.bloco_mercado,
            self.bloco_intercambio,
            self.bloco_nao_simuladas,
        ):
            if "ano" in bloco["df"]:
                bloco["df"]["ano"] = bloco["df"]["ano"].astype("Int64")

    @staticmethod
    def _escrever_linhas(arquivo: IO[str], linhas) -> None:
        for linha in linhas:
            arquivo.write(linha + "\n")

    def _linha_duracao_saida(self, registro, df) -> str:
        linha = registro["linha"]
        linhas = df.loc[registro["indices"]]
        if self.tipo == 1:
            if list(linhas["patamar"]) != list(
                range(1, self.numero_patamares + 1)
            ):
                raise ValueError("Patamares fora de ordem no bloco 2 tipo 1")
            nomes = linhas["nome_mes"].dropna().astype(str).unique()
            if len(nomes) != 1 or len(nomes[0]) > 3:
                raise ValueError("Nome de mes invalido no bloco 2 tipo 1")
            linha = self._substituir(linha, 1, 3, nomes[0].ljust(3))
            for _, dado in linhas.iterrows():
                patamar = int(dado["patamar"])
                linha = self._substituir(
                    linha,
                    6 + (patamar - 1) * 8,
                    6,
                    self._decimal_saida(
                        dado["duracao"],
                        6,
                        4,
                        f"duracao do patamar {patamar}",
                    ),
                )
            return linha

        linhas = self._linhas_fisicas(df, registro["indices"], "bloco 2 tipo 2")
        anos = linhas["ano"].dropna().unique()
        patamares = linhas["patamar"].unique()
        if len(anos) != 1 or len(patamares) != 1:
            raise ValueError("Ano ou patamar inconsistente no bloco 2 tipo 2")
        campo_ano = (
            self._inteiro_saida(anos[0], 4, "ano do bloco 2")
            if registro["ano_explicito"]
            else " " * 4
        )
        linha = self._substituir(linha, 0, 4, campo_ano)
        for _, dado in linhas.iterrows():
            mes = int(dado["mes"])
            linha = self._substituir(
                linha,
                6 + (mes - 1) * 8,
                6,
                self._decimal_saida(
                    dado["duracao"], 6, 4, f"duracao do mes {mes}"
                ),
            )
        return linha

    def _linha_identificacao_saida(self, bloco: int, linha: str, dado) -> str:
        if bloco == 3:
            return self._substituir(
                linha,
                1,
                3,
                self._inteiro_saida(dado["sistema"], 3, "sistema do bloco 3"),
            )
        if bloco == 4:
            linha = self._substituir(
                linha,
                1,
                3,
                self._inteiro_saida(dado["de"], 3, "origem do bloco 4"),
            )
            return self._substituir(
                linha,
                5,
                3,
                self._inteiro_saida(dado["para"], 3, "destino do bloco 4"),
            )
        linha = self._substituir(
            linha,
            1,
            3,
            self._inteiro_saida(dado["sistema"], 3, "sistema do bloco 5"),
        )
        return self._substituir(
            linha,
            5,
            3,
            self._inteiro_saida(dado["bloco"], 3, "bloco nao simulado"),
        )

    def _linha_fator_saida(self, registro, df, bloco: int) -> str:
        linhas = self._linhas_fisicas(
            df, registro["indices"], f"bloco {bloco}"
        )
        linha = registro["linha"]
        if self.tipo == 2:
            anos = linhas["ano"].dropna().unique()
            if len(anos) != 1:
                raise ValueError(f"Ano inconsistente no bloco {bloco}")
            campo_ano = (
                self._inteiro_saida(anos[0], 4, f"ano do bloco {bloco}")
                if registro["ano_explicito"]
                else " " * 4
            )
            linha = self._substituir(linha, 3, 4, campo_ano)
            inicio, passo = 8, 7
        else:
            inicio, passo = 1, 7
        for _, dado in linhas.iterrows():
            mes = int(dado["mes"])
            valor = dado["fator"]
            campo = (
                " " * 6
                if pd.isna(valor)
                else self._decimal_saida(
                    valor,
                    6,
                    4,
                    f"fator do bloco {bloco}, mes {mes}",
                )
            )
            linha = self._substituir(
                linha,
                inicio + (mes - 1) * passo,
                6,
                campo,
            )
        return linha

    def _escrever_bloco_fatores(self, arquivo: IO[str], bloco: int, df) -> None:
        estrutura = self._estrutura_blocos[bloco]
        if estrutura is None:
            raise ValueError(f"Estrutura fisica do bloco {bloco} nao foi lida")
        for grupo in estrutura["grupos"]:
            if not grupo["registros"]:
                raise ValueError(f"Grupo vazio no bloco {bloco}")
            primeiro_indice = grupo["registros"][0]["indices"][0]
            dado = df.loc[primeiro_indice]
            arquivo.write(
                self._linha_identificacao_saida(bloco, grupo["linha"], dado)
                + "\n"
            )
            for registro in grupo["registros"]:
                arquivo.write(
                    self._linha_fator_saida(registro, df, bloco) + "\n"
                )
        if estrutura["terminado"]:
            arquivo.write((estrutura["sentinela"] or self._SENTINEL) + "\n")

    def ler(self, file_name: str, dger) -> None:
        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.cont = 0
        self._numero_registros_ = 0
        self._linha_numero_patamares = None
        self._estrutura_duracao = []
        self._estrutura_blocos = {3: None, 4: None, 5: None}
        self.tem_bloco_5 = False
        self.finalizacao_bloco_4_por_eof = False
        for bloco in (
            self.bloco_numero_patamares,
            self.bloco_duracao,
            self.bloco_mercado,
            self.bloco_intercambio,
            self.bloco_nao_simuladas,
        ):
            bloco["cabecalho"] = []

        numero_anos = int(dger.num_anos["valor"])
        flag_pat = int(dger.flag_pat["valor"])
        if flag_pat not in (0, 1):
            raise ValueError(f"flag_pat deve ser 0 ou 1, recebido {flag_pat}")
        self.tipo = flag_pat + 1

        with open(file_name, "r", encoding="latin-1") as arquivo:
            self.bloco_numero_patamares["cabecalho"] = self._skip(
                arquivo, 2, "comentarios do bloco 1"
            )
            linha = self._next(arquivo, "numero de patamares")
            self._linha_numero_patamares = linha
            self.numero_patamares = self._int(linha[1:3], "numero de patamares")
            self.bloco_numero_patamares["valor"] = self.numero_patamares

            if self.numero_patamares == 1:
                self._finalizar_dataframes([], [], [], [])
                print("OK! Leitura do", self.nome_arquivo, "realizada com sucesso.")
                return

            self.bloco_duracao["cabecalho"] = self._skip(
                arquivo, 3, "comentarios do bloco 2"
            )
            duracao = self._ler_duracao(arquivo, numero_anos)

            self.bloco_mercado["cabecalho"] = self._skip(
                arquivo, 3, "comentarios do bloco 3"
            )
            mercado, _ = self._ler_fatores(
                arquivo,
                numero_anos,
                3,
                self._ids_mercado,
                self.bloco_mercado["cabecalho"],
            )

            self.bloco_intercambio["cabecalho"] = self._skip(
                arquivo, 5, "comentarios do bloco 4"
            )
            intercambio, bloco_4_terminado = self._ler_fatores(
                arquivo,
                numero_anos,
                4,
                self._ids_intercambio,
                self.bloco_intercambio["cabecalho"],
                eof_permitido=True,
            )
            self.finalizacao_bloco_4_por_eof = not bloco_4_terminado

            nao_simuladas = []
            if bloco_4_terminado:
                self.tem_bloco_5 = True
                self.bloco_nao_simuladas["cabecalho"] = self._skip(
                    arquivo, 4, "comentarios do bloco 5"
                )
                nao_simuladas, _ = self._ler_fatores(
                    arquivo,
                    numero_anos,
                    5,
                    self._ids_nao_simuladas,
                    self.bloco_nao_simuladas["cabecalho"],
                    eof_permitido=True,
                )

        self._finalizar_dataframes(duracao, mercado, intercambio, nao_simuladas)
        print("OK! Leitura do", self.nome_arquivo, "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """Escreve os blocos fisicos preservando os textos lidos."""

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]
        if self.dir_base:
            os.makedirs(self.dir_base, exist_ok=True)

        numero_patamares = self.bloco_numero_patamares["valor"]
        numero_patamares = int(numero_patamares)
        if numero_patamares != self.numero_patamares:
            raise ValueError(
                "Numero de patamares diverge da estrutura fisica lida"
            )
        if self._linha_numero_patamares is None:
            raise ValueError("PATAMAR deve ser lido antes da escrita")

        with open(file_out, "w", encoding="latin-1") as arquivo:
            self._escrever_linhas(
                arquivo, self.bloco_numero_patamares["cabecalho"]
            )
            arquivo.write(
                self._substituir(
                    self._linha_numero_patamares,
                    1,
                    2,
                    self._inteiro_saida(
                        numero_patamares, 2, "numero de patamares"
                    ),
                )
                + "\n"
            )

            if numero_patamares == 1:
                print(
                    "OK! Escrita do",
                    os.path.split(file_out)[1],
                    "realizada com sucesso.",
                )
                return

            self._escrever_linhas(arquivo, self.bloco_duracao["cabecalho"])
            df_duracao = self.bloco_duracao["df"]
            for registro in self._estrutura_duracao:
                arquivo.write(
                    self._linha_duracao_saida(registro, df_duracao) + "\n"
                )

            self._escrever_linhas(arquivo, self.bloco_mercado["cabecalho"])
            self._escrever_bloco_fatores(
                arquivo, 3, self.bloco_mercado["df"]
            )

            self._escrever_linhas(
                arquivo, self.bloco_intercambio["cabecalho"]
            )
            self._escrever_bloco_fatores(
                arquivo, 4, self.bloco_intercambio["df"]
            )

            if self.tem_bloco_5:
                self._escrever_linhas(
                    arquivo, self.bloco_nao_simuladas["cabecalho"]
                )
                self._escrever_bloco_fatores(
                    arquivo, 5, self.bloco_nao_simuladas["df"]
                )

        print(
            "OK! Escrita do",
            os.path.split(file_out)[1],
            "realizada com sucesso.",
        )
