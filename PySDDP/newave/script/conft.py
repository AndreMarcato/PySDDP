import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO

from PySDDP.newave.script.templates.conft import ConftTemplate
import numpy as np


class Conft(ConftTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo CONFT.DAT, que contem um
    registro de configuracao para cada UTE da configuracao termica estudada.

    O arquivo comeca com dois registros de comentario (ignorados) seguidos de
    um registro de dados de largura fixa por usina termica, com sete campos:

        colunas  2- 5 (I4)  codigo_usina
        colunas  7-18 (A12) nome_usina
        colunas 22-25 (I4)  codigo_submercado
        colunas 31-32 (A2)  status (EX/EE/NE/NC)
        colunas 36-39 (I4)  codigo_classe_termica
        colunas 41-43 (I3)  codigo_tecnologia (opcional)
        colunas 45-48 (I4)  codigo_classe_gas (opcional)
    """

    _FIELD_MAP = {
        'codigo_usina': ('_codigo_usina', 'valor'),
        'nome_usina': ('_nome_usina', 'valor'),
        'codigo_submercado': ('_codigo_submercado', 'valor'),
        'status': ('_status', 'valor'),
        'codigo_classe_termica': ('_codigo_classe_termica', 'valor'),
        'codigo_tecnologia': ('_codigo_tecnologia', 'valor'),
        'codigo_classe_gas': ('_codigo_classe_gas', 'valor'),
    }
    _CONFT_FIELDS = tuple(_FIELD_MAP)
    _STATUS_VALUES = frozenset(('EX', 'EE', 'NE', 'NC'))

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
    def _read_int(texto):
        """Converte um campo numerico de largura fixa; em branco vira None."""
        texto = texto.strip()
        return int(texto) if texto else None

    def _position_for_code(self, codigo):
        return self._mapa.get(codigo)

    def _normalize_conft_fields(self, values):
        """Valida e normaliza os sete campos fisicos de um registro CONFT."""
        nome = values['nome_usina']
        if not isinstance(nome, str):
            raise TypeError("nome_usina deve ser string")
        nome = nome.strip()
        try:
            nome.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError("nome_usina deve ser representavel em latin-1") from err
        if len(nome) > 12:
            raise ValueError("nome_usina deve possuir no maximo 12 caracteres")

        status = values['status']
        if not isinstance(status, str):
            raise TypeError("status deve ser string")
        status = status.strip().upper()
        if status not in self._STATUS_VALUES:
            permitidos = ", ".join(sorted(self._STATUS_VALUES))
            raise ValueError(f"status deve ser um de: {permitidos}")

        normalized = {
            'codigo_usina': self._as_int(
                'codigo_usina', values['codigo_usina'], 1, 9999
            ),
            'nome_usina': nome.ljust(12),
            'codigo_submercado': self._as_int(
                'codigo_submercado', values['codigo_submercado'], 0, 9999
            ),
            'status': status,
            'codigo_classe_termica': self._as_int(
                'codigo_classe_termica', values['codigo_classe_termica'], 0, 9999
            ),
            'codigo_tecnologia': self._as_optional_int(
                'codigo_tecnologia', values['codigo_tecnologia'], 0, 999
            ),
            'codigo_classe_gas': self._as_optional_int(
                'codigo_classe_gas', values['codigo_classe_gas'], 0, 9999
            ),
        }
        return normalized

    def ler(self, file_name: str) -> None:
        """
        Le o CONFT.DAT e preenche o cadastro de usinas termicas.

        :param file_name: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._numero_registros_ = 0
        self.numero_usinas = 0
        self._mapa = dict()

        for attr_name, value_name in set(self._FIELD_MAP.values()):
            getattr(self, attr_name)[value_name] = list()

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)  # Linha de cabecalho
                self.next_line(f)  # Linha de cabecalho
                self._numero_registros_ += 2

                while True:

                    self.next_line(f)
                    linha = self.linha.rstrip('\r\n')
                    self._numero_registros_ += 1

                    codigo_texto = linha[1:5].strip()
                    if not codigo_texto:
                        break

                    self._codigo_usina['valor'].append(int(codigo_texto))
                    self._nome_usina['valor'].append(linha[6:18].strip())
                    self._codigo_submercado['valor'].append(
                        self._read_int(linha[21:25])
                    )
                    self._status['valor'].append(linha[30:32].strip())
                    self._codigo_classe_termica['valor'].append(
                        self._read_int(linha[35:39])
                    )
                    self._codigo_tecnologia['valor'].append(
                        self._read_int(linha[40:43])
                    )
                    self._codigo_classe_gas['valor'].append(
                        self._read_int(linha[44:48])
                    )

                    self._mapa[self._codigo_usina['valor'][-1]] = self.numero_usinas
                    self.numero_usinas += 1

        except Exception as err:
            if isinstance(err, StopIteration):
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:
        """
        Escreve todos os registros fisicos do CONFT.DAT.

        :param file_out: string com o caminho completo para o arquivo

        """

        self.dir_base = os.path.split(file_out)[0]
        self.nome_arquivo = os.path.split(file_out)[1]

        self._numero_registros_ = 0

        diretorio = os.path.split(file_out)[0]
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        registros = []
        for iusi in range(self.numero_usinas):
            linha = {
                field: getattr(self, self._FIELD_MAP[field][0])[
                    self._FIELD_MAP[field][1]
                ][iusi]
                for field in self._CONFT_FIELDS
            }
            registros.append(self._normalize_conft_fields(linha))

        with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]
            f.write(" NUM  NOME           SSIS  U.EXIS CLASSE\n")
            f.write(" XXXX XXXXXXXXXXXX   XXXX     XX   XXXX\n")

            for registro in registros:
                linha = (
                    " {codigo_usina:>4d} {nome_usina:<12}   "
                    "{codigo_submercado:>4d}     {status:<2}   "
                    "{codigo_classe_termica:>4d}"
                ).format(**registro)

                if registro['codigo_tecnologia'] is not None:
                    linha += " {:>3d}".format(registro['codigo_tecnologia'])
                    if registro['codigo_classe_gas'] is not None:
                        linha += " {:>4d}".format(registro['codigo_classe_gas'])
                elif registro['codigo_classe_gas'] is not None:
                    linha += "     {:>4d}".format(registro['codigo_classe_gas'])

                f.write(linha + "\n")
                self._numero_registros_ += 1

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def _get(self, entrada, copy_values):
        """
        Busca uma usina termica do CONFT e retorna um dicionario com todos os
        seus campos.

        :param entrada: codigo (inteiro) ou nome (string) da usina

        """

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
            for i, valor in enumerate(self._nome_usina['valor']):
                if valor.strip().upper() == entrada.strip().upper():
                    posicao = i
                    break
            if posicao is None:
                return None
        else:
            raise TypeError("entrada deve ser codigo numerico ou nome")

        usina = {
            field: getattr(self, attr_name)[value_name][posicao]
            for field, (attr_name, value_name) in self._FIELD_MAP.items()
        }
        usina['nome_usina'] = usina['nome_usina'].strip()

        if copy_values:
            usina['codigo_usina_original'] = usina['codigo_usina']
            return deepcopy(usina)
        return usina

    def get(self, entrada):
        """
        Retorna o dicionario completo e independente de uma UTE.

        ``entrada`` aceita o codigo (inteiro ou real integral) ou o nome. A
        chave ``codigo_usina_original`` preserva a identidade atraves de
        ``deepcopy`` e nao deve ser modificada.
        """
        return self._get(entrada, copy_values=True)

    def put(self, usina):
        """
        Atualiza uma UTE a partir do dicionario completo retornado por get().

        ``codigo_usina`` identifica o registro e nao e editavel.

        :param usina: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        :raises TypeError: para dicionario ou tipos incompativeis
        :raises KeyError: para chaves ausentes ou desconhecidas
        :raises ValueError: para identidade ou valores invalidos
        """
        if not isinstance(usina, dict):
            raise TypeError("usina deve ser um dicionario completo")

        required = set(self._FIELD_MAP)
        received = set(usina)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        allowed = required | {'codigo_usina_original'}
        unknown = sorted(received - allowed)
        if unknown:
            raise KeyError(
                "chaves desconhecidas: " + ", ".join(unknown)
            )

        normalized = self._normalize_conft_fields(usina)
        codigo = normalized['codigo_usina']
        codigo_original = self._as_int(
            'codigo_usina_original',
            usina.get('codigo_usina_original', codigo),
            1,
            9999,
        )
        if codigo != codigo_original:
            raise ValueError(
                "codigo_usina identifica a UTE e nao pode ser alterado"
            )
        posicao = self._position_for_code(codigo_original)
        if posicao is None:
            raise ValueError(
                f"codigo_usina {codigo_original} nao corresponde a uma UTE existente"
            )

        updates = {
            field: deepcopy(value)
            for field, value in usina.items()
            if field in self._FIELD_MAP and field != 'codigo_usina'
        }
        updates.update(normalized)
        updates.pop('codigo_usina')

        for field, value in updates.items():
            attr_name, value_name = self._FIELD_MAP[field]
            getattr(self, attr_name)[value_name][posicao] = value

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario obtido por get().

        :param parametro: string contendo a chave do dicionario cujo detalhamento e desejado

        """

        if parametro == 'codigo_usina_original':
            return (
                'Identidade original da UTE; metadado somente leitura usado '
                'por put para impedir alteracao de codigo_usina'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_usinas(self):
        """
        Calcula um generator contendo todos os codigos de referencia das usinas
        pertencentes ao CONFT.

        """

        for i in range(self.numero_usinas):
            yield self._codigo_usina['valor'][i]
