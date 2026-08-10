import os
import math
import calendar
from copy import deepcopy
from datetime import date, timedelta
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

    Alem dos sete campos fisicos, cada usina expoe cinco matrizes de
    evolucao temporal (nanos x 12) - gtmin_tempo, pot_tempo, fcmax_tempo,
    ip_tempo e teif_tempo - a exemplo de Confhd.engol_tempo: iniciadas com
    o cadastro da classe Term (TERM.DAT) e atualizadas ano/mes a ano/mes
    pelas modificacoes GTMIN/POTEF/FCMAX/IPTER/TEIFT da classe Expt
    (EXPT.DAT). Ver _acerta_expt.

    Em seguida, pot_tempo tambem e abatida pelas manutencoes programadas
    da classe Manutt (MANUTT.DAT): cada evento de manutencao retira
    ``potencia`` MW da usina durante ``duracao`` dias corridos a partir de
    dia_inicio/mes_inicio/ano_inicio; o abatimento em cada mes e
    proporcional aos dias de sobreposicao entre a manutencao e o mes
    (dias_sobrepostos / dias_do_mes) * potencia. Ver _acerta_manutt.
    """

    _FIELD_MAP = {
        'codigo_usina': ('_codigo_usina', 'valor'),
        'nome_usina': ('_nome_usina', 'valor'),
        'codigo_submercado': ('_codigo_submercado', 'valor'),
        'status': ('_status', 'valor'),
        'codigo_classe_termica': ('_codigo_classe_termica', 'valor'),
        'codigo_tecnologia': ('_codigo_tecnologia', 'valor'),
        'codigo_classe_gas': ('_codigo_classe_gas', 'valor'),
        'gtmin_tempo': ('_gtmin_tempo', 'valor'),
        'pot_tempo': ('_pot_tempo', 'valor'),
        'fcmax_tempo': ('_fcmax_tempo', 'valor'),
        'ip_tempo': ('_ip_tempo', 'valor'),
        'teif_tempo': ('_teif_tempo', 'valor'),
    }
    _CONFT_FIELDS = (
        'codigo_usina', 'nome_usina', 'codigo_submercado', 'status',
        'codigo_classe_termica', 'codigo_tecnologia', 'codigo_classe_gas',
    )
    _STATUS_VALUES = frozenset(('EX', 'EE', 'NE', 'NC'))

    # Mapeia o tipo_modificacao do EXPT.DAT para o atributo _xxx_tempo
    # correspondente
    _TIPO_PARA_CAMPO = {
        'GTMIN': '_gtmin_tempo',
        'POTEF': '_pot_tempo',
        'FCMAX': '_fcmax_tempo',
        'IPTER': '_ip_tempo',
        'TEIFT': '_teif_tempo',
    }

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

    def ler(self, file_name: str, dger, term, expt, manutt) -> None:
        """
        Le o CONFT.DAT e preenche o cadastro de usinas termicas, incluindo
        a evolucao temporal (nanos x 12) de gtmin_tempo, pot_tempo,
        fcmax_tempo, ip_tempo e teif_tempo, iniciada com o cadastro da
        classe Term, atualizada pelas modificacoes da classe Expt e, no
        caso de pot_tempo, tambem abatida pelas manutencoes programadas da
        classe Manutt.

        :param file_name: string com o caminho completo para o arquivo
        :param dger: classe Dger, usada para o numero de anos/ano inicial/
               mes inicial do horizonte de planejamento
        :param term: classe Term, usada como cadastro base de gtmin, potef,
               fcmax, teif e ip de cada usina termica
        :param expt: classe Expt, usada para as modificacoes temporais de
               gtmin, potef, fcmax, ipter e teift de cada usina termica
        :param manutt: classe Manutt, usada para abater de pot_tempo a
               potencia retirada de operacao pelas manutencoes programadas

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        self._numero_registros_ = 0
        self.numero_usinas = 0
        self.nanos = dger.num_anos['valor']
        self._mapa = dict()

        for attr_name, value_name in set(self._FIELD_MAP.values()):
            getattr(self, attr_name)[value_name] = list()

        # codigo_usina (Term) -> posicao nas listas internas de Term
        mapa_term = {codigo: i for i, codigo in enumerate(term._codigo['valor'])}

        # codigo_usina (Expt) -> lista de indices (na ordem do arquivo) das
        # modificacoes temporais dessa usina
        expt_por_codigo = {}
        for indice in range(expt.numero_expansoes):
            codigo_expt = expt._codigo_usina['valor'][indice]
            expt_por_codigo.setdefault(codigo_expt, []).append(indice)

        # codigo_usina (Manutt) -> lista de indices (na ordem do arquivo)
        # dos eventos de manutencao programada dessa usina
        manutt_por_codigo = {}
        for indice in range(manutt.numero_manutencoes):
            codigo_manutt = manutt._codigo_usina['valor'][indice]
            manutt_por_codigo.setdefault(codigo_manutt, []).append(indice)

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

                    # Evolucao temporal (cadastro Term + modificacoes Expt)
                    self._acerta_expt(dger, term, expt, mapa_term, expt_por_codigo)
                    # Abate de pot_tempo pelas manutencoes programadas (Manutt)
                    self._acerta_manutt(dger, manutt, manutt_por_codigo)

                    self._mapa[self._codigo_usina['valor'][-1]] = self.numero_usinas
                    self.numero_usinas += 1

        except Exception as err:
            if isinstance(err, StopIteration):
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def _acerta_expt(self, dger, term, expt, mapa_term, expt_por_codigo):
        """
        Monta, para a usina que acabou de ser lida (ultima posicao das
        listas internas), as cinco matrizes de evolucao temporal (nanos x
        12) gtmin_tempo/pot_tempo/fcmax_tempo/ip_tempo/teif_tempo.

        Cada matriz e iniciada com o cadastro correspondente da classe
        Term (gtmin e mensal apenas no primeiro ano de estudo, com um
        unico valor "D+ anos" para os anos seguintes; os demais campos sao
        um unico valor cadastral repetido em todo o horizonte), com os
        meses do primeiro ano anteriores ao mes inicial de estudo
        (dger.mesi_est) zerados. Em seguida, as modificacoes temporais da
        usina em Expt (GTMIN/POTEF/FCMAX/IPTER/TEIFT) sao aplicadas, na
        ordem em que aparecem no EXPT.DAT, sobre a janela
        [mes_inicio/ano_inicio, mes_fim/ano_fim] de cada modificacao (ou
        ate o fim do horizonte, quando mes_fim/ano_fim estao em branco) -
        a exemplo de Confhd._acerta_exph/Confhd._acerta_modif.
        """
        codigo = self._codigo_usina['valor'][-1]
        nanos = self.nanos
        termo = mapa_term.get(codigo)
        mesi_est = dger.mesi_est['valor']

        campos_escalares = {
            '_pot_tempo': '_pot',
            '_fcmax_tempo': '_fcmax',
            '_ip_tempo': '_ip',
            '_teif_tempo': '_teif',
        }

        for attr_name in self._TIPO_PARA_CAMPO.values():
            if attr_name == '_gtmin_tempo':
                if termo is not None:
                    gtmin = term._gtmin['valor'][termo]
                    matriz = np.empty((nanos, 12), 'f')
                    matriz[0, :] = gtmin[0:12]
                    if nanos > 1:
                        matriz[1:, :] = gtmin[12]
                else:
                    matriz = np.zeros((nanos, 12), 'f')
            else:
                if termo is not None:
                    valor_base = getattr(term, campos_escalares[attr_name])['valor'][termo]
                    matriz = valor_base * np.ones((nanos, 12), 'f')
                else:
                    matriz = np.zeros((nanos, 12), 'f')

            # Zera os meses do primeiro ano anteriores ao mes inicial de estudo
            if mesi_est and mesi_est > 1:
                matriz[0, :mesi_est - 1] = 0.0

            getattr(self, attr_name)['valor'].append(matriz)

        for indice in expt_por_codigo.get(codigo, []):
            registro = expt.get(indice)
            attr_name = self._TIPO_PARA_CAMPO.get(registro['tipo_modificacao'])
            if attr_name is None:
                continue
            matriz = getattr(self, attr_name)['valor'][-1]
            self._aplica_janela_expt(matriz, registro, dger)

    @staticmethod
    def _aplica_janela_expt(matriz, registro, dger):
        """
        Escreve ``registro['novo_valor']`` em ``matriz`` (nanos x 12) na
        janela [mes_inicio/ano_inicio, mes_fim/ano_fim]. Quando
        mes_fim/ano_fim estao em branco, a modificacao vale ate o fim do
        horizonte de planejamento. Janelas parcialmente fora do horizonte
        sao recortadas; janelas totalmente fora do horizonte sao ignoradas.
        """
        nanos = matriz.shape[0]
        ano_ini_estudo = dger.ano_ini['valor']

        iano_ini = registro['ano_inicio'] - ano_ini_estudo
        mes_ini = registro['mes_inicio']

        if registro['ano_fim'] is not None:
            iano_fim = registro['ano_fim'] - ano_ini_estudo
            mes_fim = registro['mes_fim']
        else:
            iano_fim = nanos - 1
            mes_fim = 12

        if iano_fim < 0 or iano_ini > nanos - 1:
            return

        if iano_ini < 0:
            iano_ini, mes_ini = 0, 1
        if iano_fim > nanos - 1:
            iano_fim, mes_fim = nanos - 1, 12

        for iano in range(iano_ini, iano_fim + 1):
            m_ini = mes_ini if iano == iano_ini else 1
            m_fim = mes_fim if iano == iano_fim else 12
            matriz[iano, m_ini - 1:m_fim] = registro['novo_valor']

    def _acerta_manutt(self, dger, manutt, manutt_por_codigo):
        """
        Abate de pot_tempo (ultima usina lida) a potencia retirada de
        operacao por cada evento de manutencao programada da usina em
        Manutt, aplicada por cima do que ja estiver em pot_tempo (cadastro
        de Term e eventuais modificacoes POTEF de Expt).
        """
        codigo = self._codigo_usina['valor'][-1]
        matriz = self._pot_tempo['valor'][-1]
        ano_ini_estudo = dger.ano_ini['valor']
        nanos = matriz.shape[0]

        for indice in manutt_por_codigo.get(codigo, []):
            registro = manutt.get(indice)
            self._abate_manutt(matriz, registro, ano_ini_estudo, nanos)

    @staticmethod
    def _abate_manutt(matriz, registro, ano_ini_estudo, nanos):
        """
        Subtrai ``registro['potencia']`` de ``matriz`` (pot_tempo, nanos x
        12) em cada mes tocado pela manutencao, proporcionalmente aos dias
        de sobreposicao entre a manutencao e o mes: (dias_sobrepostos /
        dias_do_mes) * potencia. A manutencao comeca em
        dia_inicio/mes_inicio/ano_inicio e dura ``duracao`` dias corridos
        (o ultimo dia da manutencao e dia_inicio + duracao - 1). Meses
        fora do horizonte de planejamento sao ignorados.
        """
        inicio = date(registro['ano_inicio'], registro['mes_inicio'], registro['dia_inicio'])
        fim = inicio + timedelta(days=registro['duracao'] - 1)

        ano, mes = inicio.year, inicio.month
        while (ano, mes) <= (fim.year, fim.month):
            iano = ano - ano_ini_estudo
            if 0 <= iano < nanos:
                dias_no_mes = calendar.monthrange(ano, mes)[1]
                primeiro_dia_mes = date(ano, mes, 1)
                ultimo_dia_mes = date(ano, mes, dias_no_mes)

                inicio_sobreposto = max(inicio, primeiro_dia_mes)
                fim_sobreposto = min(fim, ultimo_dia_mes)
                dias_sobrepostos = (fim_sobreposto - inicio_sobreposto).days + 1

                fracao = dias_sobrepostos / dias_no_mes
                matriz[iano, mes - 1] -= fracao * registro['potencia']

            if mes == 12:
                ano, mes = ano + 1, 1
            else:
                mes += 1

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
