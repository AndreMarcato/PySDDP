"""
Rotinas comuns de layout binario do arquivo HIDR.DAT (cadastro de usinas hidreletricas do CEPEL), usadas pelos
leitores do NEWAVE, DECOMP e DESSEM. Este modulo nao importa nenhum dos modelos.

Layouts confirmados (um registro por usina, sem cabecalho/rodape, little-endian):
    792 bytes -> polinomios cota-volume e cota-area com 5 coeficientes float32 cada (layout antigo)
    832 bytes -> os mesmos polinomios com 5 coeficientes float64 cada (layout novo, observado nos decks
                 NEWAVE v31 de nov/2026); demais campos identicos, deslocados de 40 bytes a partir do offset 104
"""
import os
from typing import IO, Iterable, Optional

REGISTRO_ANTIGO = 792
REGISTRO_NOVO = 832
FMT_POLINOMIO = {REGISTRO_ANTIGO: 'f', REGISTRO_NOVO: 'd'}
# Offsets relativos dos campos data (8s) e tipo_reg (1s) usados para desempatar tamanhos ambiguos
_OFFSETS_VALIDACAO = {REGISTRO_ANTIGO: (736, 791), REGISTRO_NOVO: (776, 831)}


class HidrFormatoError(ValueError):
    """Erro de estrutura/formato do HIDR.DAT (tamanho invalido, layout ambiguo ou campo ilegivel)."""


def _texto_valido(bruto: bytes) -> bool:
    return all(c == 0 or 0x20 <= c <= 0x7E for c in bruto)


def detectar_tamanho_registro(file_name: str, modelo: str = 'NEWAVE') -> int:
    """
    Identifica o tamanho do registro do HIDR.DAT (792 ou 832 bytes) antes de interpretar o arquivo.

    O criterio principal e o tamanho total do arquivo. Se ele for multiplo dos dois layouts, os campos
    textuais data e tipo_reg de todos os registros sao validados em cada layout; se nenhum ou ambos forem
    validos, levanta HidrFormatoError em vez de adivinhar.

    :param file_name: caminho completo para o arquivo
    :param modelo: nome do modelo, usado nas mensagens de erro
    :return: tamanho do registro em bytes
    """
    tamanho = os.stat(file_name).st_size
    if tamanho == 0:
        raise HidrFormatoError(f"{modelo} - {file_name}: arquivo HIDR vazio.")

    candidatos = [r for r in FMT_POLINOMIO if tamanho % r == 0]
    if not candidatos:
        raise HidrFormatoError(
            f"{modelo} - {file_name}: tamanho {tamanho} bytes nao e multiplo de {REGISTRO_ANTIGO} (layout antigo) "
            f"nem de {REGISTRO_NOVO} (layout novo); sobram {tamanho % REGISTRO_ANTIGO} e "
            f"{tamanho % REGISTRO_NOVO} bytes, respectivamente. Arquivo truncado ou formato nao reconhecido.")
    if len(candidatos) == 1:
        return candidatos[0]

    with open(file_name, 'rb') as f:  # type: IO[bytes]
        conteudo = f.read()
    validos = []
    for registro in candidatos:
        off_data, off_tipo = _OFFSETS_VALIDACAO[registro]
        if all(_texto_valido(conteudo[i + off_data:i + off_data + 8]) and
               _texto_valido(conteudo[i + off_tipo:i + off_tipo + 1])
               for i in range(0, tamanho, registro)):
            validos.append(registro)
    if len(validos) != 1:
        raise HidrFormatoError(
            f"{modelo} - {file_name}: tamanho {tamanho} bytes e compativel com registros de {REGISTRO_ANTIGO} e de "
            f"{REGISTRO_NOVO} bytes e a validacao estrutural nao identificou um layout unico "
            f"(validos: {validos}). Informe tamanho_registro explicitamente em Hidr.ler.")
    return validos[0]


def resolver_tamanho_registro(file_name: str, tamanho_registro: Optional[int], modelo: str,
                              automaticos: Iterable[int] = (REGISTRO_ANTIGO, REGISTRO_NOVO)) -> int:
    """
    Determina o layout a ser usado na leitura.

    :param file_name: caminho completo para o arquivo
    :param tamanho_registro: layout forcado pelo usuario (792 ou 832) ou None para detectar
    :param modelo: nome do modelo, usado nas mensagens de erro
    :param automaticos: layouts aceitos sem pedido explicito para este modelo
    :return: tamanho do registro em bytes
    """
    tamanho = os.stat(file_name).st_size
    if tamanho_registro is not None:
        if tamanho_registro not in FMT_POLINOMIO:
            raise HidrFormatoError(f"{modelo}: tamanho_registro {tamanho_registro} invalido; use "
                                   f"{REGISTRO_ANTIGO} ou {REGISTRO_NOVO}.")
        if tamanho == 0 or tamanho % tamanho_registro != 0:
            raise HidrFormatoError(f"{modelo} - {file_name}: tamanho {tamanho} bytes nao e multiplo positivo do "
                                   f"registro de {tamanho_registro} bytes.")
        return tamanho_registro

    detectado = detectar_tamanho_registro(file_name, modelo)
    if detectado not in automaticos:
        raise HidrFormatoError(
            f"{modelo} - {file_name}: o arquivo tem o layout de {detectado} bytes por registro, que ainda nao foi "
            f"validado com decks reais do {modelo}. Para le-lo com o layout confirmado no NEWAVE, informe "
            f"tamanho_registro={detectado} explicitamente.")
    return detectado


def validar_tamanho_escrita(tamanho_registro: int, modelo: str) -> str:
    """Valida o layout de escrita e retorna o formato struct (little-endian) dos coeficientes dos polinomios."""
    if tamanho_registro not in FMT_POLINOMIO:
        raise HidrFormatoError(f"{modelo}: tamanho_registro {tamanho_registro} invalido; use "
                               f"{REGISTRO_ANTIGO} ou {REGISTRO_NOVO}.")
    return '<' + FMT_POLINOMIO[tamanho_registro]


def decodificar_texto(bruto: bytes, errors: str, campo: str, file_name: str, modelo: str, indice: int,
                      offset: int, tamanho_registro: int) -> str:
    """Decodifica um campo textual em UTF-8; em caso de erro, informa registro, campo, offset e bytes."""
    try:
        return bruto.decode('utf-8', errors)
    except UnicodeDecodeError as err:
        raise HidrFormatoError(
            f"{modelo} - {file_name}: registro {indice + 1}, campo {campo}, offset absoluto {offset}: bytes "
            f"{bruto.hex(' ')} nao formam texto UTF-8 valido (layout de {tamanho_registro} bytes).") from err


def texto_bytes(valor, original: Optional[bytes], errors: str = 'strict') -> bytes:
    """
    Retorna os bytes originais do campo textual quando o valor nao foi alterado desde a leitura; caso contrario,
    codifica o valor atual em UTF-8. Valores ja em bytes sao gravados como estao.
    """
    if isinstance(valor, (bytes, bytearray)):
        return bytes(valor)
    if original is not None and original.decode('utf-8', errors) == valor:
        return original
    return bytes(valor, 'utf-8')
