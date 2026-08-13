import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO
import pandas as pd
import numpy as np

from PySDDP.newave.script.templates.exph import ExphTemplate


class Exph(ExphTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo EXPH.DAT.

    O EXPH.DAT nao possui uma chave unica por registro: uma mesma usina hidreletrica pode ter varios registros
    (enchimento do volume morto e/ou entrada de maquinas) ao longo do arquivo. Por isso, assim como
    Expt.get/Expt.put e Manutt.get/Manutt.put, a identidade de cada registro em Exph.get/Exph.put e a sua posicao
    (indice, 0-based) na lista de registros, preservada pela chave somente-leitura ``indice_original``.
    """

    _FIELD_MAP = {
        'codigo': ('_codigo', 'valor'),
        'nome': ('_nome', 'valor'),
        'mesi_evm': ('_mesi_evm', 'valor'),
        'anoi_evm': ('_anoi_evm', 'valor'),
        'dura_evm': ('_dura_evm', 'valor'),
        'perc_evm': ('_perc_evm', 'valor'),
        'mesi_tur': ('_mesi_tur', 'valor'),
        'anoi_tur': ('_anoi_tur', 'valor'),
        'comentar': ('_comentar', 'valor'),
        'nume_tur': ('_nume_tur', 'valor'),
        'nume_cnj': ('_nume_cnj', 'valor'),
    }
    _EXPH_FIELDS = tuple(_FIELD_MAP)

    # Campos preenchidos em um registro tipo 1 (enchimento de volume morto)
    _GRUPO_ENCHIMENTO = ('mesi_evm', 'anoi_evm', 'dura_evm', 'perc_evm')
    # Campos preenchidos em um registro tipo 2 (entrada de maquina/conjunto)
    _GRUPO_TURBINAMENTO = ('mesi_tur', 'anoi_tur', 'comentar', 'nume_tur', 'nume_cnj')

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_exps = None
        self.usina = dict()

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

    @classmethod
    def _as_optional_float(cls, field, value, minimum, maximum, decimals=None):
        """Como _as_float, mas preserva None para campos opcionais em branco."""
        if value is None:
            return None
        return cls._as_float(field, value, minimum, maximum, decimals=decimals)

    @staticmethod
    def _as_optional_str(field, value):
        """Valida um campo textual opcional (None ou string)."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError(f"{field} deve ser string")
        return value

    def _normalize_exph_fields(self, values):
        """Valida e normaliza os onze campos fisicos de um registro do EXPH."""
        nome = values['nome']
        if not isinstance(nome, str):
            raise TypeError("nome deve ser string")
        try:
            nome.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError("nome deve ser representavel em latin-1") from err
        if len(nome.rstrip()) > 12:
            raise ValueError("nome deve possuir no maximo 12 caracteres")

        preenchidos_enchimento = [values[campo] is not None for campo in self._GRUPO_ENCHIMENTO]
        preenchidos_turbinamento = [values[campo] is not None for campo in self._GRUPO_TURBINAMENTO]

        if any(preenchidos_enchimento) and not all(preenchidos_enchimento):
            raise ValueError(
                "mesi_evm, anoi_evm, dura_evm e perc_evm devem estar todos preenchidos ou todos em branco"
            )
        if any(preenchidos_turbinamento) and not all(preenchidos_turbinamento):
            raise ValueError(
                "mesi_tur, anoi_tur, comentar, nume_tur e nume_cnj devem estar todos preenchidos ou todos em "
                "branco"
            )
        if all(preenchidos_enchimento) == all(preenchidos_turbinamento):
            raise ValueError(
                "um registro do EXPH deve preencher exatamente um dos grupos: enchimento de volume morto "
                "(mesi_evm/anoi_evm/dura_evm/perc_evm) ou entrada de maquina (mesi_tur/anoi_tur/comentar/"
                "nume_tur/nume_cnj)"
            )

        normalized = {
            'codigo': self._as_int('codigo', values['codigo'], 1, 9999),
            'nome': nome,
            'mesi_evm': self._as_optional_int('mesi_evm', values['mesi_evm'], 1, 12),
            'anoi_evm': self._as_optional_int('anoi_evm', values['anoi_evm'], 0, 9999),
            'dura_evm': self._as_optional_int('dura_evm', values['dura_evm'], 0, 99),
            'perc_evm': self._as_optional_float('perc_evm', values['perc_evm'], 0.0, 100.0, decimals=1),
            'mesi_tur': self._as_optional_int('mesi_tur', values['mesi_tur'], 1, 12),
            'anoi_tur': self._as_optional_int('anoi_tur', values['anoi_tur'], 0, 9999),
            'comentar': self._as_optional_str('comentar', values['comentar']),
            'nume_tur': self._as_optional_int('nume_tur', values['nume_tur'], 0, 99),
            'nume_cnj': self._as_optional_int('nume_cnj', values['nume_cnj'], 0, 9),
        }
        return normalized

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo EXPH.DAT que contem a expansão das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               confhd: classe contendo a configuracao de todas as usinas hidreletrica pertencentes ao estudo,
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_exps = 0

        # listas referentes ao dicionário USINA, apontando para as mesmas listas expostas pelo template
        # (self._codigo['valor'], self._nome['valor'], ...) seguindo o padrao factory das demais subclasses
        for attr_name, value_name in set(self._FIELD_MAP.values()):
            getattr(self, attr_name)[value_name] = list()

        self.usina = {
            field: getattr(self, attr_name)[value_name]
            for field, (attr_name, value_name) in self._FIELD_MAP.items()
        }

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho
                self.next_line(f)   # Linha de cabeçalho

                self.next_line(f)

                linha = self.linha

                continua = True

                while continua:
                    self.numero_exps += 1

                    codigo = int(linha[0:4])
                    nome = linha[5:17]

                    if linha[18:20] != '  ':
                        #
                        # Usina está enchendo o VM no início do estudo ou irá começar encher o VM no decorrer do estudo
                        #
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(int(linha[18:20]))
                        self.usina['anoi_evm'].append(int(linha[21:25]))
                        self.usina['dura_evm'].append(int(linha[31:33]))
                        self.usina['perc_evm'].append(float(linha[37:42]))
                        self.usina['mesi_tur'].append(None)
                        self.usina['anoi_tur'].append(None)
                        self.usina['comentar'].append(None)
                        self.usina['nume_tur'].append(None)
                        self.usina['nume_cnj'].append(None)
                    else:
                        #
                        # Usina já encheu o VM antes do início do estudo, mas receberá mais máquinas
                        #
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(None)
                        self.usina['anoi_evm'].append(None)
                        self.usina['dura_evm'].append(None)
                        self.usina['perc_evm'].append(None)
                        self.usina['mesi_tur'].append(int(linha[44:46]))
                        self.usina['anoi_tur'].append(int(linha[47:51]))
                        self.usina['comentar'].append(linha[52:59])
                        self.usina['nume_tur'].append(int(linha[60:62]))
                        self.usina['nume_cnj'].append(int(linha[63:65]))

                    self.next_line(f)
                    linha = self.linha

                    #
                    # Inserção de máquinas restantes
                    #
                    while linha[0:4] != '9999':
                        self.usina['codigo'].append(codigo)
                        self.usina['nome'].append(nome)
                        self.usina['mesi_evm'].append(None)
                        self.usina['anoi_evm'].append(None)
                        self.usina['dura_evm'].append(None)
                        self.usina['perc_evm'].append(None)
                        self.usina['mesi_tur'].append(int(linha[44:46]))
                        self.usina['anoi_tur'].append(int(linha[47:51]))
                        self.usina['comentar'].append(linha[52:59])
                        self.usina['nume_tur'].append(int(linha[60:62]))
                        self.usina['nume_cnj'].append(int(linha[64:65]))
                        self.next_line(f)
                        linha = self.linha

                    #
                    # Passa para a próxima usina
                    #
                    self.next_line(f)
                    linha = self.linha

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_usina['df'] = pd.DataFrame(self.usina, columns = [ 'codigo',
                                                                              'nome',
                                                                              'mesi_evm',
                                                                              'anoi_evm',
                                                                              'dura_evm',
                                                                              'perc_evm',
                                                                              'mesi_tur',
                                                                              'anoi_tur',
                                                                              'comentar',
                                                                              'nume_tur',
                                                                              'nume_cnj'] )
                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso. (', self.numero_exps,
                      'Usinas Hidraulicas Expandidas )')
            else:
                raise

        return

    def escrever(self, file_out: str) -> None:

        df = self.bloco_usina['df']

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write("COD  NOME        ENCHIMENTO  VOLUME MORTO    DATA    POT.   MQ CJ\n" )
                f.write("                  INICIO    DUR.MESES  %    ENTRADA\n" )
                f.write("XXXX XXXXXXXXXXXX XX/XXXX      XX     XX.X  XX/XXXX XXXX.X\n")

                tamanho = df.shape
                tamanho = tamanho[0]

                linha = 0

                conta_usi = 0

                while linha < tamanho:

                    registro = df.iloc[linha].values
                    codigo = int(registro[0])
                    conta_usi += 1

                    #
                    # Cria dataframe apenas com a usina. Este procedimento é para manter a ordem do arquivo original
                    #

                    usinadf = df[df['codigo'] == codigo]
                    nr_reg = usinadf.shape
                    nr_reg = nr_reg[0]
                    reg = 0


                    if not np.isnan(registro[2]):
                        formato = "{codigo: >4} {nome: <12} {mesi_evm: >2}/{anoi_evm: <4}      {dura_evm: >2}     {perc_evm: >4.1f}\n"
                        row = dict(
                            codigo=int(registro[0]),
                            nome=registro[1],
                            mesi_evm=int(registro[2]),
                            anoi_evm=int(registro[3]),
                            dura_evm=int(registro[4]),
                            perc_evm=float(registro[5]),
                        )
                    else:
                        formato = "{codigo: >4} {nome: <12} {mesi_tur: >28}/{anoi_tur: <4} {comentar: >7} {nume_tur: >2} {nume_cnj: >2}\n"
                        row = dict(
                                    codigo=int(registro[0]),
                                    nome=registro[1],
                                    mesi_tur=int(registro[6]),
                                    anoi_tur=int(registro[7]),
                                    comentar=registro[8],
                                    nume_tur=int(registro[9]),
                                    nume_cnj=int(registro[10])
                                  )
                    f.write(formato.format(**row))
                    reg += 1

                    while reg < nr_reg:
                        registro = usinadf.iloc[reg].values
                        formato = "{codigo: >4} {nome: <12} {mesi_tur: >28}/{anoi_tur: <4} {comentar: >7} {nume_tur: >2} {nume_cnj: >2}\n"
                        row = dict(
                            codigo="    ",
                            nome="            ",
                            mesi_tur=int(registro[6]),
                            anoi_tur=int(registro[7]),
                            comentar=registro[8],
                            nume_tur=int(registro[9]),
                            nume_cnj=int(registro[10])
                        )
                        f.write(formato.format(**row))
                        reg += 1
                    f.write('9999\n')

                    #
                    # Pula para próxima usina
                    #
                    registro = df.iloc[linha].values
                    codigo = int(registro[0])
                    while codigo == int(registro[0]):
                        linha += 1
                        if linha == tamanho:
                            break
                        registro = df.iloc[linha].values

            print('OK! Escrita do', self.nome_arquivo ,'realizada com sucesso. (', conta_usi,
                  'Usinas Hidraulicas Modificadas )')

        except Exception:
            raise

    def _get(self, indice, copy_values):
        indice = self._as_int('indice', indice, 0, len(self._codigo['valor']) - 1)

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
        Retorna o dicionario completo e independente de um registro do EXPH, pela sua posicao (0-based) na lista
        de registros. A chave ``indice_original`` preserva essa identidade e nao deve ser modificada.
        """
        return self._get(indice, copy_values=True)

    def put(self, registro):
        """
        Atualiza um registro do EXPH a partir do dicionario completo retornado por get(). A posicao e
        identificada por ``indice_original`` e nao e editavel.

        :param registro: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(registro, dict):
            raise TypeError("registro deve ser um dicionario completo")

        required = set(self._FIELD_MAP) | {'indice_original'}
        received = set(registro)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        unknown = sorted(received - required)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        indice = self._as_int(
            'indice_original', registro['indice_original'],
            0, len(self._codigo['valor']) - 1
        )

        normalized = self._normalize_exph_fields(registro)

        for field, value in normalized.items():
            attr_name, value_name = self._FIELD_MAP[field]
            getattr(self, attr_name)[value_name][indice] = value
            if self.bloco_usina['df'] is not None:
                self.bloco_usina['df'].at[indice, field] = value

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario obtido por get().

        :param parametro: string contendo a chave cujo detalhamento e desejado

        """

        if parametro == 'indice_original':
            return (
                'Posicao original do registro do EXPH; metadado somente leitura usado por put para impedir '
                'alteracao de posicao'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_registros(self):
        """
        Calcula um generator contendo as posicoes (0-based) de todos os registros pertencentes ao EXPH.

        """

        for i in range(len(self._codigo['valor'])):
            yield i
