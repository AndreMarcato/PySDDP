import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO

from PySDDP.newave.script.templates.clast import ClastTemplate
import numpy as np


class Clast(ClastTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo CLAST.DAT.

    Bloco Tipo 1 (cadastro), um registro de largura fixa por classe termica,
    ate o sentinela 9999:

        colunas  2- 5 (I4)   numero_classe_termica
        colunas  7-18 (A12)  nome_classe_termica
        colunas 20-29 (A10)  tipo_combustivel
        colunas 31-37 (F7.2) custo_ano_1
        colunas 39-45 (F7.2) custo_ano_2
        ...                  uma janela F7.2 a cada 8 colunas, uma por ano
                              do horizonte de planejamento (dger.num_anos)

    Bloco Tipo 2 (alteracoes), apos dois novos registros de comentario:

        colunas  2- 5 (I4)   numero_classe_termica
        colunas  9-15 (F7.2) novo_custo
        colunas 18-19 (I2)   mes_inicio (opcional)
        colunas 21-24 (I4)   ano_inicio (opcional)
        colunas 27-28 (I2)   mes_fim (opcional)
        colunas 30-33 (I4)   ano_fim (opcional)
    """

    _SENTINEL = 9999

    _FIELD_MAP_CLASSE = {
        'numero_classe_termica': ('_numero_classe_termica', 'valor'),
        'nome_classe_termica': ('_nome_classe_termica', 'valor'),
        'tipo_combustivel': ('_tipo_combustivel', 'valor'),
        'custos': ('_custos', 'valor'),
    }
    _CLASSE_FIELDS = tuple(_FIELD_MAP_CLASSE)

    _FIELD_MAP_ALTERACAO = {
        'numero_classe_termica': ('_alt_numero_classe_termica', 'valor'),
        'novo_custo': ('_alt_novo_custo', 'valor'),
        'mes_inicio': ('_alt_mes_inicio', 'valor'),
        'ano_inicio': ('_alt_ano_inicio', 'valor'),
        'mes_fim': ('_alt_mes_fim', 'valor'),
        'ano_fim': ('_alt_ano_fim', 'valor'),
    }
    _ALTERACAO_FIELDS = tuple(_FIELD_MAP_ALTERACAO)

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
        texto = texto.strip()
        return int(texto) if texto else None

    @staticmethod
    def _read_float(texto):
        texto = texto.strip()
        return float(texto) if texto else None

    def _position_for_code(self, codigo):
        return self._mapa.get(codigo)

    def _normalize_classe_fields(self, values):
        """Valida e normaliza um registro do bloco Tipo 1 (cadastro)."""
        nome = values['nome_classe_termica']
        if not isinstance(nome, str):
            raise TypeError("nome_classe_termica deve ser string")
        nome = nome.strip()
        try:
            nome.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError(
                "nome_classe_termica deve ser representavel em latin-1"
            ) from err
        if len(nome) > 12:
            raise ValueError(
                "nome_classe_termica deve possuir no maximo 12 caracteres"
            )

        tipo_combustivel = values['tipo_combustivel']
        if not isinstance(tipo_combustivel, str):
            raise TypeError("tipo_combustivel deve ser string")
        tipo_combustivel = tipo_combustivel.strip()
        if len(tipo_combustivel) > 10:
            raise ValueError(
                "tipo_combustivel deve possuir no maximo 10 caracteres"
            )

        custos = values['custos']
        try:
            custos = list(custos)
        except TypeError as err:
            raise TypeError("custos deve ser uma sequencia de valores") from err
        if self.nanos is not None and len(custos) != self.nanos:
            raise ValueError(
                f"custos deve possuir {self.nanos} valores, recebido {len(custos)}"
            )
        custos_normalizados = [
            self._as_float(f"custos[{i}]", custo, 0.0, 9999.99, decimals=2)
            for i, custo in enumerate(custos)
        ]

        normalized = {
            'numero_classe_termica': self._as_int(
                'numero_classe_termica',
                values['numero_classe_termica'],
                1,
                self._SENTINEL - 1,
            ),
            'nome_classe_termica': nome.ljust(12),
            'tipo_combustivel': tipo_combustivel.ljust(10),
            'custos': custos_normalizados,
        }
        return normalized

    def _normalize_alteracao_fields(self, values):
        """Valida e normaliza um registro do bloco Tipo 2 (alteracoes)."""
        mes_inicio = self._as_optional_int(
            'mes_inicio', values['mes_inicio'], 1, 12
        )
        ano_inicio = self._as_optional_int(
            'ano_inicio', values['ano_inicio'], 0, 9999
        )
        mes_fim = self._as_optional_int('mes_fim', values['mes_fim'], 1, 12)
        ano_fim = self._as_optional_int('ano_fim', values['ano_fim'], 0, 9999)

        if (mes_inicio is None) != (ano_inicio is None):
            raise ValueError(
                "mes_inicio e ano_inicio devem estar ambos preenchidos ou "
                "ambos em branco"
            )
        if (mes_fim is None) != (ano_fim is None):
            raise ValueError(
                "mes_fim e ano_fim devem estar ambos preenchidos ou ambos "
                "em branco"
            )
        if mes_fim is not None and mes_inicio is None:
            raise ValueError(
                "mes_fim/ano_fim exigem mes_inicio/ano_inicio preenchidos"
            )

        normalized = {
            'numero_classe_termica': self._as_int(
                'numero_classe_termica',
                values['numero_classe_termica'],
                1,
                self._SENTINEL - 1,
            ),
            'novo_custo': self._as_float(
                'novo_custo', values['novo_custo'], 0.0, 9999.99, decimals=2
            ),
            'mes_inicio': mes_inicio,
            'ano_inicio': ano_inicio,
            'mes_fim': mes_fim,
            'ano_fim': ano_fim,
        }
        return normalized

    def ler(self, file_name: str, dger) -> None:
        """
        Le o CLAST.DAT e preenche o cadastro de classes termicas e as
        alteracoes temporais de custo.

        :param file_name: string com o caminho completo para o arquivo
        :param dger: classe Dger, usada para saber o numero de anos do
               horizonte de planejamento (quantidade de custos por classe)

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._numero_registros_ = 0
        self.numero_classes = 0
        self.numero_alteracoes = 0
        self.nanos = dger.num_anos['valor']
        self._mapa = dict()

        for attr_name, value_name in set(self._FIELD_MAP_CLASSE.values()) | set(
                self._FIELD_MAP_ALTERACAO.values()):
            getattr(self, attr_name)[value_name] = list()

        with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

            self.next_line(f)  # Cabecalho do bloco Tipo 1
            self.next_line(f)  # Cabecalho do bloco Tipo 1
            self._numero_registros_ += 2

            # Bloco Tipo 1 - cadastro das classes termicas, ate o sentinela
            while True:

                self.next_line(f)
                linha = self.linha.rstrip('\r\n')
                self._numero_registros_ += 1

                codigo = int(linha[1:5])
                if codigo == self._SENTINEL:
                    break

                self._numero_classe_termica['valor'].append(codigo)
                self._nome_classe_termica['valor'].append(linha[6:18].strip())
                self._tipo_combustivel['valor'].append(linha[19:29].strip())

                custos = []
                for iano in range(self.nanos):
                    inicio = 30 + iano * 8
                    fim = inicio + 7
                    custos.append(self._read_float(linha[inicio:fim]))
                self._custos['valor'].append(custos)

                self._mapa[codigo] = self.numero_classes
                self.numero_classes += 1

            self.next_line(f)  # Cabecalho do bloco Tipo 2
            self.next_line(f)  # Cabecalho do bloco Tipo 2
            self._numero_registros_ += 2

            # Bloco Tipo 2 - alteracoes temporais de custo, ate o fim do arquivo
            try:
                while True:

                    self.next_line(f)
                    linha = self.linha.rstrip('\r\n')
                    self._numero_registros_ += 1

                    if not linha.strip():
                        continue

                    self._alt_numero_classe_termica['valor'].append(
                        int(linha[1:5])
                    )
                    self._alt_novo_custo['valor'].append(
                        float(linha[8:15])
                    )
                    self._alt_mes_inicio['valor'].append(
                        self._read_int(linha[17:19])
                    )
                    self._alt_ano_inicio['valor'].append(
                        self._read_int(linha[20:24])
                    )
                    self._alt_mes_fim['valor'].append(
                        self._read_int(linha[26:28])
                    )
                    self._alt_ano_fim['valor'].append(
                        self._read_int(linha[29:33])
                    )

                    self.numero_alteracoes += 1

            except StopIteration:
                pass

        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve todos os registros fisicos do CLAST.DAT (blocos Tipo 1 e Tipo 2).

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        self._numero_registros_ = 0

        diretorio = os.path.split(file_out)[0]
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        classes = []
        for iclasse in range(self.numero_classes):
            linha = {
                field: getattr(self, self._FIELD_MAP_CLASSE[field][0])[
                    self._FIELD_MAP_CLASSE[field][1]
                ][iclasse]
                for field in self._CLASSE_FIELDS
            }
            classes.append(self._normalize_classe_fields(linha))

        alteracoes = []
        for ialt in range(self.numero_alteracoes):
            linha = {
                field: getattr(self, self._FIELD_MAP_ALTERACAO[field][0])[
                    self._FIELD_MAP_ALTERACAO[field][1]
                ][ialt]
                for field in self._ALTERACAO_FIELDS
            }
            alteracoes.append(self._normalize_alteracao_fields(linha))

        nanos = self.nanos or 0

        with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

            f.write(
                " NUM  NOME CLASSE  TIPO COMB.  " + "CUSTO   " * nanos + "\n"
            )
            f.write(
                (" XXXX XXXXXXXXXXXX XXXXXXXXXX " + "XXXX.XX " * nanos).rstrip()
                + "\n"
            )

            for registro in classes:
                prefixo = " {numero_classe_termica:>4d} {nome_classe_termica:<12} " \
                          "{tipo_combustivel:<10} ".format(**registro)
                custos_txt = " ".join(
                    f"{custo:>7.2f}" for custo in registro['custos']
                )
                f.write(prefixo + custos_txt + "\n")
                self._numero_registros_ += 1

            f.write(f" {self._SENTINEL:>4d}\n")
            self._numero_registros_ += 1

            f.write(" NUM     CUSTO\n")
            f.write(" XXXX   XXXX.XX  XX XXXX  XX XXXX\n")

            for registro in alteracoes:
                linha = " {numero_classe_termica:>4d}   {novo_custo:>7.2f}".format(
                    **registro
                )
                if registro['mes_inicio'] is not None:
                    linha += "  {mes_inicio:>2d} {ano_inicio:>4d}".format(**registro)
                    if registro['mes_fim'] is not None:
                        linha += "  {mes_fim:>2d} {ano_fim:>4d}".format(**registro)
                f.write(linha + "\n")
                self._numero_registros_ += 1

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def _get_classe(self, entrada, copy_values):
        if isinstance(entrada, np.generic):
            entrada = entrada.item()

        if isinstance(entrada, bool):
            raise TypeError("entrada deve ser codigo numerico ou nome")
        if isinstance(entrada, Integral):
            posicao = self._position_for_code(int(entrada))
            if posicao is None:
                return None
        elif isinstance(entrada, Real):
            numeric = float(entrada)
            if not math.isfinite(numeric) or not numeric.is_integer():
                raise ValueError("codigo numerico deve ser um inteiro exato")
            posicao = self._position_for_code(int(numeric))
            if posicao is None:
                return None
        elif isinstance(entrada, str):
            posicao = None
            for i, valor in enumerate(self._nome_classe_termica['valor']):
                if valor.strip().upper() == entrada.strip().upper():
                    posicao = i
                    break
            if posicao is None:
                return None
        else:
            raise TypeError("entrada deve ser codigo numerico ou nome")

        classe = {
            field: getattr(self, attr_name)[value_name][posicao]
            for field, (attr_name, value_name) in self._FIELD_MAP_CLASSE.items()
        }
        classe['nome_classe_termica'] = classe['nome_classe_termica'].strip()
        classe['tipo_combustivel'] = classe['tipo_combustivel'].strip()

        if copy_values:
            classe['numero_classe_termica_original'] = classe['numero_classe_termica']
            return deepcopy(classe)
        return classe

    def get(self, entrada):
        """
        Retorna o dicionario completo e independente de uma classe termica
        (bloco Tipo 1). ``entrada`` aceita o codigo (inteiro ou real integral)
        ou o nome. A chave ``numero_classe_termica_original`` preserva a
        identidade atraves de ``deepcopy`` e nao deve ser modificada.
        """
        return self._get_classe(entrada, copy_values=True)

    def put(self, classe):
        """
        Atualiza uma classe termica (bloco Tipo 1) a partir do dicionario
        completo retornado por get(). ``numero_classe_termica`` identifica o
        registro e nao e editavel.

        :param classe: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(classe, dict):
            raise TypeError("classe deve ser um dicionario completo")

        required = set(self._FIELD_MAP_CLASSE)
        received = set(classe)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        allowed = required | {'numero_classe_termica_original'}
        unknown = sorted(received - allowed)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        normalized = self._normalize_classe_fields(classe)
        codigo = normalized['numero_classe_termica']
        codigo_original = self._as_int(
            'numero_classe_termica_original',
            classe.get('numero_classe_termica_original', codigo),
            1,
            self._SENTINEL - 1,
        )
        if codigo != codigo_original:
            raise ValueError(
                "numero_classe_termica identifica a classe e nao pode ser alterado"
            )
        posicao = self._position_for_code(codigo_original)
        if posicao is None:
            raise ValueError(
                f"numero_classe_termica {codigo_original} nao corresponde a "
                "uma classe existente"
            )

        updates = {
            field: deepcopy(value)
            for field, value in classe.items()
            if field in self._FIELD_MAP_CLASSE and field != 'numero_classe_termica'
        }
        updates.update(normalized)
        updates.pop('numero_classe_termica')

        for field, value in updates.items():
            attr_name, value_name = self._FIELD_MAP_CLASSE[field]
            getattr(self, attr_name)[value_name][posicao] = value

        return 'sucesso'

    def get_alteracao(self, indice):
        """
        Retorna o dicionario completo e independente de uma alteracao de
        custo (bloco Tipo 2), pela sua posicao (0-based) na lista de
        alteracoes. A chave ``indice_original`` preserva a identidade e nao
        deve ser modificada.
        """
        indice = self._as_int('indice', indice, 0, self.numero_alteracoes - 1)

        alteracao = {
            field: getattr(self, attr_name)[value_name][indice]
            for field, (attr_name, value_name) in self._FIELD_MAP_ALTERACAO.items()
        }
        alteracao['indice_original'] = indice
        return deepcopy(alteracao)

    def put_alteracao(self, alteracao):
        """
        Atualiza uma alteracao de custo (bloco Tipo 2) a partir do dicionario
        completo retornado por get_alteracao(). A posicao e identificada por
        ``indice_original`` e nao e editavel.

        :param alteracao: dicionario completo retornado por :meth:`get_alteracao`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(alteracao, dict):
            raise TypeError("alteracao deve ser um dicionario completo")

        required = set(self._FIELD_MAP_ALTERACAO) | {'indice_original'}
        received = set(alteracao)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        unknown = sorted(received - required)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        indice = self._as_int(
            'indice_original', alteracao['indice_original'],
            0, self.numero_alteracoes - 1
        )

        normalized = self._normalize_alteracao_fields(alteracao)

        for field, value in normalized.items():
            attr_name, value_name = self._FIELD_MAP_ALTERACAO[field]
            getattr(self, attr_name)[value_name][indice] = value

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave dos dicionarios obtidos por
        get() ou get_alteracao().

        :param parametro: string contendo a chave cujo detalhamento e desejado

        """

        if parametro == 'numero_classe_termica_original':
            return (
                'Identidade original da classe termica; metadado somente '
                'leitura usado por put para impedir alteracao de '
                'numero_classe_termica'
            )
        if parametro == 'indice_original':
            return (
                'Posicao original da alteracao de custo; metadado somente '
                'leitura usado por put_alteracao para impedir alteracao de '
                'posicao'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_classes(self):
        """
        Calcula um generator contendo todos os codigos de referencia das
        classes termicas pertencentes ao CLAST.

        """

        for i in range(self.numero_classes):
            yield self._numero_classe_termica['valor'][i]
