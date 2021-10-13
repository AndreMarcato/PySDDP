from PySDDP.dessem.script.templates.dados_eletricos import DadosEletricosTemplate


import pandas as pd
from typing import IO
import os

COMENTARIO = '('
END = ['9999', '99999']
SIZE_LINE = int(1e2)


class DadosEletricos(DadosEletricosTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao dos arquivos contendo os casos bases e os arquivos de
    modificacoes sobre os casos bases do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self, caso_base=True):

        super().__init__()

        self.caso_base = caso_base

        self.titu = dict()
        self.titu['titu'] = list()

        self.dbar = dict()
        self.dbar['num'] = list()
        self.dbar['cod_oper'] = list()
        self.dbar['status'] = list()
        self.dbar['tipo'] = list()
        self.dbar['tensao'] = list()
        self.dbar['nome'] = list()
        self.dbar['angulo'] = list()
        self.dbar['ger_ativa'] = list()
        self.dbar['carga_ativa'] = list()
        self.dbar['area'] = list()
        self.dbar['num_subs'] = list()

        self.dlin = dict()
        self.dlin['barra_de'] = list()
        self.dlin['cod_oper'] = list()
        self.dlin['barra_para'] = list()
        self.dlin['circ'] = list()
        self.dlin['status'] = list()
        self.dlin['cod_ident'] = list()
        self.dlin['resist'] = list()
        self.dlin['reat'] = list()
        self.dlin['tap'] = list()
        self.dlin['defasagem'] = list()
        self.dlin['capac_norm'] = list()
        self.dlin['capac_emerg'] = list()
        self.dlin['flag_viol'] = list()
        self.dlin['flag_perd'] = list()

        self.dare = dict()
        self.dare['num_area'] = list()
        self.dare['cod_oper'] = list()
        self.dare['nome_area'] = list()

        self.danc = dict()
        self.danc['num_area'] = list()
        self.danc['fator'] = list()

        self.dusi = dict()
        self.dusi['num_elem'] = list()
        self.dusi['cod_oper'] = list()
        self.dusi['num_barra'] = list()
        self.dusi['nome_elem'] = list()
        self.dusi['num_unid'] = list()
        self.dusi['pmin'] = list()
        self.dusi['pmax'] = list()
        self.dusi['num_cad'] = list()
        self.dusi['num_grupo'] = list()
        self.dusi['tipo'] = list()

        self.dcsc = dict()
        self.dcsc['barra_de'] = list()
        self.dcsc['cod_oper'] = list()
        self.dcsc['barra_para'] = list()
        self.dcsc['circ'] = list()
        self.dcsc['reat_csc'] = list()

        self.dref = dict()
        self.dref['id'] = list()
        self.dref['cod_oper'] = list()
        self.dref['num_restr'] = list()
        self.dref['lim_inf'] = list()
        self.dref['lim_sup'] = list()
        self.dref['flag_lim'] = list()
        self.dref['obs'] = list()
        # Essa lista sera importante para escrita do arquivo
        self.dref['num_restr2'] = list()
        self.dref['cod_elem'] = list()
        self.dref['cod_oper_real'] = list()
        self.dref['barra_de'] = list()
        self.dref['barra_para'] = list()
        self.dref['circ'] = list()
        self.dref['fator'] = list()

        self.dgbt = dict()
        self.dgbt['niv_tensao'] = list()
        self.dgbt['tensao_nom'] = list()
        self.dgbt['flag_lim'] = list()
        self.dgbt['flag_perdas'] = list()

        self.comentarios = list()

    def ler(self, file_name: str) -> None:
        try:
            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True

                while continua:
                    self.next_line(f)

                    if self.linha[0] == COMENTARIO:
                        self.comentarios.append(self.linha)
                        continue

                    elif self.linha[:4] == 'TITU':
                        self.next_line(f)
                        self.titu['titu'].append(self.linha[:80])

                    elif self.linha[:4] == 'DBAR':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dbar['num'].append(self.linha[:5])
                                self.dbar['cod_oper'].append(self.linha[5])
                                self.dbar['status'].append(self.linha[6])
                                self.dbar['tipo'].append(self.linha[7])
                                self.dbar['tensao'].append(self.linha[8:10])
                                self.dbar['nome'].append(self.linha[10:22])
                                self.dbar['angulo'].append(self.linha[28:32])
                                self.dbar['ger_ativa'].append(self.linha[32:37])
                                self.dbar['carga_ativa'].append(self.linha[58:63])
                                self.dbar['area'].append(self.linha[73:76])
                                self.dbar['num_subs'].append(self.linha[96:100])
                            self.next_line(f)

                    elif self.linha[:4] == 'DLIN':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dlin['barra_de'].append(self.linha[:5])
                                self.dlin['cod_oper'].append(self.linha[7])
                                self.dlin['barra_para'].append(self.linha[10:15])
                                self.dlin['circ'].append(self.linha[15:17])
                                self.dlin['status'].append(self.linha[17])
                                self.dlin['cod_ident'].append(self.linha[18])
                                self.dlin['resist'].append(self.linha[20:26])
                                self.dlin['reat'].append(self.linha[26:32])
                                self.dlin['tap'].append(self.linha[38:43])
                                self.dlin['defasagem'].append(self.linha[53:58])
                                self.dlin['capac_norm'].append(self.linha[64:68])
                                self.dlin['capac_emerg'].append(self.linha[68:72])
                                self.dlin['flag_viol'].append(self.linha[96])
                                self.dlin['flag_perd'].append(self.linha[98])
                            self.next_line(f)

                    elif self.linha[:4] == 'DARE':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dare['num_area'].append(self.linha[:3])
                                self.dare['cod_oper'].append(self.linha[5])
                                self.dare['nome_area'].append(self.linha[18:54])
                            self.next_line(f)

                    elif self.linha[:4] == 'DANC':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.danc['num_area'].append(self.linha[:3])
                                self.danc['fator'].append(self.linha[4:10])
                            self.next_line(f)

                    elif self.linha[:4] == 'DUSI':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dusi['num_elem'].append(self.linha[:4])
                                self.dusi['cod_oper'].append(self.linha[5])
                                self.dusi['num_barra'].append(self.linha[6:11])
                                self.dusi['nome_elem'].append(self.linha[12:24])
                                self.dusi['num_unid'].append(self.linha[26:29])
                                self.dusi['pmin'].append(self.linha[32:38])
                                self.dusi['pmax'].append(self.linha[38:44])
                                self.dusi['num_cad'].append(self.linha[72:76])
                                self.dusi['num_grupo'].append(self.linha[76])
                                self.dusi['tipo'].append(self.linha[77])
                            self.next_line(f)

                    elif self.linha[:4] == 'DCSC':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dcsc['barra_de'].append(self.linha[:5])
                                self.dcsc['cod_oper'].append(self.linha[6])
                                self.dcsc['barra_para'].append(self.linha[9:14])
                                self.dcsc['circ'].append(self.linha[14:16])
                                self.dcsc['reat_csc'].append(self.linha[37:43])
                            self.next_line(f)

                    elif self.linha[:4] == 'DREF':
                        self.next_line(f)
                        self.num_restr = None
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            elif self.linha[:4] == 'RESP':
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dref['id'].append(self.linha[:4])
                                self.dref['cod_oper'].append(self.linha[5])
                                self.dref['num_restr'].append(self.linha[7:11])
                                self.dref['lim_inf'].append(self.linha[12:22])
                                self.dref['lim_sup'].append(self.linha[22:32])
                                self.dref['flag_lim'].append(self.linha[34])
                                self.dref['obs'].append(self.linha[39:89])
                                self.num_restr = self.dref['num_restr'][-1]
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dref['num_restr2'].append(self.num_restr)
                                self.dref['cod_elem'].append(self.linha[1])
                                self.dref['cod_oper_real'].append(self.linha[3])
                                self.dref['barra_de'].append(self.linha[5:10])
                                self.dref['barra_para'].append(self.linha[10:15])
                                self.dref['circ'].append(self.linha[15:17])
                                self.dref['fator'].append(self.linha[19:29])
                            self.next_line(f)

                    elif self.linha[:4] == 'DGBT':
                        self.next_line(f)
                        while self.linha.strip() not in END:
                            if self.linha[0] == COMENTARIO:
                                self.comentarios.append(self.linha)
                            else:
                                self.linha = self.linha.replace('\n', '')

                                if len(self.linha) < SIZE_LINE:
                                    self.linha += ' ' * (SIZE_LINE - len(self.linha))
                                else:
                                    pass

                                self.dgbt['niv_tensao'].append(self.linha[:2])
                                self.dgbt['tensao_nom'].append(self.linha[3:8])
                                self.dgbt['flag_lim'].append(self.linha[10])
                                try:
                                    self.dgbt['flag_perdas'].append(self.linha[15])
                                except IndexError:
                                    self.dgbt['flag_perdas'].append('')
                            self.next_line(f)

                    elif self.linha[:3] == 'FIM':
                        self.bloco_titu['df'] = pd.DataFrame(self.titu)
                        self.bloco_dbar['df'] = pd.DataFrame(self.dbar)
                        self.bloco_dlin['df'] = pd.DataFrame(self.dlin)
                        self.bloco_dare['df'] = pd.DataFrame(self.dare)
                        self.bloco_danc['df'] = pd.DataFrame(self.danc)
                        self.bloco_dusi['df'] = pd.DataFrame(self.dusi)
                        self.bloco_dcsc['df'] = pd.DataFrame(self.dcsc)
                        self.bloco_dgbt['df'] = pd.DataFrame(self.dgbt)

                        # Tratamento do bloco dref
                        self.dref['id'].append(None)
                        self.dref['cod_oper'].append(None)
                        self.dref['num_restr'].append(None)
                        self.dref['lim_inf'].append(None)
                        self.dref['lim_sup'].append(None)
                        self.dref['flag_lim'].append(None)
                        self.dref['obs'].append(None)
                        for id, value in enumerate(self.dref['num_restr2']):
                            if value is self.dref['num_restr'][id]:
                                pass
                            else:
                                self.dref['id'].insert(id, self.dref['id'][id - 1])
                                self.dref['cod_oper'].insert(id, self.dref['cod_oper'][id - 1])
                                self.dref['num_restr'].insert(id, self.dref['num_restr'][id - 1])
                                self.dref['lim_inf'].insert(id, self.dref['lim_inf'][id - 1])
                                self.dref['lim_sup'].insert(id, self.dref['lim_sup'][id - 1])
                                self.dref['flag_lim'].insert(id, self.dref['flag_lim'][id - 1])
                                self.dref['obs'].insert(id, self.dref['obs'][id - 1])
                        self.dref['id'].remove(None)
                        self.dref['cod_oper'].remove(None)
                        self.dref['num_restr'].remove(None)
                        self.dref['lim_inf'].remove(None)
                        self.dref['lim_sup'].remove(None)
                        self.dref['flag_lim'].remove(None)
                        self.dref['obs'].remove(None)
                        self.bloco_dref['df'] = pd.DataFrame(self.dref)

                        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
                        break

                    else:
                        continue

        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_titu['df'] = pd.DataFrame(self.titu)
                self.bloco_dbar['df'] = pd.DataFrame(self.dbar)
                self.bloco_dlin['df'] = pd.DataFrame(self.dlin)
                self.bloco_dare['df'] = pd.DataFrame(self.dare)
                self.bloco_danc['df'] = pd.DataFrame(self.danc)
                self.bloco_dusi['df'] = pd.DataFrame(self.dusi)
                self.bloco_dcsc['df'] = pd.DataFrame(self.dcsc)
                self.bloco_dgbt['df'] = pd.DataFrame(self.dgbt)

                # Tratamento do bloco dref
                self.dref['id'].append(None)
                self.dref['cod_oper'].append(None)
                self.dref['num_restr'].append(None)
                self.dref['lim_inf'].append(None)
                self.dref['lim_sup'].append(None)
                self.dref['flag_lim'].append(None)
                self.dref['obs'].append(None)
                for id, value in enumerate(self.dref['num_restr2']):
                    if value is self.dref['num_restr'][id]:
                        pass
                    else:
                        self.dref['id'].insert(id, self.dref['id'][id - 1])
                        self.dref['cod_oper'].insert(id, self.dref['cod_oper'][id - 1])
                        self.dref['num_restr'].insert(id, self.dref['num_restr'][id - 1])
                        self.dref['lim_inf'].insert(id, self.dref['lim_inf'][id - 1])
                        self.dref['lim_sup'].insert(id, self.dref['lim_sup'][id - 1])
                        self.dref['flag_lim'].insert(id, self.dref['flag_lim'][id - 1])
                        self.dref['obs'].insert(id, self.dref['obs'][id - 1])
                self.dref['id'].remove(None)
                self.dref['cod_oper'].remove(None)
                self.dref['num_restr'].remove(None)
                self.dref['lim_inf'].remove(None)
                self.dref['lim_sup'].remove(None)
                self.dref['flag_lim'].remove(None)
                self.dref['obs'].remove(None)
                self.bloco_dref['df'] = pd.DataFrame(self.dref)

                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                if not self.bloco_titu['df'].empty:
                    if self.caso_base:
                        f.write('TITU\n')
                    else:
                        f.write('TITU MUDA\n')
                    for idx, value in self.bloco_titu['df'].iterrows():
                        linha = self.bloco_titu['formato'].format(**value)
                        f.write(linha)
                    # f.write('99999\n')

                if not self.bloco_dbar['df'].empty:
                    if self.caso_base:
                        f.write('DBAR\n')
                    else:
                        f.write('DBAR MUDA\n')
                    f.write(self.bloco_dbar['descricao'])
                    for idx, value in self.bloco_dbar['df'].iterrows():
                        linha = self.bloco_dbar['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_dlin['df'].empty:
                    if self.caso_base:
                        f.write('DLIN\n')
                    else:
                        f.write('DLIN MUDA\n')
                    f.write(self.bloco_dlin['descricao'])
                    for idx, value in self.bloco_dlin['df'].iterrows():
                        linha = self.bloco_dlin['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_dare['df'].empty:
                    if self.caso_base:
                        f.write('DARE\n')
                    else:
                        f.write('DARE MUDA\n')
                    f.write(self.bloco_dare['descricao'])
                    for idx, value in self.bloco_dare['df'].iterrows():
                        linha = self.bloco_dare['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_danc['df'].empty:
                    if self.caso_base:
                        f.write('DANC\n')
                    else:
                        f.write('DANC MUDA\n')
                    # f.write(self.bloco_danc['descricao'])
                    for idx, value in self.bloco_danc['df'].iterrows():
                        linha = self.bloco_danc['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_dusi['df'].empty:
                    if self.caso_base:
                        f.write('DUSI\n')
                    else:
                        f.write('DUSI MUDA\n')
                    f.write(self.bloco_dusi['descricao'])
                    for idx, value in self.bloco_dusi['df'].iterrows():
                        linha = self.bloco_dusi['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_dcsc['df'].empty:
                    if self.caso_base:
                        f.write('DCSC\n')
                    else:
                        f.write('DCSC MUDA\n')
                    f.write(self.bloco_dcsc['descricao'])
                    for idx, value in self.bloco_dcsc['df'].iterrows():
                        linha = self.bloco_dcsc['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                if not self.bloco_dref['df'].empty:
                    if self.caso_base:
                        f.write('DREF\n')
                    else:
                        f.write('DREF MUDA\n')
                    f.write(self.bloco_dref['descricao_resp'])
                    f.write(self.bloco_dref['descricao'])
                    id = None
                    for idx, value in self.bloco_dref['df'].iterrows():
                        linha1 = self.bloco_dref['formato_resp'].format(**value)
                        if linha1 == id:
                            pass
                        else:
                            f.write(linha1)
                            id = linha1
                        linha2 = self.bloco_dref['formato'].format(**value)
                        f.write(linha2)
                    f.write('99999\n')

                if not self.bloco_dgbt['df'].empty:
                    if self.caso_base:
                        f.write('DGBT\n')
                    else:
                        f.write('DGBT MUDA\n')
                    f.write(self.bloco_dgbt['descricao'])
                    for idx, value in self.bloco_dgbt['df'].iterrows():
                        linha = self.bloco_dgbt['formato'].format(**value)
                        f.write(linha)
                    f.write('99999\n')

                f.write('FIM')

        except Exception:
            raise
