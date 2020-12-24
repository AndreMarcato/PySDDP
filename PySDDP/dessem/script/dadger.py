from PySDDP.dessem.script.templates.dadger import DadgerTemplate

import pandas as pd
import os
from typing import IO

COMENTARIO = '&'


class Dadger(DadgerTemplate):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Entdados do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.comentarios = list()
        self.tm = dict()
        self.sist = dict()
        self.ree = dict()
        self.uh = dict()
        self.tviag = dict()
        self.ut = dict()
        self.usie = dict()
        self.dp = dict()
        self.de = dict()
        self.cd = dict()
        self.ri = dict()
        self.ia = dict()
        self.rd = dict()
        self.rivar = dict()
        self.it = dict()
        self.gp = dict()
        self.ni = dict()
        self.ve = dict()
        self.ci_ce = dict()
        self.re = dict()
        self.lu = dict()
        self.fh = dict()
        self.ft = dict()
        self.fi = dict()
        self.fe = dict()
        self.fr = dict()
        self.fc = dict()
        self.ac = dict()
        self.da = dict()
        self.fp = dict()
        self.ez = dict()
        self.ag = dict()
        self.mh = dict()
        self.mt = dict()
        self.tx = dict()
        self.pq = dict()
        self.secr = dict()
        self.cr = dict()
        self.r11 = dict()
        self.vr = dict()
        self.pd = dict()
        self.vm = dict()
        self.df = dict()
        self.me = dict()
        self.meta_cjsist = dict()
        self.meta_sist = dict()
        self.meta_usit = dict()
        self.sh = dict()
        self.tf = dict()
        self.rs = dict()
        self.sp = dict()
        self.ps = dict()
        self.pp = dict()

    def ler(self, file_name: str) -> None:

        self.entdados = list()

        # listas referentes ao dicionário TM
        self.tm['mne'] = list()
        self.tm['dd'] = list()
        self.tm['hr'] = list()
        self.tm['mh'] = list()
        self.tm['durac'] = list()
        self.tm['rede'] = list()
        self.tm['patamar'] = list()

        # listas referentes ao dicionário SIST
        self.sist['mne'] = list()
        self.sist['num'] = list()
        self.sist['mne_iden'] = list()
        self.sist['flag'] = list()
        self.sist['nome'] = list()

        # listas referentes ao dicionário REE
        self.ree['mne'] = list()
        self.ree['num_ree'] = list()
        self.ree['num_sub'] = list()
        self.ree['nome'] = list()

        # listas referentes ao dicionário UH
        self.uh['mne'] = list()
        self.uh['ind'] = list()
        self.uh['nome'] = list()
        self.uh['ss'] = list()
        self.uh['vinic'] = list()
        self.uh['evap'] = list()
        self.uh['di'] = list()
        self.uh['hi'] = list()
        self.uh['m'] = list()
        self.uh['vmor'] = list()
        self.uh['prod'] = list()
        self.uh['rest'] = list()

        # listas referentes ao dicionário TVIAG
        self.tviag['mne'] = list()
        self.tviag['mont'] = list()
        self.tviag['jus'] = list()
        self.tviag['tp'] = list()
        self.tviag['hr'] = list()
        self.tviag['tpTviag'] = list()

        # listas referentes ao dicionário UT
        self.ut['mne'] = list()
        self.ut['num'] = list()
        self.ut['nome'] = list()
        self.ut['ss'] = list()
        self.ut['flag'] = list()
        self.ut['di'] = list()
        self.ut['hi'] = list()
        self.ut['mi'] = list()
        self.ut['df'] = list()
        self.ut['hf'] = list()
        self.ut['mf'] = list()
        self.ut['rest'] = list()
        self.ut['gmin'] = list()
        self.ut['gmax'] = list()
        self.ut['g_anterior'] = list()

        # listas referentes ao dicionário USIE
        self.usie['mne'] = list()
        self.usie['num'] = list()
        self.usie['ss'] = list()
        self.usie['nome'] = list()
        self.usie['mont'] = list()
        self.usie['jus'] = list()
        self.usie['qmin'] = list()
        self.usie['qmax'] = list()
        self.usie['taxa_consumo'] = list()

        # listas referentes ao dicionário DP
        self.dp['mne'] = list()
        self.dp['ss'] = list()
        self.dp['di'] = list()
        self.dp['hi'] = list()
        self.dp['mi'] = list()
        self.dp['df'] = list()
        self.dp['hf'] = list()
        self.dp['mf'] = list()
        self.dp['demanda'] = list()

        # listas referentes ao dicionário DE
        self.de['mne'] = list()
        self.de['nde'] = list()
        self.de['di'] = list()
        self.de['hi'] = list()
        self.de['mi'] = list()
        self.de['df'] = list()
        self.de['hf'] = list()
        self.de['mf'] = list()
        self.de['demanda'] = list()
        self.de['justific'] = list()

        # listas referentes ao dicionário CD
        self.cd['mne'] = list()
        self.cd['is'] = list()
        self.cd['cd'] = list()
        self.cd['di'] = list()
        self.cd['hi'] = list()
        self.cd['mi'] = list()
        self.cd['df'] = list()
        self.cd['hf'] = list()
        self.cd['mf'] = list()
        self.cd['custo'] = list()
        self.cd['limsup'] = list()

        # listas referentes ao dicionário RI
        self.ri['mne'] = list()
        self.ri['di'] = list()
        self.ri['hi'] = list()
        self.ri['mi'] = list()
        self.ri['df'] = list()
        self.ri['hf'] = list()
        self.ri['mf'] = list()
        self.ri['gh50min'] = list()
        self.ri['gh50max'] = list()
        self.ri['gh60min'] = list()
        self.ri['gh60max'] = list()
        self.ri['ande'] = list()

        # listas referentes ao dicionário IA
        self.ia['mne'] = list()
        self.ia['ss1'] = list()
        self.ia['ss2'] = list()
        self.ia['di'] = list()
        self.ia['hi'] = list()
        self.ia['mi'] = list()
        self.ia['df'] = list()
        self.ia['hf'] = list()
        self.ia['mf'] = list()
        self.ia['ss1_ss2'] = list()
        self.ia['ss2_ss1'] = list()

        # listas referentes ao dicionário RD
        self.rd['mne'] = list()
        self.rd['flag_fol'] = list()
        self.rd['ncirc'] = list()
        self.rd['dbar'] = list()
        self.rd['lim'] = list()
        self.rd['dlin'] = list()
        self.rd['perd'] = list()
        self.rd['formato'] = list()

        # listas referentes ao dicionário RIVAR
        self.rivar['mne'] = list()
        self.rivar['num'] = list()
        self.rivar['ss'] = list()
        self.rivar['cod'] = list()
        self.rivar['penalidade'] = list()

        # listas referentes ao dicionário IT
        self.it['mne'] = list()
        self.it['num'] = list()
        self.it['coef'] = list()

        # listas referentes ao dicionário GP
        self.gp['mne'] = list()
        self.gp['tol_conv'] = list()
        self.gp['tol_prob'] = list()

        # listas referentes ao dicionário NI
        self.ni['mne'] = list()
        self.ni['flag'] = list()
        self.ni['nmax'] = list()

        # listas referentes ao dicionário VE
        self.ve['mne'] = list()
        self.ve['ind'] = list()
        self.ve['di'] = list()
        self.ve['hi'] = list()
        self.ve['mi'] = list()
        self.ve['df'] = list()
        self.ve['hf'] = list()
        self.ve['mf'] = list()
        self.ve['vol'] = list()

        # listas referentes ao dicionário CI/CE
        self.ci_ce['mne'] = list()
        self.ci_ce['num'] = list()
        self.ci_ce['nome'] = list()
        self.ci_ce['ss_busf'] = list()
        self.ci_ce['flag'] = list()
        self.ci_ce['di'] = list()
        self.ci_ce['hi'] = list()
        self.ci_ce['mi'] = list()
        self.ci_ce['df'] = list()
        self.ci_ce['hf'] = list()
        self.ci_ce['mf'] = list()
        self.ci_ce['unid'] = list()
        self.ci_ce['linf'] = list()
        self.ci_ce['lsup'] = list()
        self.ci_ce['custo'] = list()
        self.ci_ce['energia'] = list()

        # listas referentes ao dicionário RE
        self.re['mne'] = list()
        self.re['ind'] = list()
        self.re['di'] = list()
        self.re['hi'] = list()
        self.re['mi'] = list()
        self.re['df'] = list()
        self.re['hf'] = list()
        self.re['mf'] = list()

        # listas referentes ao dicionário LU
        self.lu['mne'] = list()
        self.lu['ind'] = list()
        self.lu['di'] = list()
        self.lu['hi'] = list()
        self.lu['mi'] = list()
        self.lu['df'] = list()
        self.lu['hf'] = list()
        self.lu['mf'] = list()
        self.lu['linf'] = list()
        self.lu['lsup'] = list()

        # listas referentes ao dicionário FH
        self.fh['mne'] = list()
        self.fh['ind'] = list()
        self.fh['di'] = list()
        self.fh['hi'] = list()
        self.fh['mi'] = list()
        self.fh['df'] = list()
        self.fh['hf'] = list()
        self.fh['mf'] = list()
        self.fh['ush'] = list()
        self.fh['unh'] = list()
        self.fh['fator'] = list()

        # listas referentes ao dicionário FT
        self.ft['mne'] = list()
        self.ft['ind'] = list()
        self.ft['di'] = list()
        self.ft['hi'] = list()
        self.ft['mi'] = list()
        self.ft['df'] = list()
        self.ft['hf'] = list()
        self.ft['mf'] = list()
        self.ft['ust'] = list()
        self.ft['fator'] = list()

        # listas referentes ao dicionário FI
        self.fi['mne'] = list()
        self.fi['ind'] = list()
        self.fi['di'] = list()
        self.fi['hi'] = list()
        self.fi['mi'] = list()
        self.fi['df'] = list()
        self.fi['hf'] = list()
        self.fi['mf'] = list()
        self.fi['ss1'] = list()
        self.fi['ss2'] = list()
        self.fi['fator'] = list()

        # listas referentes ao dicionário FE
        self.fe['mne'] = list()
        self.fe['ind'] = list()
        self.fe['di'] = list()
        self.fe['hi'] = list()
        self.fe['mi'] = list()
        self.fe['df'] = list()
        self.fe['hf'] = list()
        self.fe['mf'] = list()
        self.fe['num_contrato'] = list()
        self.fe['fator'] = list()

        # listas referentes ao dicionário FR
        self.fr['mne'] = list()
        self.fr['ind'] = list()
        self.fr['di'] = list()
        self.fr['hi'] = list()
        self.fr['mi'] = list()
        self.fr['df'] = list()
        self.fr['hf'] = list()
        self.fr['mf'] = list()
        self.fr['useol'] = list()
        self.fr['fator'] = list()

        # listas referentes ao dicionário FC
        self.fc['mne'] = list()
        self.fc['ind'] = list()
        self.fc['di'] = list()
        self.fc['hi'] = list()
        self.fc['mi'] = list()
        self.fc['df'] = list()
        self.fc['hf'] = list()
        self.fc['mf'] = list()
        self.fc['demanda'] = list()
        self.fc['fator'] = list()

        # listas referentes ao dicionário AC
        self.ac['mne'] = list()
        self.ac['usi'] = list()
        self.ac['mneumonico'] = list()
        self.ac['ind'] = list()
        self.ac['valor'] = list()

        # listas referentes ao dicionário DA
        self.da['mne'] = list()
        self.da['ind'] = list()
        self.da['di'] = list()
        self.da['hi'] = list()
        self.da['mi'] = list()
        self.da['df'] = list()
        self.da['hf'] = list()
        self.da['mf'] = list()
        self.da['taxa'] = list()
        self.da['obs'] = list()

        # listas referentes ao dicionário FP
        self.fp['mne'] = list()
        self.fp['usi'] = list()
        self.fp['f'] = list()
        self.fp['nptQ'] = list()
        self.fp['nptV'] = list()
        self.fp['concavidade'] = list()
        self.fp['min_quadraticos'] = list()
        self.fp['deltaV'] = list()
        self.fp['tr'] = list()

        # listas referentes ao dicionário EZ
        self.ez['mne'] = list()
        self.ez['usi'] = list()
        self.ez['perc_vol'] = list()

        # listas referentes ao dicionário AG
        self.ag['mne'] = list()
        self.ag['num_estagios'] = list()

        # listas referentes ao dicionário MH
        self.mh['mne'] = list()
        self.mh['num'] = list()
        self.mh['gr'] = list()
        self.mh['id'] = list()
        self.mh['di'] = list()
        self.mh['hi'] = list()
        self.mh['mi'] = list()
        self.mh['df'] = list()
        self.mh['hf'] = list()
        self.mh['mf'] = list()
        self.mh['f'] = list()

        # listas referentes ao dicionário MT
        self.mt['mne'] = list()
        self.mt['ute'] = list()
        self.mt['ug'] = list()
        self.mt['di'] = list()
        self.mt['hi'] = list()
        self.mt['mi'] = list()
        self.mt['df'] = list()
        self.mt['hf'] = list()
        self.mt['mf'] = list()
        self.mt['f'] = list()

        # listas referentes ao dicionário TX
        self.tx['mne'] = list()
        self.tx['taxa_fcf'] = list()

        # listas referentes ao dicionário PQ
        self.pq['mne'] = list()
        self.pq['ind'] = list()
        self.pq['nome'] = list()
        self.pq['ss/b'] = list()
        self.pq['di'] = list()
        self.pq['hi'] = list()
        self.pq['mi'] = list()
        self.pq['df'] = list()
        self.pq['hf'] = list()
        self.pq['mf'] = list()
        self.pq['geracao'] = list()

        # listas referentes ao dicionário SECR
        self.secr['mne'] = list()
        self.secr['num'] = list()
        self.secr['nome'] = list()
        self.secr['usi_1'] = list()
        self.secr['fator_1'] = list()
        self.secr['usi_2'] = list()
        self.secr['fator_2'] = list()
        self.secr['usi_3'] = list()
        self.secr['fator_3'] = list()
        self.secr['usi_4'] = list()
        self.secr['fator_4'] = list()
        self.secr['usi_5'] = list()
        self.secr['fator_5'] = list()

        # listas referentes ao dicionário CR
        self.cr['mne'] = list()
        self.cr['num'] = list()
        self.cr['nome'] = list()
        self.cr['gr'] = list()
        self.cr['A0'] = list()
        self.cr['A1'] = list()
        self.cr['A2'] = list()
        self.cr['A3'] = list()
        self.cr['A4'] = list()
        self.cr['A5'] = list()
        self.cr['A6'] = list()

        # listas referentes ao dicionário R11
        self.r11['mne'] = list()
        self.r11['di'] = list()
        self.r11['hi'] = list()
        self.r11['mi'] = list()
        self.r11['df'] = list()
        self.r11['hf'] = list()
        self.r11['mf'] = list()
        self.r11['cotaIni'] = list()
        self.r11['varhora'] = list()
        self.r11['vardia'] = list()
        self.r11['coef'] = list()

        # listas referentes ao dicionário VR
        self.vr['mne'] = list()
        self.vr['dia'] = list()
        self.vr['mneumo_verao'] = list()

        # listas referentes ao dicionário PD
        self.pd['mne'] = list()
        self.pd['tol_perc'] = list()
        self.pd['tol_MW'] = list()

        # listas referentes ao dicionário VM
        self.vm['mne'] = list()
        self.vm['ind'] = list()
        self.vm['di'] = list()
        self.vm['hi'] = list()
        self.vm['mi'] = list()
        self.vm['df'] = list()
        self.vm['hf'] = list()
        self.vm['mf'] = list()
        self.vm['taxa_enchimento'] = list()

        # listas referentes ao dicionário DF
        self.df['mne'] = list()
        self.df['ind'] = list()
        self.df['di'] = list()
        self.df['hi'] = list()
        self.df['mi'] = list()
        self.df['df'] = list()
        self.df['hf'] = list()
        self.df['mf'] = list()
        self.df['taxa_descarga'] = list()

        # listas referentes ao dicionário ME
        self.me['mne'] = list()
        self.me['ind'] = list()
        self.me['di'] = list()
        self.me['hi'] = list()
        self.me['mi'] = list()
        self.me['df'] = list()
        self.me['hf'] = list()
        self.me['mf'] = list()
        self.me['fator'] = list()

        # listas referentes ao dicionário META CJSIST
        self.meta_cjsist['mneumo'] = list()
        self.meta_cjsist['ind'] = list()
        self.meta_cjsist['nome'] = list()

        # listas referentes ao dicionário META SIST
        self.meta_sist['mne'] = list()
        self.meta_sist['ind'] = list()
        self.meta_sist['tp'] = list()
        self.meta_sist['num'] = list()
        self.meta_sist['meta'] = list()
        self.meta_sist['tol_MW'] = list()
        self.meta_sist['tol_perc'] = list()

        # listas referentes ao dicionário META USIT
        self.meta_usit['mne'] = list()
        self.meta_usit['ind'] = list()
        self.meta_usit['tp'] = list()
        self.meta_usit['num'] = list()
        self.meta_usit['meta'] = list()
        self.meta_usit['tol_MW'] = list()
        self.meta_usit['tol_perc'] = list()

        # listas referentes ao dicionário SH
        self.sh['mne'] = list()
        self.sh['flag_simul'] = list()
        self.sh['flag_pl'] = list()
        self.sh['num_min'] = list()
        self.sh['num_max'] = list()
        self.sh['flag_quebra'] = list()
        self.sh['ind_1'] = list()
        self.sh['ind_2'] = list()
        self.sh['ind_3'] = list()
        self.sh['ind_4'] = list()
        self.sh['ind_5'] = list()

        # listas referentes ao dicionário TF
        self.tf['mne'] = list()
        self.tf['custo'] = list()

        # listas referentes ao dicionário RS
        self.rs['mne'] = list()
        self.rs['cod'] = list()
        self.rs['ind'] = list()
        self.rs['subs'] = list()
        self.rs['tp'] = list()
        self.rs['comentario'] = list()

        # listas referentes ao dicionário SP
        self.sp['mne'] = list()
        self.sp['flag'] = list()

        # listas referentes ao dicionário PS
        self.ps['mne'] = list()
        self.ps['flag'] = list()

        # listas referentes ao dicionário PP
        self.pp['mne'] = list()
        self.pp['flag'] = list()
        self.pp['iteracoes'] = list()
        self.pp['num'] = list()
        self.pp['tp'] = list()

        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]

                continua = True
                while continua:

                    self.next_line(f)
                    linha = self.linha

                    if linha[0] == COMENTARIO:
                        self.comentarios.append(linha)
                        self.entdados.append(linha)
                        continue
                    mne = linha[:6].strip().lower()
                    mne_sigla = linha[:3].strip().lower()
                    mneumo = linha[:13].strip().lower()
                    self.entdados.append(linha[:6])

                    # Leitura dos dados de acordo com o mneumo correspondente
                    if mne_sigla == 'tm':
                        self.tm['mne'].append(self.linha[:2])
                        self.tm['dd'].append(self.linha[4:6])
                        self.tm['hr'].append(self.linha[9:11])
                        self.tm['mh'].append(self.linha[14:15])
                        self.tm['durac'].append(self.linha[19:24])
                        self.tm['rede'].append(self.linha[29:30])
                        self.tm['patamar'].append(self.linha[33:39])
                        continue
                    if mne == 'sist':
                        self.sist['mne'].append(self.linha[:6])
                        self.sist['num'].append(self.linha[7:9])
                        self.sist['mne_iden'].append(self.linha[10:12])
                        self.sist['flag'].append(self.linha[13:15])
                        self.sist['nome'].append(self.linha[16:26])
                        continue
                    if mne == 'ree':
                        self.ree['mne'].append(self.linha[:3])
                        self.ree['num_ree'].append(self.linha[6:8])
                        self.ree['num_sub'].append(self.linha[9:11])
                        self.ree['nome'].append(self.linha[12:22])
                        continue
                    if mne_sigla == 'uh':
                        self.uh['mne'].append(self.linha[:2])
                        self.uh['ind'].append(self.linha[4:7])
                        self.uh['nome'].append(self.linha[9:21])
                        self.uh['ss'].append(self.linha[24:26])
                        self.uh['vinic'].append(self.linha[29:39])
                        self.uh['evap'].append(self.linha[39:40])
                        self.uh['di'].append(self.linha[41:43])
                        self.uh['hi'].append(self.linha[44:46])
                        self.uh['m'].append(self.linha[47:48])
                        self.uh['vmor'].append(self.linha[49:59])
                        self.uh['prod'].append(self.linha[64:65])
                        self.uh['rest'].append(self.linha[69:70])
                        continue
                    if mne == 'tviag':
                        self.tviag['mne'].append(self.linha[:6])
                        self.tviag['mont'].append(self.linha[6:9])
                        self.tviag['jus'].append(self.linha[10:13])
                        self.tviag['tp'].append(self.linha[14:15])
                        self.tviag['hr'].append(self.linha[19:22])
                        self.tviag['tpTviag'].append(self.linha[24:25])
                        continue
                    if mne_sigla == 'ut':
                        self.ut['mne'].append(self.linha[:2])
                        self.ut['num'].append(self.linha[4:7])
                        self.ut['nome'].append(self.linha[9:21])
                        self.ut['ss'].append(self.linha[22:24])
                        self.ut['flag'].append(self.linha[25:26])
                        self.ut['di'].append(self.linha[27:29])
                        self.ut['hi'].append(self.linha[30:32])
                        self.ut['mi'].append(self.linha[33:34])
                        self.ut['df'].append(self.linha[35:37])
                        self.ut['hf'].append(self.linha[38:40])
                        self.ut['mf'].append(self.linha[41:42])
                        self.ut['rest'].append(self.linha[46:47])
                        self.ut['gmin'].append(self.linha[47:57])
                        self.ut['gmax'].append(self.linha[57:67])
                        self.ut['g_anterior'].append(self.linha[67:77])
                        continue
                    if mne == 'usie':
                        self.usie['mne'].append(self.linha[:4])
                        self.usie['num'].append(self.linha[5:8])
                        self.usie['ss'].append(self.linha[9:11])
                        self.usie['nome'].append(self.linha[14:26])
                        self.usie['mont'].append(self.linha[29:32])
                        self.usie['jus'].append(self.linha[34:37])
                        self.usie['qmin'].append(self.linha[39:49])
                        self.usie['qmax'].append(self.linha[49:59])
                        self.usie['taxa_consumo'].append(self.linha[59:69])
                        continue
                    if mne_sigla == 'dp':
                        self.dp['mne'].append(self.linha[:2])
                        self.dp['ss'].append(self.linha[4:6])
                        self.dp['di'].append(self.linha[8:10])
                        self.dp['hi'].append(self.linha[11:13])
                        self.dp['mi'].append(self.linha[14:15])
                        self.dp['df'].append(self.linha[16:18])
                        self.dp['hf'].append(self.linha[19:21])
                        self.dp['mf'].append(self.linha[22:23])
                        self.dp['demanda'].append(self.linha[24:34])
                        continue
                    if mne_sigla == 'de':
                        self.de['mne'].append(self.linha[:2])
                        self.de['nde'].append(self.linha[4:7])
                        self.de['di'].append(self.linha[8:10])
                        self.de['hi'].append(self.linha[11:13])
                        self.de['mi'].append(self.linha[14:15])
                        self.de['df'].append(self.linha[16:18])
                        self.de['hf'].append(self.linha[19:21])
                        self.de['mf'].append(self.linha[22:23])
                        self.de['demanda'].append(self.linha[24:34])
                        self.de['justific'].append(self.linha[35:45])
                        continue
                    if mne_sigla == 'cd':
                        self.cd['mne'].append(self.linha[:2])
                        self.cd['is'].append(self.linha[3:5])
                        self.cd['cd'].append(self.linha[6:8])
                        self.cd['di'].append(self.linha[9:11])
                        self.cd['hi'].append(self.linha[12:14])
                        self.cd['mi'].append(self.linha[15:16])
                        self.cd['df'].append(self.linha[17:19])
                        self.cd['hf'].append(self.linha[20:22])
                        self.cd['mf'].append(self.linha[23:24])
                        self.cd['custo'].append(self.linha[25:35])
                        self.cd['limsup'].append(self.linha[35:45])
                        continue
                    if mne_sigla == 'ri':
                        self.ri['mne'].append(self.linha[:2])
                        self.ri['di'].append(self.linha[8:10])
                        self.ri['hi'].append(self.linha[11:13])
                        self.ri['mi'].append(self.linha[14:15])
                        self.ri['df'].append(self.linha[16:18])
                        self.ri['hf'].append(self.linha[19:21])
                        self.ri['mf'].append(self.linha[22:23])
                        self.ri['gh50min'].append(self.linha[26:36])
                        self.ri['gh50max'].append(self.linha[36:46])
                        self.ri['gh60min'].append(self.linha[46:56])
                        self.ri['gh60max'].append(self.linha[56:66])
                        self.ri['ande'].append(self.linha[66:76])
                        continue
                    if mne_sigla == 'ia':
                        self.ia['mne'].append(self.linha[:2])
                        self.ia['ss1'].append(self.linha[4:6])
                        self.ia['ss2'].append(self.linha[9:11])
                        self.ia['di'].append(self.linha[13:15])
                        self.ia['hi'].append(self.linha[16:18])
                        self.ia['mi'].append(self.linha[19:20])
                        self.ia['df'].append(self.linha[21:23])
                        self.ia['hf'].append(self.linha[24:26])
                        self.ia['mf'].append(self.linha[27:28])
                        self.ia['ss1_ss2'].append(self.linha[29:39])
                        self.ia['ss2_ss1'].append(self.linha[39:49])
                        continue
                    if mne_sigla == 'rd':
                        self.rd['mne'].append(self.linha[:2])
                        self.rd['flag_fol'].append(self.linha[4:5])
                        self.rd['ncirc'].append(self.linha[8:12])
                        self.rd['dbar'].append(self.linha[14:15])
                        self.rd['lim'].append(self.linha[16:17])
                        self.rd['dlin'].append(self.linha[18:19])
                        self.rd['perd'].append(self.linha[20:21])
                        self.rd['formato'].append(self.linha[22:23])
                        continue
                    if mne == 'rivar':
                        self.rivar['mne'].append(self.linha[:5])
                        self.rivar['num'].append(self.linha[7:10])
                        self.rivar['ss'].append(self.linha[11:14])
                        self.rivar['cod'].append(self.linha[15:17])
                        self.rivar['penalidade'].append(self.linha[19:29])
                        continue
                    if mne_sigla == 'it':
                        self.it['mne'].append(self.linha[:2])
                        self.it['num'].append(self.linha[4:6])
                        self.it['coef'].append(self.linha[9:84])
                        continue
                    if mne_sigla == 'gp':
                        self.gp['mne'].append(self.linha[:2])
                        self.gp['tol_conv'].append(self.linha[4:14])
                        self.gp['tol_prob'].append(self.linha[15:25])
                        continue
                    if mne_sigla == 'ni':
                        self.ni['mne'].append(self.linha[:2])
                        self.ni['flag'].append(self.linha[4:5])
                        self.ni['nmax'].append(self.linha[9:12])
                        continue
                    if mne_sigla == 've':
                        self.ve['mne'].append(self.linha[:2])
                        self.ve['ind'].append(self.linha[4:7])
                        self.ve['di'].append(self.linha[8:10])
                        self.ve['hi'].append(self.linha[11:13])
                        self.ve['mi'].append(self.linha[14:15])
                        self.ve['df'].append(self.linha[16:18])
                        self.ve['hf'].append(self.linha[19:21])
                        self.ve['mf'].append(self.linha[22:23])
                        self.ve['vol'].append(self.linha[24:34])
                        continue
                    if mne_sigla == 'ci' or mne_sigla == 'ce':
                        self.ci_ce['mne'].append(self.linha[:2])
                        self.ci_ce['num'].append(self.linha[3:6])
                        self.ci_ce['nome'].append(self.linha[7:17])
                        self.ci_ce['ss_busf'].append(self.linha[18:23])
                        self.ci_ce['flag'].append(self.linha[23:24])
                        self.ci_ce['di'].append(self.linha[25:27])
                        self.ci_ce['hi'].append(self.linha[28:30])
                        self.ci_ce['mi'].append(self.linha[31:32])
                        self.ci_ce['df'].append(self.linha[33:35])
                        self.ci_ce['hf'].append(self.linha[36:38])
                        self.ci_ce['mf'].append(self.linha[39:40])
                        self.ci_ce['unid'].append(self.linha[41:42])
                        self.ci_ce['linf'].append(self.linha[43:53])
                        self.ci_ce['lsup'].append(self.linha[53:63])
                        self.ci_ce['custo'].append(self.linha[63:73])
                        self.ci_ce['energia'].append(self.linha[73:83])
                        continue
                    if mne_sigla == 're':
                        self.re['mne'].append(self.linha[:2])
                        self.re['ind'].append(self.linha[4:7])
                        self.re['di'].append(self.linha[9:11])
                        self.re['hi'].append(self.linha[12:14])
                        self.re['mi'].append(self.linha[15:16])
                        self.re['df'].append(self.linha[17:19])
                        self.re['hf'].append(self.linha[20:22])
                        self.re['mf'].append(self.linha[23:24])
                        continue
                    if mne_sigla == 'lu':
                        self.lu['mne'].append(self.linha[:2])
                        self.lu['ind'].append(self.linha[4:7])
                        self.lu['di'].append(self.linha[8:10])
                        self.lu['hi'].append(self.linha[11:13])
                        self.lu['mi'].append(self.linha[14:15])
                        self.lu['df'].append(self.linha[16:18])
                        self.lu['hf'].append(self.linha[19:21])
                        self.lu['mf'].append(self.linha[22:23])
                        self.lu['linf'].append(self.linha[24:34])
                        self.lu['lsup'].append(self.linha[34:44])
                        continue
                    if mne_sigla == 'fh':
                        self.fh['mne'].append(self.linha[:2])
                        self.fh['ind'].append(self.linha[4:7])
                        self.fh['di'].append(self.linha[8:10])
                        self.fh['hi'].append(self.linha[11:13])
                        self.fh['mi'].append(self.linha[14:15])
                        self.fh['df'].append(self.linha[16:18])
                        self.fh['hf'].append(self.linha[19:21])
                        self.fh['mf'].append(self.linha[22:23])
                        self.fh['ush'].append(self.linha[24:27])
                        self.fh['unh'].append(self.linha[27:29])
                        self.fh['fator'].append(self.linha[34:44])
                        continue
                    if mne_sigla == 'ft':
                        self.ft['mne'].append(self.linha[:2])
                        self.ft['ind'].append(self.linha[4:7])
                        self.ft['di'].append(self.linha[8:10])
                        self.ft['hi'].append(self.linha[11:13])
                        self.ft['mi'].append(self.linha[14:15])
                        self.ft['df'].append(self.linha[16:18])
                        self.ft['hf'].append(self.linha[19:21])
                        self.ft['mf'].append(self.linha[22:23])
                        self.ft['ust'].append(self.linha[24:27])
                        self.ft['fator'].append(self.linha[34:44])
                        continue
                    if mne_sigla == 'fi':
                        self.fi['mne'].append(self.linha[:2])
                        self.fi['ind'].append(self.linha[4:7])
                        self.fi['di'].append(self.linha[8:10])
                        self.fi['hi'].append(self.linha[11:13])
                        self.fi['mi'].append(self.linha[14:15])
                        self.fi['df'].append(self.linha[16:18])
                        self.fi['hf'].append(self.linha[19:21])
                        self.fi['mf'].append(self.linha[22:23])
                        self.fi['ss1'].append(self.linha[24:26])
                        self.fi['ss2'].append(self.linha[29:31])
                        self.fi['fator'].append(self.linha[34:44])
                        continue
                    if mne_sigla == 'fe':
                        self.fe['mne'].append(self.linha[:2])
                        self.fe['ind'].append(self.linha[4:7])
                        self.fe['di'].append(self.linha[8:10])
                        self.fe['hi'].append(self.linha[11:13])
                        self.fe['mi'].append(self.linha[14:15])
                        self.fe['df'].append(self.linha[16:18])
                        self.fe['hf'].append(self.linha[19:21])
                        self.fe['mf'].append(self.linha[22:23])
                        self.fe['num_contrato'].append(self.linha[24:27])
                        self.fe['fator'].append(self.linha[34:44])
                        continue
                    if mne_sigla == 'fr':
                        self.fr['mne'].append(self.linha[:2])
                        self.fr['ind'].append(self.linha[4:9])
                        self.fr['di'].append(self.linha[10:12])
                        self.fr['hi'].append(self.linha[13:15])
                        self.fr['mi'].append(self.linha[16:17])
                        self.fr['df'].append(self.linha[18:20])
                        self.fr['hf'].append(self.linha[21:23])
                        self.fr['mf'].append(self.linha[24:25])
                        self.fr['useol'].append(self.linha[26:31])
                        self.fr['fator'].append(self.linha[36:46])
                        continue
                    if mne_sigla == 'fc':
                        self.fc['mne'].append(self.linha[:2])
                        self.fc['ind'].append(self.linha[4:7])
                        self.fc['di'].append(self.linha[10:12])
                        self.fc['hi'].append(self.linha[13:15])
                        self.fc['mi'].append(self.linha[16:17])
                        self.fc['df'].append(self.linha[18:20])
                        self.fc['hf'].append(self.linha[21:23])
                        self.fc['mf'].append(self.linha[24:25])
                        self.fc['demanda'].append(self.linha[26:29])
                        self.fc['fator'].append(self.linha[36:46])
                        continue
                    if mne_sigla == 'ac':
                        self.ac['mne'].append(self.linha[:2])
                        self.ac['usi'].append(self.linha[4:7])
                        self.ac['mneumonico'].append(self.linha[9:15])
                        self.ac['ind'].append(self.linha[15:19])
                        self.ac['valor'].append(self.linha[19:])
                        continue
                    if mne_sigla == 'da':
                        self.da['mne'].append(self.linha[:2])
                        self.da['ind'].append(self.linha[4:7])
                        self.da['di'].append(self.linha[8:10])
                        self.da['hi'].append(self.linha[11:13])
                        self.da['mi'].append(self.linha[14:15])
                        self.da['df'].append(self.linha[16:18])
                        self.da['hf'].append(self.linha[19:21])
                        self.da['mf'].append(self.linha[22:23])
                        self.da['taxa'].append(self.linha[24:34])
                        self.da['obs'].append(self.linha[35:47])
                        continue
                    if mne_sigla == 'fp':
                        self.fp['mne'].append(self.linha[:2])
                        self.fp['usi'].append(self.linha[3:6])
                        self.fp['f'].append(self.linha[7:8])
                        self.fp['nptQ'].append(self.linha[10:13])
                        self.fp['nptV'].append(self.linha[15:18])
                        self.fp['concavidade'].append(self.linha[20:21])
                        self.fp['min_quadraticos'].append(self.linha[24:25])
                        self.fp['deltaV'].append(self.linha[29:39])
                        self.fp['tr'].append(self.linha[39:49])
                        continue
                    if mne_sigla == 'ez':
                        self.ez['mne'].append(self.linha[:2])
                        self.ez['usi'].append(self.linha[4:7])
                        self.ez['perc_vol'].append(self.linha[9:14])
                        continue
                    if mne_sigla == 'ag':
                        self.ag['mne'].append(self.linha[:2])
                        self.ag['num_estagios'].append(self.linha[3:6])
                        continue
                    if mne_sigla == 'mh':
                        self.mh['mne'].append(self.linha[:2])
                        self.mh['num'].append(self.linha[4:7])
                        self.mh['gr'].append(self.linha[9:11])
                        self.mh['id'].append(self.linha[12:14])
                        self.mh['di'].append(self.linha[14:16])
                        self.mh['hi'].append(self.linha[17:19])
                        self.mh['mi'].append(self.linha[20:21])
                        self.mh['df'].append(self.linha[22:24])
                        self.mh['hf'].append(self.linha[25:27])
                        self.mh['mf'].append(self.linha[28:29])
                        self.mh['f'].append(self.linha[30:31])
                        continue
                    if mne_sigla == 'mt':
                        self.mt['mne'].append(self.linha[:2])
                        self.mt['ute'].append(self.linha[4:7])
                        self.mt['ug'].append(self.linha[8:11])
                        self.mt['di'].append(self.linha[13:15])
                        self.mt['hi'].append(self.linha[16:18])
                        self.mt['mi'].append(self.linha[19:20])
                        self.mt['df'].append(self.linha[21:23])
                        self.mt['hf'].append(self.linha[24:26])
                        self.mt['mf'].append(self.linha[27:28])
                        self.mt['f'].append(self.linha[29:30])
                        continue
                    if mne_sigla == 'tx':
                        self.tx['mne'].append(self.linha[:2])
                        self.tx['taxa_fcf'].append(self.linha[4:14])
                        continue
                    if mne_sigla == 'pq':
                        self.pq['mne'].append(self.linha[:2])
                        self.pq['ind'].append(self.linha[4:7])
                        self.pq['nome'].append(self.linha[9:19])
                        self.pq['ss/b'].append(self.linha[19:24])
                        self.pq['di'].append(self.linha[24:26])
                        self.pq['hi'].append(self.linha[27:29])
                        self.pq['mi'].append(self.linha[30:31])
                        self.pq['df'].append(self.linha[32:34])
                        self.pq['hf'].append(self.linha[35:37])
                        self.pq['mf'].append(self.linha[38:39])
                        self.pq['geracao'].append(self.linha[40:50])
                        continue
                    if mne == 'secr':
                        self.secr['mne'].append(self.linha[:4])
                        self.secr['num'].append(self.linha[5:8])
                        self.secr['nome'].append(self.linha[9:21])
                        self.secr['usi_1'].append(self.linha[24:27])
                        self.secr['fator_1'].append(self.linha[28:33])
                        self.secr['usi_2'].append(self.linha[34:37])
                        self.secr['fator_2'].append(self.linha[38:43])
                        self.secr['usi_3'].append(self.linha[44:47])
                        self.secr['fator_3'].append(self.linha[48:53])
                        self.secr['usi_4'].append(self.linha[54:57])
                        self.secr['fator_4'].append(self.linha[58:63])
                        self.secr['usi_5'].append(self.linha[64:67])
                        self.secr['fator_5'].append(self.linha[68:73])
                        continue
                    if mne_sigla == 'cr':
                        self.cr['mne'].append(self.linha[:2])
                        self.cr['num'].append(self.linha[4:7])
                        self.cr['nome'].append(self.linha[9:21])
                        self.cr['gr'].append(self.linha[24:26])
                        self.cr['A0'].append(self.linha[27:42])
                        self.cr['A1'].append(self.linha[43:58])
                        self.cr['A2'].append(self.linha[59:74])
                        self.cr['A3'].append(self.linha[75:90])
                        self.cr['A4'].append(self.linha[91:106])
                        self.cr['A5'].append(self.linha[107:122])
                        self.cr['A6'].append(self.linha[123:138])
                        continue
                    if mne_sigla == 'r11':
                        self.r11['mne'].append(self.linha[:3])
                        self.r11['di'].append(self.linha[4:6])
                        self.r11['hi'].append(self.linha[7:9])
                        self.r11['mi'].append(self.linha[10:11])
                        self.r11['df'].append(self.linha[12:14])
                        self.r11['hf'].append(self.linha[15:17])
                        self.r11['mf'].append(self.linha[18:19])
                        self.r11['cotaIni'].append(self.linha[20:30])
                        self.r11['varhora'].append(self.linha[30:40])
                        self.r11['vardia'].append(self.linha[40:50])
                        self.r11['coef'].append(self.linha[59:164])
                        continue
                    if mne_sigla == 'vr':
                        self.vr['mne'].append(self.linha[:2])
                        self.vr['dia'].append(self.linha[4:6])
                        self.vr['mneumo_verao'].append(self.linha[9:12])
                        continue
                    if mne_sigla == 'pd':
                        self.pd['mne'].append(self.linha[:2])
                        self.pd['tol_perc'].append(self.linha[3:9])
                        self.pd['tol_MW'].append(self.linha[12:22])
                        continue
                    if mne_sigla == 'vm':
                        self.vm['mne'].append(self.linha[:2])
                        self.vm['ind'].append(self.linha[4:7])
                        self.vm['di'].append(self.linha[8:10])
                        self.vm['hi'].append(self.linha[11:13])
                        self.vm['mi'].append(self.linha[14:15])
                        self.vm['df'].append(self.linha[16:18])
                        self.vm['hf'].append(self.linha[19:21])
                        self.vm['mf'].append(self.linha[22:23])
                        self.vm['taxa_enchimento'].append(self.linha[24:34])
                        continue
                    if mne_sigla == 'df':
                        self.df['mne'].append(self.linha[:2])
                        self.df['ind'].append(self.linha[4:7])
                        self.df['di'].append(self.linha[8:10])
                        self.df['hi'].append(self.linha[11:13])
                        self.df['mi'].append(self.linha[14:15])
                        self.df['df'].append(self.linha[16:18])
                        self.df['hf'].append(self.linha[19:21])
                        self.df['mf'].append(self.linha[22:23])
                        self.df['taxa_descarga'].append(self.linha[24:34])
                        continue
                    if mne_sigla == 'me':
                        self.me['mne'].append(self.linha[:2])
                        self.me['ind'].append(self.linha[4:7])
                        self.me['di'].append(self.linha[8:10])
                        self.me['hi'].append(self.linha[11:13])
                        self.me['mi'].append(self.linha[14:15])
                        self.me['df'].append(self.linha[16:18])
                        self.me['hf'].append(self.linha[19:21])
                        self.me['mf'].append(self.linha[22:23])
                        self.me['fator'].append(self.linha[24:34])
                        continue
                    if mneumo == 'meta cjsist':
                        self.meta_cjsist['mneumo'].append(self.linha[:13])
                        self.meta_cjsist['ind'].append(self.linha[14:17])
                        self.meta_cjsist['nome'].append(self.linha[18:20])
                        continue
                    if mneumo == 'meta receb':
                        self.meta_sist['mne'].append(self.linha[:13])
                        self.meta_sist['ind'].append(self.linha[14:17])
                        self.meta_sist['tp'].append(self.linha[19:21])
                        self.meta_sist['num'].append(self.linha[22:23])
                        self.meta_sist['meta'].append(self.linha[24:34])
                        self.meta_sist['tol_MW'].append(self.linha[34:44])
                        self.meta_sist['tol_perc'].append(self.linha[44:54])
                        continue
                    if mneumo == 'meta gter':
                        self.meta_usit['mne'].append(self.linha[:13])
                        self.meta_usit['ind'].append(self.linha[14:17])
                        self.meta_usit['tp'].append(self.linha[19:21])
                        self.meta_usit['num'].append(self.linha[22:23])
                        self.meta_usit['meta'].append(self.linha[24:34])
                        self.meta_usit['tol_MW'].append(self.linha[34:44])
                        self.meta_usit['tol_perc'].append(self.linha[44:54])
                        continue
                    if mne_sigla == 'sh':
                        self.sh['mne'].append(self.linha[:2])
                        self.sh['flag_simul'].append(self.linha[4:5])
                        self.sh['flag_pl'].append(self.linha[9:10])
                        self.sh['num_min'].append(self.linha[14:17])
                        self.sh['num_max'].append(self.linha[19:22])
                        self.sh['flag_quebra'].append(self.linha[24:25])
                        self.sh['ind_1'].append(self.linha[29:32])
                        self.sh['ind_2'].append(self.linha[34:37])
                        self.sh['ind_3'].append(self.linha[39:42])
                        self.sh['ind_4'].append(self.linha[44:47])
                        self.sh['ind_5'].append(self.linha[49:52])
                        continue
                    if mne_sigla == 'tf':
                        self.tf['mne'].append(self.linha[:2])
                        self.tf['custo'].append(self.linha[4:14])
                        continue
                    if mne_sigla == 'rs':
                        self.rs['mne'].append(self.linha[:2])
                        self.rs['cod'].append(self.linha[3:6])
                        self.rs['ind'].append(self.linha[7:11])
                        self.rs['subs'].append(self.linha[12:16])
                        self.rs['tp'].append(self.linha[22:26])
                        self.rs['comentario'].append(self.linha[27:39])
                        continue
                    if mne_sigla == 'sp':
                        self.sp['mne'].append(self.linha[:2])
                        self.sp['flag'].append(self.linha[4:5])
                        continue
                    if mne_sigla == 'ps':
                        self.ps['mne'].append(self.linha[:2])
                        self.ps['flag'].append(self.linha[4:5])
                        continue
                    if mne_sigla == 'pp':
                        self.pp['mne'].append(self.linha[:2])
                        self.pp['flag'].append(self.linha[3:4])
                        self.pp['iteracoes'].append(self.linha[5:8])
                        self.pp['num'].append(self.linha[9:12])
                        self.pp['tp'].append(self.linha[13:14])
                        continue



        except Exception as err:
            if isinstance(err, StopIteration):
                self.bloco_tm['df'] = pd.DataFrame(self.tm)
                self.bloco_sist['df'] = pd.DataFrame(self.sist)
                self.bloco_ree['df'] = pd.DataFrame(self.ree)
                self.bloco_uh['df'] = pd.DataFrame(self.uh)
                self.bloco_tviag['df'] = pd.DataFrame(self.tviag)
                self.bloco_ut['df'] = pd.DataFrame(self.ut)
                self.bloco_usie['df'] = pd.DataFrame(self.usie)
                self.bloco_dp['df'] = pd.DataFrame(self.dp)
                self.bloco_de['df'] = pd.DataFrame(self.de)
                self.bloco_cd['df'] = pd.DataFrame(self.cd)
                self.bloco_ri['df'] = pd.DataFrame(self.ri)
                self.bloco_ia['df'] = pd.DataFrame(self.ia)
                self.bloco_rd['df'] = pd.DataFrame(self.rd)
                self.bloco_rivar['df'] = pd.DataFrame(self.rivar)
                self.bloco_it['df'] = pd.DataFrame(self.it)
                self.bloco_gp['df'] = pd.DataFrame(self.gp)
                self.bloco_ni['df'] = pd.DataFrame(self.ni)
                self.bloco_ve['df'] = pd.DataFrame(self.ve)
                self.bloco_ci_ce['df'] = pd.DataFrame(self.ci_ce)
                self.bloco_re['df'] = pd.DataFrame(self.re)
                self.bloco_lu['df'] = pd.DataFrame(self.lu)
                self.bloco_fh['df'] = pd.DataFrame(self.fh)
                self.bloco_ft['df'] = pd.DataFrame(self.ft)
                self.bloco_fi['df'] = pd.DataFrame(self.fi)
                self.bloco_fe['df'] = pd.DataFrame(self.fe)
                self.bloco_fr['df'] = pd.DataFrame(self.fr)
                self.bloco_fc['df'] = pd.DataFrame(self.fc)
                self.bloco_ac['df'] = pd.DataFrame(self.ac)
                self.bloco_da['df'] = pd.DataFrame(self.da)
                self.bloco_fp['df'] = pd.DataFrame(self.fp)
                self.bloco_ez['df'] = pd.DataFrame(self.ez)
                self.bloco_ag['df'] = pd.DataFrame(self.ag)
                self.bloco_mh['df'] = pd.DataFrame(self.mh)
                self.bloco_mt['df'] = pd.DataFrame(self.mt)
                self.bloco_tx['df'] = pd.DataFrame(self.tx)
                self.bloco_pq['df'] = pd.DataFrame(self.pq)
                self.bloco_secr['df'] = pd.DataFrame(self.secr)
                self.bloco_cr['df'] = pd.DataFrame(self.cr)
                self.bloco_r11['df'] = pd.DataFrame(self.r11)
                self.bloco_vr['df'] = pd.DataFrame(self.vr)
                self.bloco_pd['df'] = pd.DataFrame(self.pd)
                self.bloco_vm['df'] = pd.DataFrame(self.vm)
                self.bloco_df['df'] = pd.DataFrame(self.df)
                self.bloco_me['df'] = pd.DataFrame(self.me)
                self.bloco_meta_cjsist['df'] = pd.DataFrame(self.meta_cjsist)
                self.bloco_meta_sist['df'] = pd.DataFrame(self.meta_sist)
                self.bloco_meta_usit['df'] = pd.DataFrame(self.meta_usit)
                self.bloco_sh['df'] = pd.DataFrame(self.sh)
                self.bloco_tf['df'] = pd.DataFrame(self.tf)
                self.bloco_rs['df'] = pd.DataFrame(self.rs)
                self.bloco_sp['df'] = pd.DataFrame(self.sp)
                self.bloco_ps['df'] = pd.DataFrame(self.ps)
                self.bloco_pp['df'] = pd.DataFrame(self.pp)
                print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")
            else:
                raise

    def escrever(self, file_out: str) -> None:

        try:
            with open(file_out, 'w', encoding='latin-1') as f:  # type: IO[str]

                num_linhas = len(self.entdados)
                i_tm = 0
                i_sist = 0
                i_ree = 0
                i_uh = 0
                i_tviag = 0
                i_ut = 0
                i_usie = 0
                i_dp = 0
                i_de = 0
                i_cd = 0
                i_ri = 0
                i_ia = 0
                i_rd = 0
                i_rivar = 0
                i_it = 0
                i_gp = 0
                i_ni = 0
                i_ve = 0
                i_ci_ce = 0
                i_re = 0
                i_lu = 0
                i_fh = 0
                i_ft = 0
                i_fi = 0
                i_fe = 0
                i_fr = 0
                i_fc = 0
                i_ac = 0
                i_da = 0
                i_fp = 0
                i_ez = 0
                i_ag = 0
                i_mh = 0
                i_mt = 0
                i_tx = 0
                i_pq = 0
                i_secr = 0
                i_cr = 0
                i_r11 = 0
                i_vr = 0
                i_pd = 0
                i_vm = 0
                i_df = 0
                i_me = 0
                i_meta_cjsist = 0
                i_meta_sist = 0
                i_meta_usit = 0
                i_sh = 0
                i_tf = 0
                i_rs = 0
                i_sp = 0
                i_ps = 0
                i_pp = 0

                for i in range(num_linhas):
                    # Verifica comentário
                    self.entdados[i] = self.entdados[i].replace('\n', '')
                    linha = self.entdados[i].strip()
                    verifica_comentario = linha[0] == COMENTARIO
                    if verifica_comentario:
                        f.write(self.entdados[i])
                        f.write("\n")
                        continue

                    if linha[:2] == 'TM':
                        self.bloco_tm['df']['patamar'] = self.bloco_tm['df']['patamar'].str.replace('\n', '')
                        for idx, value in self.bloco_tm['df'].iterrows():
                            if idx == i_tm:
                                linha = self.bloco_tm['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_tm = i_tm + 1
                        continue
                    if linha == 'SIST':
                        self.bloco_sist['df']['nome'] = self.bloco_sist['df']['nome'].str.replace('\n', '')
                        for idx, value in self.bloco_sist['df'].iterrows():
                            if idx == i_sist:
                                linha = self.bloco_sist['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_sist = i_sist + 1
                        continue
                    if linha == 'REE':
                        self.bloco_ree['df']['nome'] = self.bloco_ree['df']['nome'].str.replace('\n', '')
                        for idx, value in self.bloco_ree['df'].iterrows():
                            if idx == i_ree:
                                linha = self.bloco_ree['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ree = i_ree + 1
                        continue
                    if linha[:2] == 'UH':
                        self.bloco_uh['df']['di'] = self.bloco_uh['df']['di'].str.replace('\n', '')
                        for idx, value in self.bloco_uh['df'].iterrows():
                            if idx == i_uh:
                                linha = self.bloco_uh['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_uh = i_uh + 1
                        continue
                    if linha == 'TVIAG':
                        self.bloco_tviag['df']['tpTviag'] = self.bloco_tviag['df']['tpTviag'].str.replace('\n', '')
                        for idx, value in self.bloco_tviag['df'].iterrows():
                            if idx == i_tviag:
                                linha = self.bloco_tviag['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_tviag = i_tviag + 1
                        continue
                    if linha[:2] == 'UT':
                        self.bloco_ut['df']['g_anterior'] = self.bloco_ut['df']['g_anterior'].str.replace('\n', '')
                        for idx, value in self.bloco_ut['df'].iterrows():
                            if idx == i_ut:
                                linha = self.bloco_ut['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ut = i_ut + 1
                        continue
                    if linha == 'USIE':
                        self.bloco_usie['df']['taxa_consumo'] = self.bloco_usie['df']['taxa_consumo'].str.replace('\n',
                                                                                                                  '')
                        for idx, value in self.bloco_usie['df'].iterrows():
                            if idx == i_usie:
                                linha = self.bloco_usie['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_usie = i_usie + 1
                        continue
                    if linha[:2] == 'DP':
                        self.bloco_dp['df']['demanda'] = self.bloco_dp['df']['demanda'].str.replace('\n', '')
                        for idx, value in self.bloco_dp['df'].iterrows():
                            if idx == i_dp:
                                linha = self.bloco_dp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_dp = i_dp + 1
                        continue
                    if linha[:2] == 'DE':
                        self.bloco_de['df']['justific'] = self.bloco_de['df']['justific'].str.replace('\n', '')
                        for idx, value in self.bloco_de['df'].iterrows():
                            if idx == i_de:
                                linha = self.bloco_de['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_de = i_de + 1
                        continue
                    if linha[:2] == 'CD':
                        self.bloco_cd['df']['limsup'] = self.bloco_cd['df']['limsup'].str.replace('\n', '')
                        for idx, value in self.bloco_cd['df'].iterrows():
                            if idx == i_cd:
                                linha = self.bloco_cd['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_cd = i_cd + 1
                        continue
                    if linha[:3] == 'RI':
                        self.bloco_ri['df']['ande'] = self.bloco_ri['df']['ande'].str.replace('\n', '')
                        for idx, value in self.bloco_ri['df'].iterrows():
                            if idx == i_ri:
                                linha = self.bloco_ri['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ri = i_ri + 1
                        continue
                    if linha[:2] == 'IA':
                        self.bloco_ia['df']['ss2_ss1'] = self.bloco_ia['df']['ss2_ss1'].str.replace('\n', '')
                        for idx, value in self.bloco_ia['df'].iterrows():
                            if idx == i_ia:
                                linha = self.bloco_ia['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ia = i_ia + 1
                        continue
                    if linha[:2] == 'RD':
                        self.bloco_rd['df']['formato'] = self.bloco_rd['df']['formato'].str.replace('\n', '')
                        for idx, value in self.bloco_rd['df'].iterrows():
                            if idx == i_rd:
                                linha = self.bloco_rd['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_rd = i_rd + 1
                        continue
                    if linha == 'RIVAR':
                        self.bloco_rivar['df']['cod'] = self.bloco_rivar['df']['cod'].str.replace('\n', '')
                        for idx, value in self.bloco_rivar['df'].iterrows():
                            if idx == i_rivar:
                                linha = self.bloco_rivar['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_rivar = i_rivar + 1
                        continue
                    if linha[:2] == 'IT':
                        self.bloco_it['df']['coef'] = self.bloco_it['df']['coef'].str.replace('\n', '')
                        for idx, value in self.bloco_it['df'].iterrows():
                            if idx == i_it:
                                linha = self.bloco_it['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_it = i_it + 1
                        continue
                    if linha[:2] == 'GP':
                        self.bloco_gp['df']['tol_prob'] = self.bloco_gp['df']['tol_prob'].str.replace('\n', '')
                        for idx, value in self.bloco_gp['df'].iterrows():
                            if idx == i_gp:
                                linha = self.bloco_gp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_gp = i_gp + 1
                        continue
                    if linha[:2] == 'NI':
                        self.bloco_ni['df']['nmax'] = self.bloco_ni['df']['nmax'].str.replace('\n', '')
                        for idx, value in self.bloco_ni['df'].iterrows():
                            if idx == i_ni:
                                linha = self.bloco_ni['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ni = i_ni + 1
                        continue
                    if linha[:2] == 'VE':
                        self.bloco_ve['df']['valor'] = self.bloco_ve['df']['vol'].str.replace('\n', '')
                        for idx, value in self.bloco_ve['df'].iterrows():
                            if idx == i_ve:
                                linha = self.bloco_ve['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ve = i_ve + 1
                        continue
                    if linha[:2] == 'CI' or linha[:2] == 'CE':
                        self.bloco_ci_ce['df']['energia'] = self.bloco_ci_ce['df']['energia'].str.replace('\n', '')
                        for idx, value in self.bloco_ci_ce['df'].iterrows():
                            if idx == i_ci_ce:
                                linha = self.bloco_ci_ce['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ci_ce = i_ci_ce + 1
                        continue
                    if linha[:2] == 'RE':
                        self.bloco_re['df']['mf'] = self.bloco_re['df']['mf'].str.replace('\n', '')
                        self.bloco_re['df']['df'] = self.bloco_re['df']['df'].str.replace('\n', '')
                        for idx, value in self.bloco_re['df'].iterrows():
                            if idx == i_re:
                                linha = self.bloco_re['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_re = i_re + 1
                        continue
                    if linha[:2] == 'LU':
                        self.bloco_lu['df']['lsup'] = self.bloco_lu['df']['lsup'].str.replace('\n', '')
                        self.bloco_lu['df']['linf'] = self.bloco_lu['df']['linf'].str.replace('\n', '')
                        for idx, value in self.bloco_lu['df'].iterrows():
                            if idx == i_lu:
                                linha = self.bloco_lu['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_lu = i_lu + 1
                        continue
                    if linha[:2] == 'FH':
                        self.bloco_fh['df']['fator'] = self.bloco_fh['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_fh['df'].iterrows():
                            if idx == i_fh:
                                linha = self.bloco_fh['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fh = i_fh + 1
                        continue
                    if linha[:2] == 'FT':
                        self.bloco_ft['df']['fator'] = self.bloco_ft['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_ft['df'].iterrows():
                            if idx == i_ft:
                                linha = self.bloco_ft['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ft = i_ft + 1
                        continue
                    if linha[:2] == 'FI':
                        self.bloco_fi['df']['fator'] = self.bloco_fi['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_fi['df'].iterrows():
                            if idx == i_fi:
                                linha = self.bloco_fi['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fi = i_fi + 1
                        continue
                    if linha[:2] == 'FE':
                        self.bloco_fe['df']['fator'] = self.bloco_fe['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_fe['df'].iterrows():
                            if idx == i_fe:
                                linha = self.bloco_fe['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fe = i_fe + 1
                        continue
                    if linha[:2] == 'FR':
                        self.bloco_fr['df']['fator'] = self.bloco_fr['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_fr['df'].iterrows():
                            if idx == i_fr:
                                linha = self.bloco_fr['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fr = i_fr + 1
                        continue
                    if linha[:2] == 'FC':
                        self.bloco_fc['df']['fator'] = self.bloco_fc['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_fc['df'].iterrows():
                            if idx == i_fc:
                                linha = self.bloco_fc['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fc = i_fc + 1
                        continue
                    if linha[:2] == 'AC':
                        self.bloco_ac['df']['valor'] = self.bloco_ac['df']['valor'].str.replace('\n', '')
                        for idx, value in self.bloco_ac['df'].iterrows():
                            if idx == i_ac:
                                linha = self.bloco_ac['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ac = i_ac + 1
                        continue
                    if linha[:2] == 'DA':
                        self.bloco_da['df']['obs'] = self.bloco_da['df']['obs'].str.replace('\n', '')
                        for idx, value in self.bloco_da['df'].iterrows():
                            if idx == i_da:
                                linha = self.bloco_da['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_da = i_da + 1
                        continue
                    if linha[:2] == 'FP':
                        for idx, value in self.bloco_fp['df'].iterrows():
                            self.bloco_fp['df']['deltaV'] = self.bloco_fp['df']['deltaV'].str.replace('\n', '')
                            if idx == i_fp:
                                linha = self.bloco_fp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_fp = i_fp + 1
                        continue
                    if linha[:2] == 'EZ':
                        self.bloco_ez['df']['perc_vol'] = self.bloco_ez['df']['perc_vol'].str.replace('\n', '')
                        for idx, value in self.bloco_ez['df'].iterrows():
                            if idx == i_ez:
                                linha = self.bloco_ez['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ez = i_ez + 1
                        continue
                    if linha[:2] == 'AG':
                        self.bloco_ag['df']['num_estagios'] = self.bloco_ag['df']['num_estagios'].str.replace('\n', '')
                        for idx, value in self.bloco_ag['df'].iterrows():
                            if idx == i_ag:
                                linha = self.bloco_ag['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ag = i_ag + 1
                        continue
                    if linha[:2] == 'MH':
                        self.bloco_mh['df']['f'] = self.bloco_mh['df']['f'].str.replace('\n', '')
                        for idx, value in self.bloco_mh['df'].iterrows():
                            if idx == i_mh:
                                linha = self.bloco_mh['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_mh = i_mh + 1
                        continue
                    if linha[:2] == 'MT':
                        self.bloco_mt['df']['f'] = self.bloco_mt['df']['f'].str.replace('\n', '')
                        for idx, value in self.bloco_mt['df'].iterrows():
                            if idx == i_mt:
                                linha = self.bloco_mt['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_mt = i_mt + 1
                        continue
                    if linha[:2] == 'TX':
                        self.bloco_tx['df']['taxa_fcf'] = self.bloco_tx['df']['taxa_fcf'].str.replace('\n', '')
                        for idx, value in self.bloco_tx['df'].iterrows():
                            if idx == i_tx:
                                linha = self.bloco_tx['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_tx = i_tx + 1
                        continue
                    if linha[:2] == 'PQ':
                        self.bloco_pq['df']['geracao'] = self.bloco_pq['df']['geracao'].str.replace('\n', '')
                        for idx, value in self.bloco_pq['df'].iterrows():
                            if idx == i_pq:
                                linha = self.bloco_pq['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_pq = i_pq + 1
                        continue
                    if linha == 'SECR':
                        self.bloco_secr['df']['fator_5'] = self.bloco_secr['df']['fator_5'].str.replace('\n', '')
                        self.bloco_secr['df']['fator_4'] = self.bloco_secr['df']['fator_4'].str.replace('\n', '')
                        self.bloco_secr['df']['fator_3'] = self.bloco_secr['df']['fator_3'].str.replace('\n', '')
                        self.bloco_secr['df']['fator_2'] = self.bloco_secr['df']['fator_2'].str.replace('\n', '')
                        self.bloco_secr['df']['fator_1'] = self.bloco_secr['df']['fator_1'].str.replace('\n', '')
                        for idx, value in self.bloco_secr['df'].iterrows():
                            if idx == i_secr:
                                linha = self.bloco_secr['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_secr = i_secr + 1
                        continue
                    if linha[:2] == 'CR':
                        self.bloco_cr['df']['A6'] = self.bloco_cr['df']['A6'].str.replace('\n', '')
                        self.bloco_cr['df']['A5'] = self.bloco_cr['df']['A5'].str.replace('\n', '')
                        self.bloco_cr['df']['A4'] = self.bloco_cr['df']['A4'].str.replace('\n', '')
                        self.bloco_cr['df']['A3'] = self.bloco_cr['df']['A3'].str.replace('\n', '')
                        for idx, value in self.bloco_cr['df'].iterrows():
                            if idx == i_cr:
                                linha = self.bloco_cr['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_cr = i_cr + 1
                        continue
                    if linha[:3] == 'R11':
                        self.bloco_r11['df']['vardia'] = self.bloco_r11['df']['vardia'].str.replace('\n', '')
                        self.bloco_r11['df']['coef'] = self.bloco_r11['df']['coef'].str.replace('\n', '')
                        for idx, value in self.bloco_r11['df'].iterrows():
                            if idx == i_r11:
                                linha = self.bloco_r11['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_r11 = i_r11 + 1
                        continue
                    if linha[:2] == 'VR':
                        self.bloco_vr['df']['mneumo_verao'] = self.bloco_vr['df']['mneumo_verao'].str.replace('\n', '')
                        for idx, value in self.bloco_vr['df'].iterrows():
                            if idx == i_vr:
                                linha = self.bloco_vr['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_vr = i_vr + 1
                        continue
                    if linha[:2] == 'PD':
                        self.bloco_pd['df']['tol_perc'] = self.bloco_pd['df']['tol_perc'].str.replace('\n', '')
                        self.bloco_pd['df']['tol_MW'] = self.bloco_pd['df']['tol_MW'].str.replace('\n', '')
                        for idx, value in self.bloco_pd['df'].iterrows():
                            if idx == i_pd:
                                linha = self.bloco_pd['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_pd = i_pd + 1
                        continue
                    if linha[:2] == 'VM':
                        self.bloco_vm['df']['taxa_enchimento'] = self.bloco_vm['df']['taxa_enchimento'].str.replace(
                            '\n', '')
                        for idx, value in self.bloco_vm['df'].iterrows():
                            if idx == i_vm:
                                linha = self.bloco_vm['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_vm = i_vm + 1
                        continue
                    if linha[:2] == 'DF':
                        self.bloco_df['df']['taxa_descarga'] = self.bloco_df['df']['taxa_descarga'].str.replace('\n',
                                                                                                                '')
                        for idx, value in self.bloco_df['df'].iterrows():
                            if idx == i_df:
                                linha = self.bloco_df['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_df = i_df + 1
                        continue
                    if linha[:2] == 'ME':
                        self.bloco_me['df']['fator'] = self.bloco_me['df']['fator'].str.replace('\n', '')
                        for idx, value in self.bloco_me['df'].iterrows():
                            if idx == i_me:
                                linha = self.bloco_me['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_me = i_me + 1
                        continue
                    if linha[:13] == 'META CJSIST':
                        self.bloco_meta_cjsist['df']['nome'] = self.bloco_meta_cjsist['df']['nome'].str.replace('\n',
                                                                                                                '')
                        for idx, value in self.bloco_meta_cjsist['df'].iterrows():
                            if idx == i_meta_cjsist:
                                linha = self.bloco_meta_cjsist['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_meta_cjsist = i_meta_cjsist + 1
                        continue
                    if linha[:13] == 'META RECEB':
                        self.bloco_meta_sist['df']['tol_perc'] = self.bloco_meta_sist['df']['tol_perc'].str.replace(
                            '\n', '')
                        self.bloco_meta_sist['df']['tol_MW'] = self.bloco_meta_sist['df']['tol_MW'].str.replace('\n',
                                                                                                                '')
                        for idx, value in self.bloco_meta_sist['df'].iterrows():
                            if idx == i_meta_sist:
                                linha = self.bloco_meta_sist['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_meta_sist = i_meta_sist + 1
                        continue
                    if linha[:13] == 'META GTER':
                        self.bloco_meta_usit['df']['tol_perc'] = self.bloco_meta_usit['df']['tol_perc'].str.replace(
                            '\n', '')
                        self.bloco_meta_usit['df']['tol_MW'] = self.bloco_meta_usit['df']['tol_MW'].str.replace('\n',
                                                                                                                '')
                        for idx, value in self.bloco_meta_usit['df'].iterrows():
                            if idx == i_meta_usit:
                                linha = self.bloco_meta_usit['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_meta_usit = i_meta_usit + 1
                        continue
                    if linha[:2] == 'SH':
                        self.bloco_sh['df']['ind_1'] = self.bloco_sh['df']['ind_1'].str.replace('\n', '')
                        self.bloco_sh['df']['ind_2'] = self.bloco_sh['df']['ind_2'].str.replace('\n', '')
                        self.bloco_sh['df']['ind_3'] = self.bloco_sh['df']['ind_3'].str.replace('\n', '')
                        self.bloco_sh['df']['ind_4'] = self.bloco_sh['df']['ind_4'].str.replace('\n', '')
                        self.bloco_sh['df']['ind_5'] = self.bloco_sh['df']['ind_5'].str.replace('\n', '')
                        for idx, value in self.bloco_sh['df'].iterrows():
                            if idx == i_sh:
                                linha = self.bloco_sh['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_sh = i_sh + 1
                        continue
                    if linha[:2] == 'TF':
                        self.bloco_tf['df']['custo'] = self.bloco_tf['df']['custo'].str.replace('\n', '')
                        for idx, value in self.bloco_tf['df'].iterrows():
                            if idx == i_tf:
                                linha = self.bloco_tf['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_tf = i_tf + 1
                        continue
                    if linha[:2] == 'RS':
                        self.bloco_rs['df']['comentario'] = self.bloco_rs['df']['comentario'].str.replace('\n', '')
                        for idx, value in self.bloco_rs['df'].iterrows():
                            if idx == i_rs:
                                linha = self.bloco_rs['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_rs = i_rs + 1
                        continue
                    if linha[:2] == 'SP':
                        self.bloco_sp['df']['flag'] = self.bloco_sp['df']['flag'].str.replace('\n', '')
                        for idx, value in self.bloco_sp['df'].iterrows():
                            if idx == i_sp:
                                linha = self.bloco_sp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_sp = i_sp + 1
                        continue
                    if linha[:2] == 'PS':
                        self.bloco_ps['df']['flag'] = self.bloco_ps['df']['flag'].str.replace('\n', '')
                        for idx, value in self.bloco_ps['df'].iterrows():
                            if idx == i_ps:
                                linha = self.bloco_ps['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_ps = i_ps + 1
                        continue
                    if linha[:2] == 'PP':
                        self.bloco_pp['df']['num'] = self.bloco_pp['df']['num'].str.replace('\n', '')
                        self.bloco_pp['df']['tp'] = self.bloco_pp['df']['tp'].str.replace('\n', '')
                        for idx, value in self.bloco_pp['df'].iterrows():
                            if idx == i_pp:
                                linha = self.bloco_pp['formato'].format(**value)
                                f.write(linha)
                                continue
                        i_pp = i_pp + 1
                        continue
        except Exception:
            raise
