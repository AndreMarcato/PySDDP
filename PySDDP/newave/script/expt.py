import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO

from PySDDP.newave.script.templates.expt import ExptTemplate
import numpy as np


class Expt(ExptTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo EXPT.DAT.

    O EXPT.DAT nao possui uma chave unica por registro: uma mesma usina
    termica pode ter varias modificacoes de cadastro (uma por
    tipo_modificacao/vigencia) ao longo do arquivo. Por isso, assim como
    Clast.get_alteracao/put_alteracao (bloco de alteracoes de custo, que
    tambem nao possui chave natural), a identidade de cada modificacao em
    Expt.get/Expt.put e a sua posicao (indice, 0-based) na lista de
    modificacoes, preservada pela chave somente-leitura ``indice_original``.
    """

    _TIPO_MODIFICACAO_VALUES = frozenset(('GTMIN', 'POTEF', 'FCMAX', 'IPTER', 'TEIFT'))

    _FIELD_MAP = {
        'codigo_usina': ('_codigo_usina', 'valor'),
        'tipo_modificacao': ('_tipo_modificacao', 'valor'),
        'novo_valor': ('_novo_valor', 'valor'),
        'mes_inicio': ('_mes_inicio', 'valor'),
        'ano_inicio': ('_ano_inicio', 'valor'),
        'mes_fim': ('_mes_fim', 'valor'),
        'ano_fim': ('_ano_fim', 'valor'),
        'comentario': ('_comentario', 'valor'),
    }
    _EXPT_FIELDS = tuple(_FIELD_MAP)

    # Coluna (0-based) onde comeca o comentario livre, quando presente
    _COMENTARIO_INICIO = 37
    _COMENTARIO_TAMANHO = 12

    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    @staticmethod
    def _as_int(field, value, minimum, maximum):
        """Converte escalares inteiros Python/NumPy sem truncamento."""
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, bool):
            raise TypeError(f"{field} deve ser inteiro")
        if isinstance(value, Integral):
            result = int(value)
        elif isinstance(value, Real):
            numeric = float(value)
            if not math.isfinite(numeric) or not numeric.is_integer():
                raise ValueError(f"{field} deve ser um inteiro exato")
            result = int(numeric)
        else:
            raise TypeError(f"{field} deve ser inteiro")
        if result < minimum or result > maximum:
            raise ValueError(
                f"{field} deve estar entre {minimum} e {maximum}"
            )
        return result

    @classmethod
    def _as_optional_int(cls, field, value, minimum, maximum):
        """Como _as_int, mas preserva None para campos opcionais em branco."""
        if value is None:
            return None
        return cls._as_int(field, value, minimum, maximum)

    @staticmethod
    def _as_float(field, value, minimum, maximum, decimals=None):
        """Converte escalares reais Python/NumPy e verifica finitude."""
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{field} deve ser numerico")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{field} deve ser finito")
        if result < minimum or result > maximum:
            raise ValueError(
                f"{field} deve estar entre {minimum} e {maximum}"
            )
        if decimals is not None:
            result = float(f"{result:.{decimals}f}")
        return result

    @staticmethod
    def _read_int(texto):
        """Converte um campo numerico de largura fixa; em branco vira None."""
        texto = texto.strip()
        return int(texto) if texto else None

    @staticmethod
    def _splice(linha, inicio, texto):
        """Substitui os caracteres a partir de ``inicio`` por ``texto``,
        preservando o restante da linha (campos nao interpretados, como o
        comentario livre no final do registro)."""
        if len(linha) < inicio:
            linha = linha.ljust(inicio)
        fim = inicio + len(texto)
        return linha[:inicio] + texto + linha[fim:]

    def _normalize_expt_fields(self, values):
        """Valida e normaliza os sete campos fisicos de um registro EXPT."""
        tipo = values['tipo_modificacao']
        if not isinstance(tipo, str):
            raise TypeError("tipo_modificacao deve ser string")
        tipo = tipo.strip().upper()
        if tipo not in self._TIPO_MODIFICACAO_VALUES:
            permitidos = ", ".join(sorted(self._TIPO_MODIFICACAO_VALUES))
            raise ValueError(f"tipo_modificacao deve ser um de: {permitidos}")

        mes_fim = self._as_optional_int('mes_fim', values['mes_fim'], 1, 12)
        ano_fim = self._as_optional_int('ano_fim', values['ano_fim'], 0, 9999)
        if (mes_fim is None) != (ano_fim is None):
            raise ValueError(
                "mes_fim e ano_fim devem estar ambos preenchidos ou ambos "
                "em branco"
            )

        comentario = values['comentario']
        if not isinstance(comentario, str):
            raise TypeError("comentario deve ser string")
        comentario = comentario.strip()
        try:
            comentario.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError(
                "comentario deve ser representavel em latin-1"
            ) from err
        if len(comentario) > self._COMENTARIO_TAMANHO:
            raise ValueError(
                f"comentario deve possuir no maximo "
                f"{self._COMENTARIO_TAMANHO} caracteres"
            )

        normalized = {
            'codigo_usina': self._as_int(
                'codigo_usina', values['codigo_usina'], 1, 9999
            ),
            'tipo_modificacao': tipo.ljust(5),
            'novo_valor': self._as_float(
                'novo_valor', values['novo_valor'], 0.0, 99999.99, decimals=2
            ),
            'mes_inicio': self._as_int(
                'mes_inicio', values['mes_inicio'], 1, 12
            ),
            'ano_inicio': self._as_int(
                'ano_inicio', values['ano_inicio'], 0, 9999
            ),
            'mes_fim': mes_fim,
            'ano_fim': ano_fim,
            'comentario': comentario,
        }
        return normalized

    @classmethod
    def _splice_comentario(cls, linha, comentario):
        """Substitui todo o restante da linha a partir da coluna do
        comentario. Diferente de ``_splice``, o comentario e o ultimo
        campo do registro, por isso nada apos ele e preservado: quando
        ausente, a linha e truncada (sem preenchimento) no mesmo estilo
        adotado pelo deck real para registros sem comentario."""
        inicio = cls._COMENTARIO_INICIO
        nova = linha[:inicio].ljust(inicio) + comentario
        if not comentario:
            nova = nova.rstrip()
        return nova

    def _splice_registro(self, linha, registro):
        linha = self._splice(linha, 0, "{:>4d}".format(registro['codigo_usina']))
        linha = self._splice(linha, 5, "{:<5}".format(registro['tipo_modificacao']))
        linha = self._splice(linha, 11, "{:>8.2f}".format(registro['novo_valor']))
        linha = self._splice(linha, 20, "{:>2d}".format(registro['mes_inicio']))
        linha = self._splice(linha, 23, "{:>4d}".format(registro['ano_inicio']))
        if registro['mes_fim'] is not None:
            linha = self._splice(linha, 28, "{:>2d}".format(registro['mes_fim']))
            linha = self._splice(linha, 31, "{:>4d}".format(registro['ano_fim']))
        linha = self._splice_comentario(linha, registro['comentario'])
        return linha

    def ler(self, file_name: str) -> None:
        """
        Le o EXPT.DAT e preenche a lista de modificacoes de expansao
        termica.

        :param file_name: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._numero_registros_ = 0
        self.numero_expansoes = 0
        self._cabecalho = list()
        self._linhas = list()

        for attr_name, value_name in set(self._FIELD_MAP.values()):
            getattr(self, attr_name)[value_name] = list()

        with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

            self._cabecalho.append(self.next_line(f).rstrip('\r\n'))
            self._cabecalho.append(self.next_line(f).rstrip('\r\n'))
            self._numero_registros_ += 2

            try:
                while True:

                    self.next_line(f)
                    linha = self.linha.rstrip('\r\n')
                    self._numero_registros_ += 1

                    if not linha.strip():
                        continue

                    self._linhas.append(linha)
                    self._codigo_usina['valor'].append(int(linha[0:4]))
                    self._tipo_modificacao['valor'].append(linha[5:10].strip())
                    self._novo_valor['valor'].append(float(linha[11:19]))
                    self._mes_inicio['valor'].append(int(linha[20:22]))
                    self._ano_inicio['valor'].append(int(linha[23:27]))
                    self._mes_fim['valor'].append(self._read_int(linha[28:30]))
                    self._ano_fim['valor'].append(self._read_int(linha[31:35]))
                    self._comentario['valor'].append(
                        linha[self._COMENTARIO_INICIO:
                              self._COMENTARIO_INICIO + self._COMENTARIO_TAMANHO].strip()
                    )

                    self.numero_expansoes += 1

            except StopIteration:
                pass

        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o EXPT.DAT, preservando os registros de comentario iniciais
        e os trechos nao interpretados de cada linha (ex.: comentario
        livre com o nome da usina).

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        self._numero_registros_ = 0

        diretorio = os.path.split(file_out)[0]
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

            f.write(self._cabecalho[0] + "\n")
            f.write(self._cabecalho[1] + "\n")
            self._numero_registros_ += 2

            for linha in self._linhas:
                f.write(linha + "\n")
                self._numero_registros_ += 1

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def _get(self, indice, copy_values):
        indice = self._as_int('indice', indice, 0, self.numero_expansoes - 1)

        registro = {
            field: getattr(self, attr_name)[value_name][indice]
            for field, (attr_name, value_name) in self._FIELD_MAP.items()
        }

        if copy_values:
            registro['indice_original'] = indice
            return deepcopy(registro)
        return registro

    def get(self, indice):
        """
        Retorna o dicionario completo e independente de uma modificacao de
        expansao termica, pela sua posicao (0-based) na lista de
        modificacoes. A chave ``indice_original`` preserva essa identidade
        e nao deve ser modificada.
        """
        return self._get(indice, copy_values=True)

    def put(self, expansao):
        """
        Atualiza uma modificacao de expansao termica a partir do
        dicionario completo retornado por get(). A posicao e identificada
        por ``indice_original`` e nao e editavel.

        :param expansao: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(expansao, dict):
            raise TypeError("expansao deve ser um dicionario completo")

        required = set(self._FIELD_MAP) | {'indice_original'}
        received = set(expansao)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        unknown = sorted(received - required)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        indice = self._as_int(
            'indice_original', expansao['indice_original'],
            0, self.numero_expansoes - 1
        )

        normalized = self._normalize_expt_fields(expansao)

        for field, value in normalized.items():
            attr_name, value_name = self._FIELD_MAP[field]
            getattr(self, attr_name)[value_name][indice] = value

        self._linhas[indice] = self._splice_registro(self._linhas[indice], normalized)

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario obtido por
        get().

        :param parametro: string contendo a chave cujo detalhamento e desejado

        """

        if parametro == 'indice_original':
            return (
                'Posicao original da modificacao de expansao termica; '
                'metadado somente leitura usado por put para impedir '
                'alteracao de posicao'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_expansoes(self):
        """
        Calcula um generator contendo as posicoes (0-based) de todas as
        modificacoes de expansao termica pertencentes ao EXPT.

        """

        for i in range(self.numero_expansoes):
            yield i
