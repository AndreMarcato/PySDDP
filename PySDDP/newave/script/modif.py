import os
import math
from copy import deepcopy
from numbers import Integral, Real
from typing import IO
import pandas as pd
import numpy as np

from PySDDP.newave.script.templates.modif import ModifTemplate


class Modif(ModifTemplate):
    """
    Le, expoe, altera em memoria e escreve o arquivo MODIF.DAT.

    O MODIF.DAT nao possui uma chave unica por registro: uma mesma usina hidreletrica pode ter varias
    modificacoes de cadastro (uma por palavra-chave/vigencia) ao longo do arquivo. Por isso, assim como
    Expt.get/Expt.put e Manutt.get/Manutt.put, a identidade de cada modificacao em Modif.get/Modif.put e a sua
    posicao (indice, 0-based) na lista de modificacoes, preservada pela chave somente-leitura
    ``indice_original``.
    """

    _FIELD_MAP = {
        'codigo': ('_codigo', 'valor'),
        'comentario': ('_comentario', 'valor'),
        'palavra_chave': ('_palavra_chave', 'valor'),
        'valorA': ('_valorA', 'valor'),
        'valorB': ('_valorB', 'valor'),
        'mes': ('_mes', 'valor'),
        'ano': ('_ano', 'valor'),
    }
    _MODIF_FIELDS = tuple(_FIELD_MAP)

    # Palavras-chave sem vigencia temporal e com valorB=None (somente valorA escalar)
    _PALAVRAS_LISTA0 = ('NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'VAZMIN', 'NUMBAS')
    # Palavras-chave sem vigencia temporal, com valorA escalar e valorB obrigatorio
    _PALAVRAS_LISTA1 = ('NUMMAQ', 'POTEFE', 'COEFEVAP', 'VOLMIN', 'VOLMAX')
    # Palavras-chave cujo valorA e uma lista de 5 coeficientes polinomiais; valorB=None
    _PALAVRAS_LISTA2 = ('COTAREA', 'VOLCOTA')
    # Palavras-chave com vigencia (mes/ano) e valorB=None
    _PALAVRAS_LISTA3 = ('CFUGA', 'VAZMINT', 'CMONT')
    # Palavras-chave com vigencia (mes/ano) e valorB obrigatorio
    _PALAVRAS_LISTA4 = ('VMINP', 'VMINT', 'VMAXT')
    _PALAVRAS_VALIDAS = frozenset(
        _PALAVRAS_LISTA0 + _PALAVRAS_LISTA1 + _PALAVRAS_LISTA2 + _PALAVRAS_LISTA3 + _PALAVRAS_LISTA4
    )

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_modifs = None
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

    def _normalize_modif_fields(self, values):
        """Valida e normaliza os sete campos fisicos de um registro do MODIF."""
        palavra = values['palavra_chave']
        if not isinstance(palavra, str):
            raise TypeError("palavra_chave deve ser string")
        palavra_norm = palavra.strip().upper()
        if palavra_norm not in self._PALAVRAS_VALIDAS:
            permitidos = ", ".join(sorted(self._PALAVRAS_VALIDAS))
            raise ValueError(f"palavra_chave deve ser uma de: {permitidos}")

        comentario = values['comentario']
        if not isinstance(comentario, str):
            raise TypeError("comentario deve ser string")
        try:
            comentario.encode('latin-1')
        except UnicodeEncodeError as err:
            raise ValueError("comentario deve ser representavel em latin-1") from err

        valorA = values['valorA']
        if palavra_norm in self._PALAVRAS_LISTA2:
            try:
                valorA = [float(v) for v in valorA]
            except TypeError as err:
                raise TypeError(
                    "valorA deve ser uma sequencia de 5 coeficientes numericos para "
                    f"a palavra-chave {palavra_norm}"
                ) from err
            except ValueError as err:
                raise ValueError(
                    "valorA deve conter apenas coeficientes numericos"
                ) from err
            if len(valorA) != 5:
                raise ValueError("valorA deve possuir exatamente 5 coeficientes")
            if not all(math.isfinite(v) for v in valorA):
                raise ValueError("valorA deve conter apenas valores finitos")
        else:
            valorA = self._as_float('valorA', valorA, -1e9, 1e9)

        valorB = values['valorB']
        if palavra_norm in self._PALAVRAS_LISTA1 or palavra_norm in self._PALAVRAS_LISTA4:
            if valorB is None:
                raise ValueError(f"valorB e obrigatorio para a palavra-chave {palavra_norm}")
            valorB = str(valorB)
        else:
            if valorB is not None:
                raise ValueError(f"valorB deve ser None para a palavra-chave {palavra_norm}")

        mes = values['mes']
        ano = values['ano']
        if palavra_norm in self._PALAVRAS_LISTA3 or palavra_norm in self._PALAVRAS_LISTA4:
            mes = self._as_int('mes', mes, 1, 12)
            ano = self._as_int('ano', ano, 0, 9999)
        else:
            mes = self._as_int('mes', mes, 0, 0)
            ano = self._as_int('ano', ano, 0, 0)

        normalized = {
            'codigo': self._as_int('codigo', values['codigo'], 1, 9999),
            'comentario': comentario,
            'palavra_chave': palavra_norm,
            'valorA': valorA,
            'valorB': valorB,
            'mes': mes,
            'ano': ano,
        }
        return normalized

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo MODIF.DAT que contem as modificacoes cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo,
               confhd: classe contendo a configuracao de todas as usinas hidreletrica pertencentes ao estudo,
        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self.numero_modifs = 0

        # listas referentes ao dicionário USINA, apontando para as mesmas listas expostas pelo template
        # (self._codigo['valor'], self._comentario['valor'], ...) seguindo o padrao factory das demais subclasses
        for attr_name, value_name in set(self._FIELD_MAP.values()):
            getattr(self, attr_name)[value_name] = list()

        self.usina = {
            field: getattr(self, attr_name)[value_name]
            for field, (attr_name, value_name) in self._FIELD_MAP.items()
        }

        lista0 = ( 'NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'VAZMIN', 'NUMBAS',
                   'numcnj', 'prodesp', 'teif', 'ip', 'perdhidr', 'vazmin', 'numbas')

        lista1 = ( 'NUMMAQ', 'POTEFE', 'COEFEVAP', 'VOLMIN', 'VOLMAX',
                   'nummaq', 'potefe', 'coefevap', 'volmin', 'volmax')

        lista2 = ( 'COTAREA', 'VOLCOTA', 'cotaarea', 'volcota')

        lista3 = ( 'CFUGA', 'VAZMINT', 'CMONT',
                   'cfuga', 'vazmint', 'cmont')

        lista4 = ( 'VMINP', 'VMINT', 'VMAXT', 'vminp', 'vmint', 'vmaxt')

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                self.next_line(f)
                self.next_line(f)
                self.next_line(f)

                linha = self.linha

                continua = True

                while continua:
                    self.numero_modifs += 1
                    codigo = int(linha[10:30])
                    comentario = linha[30:]
                    self.next_line(f)
                    linha = self.linha
                    pal_chave = linha[1:9]
                    pal_chave = pal_chave.strip()
                    while pal_chave.upper() != 'USINA':
                        if pal_chave in lista0:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[0]))
                            self.usina['valorB'].append(None)
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista1:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[0]))
                            self.usina['valorB'].append(linha[9:].strip().split()[1])
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista2:
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            polinomio = []
                            polinomio.append(float(linha[9:].strip().split()[0]))
                            polinomio.append(float(linha[9:].strip().split()[1]))
                            polinomio.append(float(linha[9:].strip().split()[2]))
                            polinomio.append(float(linha[9:].strip().split()[3]))
                            polinomio.append(float(linha[9:].strip().split()[4]))
                            self.usina['valorA'].append(polinomio)
                            self.usina['valorB'].append(None)
                            self.usina['mes'].append(0)
                            self.usina['ano'].append(0)
                        elif pal_chave in lista3:
                            pal_chave.split()[0]
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[2]))
                            self.usina['valorB'].append(None)
                            mes = linha[9:].strip().split()[0]
                            mes = int(mes)
                            self.usina['mes'].append(mes)
                            ano = linha[9:].strip().split()[1]
                            ano = int(ano)
                            self.usina['ano'].append(ano)
                        elif pal_chave in lista4:
                            pal_chave.split()[0]
                            self.usina['codigo'].append(codigo)
                            self.usina['comentario'].append(comentario.strip())
                            self.usina['palavra_chave'].append(pal_chave)
                            self.usina['valorA'].append(float(linha[9:].strip().split()[2]))
                            self.usina['valorB'].append(linha[9:].strip().split()[3])
                            mes = linha[9:].strip().split()[0]
                            mes = int(mes)
                            self.usina['mes'].append(mes)
                            ano = linha[9:].strip().split()[1]
                            ano = int(ano)
                            self.usina['ano'].append(ano)
                        self.next_line(f)
                        linha = self.linha
                        pal_chave = linha[1:9]
                        pal_chave = pal_chave.strip()


        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_usina['df'] = pd.DataFrame(self.usina, columns = [ 'ano', 'codigo', 'comentario',
                                                                                'mes', 'palavra_chave',
                                                                                'valorA', 'valorB'] )
                # 'valorA'/'valorB' guardam tipos heterogeneos (escalar, lista de coeficientes ou None,
                # dependendo da palavra_chave); forcar dtype 'object' evita que o pandas infira um dtype
                # numerico quando o arquivo lido nao contem nenhum registro tipo COTAREA/VOLCOTA, o que
                # impediria put() de gravar uma lista de coeficientes na celula.
                self.bloco_usina['df']['valorA'] = self.bloco_usina['df']['valorA'].astype(object)
                self.bloco_usina['df']['valorB'] = self.bloco_usina['df']['valorB'].astype(object)

                print('OK! Leitura do', self.nome_arquivo ,'realizada com sucesso. (', self.numero_modifs,
                      'Usinas Hidraulicas Modificadas )')
            else:
                raise

        return

    def escrever(self, file_out: str) -> None:

        lista0 = ( 'NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'VAZMIN', 'NUMBAS',
                   'numcnj', 'prodesp', 'teif', 'ip', 'perdhidr', 'vazmin', 'numbas')

        lista1 = ( 'NUMMAQ', 'POTEFE', 'COEFEVAP', 'VOLMIN', 'VOLMAX',
                   'nummaq', 'potefe', 'coefevap', 'volmin', 'volmax')

        lista2 = ( 'COTAREA', 'VOLCOTA', 'cotaarea', 'volcota')

        lista3 = ( 'CFUGA', 'VAZMINT', 'CMONT',
                   'cfuga', 'vazmint', 'cmont')

        lista4 = ( 'VMINP', 'VMINT', 'VMAXT', 'vminp', 'vmint', 'vmaxt')

        df = self.bloco_usina['df']

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                f.write(" P.CHAVE  MODIFICACOES E INDICES \n" )
                f.write(" XXXXXXXX XXXXXXXXXXXXXXXXXXXXX \n" )

                tamanho = df.shape
                tamanho = tamanho[0]

                linha = 0

                conta_usi = 0

                while linha < tamanho:

                    registro = df.iloc[linha].values
                    codigo = int(registro[1])
                    comentario = registro[2]
                    conta_usi += 1

                    #
                    # Cria dataframe apenas com a usina. Este procedimento é para manter a ordem do arquivo original
                    #

                    usinadf = df[df['codigo'] == codigo]
                    nr_reg = usinadf.shape
                    nr_reg = nr_reg[0]
                    reg = 0

                    formato = " {key: <8} {codigo: <33} {comentarios: <40}\n"

                    row = dict(
                        key='USINA',
                        codigo=codigo,
                        comentarios=comentario
                    )
                    f.write(formato.format(**row))

                    while reg < nr_reg:
                        registro = usinadf.iloc[reg].values

                        if registro[4] in lista0:
                            if ( registro[4].upper() == 'NUMCNJ' or
                                 registro[4].upper() == 'VAZMIN' or
                                 registro[4].upper() == 'NUMBAS'):
                                formato = " {key: <8} {valor: >6d}\n"
                            elif ( registro[4].upper() == 'PRODESP' ):
                                formato = " {key: <8} {valor: >12.8f}\n"
                            else:
                                formato = " {key: <8} {valor: >6.3f}\n"
                            row = dict(
                                        key=registro[4],
                                        valor=int(registro[5])
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista1:
                            if ( registro[4].upper() == 'NUMMAQ' or registro[4].upper() == 'COEFEVAP' ):
                                formato = " {key: <8} {valor: >6d} {valorb: <3d}\n"
                                row = dict(
                                            key=registro[4],
                                            valor=int(registro[5]),
                                            valorb=int(registro[6])
                                          )
                            elif ( registro[4].upper() == 'VOLMIN' or registro[4].upper() == 'VOLMAX' ):
                                formato = " {key: <8} {valor: >10.3f} {valorb: <3}\n"
                                row = dict(
                                    key=registro[4],
                                    valor=registro[5],
                                    valorb=registro[6]
                                )
                            else:
                                formato = " {key: <8} {valor: >10.4f} {valorb: <2d}\n"
                                row = dict(
                                            key=registro[4],
                                            valor=registro[5],
                                            valorb=int(registro[6])
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista2:
                            formato = " {key: <8} {a: >10} {b: <10} {c: >10} {d: >10} {e: >10}\n"
                            row = dict(
                                        key=registro[4],
                                        a=registro[5][0],
                                        b=registro[5][1],
                                        c=registro[5][2],
                                        d=registro[5][3],
                                        e=registro[5][4],
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista3:
                            formato = " {key: <8} {mes:>2} {ano:>4} {valor: >7.3f}\n"
                            row = dict(
                                        key=registro[4],
                                        ano=registro[0],
                                        mes=registro[3],
                                        valor=registro[5]
                                      )
                            f.write(formato.format(**row))
                        if registro[4] in lista4:
                            formato = " {key: <8} {mes:>2} {ano:>4} {valor: >7.3f} {valorb: <3}\n"
                            row = dict(
                                        key=registro[4],
                                        ano=registro[0],
                                        mes=registro[3],
                                        valor=registro[5],
                                        valorb=registro[6]
                                      )
                            f.write(formato.format(**row))
                        reg += 1
                    #
                    # Pula para próxima usina
                    #
                    registro = df.iloc[linha].values
                    codigo = int(registro[1])
                    while codigo == int(registro[1]):
                        linha += 1
                        if linha == tamanho:
                            break
                        registro = df.iloc[linha].values

            print('OK! Escrita do', os.path.split(file_out)[1] ,'realizada com sucesso. (', conta_usi,
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
        Retorna o dicionario completo e independente de uma modificacao do MODIF, pela sua posicao (0-based) na
        lista de modificacoes. A chave ``indice_original`` preserva essa identidade e nao deve ser modificada.
        """
        return self._get(indice, copy_values=True)

    def put(self, modificacao):
        """
        Atualiza uma modificacao do MODIF a partir do dicionario completo retornado por get(). A posicao e
        identificada por ``indice_original`` e nao e editavel.

        :param modificacao: dicionario completo retornado por :meth:`get`
        :returns: ``"sucesso"`` para compatibilidade com a API existente
        """
        if not isinstance(modificacao, dict):
            raise TypeError("modificacao deve ser um dicionario completo")

        required = set(self._FIELD_MAP) | {'indice_original'}
        received = set(modificacao)
        missing = sorted(required - received)
        if missing:
            raise KeyError(
                "chaves obrigatorias ausentes: " + ", ".join(missing)
            )
        unknown = sorted(received - required)
        if unknown:
            raise KeyError("chaves desconhecidas: " + ", ".join(unknown))

        indice = self._as_int(
            'indice_original', modificacao['indice_original'],
            0, len(self._codigo['valor']) - 1
        )

        normalized = self._normalize_modif_fields(modificacao)

        for field, value in normalized.items():
            attr_name, value_name = self._FIELD_MAP[field]
            getattr(self, attr_name)[value_name][indice] = deepcopy(value)
            if self.bloco_usina['df'] is not None:
                self.bloco_usina['df'].at[indice, field] = deepcopy(value)

        return 'sucesso'

    def help(self, parametro):
        """
        Detalha o tipo de informacao de uma chave do dicionario obtido por get().

        :param parametro: string contendo a chave cujo detalhamento e desejado

        """

        if parametro == 'indice_original':
            return (
                'Posicao original da modificacao do MODIF; metadado somente leitura usado por put para impedir '
                'alteracao de posicao'
            )

        duvida = getattr(self, '_' + parametro)

        return duvida['descricao']

    def lista_registros(self):
        """
        Calcula um generator contendo as posicoes (0-based) de todas as modificacoes pertencentes ao MODIF.

        """

        for i in range(len(self._codigo['valor'])):
            yield i
