import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO

from PySDDP.newave.script.templates.manutt import ManuttTemplate
import numpy as np


class Manutt(ManuttTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo MANUTT.DAT.

    O MANUTT.DAT nao possui uma chave unica por registro: uma mesma usina
    termica pode ter varios eventos de manutencao programada ao longo do
    arquivo. Por isso, assim como Clast.get_alteracao/put_alteracao (bloco
    de alteracoes de custo, que tambem nao possui chave natural), a
    identidade de cada evento em Manutt.get/Manutt.put e a sua posicao
    (indice, 0-based) na lista de manutencoes, preservada pela chave
    somente-leitura ``indice_original``.
    """

    _FIELD_MAP = {
        'codigo_usina': ('_codigo_usina', 'valor'),
        'dia_inicio': ('_dia_inicio', 'valor'),
        'mes_inicio': ('_mes_inicio', 'valor'),
        'ano_inicio': ('_ano_inicio', 'valor'),
        'duracao': ('_duracao', 'valor'),
        'potencia': ('_potencia', 'valor'),
    }
    _MANUTT_FIELDS = tuple(_FIELD_MAP)

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
    def _splice(linha, inicio, texto):
        """Substitui os caracteres a partir de ``inicio`` por ``texto``,
        preservando o restante da linha (campos nao interpretados)."""
        if len(linha) < inicio:
            linha = linha.ljust(inicio)
        fim = inicio + len(texto)
        return linha[:inicio] + texto + linha[fim:]

    def _normalize_manutt_fields(self, values):
        """Valida e normaliza os seis campos fisicos interpretados de um
        registro de manutencao."""
        normalized = {
            'codigo_usina': self._as_int(
                'codigo_usina', values['codigo_usina'], 1, 999
            ),
            'dia_inicio': self._as_int(
                'dia_inicio', values['dia_inicio'], 1, 31
            ),
            'mes_inicio': self._as_int(
                'mes_inicio', values['mes_inicio'], 1, 12
            ),
            'ano_inicio': self._as_int(
                'ano_inicio', values['ano_inicio'], 0, 9999
            ),
            'duracao': self._as_int(
                'duracao', values['duracao'], 0, 999
            ),
            'potencia': self._as_float(
                'potencia', values['potencia'], 0.0, 9999.99, decimals=2
            ),
        }
        return normalized

    def _splice_registro(self, linha, registro):
        linha = self._splice(linha, 17, "{:>3d}".format(registro['codigo_usina']))
        linha = self._splice(linha, 40, "{:>2d}".format(registro['dia_inicio']))
        linha = self._splice(linha, 42, "{:>2d}".format(registro['mes_inicio']))
        linha = self._splice(linha, 44, "{:>4d}".format(registro['ano_inicio']))
        linha = self._splice(linha, 49, "{:>3d}".format(registro['duracao']))
        linha = self._splice(linha, 55, "{:>7.2f}".format(registro['potencia']))
        return linha

    def ler(self, file_name: str) -> None:
        """
        Le o MANUTT.DAT e preenche a lista de eventos de manutencao
        programada de usinas termicas.

        :param file_name: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._numero_registros_ = 0
        self.numero_manutencoes = 0
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
                    self._codigo_usina['valor'].append(int(linha[17:20]))
                    self._dia_inicio['valor'].append(int(linha[40:42]))
                    self._mes_inicio['valor'].append(int(linha[42:44]))
                    self._ano_inicio['valor'].append(int(linha[44:48]))
                    self._duracao['valor'].append(int(linha[49:52]))
                    self._potencia['valor'].append(float(linha[55:62]))

                    self.numero_manutencoes += 1

            except StopIteration:
                pass

        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o MANUTT.DAT, preservando os registros de comentario
        iniciais e os trechos nao interpretados de cada linha.

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
        indice = self._as_int('indice', indice, 0, self.numero_manutencoes - 1)

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
        Retorna o dicionario completo e independente de um evento de
        manutencao programada, pela sua posicao (0-based) na lista de
        manutencoes. A chave ``indice_original`` preserva essa identidade e
        nao deve ser modificada.
        """
        return self._get(indice, copy_values=True)

    def put(self, manutencao):
        """
        Atualiza um evento de manutencao a partir do dicionario completo
        retornado por get(). A posicao e identificada por
        ``indice_original`` e nao e editavel.

        :param manutencao: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(manutencao, dict):
            raise TypeError("manutencao deve ser um dicionario completo")

        required = set(self._FIELD_MAP) | {'indice_original'}
        received = set(manutencao)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        unknown = sorted(received - required)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        indice = self._as_int(
            'indice_original', manutencao['indice_original'],
            0, self.numero_manutencoes - 1
        )

        normalized = self._normalize_manutt_fields(manutencao)

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
                'Posicao original do evento de manutencao; metadado '
                'somente leitura usado por put para impedir alteracao de '
                'posicao'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_manutencoes(self):
        """
        Calcula um generator contendo as posicoes (0-based) de todos os
        eventos de manutencao programada pertencentes ao MANUTT.

        """

        for i in range(self.numero_manutencoes):
            yield i
