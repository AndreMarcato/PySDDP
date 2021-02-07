import os
from typing import IO

from PySDDP.newave.script.templates.dger import DgerTemplate


class Dger(DgerTemplate):
    def __init__(self):
        super().__init__()

        self.lista_entrada = list()
        self._conteudo_ = None
        self.dir_base = None
        self._numero_registros_ = None

    def ler(self, file_name: str) -> None:
        """
        Implementa o método para leitura do arquivo que contem os dados gerais
        para a configuração do caso que que será execucado do NEWAVE

        :param file_name: string com o caminho completo para o arquivo

        """

        self.lista_entrada.clear()

        contador = 0
        try:

            with open(file_name, 'r', encoding='latin-1') as f:  # type: IO[str]
                contador = 1
                self.next_line(f)
                self.titu_caso['valor'] = self.linha.strip()
                self.titu_caso['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.tipo_exec['resumo'] = self.linha[00:21]
                self.tipo_exec['valor'] = int(self.linha[21:25])
                self.tipo_exec['comentarios'] = self.linha[25:]
                self.tipo_exec['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.dura_peri['resumo'] = self.linha[00:21]
                self.dura_peri['valor'] = int(self.linha[21:25])
                self.dura_peri['comentarios'] = self.linha[25:]
                self.dura_peri['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.num_anos['resumo'] = self.linha[00:21]
                self.num_anos['valor'] = int(self.linha[21:25])
                self.num_anos['comentarios'] = self.linha[25:]
                self.num_anos['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.mesi_pre_est['resumo'] = self.linha[00:21]
                self.mesi_pre_est['valor'] = int(self.linha[21:25])
                self.mesi_pre_est['comentarios'] = self.linha[25:]
                self.mesi_pre_est['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.mesi_est['resumo'] = self.linha[00:21]
                self.mesi_est['valor'] = int(self.linha[21:25])
                self.mesi_est['comentarios'] = self.linha[25:]
                self.mesi_est['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.ano_ini['resumo'] = self.linha[00:21]
                self.ano_ini['valor'] = int(self.linha[21:25])
                self.ano_ini['comentarios'] = self.linha[25:]
                self.ano_ini['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.anos_pre['resumo'] = self.linha[00:21]
                self.anos_pre['valor'] = int(self.linha[21:25])
                self.anos_pre['comentarios'] = self.linha[25:]
                self.anos_pre['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.anos_pos['resumo'] = self.linha[00:21]
                self.anos_pos['valor'] = int(self.linha[21:25])
                self.anos_pos['comentarios'] = self.linha[25:]
                self.anos_pre['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.anos_pos_fin['resumo'] = self.linha[00:21]
                self.anos_pos_fin['valor'] = int(self.linha[21:25])
                self.anos_pos_fin['comentarios'] = self.linha[25:]
                self.anos_pos_fin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.imp_dado['resumo'] = self.linha[00:21]
                self.imp_dado['valor'] = int(self.linha[21:25])
                self.imp_dado['comentarios'] = self.linha[25:]
                self.imp_dado['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.imp_merc['resumo'] = self.linha[00:21]
                self.imp_merc['valor'] = int(self.linha[21:25])
                self.imp_merc['comentarios'] = self.linha[25:]
                self.imp_merc['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.imp_ener['resumo'] = self.linha[00:21]
                self.imp_ener['valor'] = int(self.linha[21:25])
                self.imp_ener['comentarios'] = self.linha[25:]
                self.imp_ener['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.imp_mode_est['resumo'] = self.linha[00:21]
                self.imp_mode_est['valor'] = int(self.linha[21:25])
                self.imp_mode_est['comentarios'] = self.linha[25:]
                self.imp_mode_est['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.imp_ree['resumo'] = self.linha[00:21]
                self.imp_ree['valor'] = int(self.linha[21:25])
                self.imp_ree['comentarios'] = self.linha[25:]
                self.imp_ree['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.max_iter['resumo'] = self.linha[00:21]
                self.max_iter['valor'] = int(self.linha[21:25])
                self.max_iter['comentarios'] = self.linha[25:]
                self.max_iter['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.nr_forw['resumo'] = self.linha[00:21]
                self.nr_forw['valor'] = int(self.linha[21:25])
                self.nr_forw['comentarios'] = self.linha[25:]
                self.nr_forw['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.nr_aber['resumo'] = self.linha[00:21]
                self.nr_aber['valor'] = int(self.linha[21:25])
                self.nr_aber['comentarios'] = self.linha[25:]
                self.nr_aber['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.nr_forw_fin['resumo'] = self.linha[00:21]
                self.nr_forw_fin['valor'] = int(self.linha[21:25])
                self.nr_forw_fin['comentarios'] = self.linha[25:]
                self.nr_forw_fin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.ord_max_parp['resumo'] = self.linha[00:21]
                self.ord_max_parp['valor'] = int(self.linha[21:25])
                self.ord_max_parp['comentarios'] = self.linha[25:]
                self.ord_max_parp['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.anoi_hist['resumo'] = self.linha[00:21]
                self.anoi_hist['valor'] = int(self.linha[21:25])
                self.anoi_hist['comentarios'] = self.linha[29:]
                self.flag_tam_vaz['resumo'] = self.linha[00:21]
                self.flag_tam_vaz['valor'] = int(self.linha[28:29])
                self.flag_tam_vaz['comentarios'] = self.linha[29:]
                self.anoi_hist['ordem'] = contador
                self.flag_tam_vaz['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_earm_inic['resumo'] = self.linha[00:21]
                self.flag_earm_inic['valor'] = int(self.linha[21:25])
                self.flag_earm_inic['comentarios'] = self.linha[25:]
                self.flag_earm_inic['ordem'] = contador
                contador += 2
                self.next_line(f)
                self.next_line(f)
                self.vol_earm_inic['resumo'] = self.linha[00:21]
                self.vol_earm_inic['valor'] = list()
                fim = 21
                for i in range(len(self.linha[19:])//7):
                    ini = 19+(i*7)
                    fim = ini+7
                    self.vol_earm_inic['valor'].append(float(self.linha[ini:fim]))
                self.vol_earm_inic['comentarios'] = self.linha[fim:]
                self.vol_earm_inic['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.int_conf['resumo'] = self.linha[00:21]
                self.int_conf['valor'] = float(self.linha[21:26])
                self.int_conf['comentarios'] = self.linha[26:]
                self.int_conf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.tx_desc['resumo'] = self.linha[00:21]
                self.tx_desc['valor'] = float(self.linha[21:26])
                self.tx_desc['comentarios'] = self.linha[26:]
                self.tx_desc['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_sim_fin['resumo'] = self.linha[00:21]
                self.flag_sim_fin['valor'] = int(self.linha[21:25])
                self.flag_sim_fin['comentarios'] = self.linha[25:]
                self.flag_sim_fin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_impr_sim_fin['resumo'] = self.linha[00:21]
                self.flag_impr_sim_fin['valor'] = int(self.linha[21:25])
                self.flag_impr_sim_fin['comentarios'] = self.linha[25:]
                self.flag_impr_sim_fin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_impr_risc_def['resumo'] = self.linha[00:21]
                self.flag_impr_risc_def['valor'] = int(self.linha[21:25])
                self.flag_impr_risc_def['comentarios'] = self.linha[25:]
                self.flag_impr_risc_def['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.ser_grav_rel['resumo'] = self.linha[00:21]
                self.ser_grav_rel['valor'] = int(self.linha[21:25])
                self.ser_grav_rel['comentarios'] = self.linha[25:]
                self.ser_grav_rel['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.num_min_iter['resumo'] = self.linha[00:21]
                self.num_min_iter['valor'] = int(self.linha[21:25])
                self.iter_inic_zinf['resumo'] = self.linha[00:21]
                if len(self.linha) >= 29:
                    self.iter_inic_zinf['valor'] = int(self.linha[28:29])
                    self.num_min_iter['comentarios'] = self.linha[29:]
                    self.iter_inic_zinf['comentarios'] = self.linha[29:]
                else:
                    self.num_min_iter['comentarios'] = self.linha[25:]
                    self.iter_inic_zinf['comentarios'] = self.linha[25:]
                self.num_min_iter['ordem'] = contador
                self.iter_inic_zinf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.rac_prev['resumo'] = self.linha[00:21]
                self.rac_prev['valor'] = int(self.linha[21:25])
                self.rac_prev['comentarios'] = self.linha[25:]
                self.rac_prev['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.nr_anos_mnut['resumo'] = self.linha[00:21]
                self.nr_anos_mnut['valor'] = int(self.linha[21:25])
                self.nr_anos_mnut['comentarios'] = self.linha[25:]
                self.nr_anos_mnut['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.tend_hidr_pol['resumo'] = self.linha[00:21]
                self.tend_hidr_pol['valor'] = int(self.linha[21:25])
                self.tend_hidr_sim['resumo'] = self.linha[00:21]
                self.tend_hidr_sim['valor'] = int(self.linha[26:30])
                self.tend_hidr_pol['comentarios'] = self.linha[30:]
                self.tend_hidr_sim['comentarios'] = self.linha[30:]
                self.tend_hidr_sim['ordem'] = contador
                self.tend_hidr_pol['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_itpu['resumo'] = self.linha[00:21]
                self.flag_itpu['valor'] = int(self.linha[21:25])
                self.flag_itpu['comentarios'] = self.linha[25:]
                self.flag_itpu['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_bid_dem['resumo'] = self.linha[00:21]
                self.flag_bid_dem['valor'] = int(self.linha[21:25])
                self.flag_bid_dem['comentarios'] = self.linha[25:]
                self.flag_bid_dem['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_tran_loss['resumo'] = self.linha[00:21]
                self.flag_tran_loss['valor'] = int(self.linha[21:25])
                self.flag_tran_loss['comentarios'] = self.linha[25:]
                self.flag_tran_loss['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_el_nino['resumo'] = self.linha[00:21]
                self.flag_el_nino['valor'] = int(self.linha[21:25])
                self.flag_el_nino['comentarios'] = self.linha[25:]
                self.flag_el_nino['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_enso['resumo'] = self.linha[00:21]
                self.flag_enso['valor'] = int(self.linha[21:25])
                self.flag_enso['comentarios'] = self.linha[25:]
                self.flag_enso['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_pat['resumo'] = self.linha[00:21]
                self.flag_pat['valor'] = int(self.linha[21:25])
                self.flag_pat['comentarios'] = self.linha[25:]
                self.flag_pat['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_dsv_agua['resumo'] = self.linha[00:21]
                self.flag_dsv_agua['valor'] = int(self.linha[21:25])
                self.flag_dsv_agua['comentarios'] = self.linha[25:]
                self.flag_dsv_agua['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_dsv_ena['resumo'] = self.linha[00:21]
                self.flag_dsv_ena['valor'] = int(self.linha[21:25])
                self.flag_dsv_ena['comentarios'] = self.linha[25:]
                self.flag_dsv_ena['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_curv_segu['resumo'] = self.linha[00:21]
                self.flag_curv_segu['valor'] = int(self.linha[21:25])
                self.flag_curv_segu['comentarios'] = self.linha[25:]
                self.flag_curv_segu['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_gera_cen['resumo'] = self.linha[00:21]
                self.flag_gera_cen['valor'] = int(self.linha[21:25])
                self.flag_gera_cen['comentarios'] = self.linha[25:]
                self.flag_gera_cen['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.prof_risc_1['resumo'] = self.linha[00:21]
                self.prof_risc_1['valor'] = float(self.linha[21:25])
                self.prof_risc_2['resumo'] = self.linha[00:21]
                self.prof_risc_2['valor'] = float(self.linha[27:31])
                self.prof_risc_1['comentarios'] = self.linha[31:]
                self.prof_risc_2['comentarios'] = self.linha[31:]
                self.prof_risc_1['ordem'] = contador
                self.prof_risc_2['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.func_part_quen['resumo'] = self.linha[00:21]
                self.func_part_quen['valor'] = int(self.linha[21:25])
                self.func_part_quen['comentarios'] = self.linha[25:]
                self.func_part_quen['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_agru_int['resumo'] = self.linha[00:21]
                self.flag_agru_int['valor'] = int(self.linha[21:25])
                self.flag_agru_int['comentarios'] = self.linha[25:]
                self.flag_agru_int['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_pen_int['resumo'] = self.linha[00:21]
                self.flag_pen_int['valor'] = int(self.linha[21:25])
                self.flag_pen_int['comentarios'] = self.linha[25:]
                self.flag_pen_int['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_sub_mot['resumo'] = self.linha[00:21]
                self.flag_sub_mot['valor'] = int(self.linha[21:25])
                self.flag_sub_mot['comentarios'] = self.linha[25:]
                self.flag_sub_mot['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_ord_auto['resumo'] = self.linha[00:21]
                self.flag_ord_auto['valor'] = int(self.linha[21:25])
                self.flag_ord_auto['comentarios'] = self.linha[25:]
                self.flag_ord_auto['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_carg_adic['resumo'] = self.linha[00:21]
                self.flag_carg_adic['valor'] = int(self.linha[21:25])
                self.flag_carg_adic['comentarios'] = self.linha[25:]
                self.flag_carg_adic['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.zsup_linf_perc['resumo'] = self.linha[00:21]
                self.zsup_linf_perc['valor'] = float(self.linha[21:25])
                self.zsup_linf_perc['comentarios'] = self.linha[25:]
                self.zsup_linf_perc['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.delt_zinf['resumo'] = self.linha[00:21]
                self.delt_zinf['valor'] = float(self.linha[21:25])
                self.delt_zinf['comentarios'] = self.linha[25:]
                self.delt_zinf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.num_delt_zinf['resumo'] = self.linha[00:21]
                self.num_delt_zinf['valor'] = int(self.linha[21:25])
                self.num_delt_zinf['comentarios'] = self.linha[25:]
                self.num_delt_zinf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_desp_gnl['resumo'] = self.linha[00:21]
                self.flag_desp_gnl['valor'] = int(self.linha[21:25])
                self.flag_desp_gnl['comentarios'] = self.linha[25:]
                self.flag_desp_gnl['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_modi_gnl['resumo'] = self.linha[00:21]
                self.flag_modi_gnl['valor'] = int(self.linha[21:25])
                self.flag_modi_gnl['comentarios'] = self.linha[25:]
                self.flag_modi_gnl['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_ghid_min['resumo'] = self.linha[00:21]
                self.flag_ghid_min['valor'] = int(self.linha[21:25])
                self.flag_ghid_min['comentarios'] = self.linha[25:]
                self.flag_ghid_min['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.mini_sim_fin['resumo'] = self.linha[00:21]
                self.mini_sim_fin['valor'] = int(self.linha[23:25])
                fim = 25
                self.aini_sim_fin['resumo'] = self.linha[00:21]
                if len(self.linha) >= 30:
                    self.aini_sim_fin['valor'] = int(self.linha[26:30])
                    fim = 30
                self.vini_ree_sim_fin['resumo'] = self.linha[00:21]
                self.vini_ree_sim_fin['valor'] = list()
                for i in range(len(self.linha[30:])//7):
                    ini = 30+(i*7)
                    fim = ini+7
                    self.vini_ree_sim_fin['valor'].append(float(self.linha[ini:fim]))
                self.mini_sim_fin['comentarios'] = self.linha[fim:]
                self.aini_sim_fin['comentariso'] = self.linha[fim:]
                self.vini_ree_sim_fin['comentarios'] = self.linha[fim:]
                self.mini_sim_fin['ordem'] = contador
                self.aini_sim_fin['ordem'] = contador
                self.vini_ree_sim_fin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_ger_ext['resumo'] = self.linha[00:21]
                self.flag_ger_ext['valor'] = int(self.linha[21:25])
                self.flag_comu_2niv['resumo'] = self.linha[00:21]
                self.flag_comu_2niv['valor'] = int(self.linha[26:30])
                self.flag_armz_loc['resumo'] = self.linha[00:21]
                self.flag_armz_loc['valor'] = int(self.linha[31:35])
                self.flag_mem_ena['resumo'] = self.linha[00:21]
                self.flag_mem_ena['valor'] = int(self.linha[36:40])
                self.flag_mem_fcf['resumo'] = self.linha[00:21]
                self.flag_mem_fcf['valor'] = int(self.linha[41:45])
                self.flag_ger_ext["comentarios"] = self.linha[45:]
                self.flag_comu_2niv["comentarios"] = self.linha[45:]
                self.flag_armz_loc["comentarios"] = self.linha[45:]
                self.flag_mem_ena["comentarios"] = self.linha[45:]
                self.flag_mem_fcf["comentarios"] = self.linha[45:]
                self.flag_ger_ext['ordem'] = contador
                self.flag_comu_2niv['ordem'] = contador
                self.flag_armz_loc['ordem'] = contador
                self.flag_mem_ena['ordem'] = contador
                self.flag_mem_fcf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_sar['resumo'] = self.linha[00:21]
                self.flag_sar['valor'] = int(self.linha[21:25])
                self.flag_sar['comentarios'] = self.linha[25:]
                self.flag_sar['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_cvar['resumo'] = self.linha[00:21]
                self.flag_cvar['valor'] = int(self.linha[21:25])
                self.flag_cvar['comentarios'] = self.linha[25:]
                self.flag_cvar['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_min_zsup['resumo'] = self.linha[00:21]
                self.flag_min_zsup['valor'] = int(self.linha[21:25])
                self.flag_min_zsup['comentarios'] = self.linha[25:]
                self.flag_min_zsup['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_req_vmin['resumo'] = self.linha[00:21]
                self.flag_req_vmin['valor'] = int(self.linha[21:25])
                self.flag_req_vmin['comentarios'] = self.linha[25:]
                self.flag_req_vmin['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_elet_ree['resumo'] = self.linha[00:21]
                self.flag_elet_ree['valor'] = int(self.linha[21:25])
                self.flag_elet_ree['comentarios'] = self.linha[25:]
                self.flag_elet_ree['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_sele_cort['resumo'] = self.linha[00:21]
                self.flag_sele_cort['valor'] = int(self.linha[21:25])
                self.flag_sele_cort['comentarios'] = self.linha[25:]
                self.flag_sele_cort['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_jane_cort['resumo'] = self.linha[00:21]
                self.flag_jane_cort['valor'] = int(self.linha[21:25])
                self.flag_jane_cort['comentarios'] = self.linha[25:]
                self.flag_jane_cort['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_cons_ream['resumo'] = self.linha[00:21]
                self.flag_cons_ream['valor'] = int(self.linha[21:25])
                self.flag_ream_cena['resumo'] = self.linha[00:21]
                self.flag_ream_cena['valor'] = int(self.linha[26:30])
                self.flag_pass_ream['resumo'] = self.linha[00:21]
                self.flag_pass_ream['valor'] = int(self.linha[31:35])
                self.flag_cons_ream['comentarios'] = self.linha[35:]
                self.flag_ream_cena['comentarios'] = self.linha[35:]
                self.flag_pass_ream['comentarios'] = self.linha[35:]
                self.flag_cons_ream['ordem'] = contador
                self.flag_ream_cena['ordem'] = contador
                self.flag_pass_ream['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_no_zero['resumo'] = self.linha[00:21]
                self.flag_no_zero['valor'] = int(self.linha[21:25])
                self.flag_no_zero['comentarios'] = self.linha[25:]
                self.flag_no_zero['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_fcf_pdde['resumo'] = self.linha[00:21]
                self.flag_fcf_pdde['valor'] = int(self.linha[21:25])
                self.flag_fcf_pdde['comentarios'] = self.linha[25:]
                self.flag_fcf_pdde['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_imp_ena['resumo'] = self.linha[00:21]
                self.flag_imp_ena['valor'] = int(self.linha[21:25])
                self.flag_imp_ena['comentarios'] = self.linha[25:]
                self.flag_imp_ena['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_imp_cor['resumo'] = self.linha[00:21]
                self.flag_imp_cor['valor'] = int(self.linha[21:25])
                self.flag_imp_cor['comentarios'] = self.linha[25:]
                self.flag_imp_cor['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_proc_agre['resumo'] = self.linha[00:21]
                self.flag_proc_agre['valor'] = int(self.linha[21:25])
                self.flag_proc_agre['comentarios'] = self.linha[25:]
                self.flag_proc_agre['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_corr_espa['resumo'] = self.linha[00:21]
                self.flag_corr_espa['valor'] = int(self.linha[21:25])
                self.flag_corr_espa['comentarios'] = self.linha[25:]
                self.flag_corr_espa['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_conv_estat['resumo'] = self.linha[00:21]
                self.flag_conv_estat['valor'] = int(self.linha[21:25])
                self.flag_conv_estat['comentarios'] = self.linha[25:]
                self.flag_conv_estat['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_mom_ream['resumo'] = self.linha[00:21]
                self.flag_mom_ream['valor'] = int(self.linha[21:25])
                self.flag_mom_ream['comentarios'] = self.linha[25:]
                self.flag_mom_ream['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_arq_ena['resumo'] = self.linha[00:21]
                self.flag_arq_ena['valor'] = int(self.linha[21:25])
                self.flag_arq_ena['comentarios'] = self.linha[25:]
                self.flag_arq_ena['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_test_conv['resumo'] = self.linha[00:21]
                self.flag_test_conv['valor'] = int(self.linha[21:25])
                self.flag_test_conv['comentarios'] = self.linha[25:]
                self.flag_test_conv['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_vmint_sazo['resumo'] = self.linha[00:21]
                self.flag_vmint_sazo['valor'] = int(self.linha[21:25])
                self.flag_vmint_sazo['comentarios'] = self.linha[25:]
                self.flag_vmint_sazo['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_vmaxt_sazo['resumo'] = self.linha[00:21]
                self.flag_vmaxt_sazo['valor'] = int(self.linha[21:25])
                self.flag_vmaxt_sazo['comentarios'] = self.linha[25:]
                self.flag_vmaxt_sazo['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_vminp_sazo['resumo'] = self.linha[00:21]
                self.flag_vminp_sazo['valor'] = int(self.linha[21:25])
                self.flag_vminp_sazo['comentarios'] = self.linha[25:]
                self.flag_vminp_sazo['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_cfuga_sazo['resumo'] = self.linha[00:21]
                self.flag_cfuga_sazo['valor'] = int(self.linha[21:25])
                self.flag_cfuga_sazo['comentarios'] = self.linha[25:]
                self.flag_cfuga_sazo['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_efei_estuf['resumo'] = self.linha[00:21]
                self.flag_efei_estuf['valor'] = int(self.linha[21:25])
                self.flag_efei_estuf['comentarios'] = self.linha[25:]
                self.flag_efei_estuf['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_esto_eolic['resumo'] = self.linha[00:21]
                self.flag_esto_eolic['valor'] = int(self.linha[21:25])
                self.flag_esto_eolic['comentarios'] = self.linha[25:]
                self.flag_esto_eolic['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_esto_solar['resumo'] = self.linha[00:21]
                self.flag_esto_solar['valor'] = int(self.linha[21:25])
                self.flag_esto_solar['comentarios'] = self.linha[25:]
                self.flag_esto_solar['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_esto_sl_eo['resumo'] = self.linha[00:21]
                self.flag_esto_sl_eo['valor'] = int(self.linha[21:25])
                self.flag_esto_sl_eo['comentarios'] = self.linha[25:]
                self.flag_esto_sl_eo['ordem'] = contador
                contador += 1
                self.next_line(f)
                self.flag_rest_gasn['resumo'] = self.linha[00:21]
                self.flag_rest_gasn['valor'] = int(self.linha[21:25])
                self.flag_rest_gasn['comentarios'] = self.linha[25:]
                self.flag_rest_gasn['ordem'] = contador

        except Exception as err:
            if isinstance(err, StopIteration):
                # Armazeno num atributo o conteudo do arquivo, exceto os comentários
                self._numero_registros_ = contador - 1
            else:
                raise

        self._numero_registros_ = contador
        self.dir_base = os.path.split(file_name)[0]
        self.nome_arquivo = os.path.split(file_name)[1]
        print("OK! Leitura do", os.path.split(file_name)[1], "realizada com sucesso.")

    def escrever(self, file_out: str) -> None:
        """
        Escreve o arquivo que contem os dados gerais que configura o caso
        a ser executado no Newave

        :param file_out: caminho completo para o arquivo
        """

        if not os.path.isdir(os.path.split(file_out)[0]):
            os.mkdir(os.path.split(file_out)[0])

        try:
            with open(file_out, 'w', encoding='utf8') as f:  # type: IO[str]

                # Imprime dados
                f.write(self.titu_caso['valor'] + ' - PySDDP - Deck Gerado pela Toolbox PySDDP/UFJF' + "\n")

                a = self.tipo_exec['resumo'][00:21]
                b = self.tipo_exec['valor']
                c = self.tipo_exec['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.dura_peri['resumo'][00:21]
                b = self.dura_peri['valor']
                c = self.dura_peri['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.num_anos['resumo'][00:21]
                b = self.num_anos['valor']
                c = self.num_anos['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.mesi_pre_est['resumo'][00:21]
                b = self.mesi_pre_est['valor']
                c = self.mesi_pre_est['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.mesi_est['resumo'][00:21]
                b = self.mesi_est['valor']
                c = self.mesi_est['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.ano_ini['resumo'][00:21]
                b = self.ano_ini['valor']
                c = self.ano_ini['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.anos_pre['resumo'][00:21]
                b = self.anos_pre['valor']
                c = self.anos_pre['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.anos_pos['resumo'][00:21]
                b = self.anos_pos['valor']
                c = self.anos_pos['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.anos_pos_fin['resumo'][00:21]
                b = self.anos_pos_fin['valor']
                c = self.anos_pos_fin['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.imp_dado['resumo'][00:21]
                b = self.imp_dado['valor']
                c = self.imp_dado['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.imp_merc['resumo'][00:21]
                b = self.imp_merc['valor']
                c = self.imp_merc['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.imp_ener['resumo'][00:21]
                b = self.imp_ener['valor']
                c = self.imp_ener['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.imp_mode_est['resumo'][00:21]
                b = self.imp_mode_est['valor']
                c = self.imp_mode_est['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.imp_ree['resumo'][00:21]
                b = self.imp_ree['valor']
                c = self.imp_ree['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.max_iter['resumo'][00:21]
                b = self.max_iter['valor']
                c = self.max_iter['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.nr_forw['resumo'][00:21]
                b = self.nr_forw['valor']
                c = self.nr_forw['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.nr_aber['resumo'][00:21]
                b = self.nr_aber['valor']
                c = self.nr_aber['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.nr_forw_fin['resumo'][00:21]
                b = self.nr_forw_fin['valor']
                c = self.nr_forw_fin['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.ord_max_parp['resumo'][00:21]
                b = self.ord_max_parp['valor']
                c = self.ord_max_parp['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.anoi_hist['resumo'][00:21]
                b = self.anoi_hist['valor']
                c = self.flag_tam_vaz['valor']
                d = self.flag_tam_vaz['comentarios']
                f.write(a + f"{b:4d}" + "   " + f"{c:1d}" + d)

                a = self.flag_earm_inic['resumo'][00:21]
                b = self.flag_earm_inic['valor']
                c = self.flag_earm_inic['comentarios']
                f.write(a + f"{b:4d}" + c)

                f.write('VOLUME INICIAL  -%   XXX.X  XXX.X  XXX.X  XXX.X  XXX.X \n')

                a = self.vol_earm_inic['resumo'][00:19]
                b = ""
                c = self.vol_earm_inic['comentarios']
                for i in range(len(self.vol_earm_inic["valor"])):
                    b = b + "  " + f"{self.vol_earm_inic['valor'][i]:5.1f}"
                f.write(a + b + c)

                a = self.int_conf['resumo'][00:21]
                b = self.int_conf['valor']
                c = self.int_conf['comentarios']
                f.write(a + f"{b:5.1f}" + c)

                a = self.tx_desc['resumo'][00:21]
                b = self.tx_desc['valor']
                c = self.tx_desc['comentarios']
                f.write(a + f"{b:5.1f}" + c)

                a = self.flag_sim_fin['resumo'][00:21]
                b = self.flag_sim_fin['valor']
                c = self.flag_sim_fin['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_impr_sim_fin['resumo'][00:21]
                b = self.flag_impr_sim_fin['valor']
                c = self.flag_impr_sim_fin['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_impr_risc_def['resumo'] = self.linha[00:21]
                b = self.flag_impr_risc_def['valor']
                c = self.flag_impr_risc_def['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.ser_grav_rel['resumo'][00:21]
                b = self.ser_grav_rel['valor']
                c = self.ser_grav_rel['comentarios']
                f.write(a + f"{b:4d}" + c)

                if self.iter_inic_zinf['valor'] is None:
                    a = self.num_min_iter['resumo'][00:21]
                    b = self.num_min_iter['valor']
                    c = self.num_min_iter['comentarios']
                    f.write(a + f"{b:4d}" + c)
                else:
                    a = self.num_min_iter['resumo'][00:21]
                    b = self.num_min_iter['valor']
                    c = self.iter_inic_zinf['valor']
                    d = self.iter_inic_zinf['comentarios']
                    f.write(a + f"{b:4d}" + "  " + f"{c:1d}" + d)

                a = self.rac_prev['resumo'][00:21]
                b = self.rac_prev['valor']
                c = self.rac_prev['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.nr_anos_mnut['resumo'][00:21]
                b = self.nr_anos_mnut['valor']
                c = self.nr_anos_mnut['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.tend_hidr_pol['resumo'][00:21]
                b = self.tend_hidr_pol['valor']
                c = self.tend_hidr_sim['valor']
                d = self.tend_hidr_pol['comentarios']
                f.write(a + f"{b:4d}" + " " + f"{c:4d}" + d)

                a = self.flag_itpu['resumo'][00:21]
                b = self.flag_itpu['valor']
                c = self.flag_itpu['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_bid_dem['resumo'][00:21]
                b = self.flag_bid_dem['valor']
                c = self.flag_bid_dem['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_tran_loss['resumo'][00:21]
                b = self.flag_tran_loss['valor']
                c = self.flag_tran_loss['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_el_nino['resumo'][00:21]
                b = self.flag_el_nino['valor']
                c = self.flag_el_nino['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_enso['resumo'][00:21]
                b = self.flag_enso['valor']
                c = self.flag_enso['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_pat['resumo'][00:21]
                b = self.flag_pat['valor']
                c = self.flag_pat['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_dsv_agua['resumo'][00:21]
                b = self.flag_dsv_agua['valor']
                c = self.flag_dsv_agua['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_dsv_ena['resumo'][00:21]
                b = self.flag_dsv_ena['valor']
                c = self.flag_dsv_ena['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_curv_segu['resumo'][00:21]
                b = self.flag_curv_segu['valor']
                c = self.flag_curv_segu['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_gera_cen['resumo'][00:21]
                b = self.flag_gera_cen['valor']
                c = self.flag_gera_cen['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.prof_risc_1['resumo'][00:21]
                b = self.prof_risc_1['valor']
                c = self.prof_risc_2['valor']
                d = self.prof_risc_1['comentarios']
                f.write(a + f"{b:5.1f}" + f"{c:5.1f}" + d)

                a = self.func_part_quen['resumo'][00:21]
                b = self.func_part_quen['valor']
                c = self.func_part_quen['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_agru_int['resumo'][00:21]
                b = self.flag_agru_int['valor']
                c = self.flag_agru_int['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_pen_int['resumo'][00:21]
                b = self.flag_pen_int['valor']
                c = self.flag_pen_int['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_sub_mot['resumo'][00:21]
                b = self.flag_sub_mot['valor']
                c = self.flag_sub_mot['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_ord_auto['resumo'][00:21]
                b = self.flag_ord_auto['valor']
                c = self.flag_ord_auto['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_carg_adic['resumo'][00:21]
                b = self.flag_carg_adic['valor']
                c = self.flag_carg_adic['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.zsup_linf_perc['resumo'][00:21]
                b = self.zsup_linf_perc['valor']
                c = self.zsup_linf_perc['comentarios']
                f.write(a + f"{b:4.1f}" + c)

                a = self.delt_zinf['resumo'][00:21]
                b = self.delt_zinf['valor']
                c = self.delt_zinf['comentarios']
                f.write(a + f"{b:4.1f}" + c)

                a = self.num_delt_zinf['resumo'][00:21]
                b = self.num_delt_zinf['valor']
                c = self.num_delt_zinf['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_desp_gnl['resumo'][00:21]
                b = self.flag_desp_gnl['valor']
                c = self.flag_desp_gnl['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_modi_gnl['resumo'][00:21]
                b = self.flag_modi_gnl['valor']
                c = self.flag_modi_gnl['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_ghid_min['resumo'][00:21]
                b = self.flag_ghid_min['valor']
                c = self.flag_ghid_min['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.mini_sim_fin['resumo'][00:21]
                b = self.mini_sim_fin['valor']
                c = self.mini_sim_fin['comentarios']
                if self.aini_sim_fin['valor'] is None:
                    f.write(a + f"{b:4d}" + c)
                else:
                    ano = self.aini_sim_fin["valor"]
                    b = f"{b:4d}" + " " + f"{ano:4d}"
                    for i in range(len(self.vini_ree_sim_fin['valor'])):
                        valor = self.vini_ree_sim_fin['valor'][i]
                        b = b + "  " + f"{valor:5.1f}"
                    f.write(a + b + c)

                a = self.flag_ger_ext['resumo'][00:21]
                b = self.flag_ger_ext['valor']
                c = self.flag_comu_2niv['valor']
                d = self.flag_armz_loc['valor']
                e = self.flag_mem_ena['valor']
                g = self.flag_mem_fcf['valor']
                h = self.flag_ger_ext['comentarios']
                f.write(a + f"{b:4d}" + " " + f"{c:4d}" + " " + f"{d:4d}" + " " + f"{e:4d}" + " " + f"{g:4d}" + h )

                a = self.flag_sar['resumo'][00:21]
                b = self.flag_sar['valor']
                c = self.flag_sar['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_cvar['resumo'][00:21]
                b = self.flag_cvar['valor']
                c = self.flag_cvar['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_min_zsup['resumo'][00:21]
                b = self.flag_min_zsup['valor']
                c = self.flag_min_zsup['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_req_vmin['resumo'][00:21]
                b = self.flag_req_vmin['valor']
                c = self.flag_req_vmin['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_elet_ree['resumo'][00:21]
                b = self.flag_elet_ree['valor']
                c = self.flag_elet_ree['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_sele_cort['resumo'][00:21]
                b = self.flag_sele_cort['valor']
                c = self.flag_sele_cort['comentarios']
                f.write(a + f"{b:4d}" + c)

                a = self.flag_jane_cort['resumo'][00:21]
                b = self.flag_jane_cort['valor']
                c = self.flag_jane_cort['comentarios']
                f.write(a + f"{b:4d}" + c)

                if self.flag_cons_ream['valor'] is not None:
                    a = self.flag_cons_ream['resumo'][00:21]
                    b = self.flag_cons_ream['valor']
                    c = self.flag_ream_cena['valor']
                    d = self.flag_pass_ream['valor']
                    e = self.flag_cons_ream['comentarios']
                    f.write(a + f"{b:4d}" + " " + f"{c:4d}" + " " + f"{d:4d}" + e)


                if self.flag_no_zero['valor'] is not None:
                    a = self.flag_no_zero['resumo'][00:21]
                    b = self.flag_no_zero['valor']
                    c = self.flag_no_zero['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_fcf_pdde['valor'] is not None:
                    a = self.flag_fcf_pdde['resumo'][00:21]
                    b = self.flag_fcf_pdde['valor']
                    c = self.flag_fcf_pdde['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_imp_ena['valor'] is not None:
                    a = self.flag_imp_ena['resumo'][00:21]
                    b = self.flag_imp_ena['valor']
                    c = self.flag_imp_ena['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_imp_cor['valor'] is not None:
                    a = self.flag_imp_cor['resumo'][00:21]
                    b = self.flag_imp_cor['valor']
                    c = self.flag_imp_cor['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_proc_agre['valor'] is not None:
                    a = self.flag_proc_agre['resumo'][00:21]
                    b = self.flag_proc_agre['valor']
                    c = self.flag_proc_agre['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_corr_espa['valor'] is not None:
                    a = self.flag_corr_espa['resumo'][00:21]
                    b = self.flag_corr_espa['valor']
                    c = self.flag_corr_espa['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_conv_estat['valor'] is not None:
                    a = self.flag_conv_estat['resumo'][00:21]
                    b = self.flag_conv_estat['valor']
                    c = self.flag_conv_estat['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_mom_ream['valor'] is not None:
                    a = self.flag_mom_ream['resumo'][00:21]
                    b = self.flag_mom_ream['valor']
                    c = self.flag_mom_ream['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_arq_ena['valor'] is not None:
                    a = self.flag_arq_ena['resumo'][00:21]
                    b = self.flag_arq_ena['valor']
                    c = self.flag_arq_ena['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_test_conv['valor'] is not None:
                    a = self.flag_test_conv['resumo'][00:21]
                    b = self.flag_test_conv['valor']
                    c = self.flag_test_conv['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_vmint_sazo['valor'] is not None:
                    a = self.flag_vmint_sazo['resumo'][00:21]
                    b = self.flag_vmint_sazo['valor']
                    c = self.flag_vmint_sazo['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_vmaxt_sazo['valor'] is not None:
                    a = self.flag_vmaxt_sazo['resumo'][00:21]
                    b = self.flag_vmaxt_sazo['valor']
                    c = self.flag_vmaxt_sazo['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_vminp_sazo['valor'] is not None:
                    a = self.flag_vminp_sazo['resumo'][00:21]
                    b = self.flag_vminp_sazo['valor']
                    c = self.flag_vminp_sazo['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_cfuga_sazo['valor'] is not None:
                    a = self.flag_cfuga_sazo['resumo'][00:21]
                    b = self.flag_cfuga_sazo['valor']
                    c = self.flag_cfuga_sazo['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_efei_estuf['valor'] is not None:
                    a = self.flag_efei_estuf['resumo'][00:21]
                    b = self.flag_efei_estuf['valor']
                    c = self.flag_efei_estuf['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_esto_eolic['valor'] is not None:
                    a = self.flag_esto_eolic['resumo'][00:21]
                    b = self.flag_esto_eolic['valor']
                    c = self.flag_esto_eolic['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_esto_solar['valor'] is not None:
                    a = self.flag_esto_solar['resumo'][00:21]
                    b = self.flag_esto_solar['valor']
                    c = self.flag_esto_solar['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_esto_sl_eo['valor'] is not None:
                    a = self.flag_esto_sl_eo['resumo'][00:21]
                    b = self.flag_esto_sl_eo['valor']
                    c = self.flag_esto_sl_eo['comentarios']
                    f.write(a + f"{b:4d}" + c)

                if self.flag_rest_gasn['valor'] is not None:
                    a = self.flag_rest_gasn['resumo'][00:21]
                    b = self.flag_rest_gasn['valor']
                    c = self.flag_rest_gasn['comentarios']
                    f.write(a + f"{b:4d}" + c)

        except Exception:
            raise

        print("OK! Escrita do", os.path.split(file_out)[1], "realizada com sucesso.")
