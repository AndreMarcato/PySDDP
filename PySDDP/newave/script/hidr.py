import io
import os
import struct
from typing import IO, Optional

from PySDDP.hidr_layout import (  # noqa: F401 (nomes reexportados para compatibilidade)
    FMT_POLINOMIO as _FMT_POLINOMIO,
    REGISTRO_ANTIGO,
    REGISTRO_NOVO,
    HidrFormatoError,
    decodificar_texto,
    detectar_tamanho_registro,
    resolver_tamanho_registro,
    texto_bytes,
    validar_tamanho_escrita,
)
from PySDDP.newave.script.templates.hidr import HidrTemplate


# Campos textuais: (nome do campo, politica de decodificacao usada historicamente pela classe)
_CAMPOS_TEXTO = (('nome', 'strict'), ('bdh', 'strict'), ('data', 'strict'), ('observ', 'ignore'),
                 ('tipo_reg', 'strict'))


class Hidr(HidrTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None
        # Tamanho do registro do arquivo de origem; None para objetos sem leitura (escreve no layout antigo)
        self._tamanho_registro_ = None
        # Bytes originais dos campos textuais de cada registro, para preservar o round-trip binario
        self._textos_originais_ = list()

    def ler(self, file_name: str, tamanho_registro: Optional[int] = None) -> None:
        """
        Implementa o método para leitura do arquivo HIDR.DAT que contem os dados cadastrais das usinas
         hidrelétricas que podem ser utilizadas para a execucao do NEWAVE

        :param file_name: string com o caminho completo para o arquivo
        :param tamanho_registro: 792 ou 832 para forcar o layout; None detecta automaticamente

        """

        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]

        tamanho_registro = resolver_tamanho_registro(file_name, tamanho_registro, 'NEWAVE')

        tot_reg = os.stat(file_name).st_size // tamanho_registro
        self.nr_usinas = tot_reg
        self._tamanho_registro_ = tamanho_registro
        fmt_pol = '<5' + _FMT_POLINOMIO[tamanho_registro]
        tam_pol = struct.calcsize(fmt_pol)

        # noinspection PyBroadException
        monitor: dict = dict()
        self._numero_registros_ = 0
        try:

            with open(file_name, 'rb') as arq:  # type: IO[bytes]

                for indice in range(tot_reg):
                    # Cada registro e lido isoladamente: nenhum desvio de offset se propaga ao seguinte
                    inicio = indice * tamanho_registro
                    f = io.BytesIO(arq.read(tamanho_registro))
                    textos = dict()

                    def texto(campo, largura, errors='strict'):
                        bruto = struct.unpack(f'{largura}s', f.read(largura))[0]
                        textos[campo] = bruto
                        return decodificar_texto(bruto, errors, campo, file_name, 'NEWAVE', indice,
                                                 inicio + f.tell() - largura, tamanho_registro)

                    self._codigo["valor"].append(indice + 1)
                    self._nome["valor"].append(texto('nome', 12))
                    self._posto["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._bdh["valor"].append(texto('bdh', 8))
                    self._sist["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._empr["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._jusante["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._desvio["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._vol_min["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._vol_max["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._vol_vert["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._vol_min_desv["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._cota_min["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._cota_max["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._pol_cota_vol["valor"].append(list(struct.unpack(fmt_pol, f.read(tam_pol))))
                    self._pol_cota_area["valor"].append(list(struct.unpack(fmt_pol, f.read(tam_pol))))
                    self._coef_evap["valor"].append(list(struct.unpack('<12i', f.read(48))))
                    self._num_conj_maq["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._maq_por_conj["valor"].append(list(struct.unpack('<5i', f.read(20))))
                    self._pef_por_conj["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqt["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqt["valor_2"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqt["valor_3"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqt["valor_4"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqt["valor_5"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqg["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqg["valor_2"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqg["valor_3"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqg["valor_4"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbqg["valor_5"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbpt["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbpt["valor_2"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbpt["valor_3"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbpt["valor_4"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cf_hbpt["valor_5"].append(list(struct.unpack('<5f', f.read(20))))
                    self._alt_efet_conj["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._vaz_efet_conj["valor"].append(list(struct.unpack('<5i', f.read(20))))
                    self._prod_esp["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._perda_hid["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._num_pol_vnj["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._pol_vaz_niv_jus["valor"].append(list(struct.unpack('<5f', f.read(20))))
                    self._pol_vaz_niv_jus["valor_2"].append(list(struct.unpack('<5f', f.read(20))))
                    self._pol_vaz_niv_jus["valor_3"].append(list(struct.unpack('<5f', f.read(20))))
                    self._pol_vaz_niv_jus["valor_4"].append(list(struct.unpack('<5f', f.read(20))))
                    self._pol_vaz_niv_jus["valor_5"].append(list(struct.unpack('<5f', f.read(20))))
                    self._pol_vaz_niv_jus["valor_6"].append(list(struct.unpack('<5f', f.read(20))))
                    self._cota_ref_nivel_jus["valor"].append(list(struct.unpack('<6f', f.read(24))))
                    self._cfmed["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._inf_canal_fuga["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._fator_carga_max["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._fator_carga_min["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._vaz_min["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._unid_base["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._tipo_turb["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._repres_conj["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._teifh["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._ip["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._tipo_perda["valor"].append(struct.unpack('<i', f.read(4))[0])
                    self._data["valor"].append(texto('data', 8))
                    self._observ["valor"].append(texto('observ', 43, errors='ignore'))
                    self._vol_ref["valor"].append(struct.unpack('<f', f.read(4))[0])
                    self._tipo_reg["valor"].append(texto('tipo_reg', 1))

                    if f.tell() != tamanho_registro:
                        raise HidrFormatoError(f"{file_name}: registro {indice + 1} consumiu {f.tell()} bytes; "
                                               f"esperado {tamanho_registro}.")

                    self._textos_originais_.append(textos)
                    # noinspection PyBroadException
                    monitor[self._nome["valor"][-1]] = 'OK'
                    self._numero_registros_ += 1

        except Exception as err:
            print(self.linha)
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._conteudo_ = monitor
            else:
                raise

        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def _texto_bytes(self, campo: str, errors: str, i: int) -> bytes:
        """
        Retorna os bytes originais do campo textual quando o valor nao foi alterado desde a leitura;
        caso contrario, codifica o valor atual em UTF-8 (comportamento historico da classe).
        """
        valor = getattr(self, '_' + campo)["valor"][i]
        original = self._textos_originais_[i].get(campo) if i < len(self._textos_originais_) else None
        return texto_bytes(valor, original, errors)

    def escrever(self, file_out: str, tamanho_registro: Optional[int] = None) -> None:
        """
        Escreve o arquivo que contem os nomes dos
        arquivos para execucao do Newave

        Por padrao, preserva o layout do arquivo lido (792 ou 832 bytes por registro). Objetos sem
        leitura previa sao gravados no layout antigo (792 bytes), como nas versoes anteriores.

        :param file_out: caminho completo para o arquivo
        :param tamanho_registro: 792 ou 832 para escolher explicitamente o layout de saida
        """

        if tamanho_registro is None:
            tamanho_registro = self._tamanho_registro_ or REGISTRO_ANTIGO
        fmt_pol = validar_tamanho_escrita(tamanho_registro, 'NEWAVE')

        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        try:
            with open(file_out, 'wb') as arq:  # type: IO[bytes]

                for i in range(self._numero_registros_):
                    f = io.BytesIO()
                    textos = {campo: self._texto_bytes(campo, errors, i) for campo, errors in _CAMPOS_TEXTO}
                    f.write(struct.pack('12s', textos['nome']))
                    f.write(struct.pack('<i', self._posto["valor"][i]))
                    f.write(struct.pack('8s', textos['bdh']))
                    f.write(struct.pack('<i', self._sist["valor"][i]))
                    f.write(struct.pack('<i', self._empr["valor"][i]))
                    f.write(struct.pack('<i', self._jusante["valor"][i]))
                    f.write(struct.pack('<i', self._desvio["valor"][i]))
                    f.write(struct.pack('<f', self._vol_min["valor"][i]))
                    f.write(struct.pack('<f', self._vol_max["valor"][i]))
                    f.write(struct.pack('<f', self._vol_vert["valor"][i]))
                    f.write(struct.pack('<f', self._vol_min_desv["valor"][i]))
                    f.write(struct.pack('<f', self._cota_min["valor"][i]))
                    f.write(struct.pack('<f', self._cota_max["valor"][i]))
                    for j in range(5):
                        f.write(struct.pack(fmt_pol, self._pol_cota_vol["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack(fmt_pol, self._pol_cota_area["valor"][i][j]))
                    for j in range(12):
                        f.write(struct.pack('<i', self._coef_evap["valor"][i][j]))
                    f.write(struct.pack('<i', self._num_conj_maq["valor"][i]))
                    for j in range(5):
                        f.write(struct.pack('<i', self._maq_por_conj["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pef_por_conj["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqt["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqt["valor_2"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqt["valor_3"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqt["valor_4"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqt["valor_5"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqg["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqg["valor_2"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqg["valor_3"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqg["valor_4"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbqg["valor_5"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbpt["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbpt["valor_2"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbpt["valor_3"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbpt["valor_4"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._cf_hbpt["valor_5"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._alt_efet_conj["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<i', self._vaz_efet_conj["valor"][i][j]))
                    f.write(struct.pack('<f', self._prod_esp["valor"][i]))
                    f.write(struct.pack('<f', self._perda_hid["valor"][i]))
                    f.write(struct.pack('<i', self._num_pol_vnj["valor"][i]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor_2"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor_3"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor_4"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor_5"][i][j]))
                    for j in range(5):
                        f.write(struct.pack('<f', self._pol_vaz_niv_jus["valor_6"][i][j]))
                    for j in range(6):
                        f.write(struct.pack('<f', self._cota_ref_nivel_jus["valor"][i][j]))
                    f.write(struct.pack('<f', self._cfmed["valor"][i]))
                    f.write(struct.pack('<i', self._inf_canal_fuga["valor"][i]))
                    f.write(struct.pack('<f', self._fator_carga_max["valor"][i]))
                    f.write(struct.pack('<f', self._fator_carga_min["valor"][i]))
                    f.write(struct.pack('<i', self._vaz_min["valor"][i]))
                    f.write(struct.pack('<i', self._unid_base["valor"][i]))
                    f.write(struct.pack('<i', self._tipo_turb["valor"][i]))
                    f.write(struct.pack('<i', self._repres_conj["valor"][i]))
                    f.write(struct.pack('<f', self._teifh["valor"][i]))
                    f.write(struct.pack('<f', self._ip["valor"][i]))
                    f.write(struct.pack('<i', self._tipo_perda["valor"][i]))
                    f.write(struct.pack('8s', textos['data']))
                    f.write(struct.pack('43s', textos['observ']))
                    f.write(struct.pack('<f', self._vol_ref["valor"][i]))
                    f.write(struct.pack('c', textos['tipo_reg']))

                    if f.tell() != tamanho_registro:
                        raise HidrFormatoError(f"registro {i + 1} gerou {f.tell()} bytes; esperado "
                                               f"{tamanho_registro}.")
                    arq.write(f.getvalue())

        except Exception:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")

    def get(self, entrada):
        posicao = None
        if (type(entrada) == float) or (type(entrada) == int):
            for i, valor in enumerate(self._codigo["valor"]):
                if valor == int(entrada):
                    posicao = i
                    break
            if posicao is None:
                return None

        if type(entrada) == str:
            for i, valor in enumerate(self._nome["valor"]):
                if (valor.upper()).strip() == (entrada.upper()).strip():
                    posicao = i
                    break
            if posicao is None:
                return None

        uhe = {
            'codigo': self._codigo['valor'][posicao],
            'nome': self._nome['valor'][posicao],
            'posto': self._posto['valor'][posicao],
            'bdh': self._bdh['valor'][posicao],
            'sist': self._sist['valor'][posicao],
            'empr': self._empr['valor'][posicao],
            'jusante': self._jusante['valor'][posicao],
            'desvio': self._desvio['valor'][posicao],
            'vol_min': self._vol_min['valor'][posicao],
            'vol_max': self._vol_max['valor'][posicao],
            'vol_vert': self._vol_vert['valor'][posicao],
            'vol_min_desv': self._vol_min_desv['valor'][posicao],
            'cota_min': self._cota_min['valor'][posicao],
            'cota_max': self._cota_max['valor'][posicao],
            'pol_cota_vol': self._pol_cota_vol['valor'][posicao],
            'pol_cota_area': self._pol_cota_area['valor'][posicao],
            'coef_evap': self._coef_evap['valor'][posicao],
            'num_conj_maq': self._num_conj_maq['valor'][posicao],
            'maq_por_conj': self._maq_por_conj['valor'][posicao],
            'pef_por_conj': self._pef_por_conj['valor'][posicao],
            'cf_hbqt': self._cf_hbqt['valor'][posicao],
            'cf_hbqt_2': self._cf_hbqt['valor_2'][posicao],
            'cf_hbqt_3': self._cf_hbqt['valor_3'][posicao],
            'cf_hbqt_4': self._cf_hbqt['valor_4'][posicao],
            'cf_hbqt_5': self._cf_hbqt['valor_5'][posicao],
            'cf_hbqg': self._cf_hbqg['valor'][posicao],
            'cf_hbqg_2': self._cf_hbqg['valor_2'][posicao],
            'cf_hbqg_3': self._cf_hbqg['valor_3'][posicao],
            'cf_hbqg_4': self._cf_hbqg['valor_4'][posicao],
            'cf_hbqg_5': self._cf_hbqg['valor_5'][posicao],
            'cf_hbpt': self._cf_hbpt['valor'][posicao],
            'cf_hbpt_2': self._cf_hbpt['valor_2'][posicao],
            'cf_hbpt_3': self._cf_hbpt['valor_3'][posicao],
            'cf_hbpt_4': self._cf_hbpt['valor_4'][posicao],
            'cf_hbpt_5': self._cf_hbpt['valor_5'][posicao],
            'alt_efet_conj': self._alt_efet_conj['valor'][posicao],
            'vaz_efet_conj': self._vaz_efet_conj['valor'][posicao],
            'prod_esp': self._prod_esp['valor'][posicao],
            'perda_hid': self._perda_hid['valor'][posicao],
            'num_pol_vnj': self._num_pol_vnj['valor'][posicao],
            'pol_vaz_niv_jus': self._pol_vaz_niv_jus['valor'][posicao],
            'pol_vaz_niv_jus_2': self._pol_vaz_niv_jus['valor_2'][posicao],
            'pol_vaz_niv_jus_3': self._pol_vaz_niv_jus['valor_3'][posicao],
            'pol_vaz_niv_jus_4': self._pol_vaz_niv_jus['valor_4'][posicao],
            'pol_vaz_niv_jus_5': self._pol_vaz_niv_jus['valor_5'][posicao],
            'pol_vaz_niv_jus_6': self._pol_vaz_niv_jus['valor_6'][posicao],
            'cota_ref_nivel_jus': self._cota_ref_nivel_jus['valor'][posicao],
            'cfmed': self._cfmed['valor'][posicao],
            'inf_canal_fuga': self._inf_canal_fuga['valor'][posicao],
            'fator_carga_max': self._fator_carga_max['valor'][posicao],
            'fator_carga_min': self._fator_carga_min['valor'][posicao],
            'vaz_min': self._vaz_min['valor'][posicao],
            'unid_base': self._unid_base['valor'][posicao],
            'tipo_turb': self._tipo_turb['valor'][posicao],
            'repres_conj': self._repres_conj['valor'][posicao],
            'teifh': self._teifh['valor'][posicao],
            'ip': self._ip['valor'][posicao],
            'tipo_perda': self._tipo_perda['valor'][posicao],
            'data': self._data['valor'][posicao],
            'observ': self._observ['valor'][posicao],
            'vol_ref': self._vol_ref['valor'][posicao],
            'tipo_reg': self._tipo_reg['valor'][posicao]
            }

        return uhe

    def put(self, uhe):
        posicao = None
        for i, valor in enumerate(self._codigo["valor"]):
            if valor == uhe['codigo']:
                posicao = i
                break
        if posicao is None:
            return None

        self._codigo['valor'][posicao] = uhe['codigo']
        self._nome['valor'][posicao] = uhe['nome']
        self._posto['valor'][posicao] = uhe['posto']
        self._bdh['valor'][posicao] = uhe['bdh']
        self._sist['valor'][posicao] = uhe['sist']
        self._empr['valor'][posicao] = uhe['empr']
        self._jusante['valor'][posicao] = uhe['jusante']
        self._desvio['valor'][posicao] = uhe['desvio']
        self._vol_min['valor'][posicao] = uhe['vol_min']
        self._vol_max['valor'][posicao] = uhe['vol_max']
        self._vol_vert['valor'][posicao] = uhe['vol_vert']
        self._vol_min_desv['valor'][posicao] = uhe['vol_min_desv']
        self._cota_min['valor'][posicao] = uhe['cota_min']
        self._cota_max['valor'][posicao] = uhe['cota_max']
        self._pol_cota_vol['valor'][posicao] = uhe['pol_cota_vol']
        self._pol_cota_area['valor'][posicao] = uhe['pol_cota_area']
        self._coef_evap['valor'][posicao] = uhe['coef_evap']
        self._num_conj_maq['valor'][posicao] = uhe['num_conj_maq']
        self._maq_por_conj['valor'][posicao] = uhe['maq_por_conj']
        self._pef_por_conj['valor'][posicao] = uhe['pef_por_conj']
        self._cf_hbqt['valor'][posicao] = uhe['cf_hbqt']
        self._cf_hbqt['valor_2'][posicao] = uhe['cf_hbqt_2']
        self._cf_hbqt['valor_3'][posicao] = uhe['cf_hbqt_3']
        self._cf_hbqt['valor_4'][posicao] = uhe['cf_hbqt_4']
        self._cf_hbqt['valor_5'][posicao] = uhe['cf_hbqt_5']
        self._cf_hbqg['valor'][posicao] = uhe['cf_hbqg']
        self._cf_hbqg['valor_2'][posicao] = uhe['cf_hbqg_2']
        self._cf_hbqg['valor_3'][posicao] = uhe['cf_hbqg_3']
        self._cf_hbqg['valor_4'][posicao] = uhe['cf_hbqg_4']
        self._cf_hbqg['valor_5'][posicao] = uhe['cf_hbqg_5']
        self._cf_hbpt['valor'][posicao] = uhe['cf_hbpt']
        self._cf_hbpt['valor_2'][posicao] = uhe['cf_hbpt_2']
        self._cf_hbpt['valor_3'][posicao] = uhe['cf_hbpt_3']
        self._cf_hbpt['valor_4'][posicao] = uhe['cf_hbpt_4']
        self._cf_hbpt['valor_5'][posicao] = uhe['cf_hbpt_5']
        self._alt_efet_conj['valor'][posicao] = uhe['alt_efet_conj']
        self._vaz_efet_conj['valor'][posicao] = uhe['vaz_efet_conj']
        self._prod_esp['valor'][posicao] = uhe['prod_esp']
        self._perda_hid['valor'][posicao] = uhe['perda_hid']
        self._num_pol_vnj['valor'][posicao] = uhe['num_pol_vnj']
        self._pol_vaz_niv_jus['valor'][posicao] = uhe['pol_vaz_niv_jus']
        self._pol_vaz_niv_jus['valor_2'][posicao] = uhe['pol_vaz_niv_jus_2']
        self._pol_vaz_niv_jus['valor_3'][posicao] = uhe['pol_vaz_niv_jus_3']
        self._pol_vaz_niv_jus['valor_4'][posicao] = uhe['pol_vaz_niv_jus_4']
        self._pol_vaz_niv_jus['valor_5'][posicao] = uhe['pol_vaz_niv_jus_5']
        self._pol_vaz_niv_jus['valor_6'][posicao] = uhe['pol_vaz_niv_jus_6']
        self._cota_ref_nivel_jus['valor'][posicao] = uhe['cota_ref_nivel_jus']
        self._cfmed['valor'][posicao] = uhe['cfmed']
        self._inf_canal_fuga['valor'][posicao] = uhe['inf_canal_fuga']
        self._fator_carga_max['valor'][posicao] = uhe['fator_carga_max']
        self._fator_carga_min['valor'][posicao] = uhe['fator_carga_min']
        self._vaz_min['valor'][posicao] = uhe['vaz_min']
        self._unid_base['valor'][posicao] = uhe['unid_base']
        self._tipo_turb['valor'][posicao] = uhe['tipo_turb']
        self._repres_conj['valor'][posicao] = uhe['repres_conj']
        self._teifh['valor'][posicao] = uhe['teifh']
        self._ip['valor'][posicao] = uhe['ip']
        self._tipo_perda['valor'][posicao] = uhe['tipo_perda']
        self._data['valor'][posicao] = uhe['data']
        self._observ['valor'][posicao] = uhe['observ']
        self._vol_ref['valor'][posicao] = uhe['vol_ref']
        self._tipo_reg['valor'][posicao] = uhe['tipo_reg']

        return 'sucesso'

    def help(self, parametro):

        duvida = getattr(self, '_'+parametro)

        return duvida['descricao']
