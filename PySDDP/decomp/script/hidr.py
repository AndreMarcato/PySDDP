import os
import struct
from typing import IO

from PySDDP.decomp.script.templates.hidr import HidrTemplate


class Hidr(HidrTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Hidr (dados de cadastro das usinas
    hidreletricas) do Decomp.
    Esta classe tem como intuito fornecer duck typing para a classe Decomp e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso, esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita.
    """

    def __init__(self):
        super().__init__()

        self.list_entr = list()
        self.dir_base = None

        self._conteudo = None
        self._numero_registros = None

    def ler(self, file_name: str) -> None:
        """
        Metodo para a leitura do arquivo perdas.dat.
        Manual do Usuário 30.1: Arquivo hidr.dat. Este arquivo contém os dados cadastrais das usinas hidreletricas que
        podem ser utilizados para a execucao do Decomp.
        :param file_name: String com o caminho completo para o arquivo.
        :return:
        """

        self.dir_base = os.path.split(file_name)[0]

        tot_reg = os.stat(file_name).st_size/792

        # noinspection PyBroadException
        monitor: dict = dict()
        self._numero_registros = 0
        try:

            with open(file_name, 'rb') as f:  # type: IO[bytes]
                
                self._numero_registros = 1
                continua = True

                while continua:
                    self.codigo['valor'].append(self._numero_registros)
                    self.nome['valor'].append(struct.unpack('12s', f.read(12))[0].decode())
                    self.posto['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.bdh['valor'].append(struct.unpack('8s', f.read(8))[0].decode())
                    self.submercado['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.empresa['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.jusante['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.desvio['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.vol_min['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.vol_max['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.vol_vert['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.vol_min_desv['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.cota_min['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.cota_max['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.pol_cota_vol['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.pol_cota_area['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.coef_evap['valor'].append(list(struct.unpack('12i', bytearray(f.read(48)))))
                    self.num_conj_maq['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.maq_por_conj['valor'].append(list(struct.unpack('5i', bytearray(f.read(20)))))
                    self.pef_por_conj['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqt['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqt['valor_2'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqt['valor_3'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqt['valor_4'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqt['valor_5'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqg['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqg['valor_2'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqg['valor_3'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqg['valor_4'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbqg['valor_5'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbpt['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbpt['valor_2'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbpt['valor_3'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbpt['valor_4'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.cf_hbpt['valor_5'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.alt_efet_conj['valor'].append(list(struct.unpack('5f', bytearray(f.read(20)))))
                    self.vaz_efet_conj['valor'].append(list(struct.unpack('5i', bytearray(f.read(20)))))
                    self.prod_esp['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.perda_hid['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.num_pol_vnj['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.pol_vaz_niv_jus['valor'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.pol_vaz_niv_jus['valor_2'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.pol_vaz_niv_jus['valor_3'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.pol_vaz_niv_jus['valor_4'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.pol_vaz_niv_jus['valor_5'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.cota_ref_nivel_jus['valor'].append(list(struct.unpack('6f', bytearray(f.read(24)))))
                    self.cfmed['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.inf_canal_fuga['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.fator_carga_max['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.fator_carga_min['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.vaz_min['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.unid_base['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.tipo_turb['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.repres_conj['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.teifh['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.ip['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.tipo_perda['valor'].append(struct.unpack('i', f.read(4))[0])
                    self.data['valor'].append(struct.unpack('8s', f.read(8))[0].decode())
                    self.observ['valor'].append(struct.unpack('43s', f.read(43))[0].decode())
                    self.vol_ref['valor'].append(struct.unpack('f', f.read(4))[0])
                    self.tipo_reg['valor'].append(struct.unpack('c', f.read(1))[0])

                    # noinspection PyBroadException
                    monitor[self.nome['valor'][-1]] = 'OK'
                    self._numero_registros += 1

                    if self._numero_registros == tot_reg+1:
                        break

        except Exception as err:
            if isinstance(err, StopIteration):
                self._conteudo = monitor
            else:
                raise

        print(f'OK! Leitura do {os.path.split(file_name)[1]} realizada com sucesso.')

    def escrever(self, file_out: str) -> None:
        """
        Metodo para a escrita do arquivo hidr.dat.
        :param file_out: Conjunto de parametros obrigatorios.
        :return:
        """

        try:
            with open(file_out, 'wb') as f:  # type: IO[bytes]

                for i in range(self._numero_registros-1):
                    f.write(struct.pack('12s', bytes(self.nome['valor'][i], 'utf-8')))
                    f.write(struct.pack('i', self.posto['valor'][i]))
                    f.write(struct.pack('8s', bytes(self.bdh['valor'][i], 'utf-8')))
                    f.write(struct.pack('i', self.sist['valor'][i]))
                    f.write(struct.pack('i', self.empr['valor'][i]))
                    f.write(struct.pack('i', self.jusante['valor'][i]))
                    f.write(struct.pack('i', self.desvio['valor'][i]))
                    f.write(struct.pack('f', self.vol_min['valor'][i]))
                    f.write(struct.pack('f', self.vol_max['valor'][i]))
                    f.write(struct.pack('f', self.vol_vert['valor'][i]))
                    f.write(struct.pack('f', self.vol_min_desv['valor'][i]))
                    f.write(struct.pack('f', self.cota_min['valor'][i]))
                    f.write(struct.pack('f', self.cota_max['valor'][i]))
                    for j in range(5):
                        f.write(struct.pack('f', self.pol_cota_vol['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.pol_cota_area['valor'][i][j]))
                    for j in range(12):
                        f.write(struct.pack('i', self.coef_evap['valor'][i][j]))
                    f.write(struct.pack('i', self.num_conj_maq['valor'][i]))
                    for j in range(5):
                        f.write(struct.pack('i', self.maq_por_conj['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.pef_por_conj['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqt['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqt['valor_2'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqt['valor_3'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqt['valor_4'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqt['valor_5'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqg['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqg['valor_2'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqg['valor_3'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqg['valor_4'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbqg['valor_5'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbpt['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbpt['valor_2'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbpt['valor_3'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbpt['valor_4'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.cf_hbpt['valor_5'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('f', self.alt_efet_conj['valor'][i][j]))
                    for j in range(5):
                        f.write(struct.pack('i', self.vaz_efet_conj['valor'][i][j]))
                    f.write(struct.pack('f', self.prod_esp['valor'][i]))
                    f.write(struct.pack('f', self.perda_hid['valor'][i]))
                    f.write(struct.pack('i', self.num_pol_vnj['valor'][i]))
                    for j in range(6):
                        f.write(struct.pack('f', self.pol_vaz_niv_jus['valor'][i][j]))
                    for j in range(6):
                        f.write(struct.pack('f', self.pol_vaz_niv_jus['valor_2'][i][j]))
                    for j in range(6):
                        f.write(struct.pack('f', self.pol_vaz_niv_jus['valor_3'][i][j]))
                    for j in range(6):
                        f.write(struct.pack('f', self.pol_vaz_niv_jus['valor_4'][i][j]))
                    for j in range(6):
                        f.write(struct.pack('f', self.pol_vaz_niv_jus['valor_5'][i][j]))
                    for j in range(6):
                        f.write(struct.pack('f', self.cota_ref_nivel_jus['valor'][i][j]))
                    f.write(struct.pack('f', self.cfmed['valor'][i]))
                    f.write(struct.pack('i', self.inf_canal_fuga['valor'][i]))
                    f.write(struct.pack('f', self.fator_carga_max['valor'][i]))
                    f.write(struct.pack('f', self.fator_carga_min['valor'][i]))
                    f.write(struct.pack('i', self.vaz_min['valor'][i]))
                    f.write(struct.pack('i', self.unid_base['valor'][i]))
                    f.write(struct.pack('i', self.tipo_turb['valor'][i]))
                    f.write(struct.pack('i', self.repres_conj['valor'][i]))
                    f.write(struct.pack('f', self.teifh['valor'][i]))
                    f.write(struct.pack('f', self.ip['valor'][i]))
                    f.write(struct.pack('i', self.tipo_perda['valor'][i]))
                    f.write(struct.pack('8s', self.data['valor'][i]))
                    f.write(struct.pack('43s', self.observ['valor'][i]))
                    f.write(struct.pack('f', self.vol_ref['valor'][i]))
                    f.write(struct.pack('c', self.tipo_reg['valor'][i]))

        except Exception:
            raise

        print(f'OK! Escrita do {os.path.split(file_out)[1]} realizada com sucesso.')
