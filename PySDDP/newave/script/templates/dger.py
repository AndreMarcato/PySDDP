from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class DgerTemplate(ArquivoEntrada):
    """
    Classe que contem os dados gerais para a execução do modelo newave.
    Esta classe tem como intuito fornecer duck typing para a classe Dger e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None

        self._numero_registros_ = None
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None

        # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)

        self.titu_caso = {
                    'descricao': 'Nome do caso',
                    'resumo': None,
                    'ordem': None,
                    'valor': None
                 }
        self.tipo_exec = {
                    'descricao': 'Tipo de execução: 1 = rodada completa ou 0 = só executa simulação final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.dura_peri = {
                    'descricao': 'Duração de cada estágio de operação, em meses (função desabilitada)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.num_anos = {
                    'descricao': 'Número de anos de planejamento',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.mesi_pre_est = {
                    'descricao': 'Mês inicial do período que antecede o período de planejamento.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.mesi_est = {
                    'descricao': 'Mês inicial do período de planejamento. Se o período que antecede o período de' +
                                 'planejamento for diferente de zero, o Newave irá considerar esse valor unitário.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.ano_ini = {
                    'descricao': 'Ano inicial do período de planejamento.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.anos_pre = {
                    'descricao': 'Número de anos iniciais para fins de estabilização no cálculo da política',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.anos_pos = {
                    'descricao': 'Número de anos finais para fins de estabilização no cálculo da política',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.anos_pos_fin = {
                    'descricao': 'Número de anos finais para fins de estabilização na simulação final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.imp_dado = {
                    'descricao': 'Controle de impressão das características das usinas: 0 = não imprime 1 = imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.imp_merc = {
                    'descricao': 'Controle de impressão dos dados de mercado de energia: 0 = não imprime 1 = imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.imp_ener = {
                    'descricao': 'Controle de impressão as energias históricas afluentes: 0 = não imprime 1 = imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.imp_mode_est = {
                    'descricao': 'Controle de impressão dos parâmetros do modelo estocástico: 0 = não imprime 1 = ' +
                                 'imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.imp_ree = {
                    'descricao': 'Controle de impressão dos parâmetros dos reservatórios equivalentes de energia: ' +
                                 '0 = não imprime 1 = imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.max_iter = {
                    'descricao': 'Número máximo de iterações',
                    'resumo': None,
                    'comentarios': None,
                    'valor': None
                 }
        self.nr_forw = {
                    'descricao': 'Número de simulações forward',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.nr_aber = {
                    'descricao': 'Número de aberturas para a simulação backward',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.nr_forw_fin = {
                    'descricao': 'Número de séries sintéticas - Simulação Final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.ord_max_parp = {
                    'descricao': 'Ordem máxima do modelo estocástico PAR(p)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.anoi_hist = {
                    'descricao': 'Ano inicial do arquivo de vazões históricas',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_tam_vaz = {
                    'descricao': 'Tamanho do registro do arquivo de vazões históricas: 0 = 320 palavras 1 = 600 ' +
                                 'palavras',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }

        self.flag_earm_inic = {
                    'descricao': 'Cálculo de energia armazenada inicial: 0 = utiliza o valor do volume inicial' +
                                 'informado o percentual do REE informado no arquivo de Dados Gerais' +
                                 '1 = utiliza o valor do volume inicial' +
                                 'informado por usina no arquivo de configuração hidroelétrica',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.vol_earm_inic = {
                    'descricao': 'Volume armazenado inicial (%) por REE.' +
                                 'Somente será considerado  se o volume inicial for considerado por REE',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.int_conf = {
                    'descricao': 'Probabilidade associada ao intervalo de confiança para convergência do algoritmo (%)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.tx_desc = {
                    'descricao': 'Taxa de desconto anual (%), sendo: tx_periodo = (tx_anual+1)**(per/12) - 1, onde' +
                                 'período anual per é a duração em meses do período',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_sim_fin = {
                    'descricao': 'Simulação final após convergência PDDE 0 = não simula: 1 = simulação com ' +
                                 'séries sintéticas 2 = simulação com a série histórica 3 = consistência de dados',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_impr_sim_fin = {
                    'descricao': 'Controle de impressão dos resultados da simulação final e do cálculo da política: ' +
                                 '0 = não imprime; 1 = impressão para simulação final' +
                                 '2 = impressão para simulação final e cálculo da política',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_impr_risc_def = {
                    'descricao': 'Controle de impressão dos riscos de déficit e valor esperado da ENS' +
                                 '0 = convergência final apenas 1 = todas as iterações',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.ser_grav_rel = {
                    'descricao': 'Este campo indica de quantas em quantas séries será gravado o relatório ' +
                                 'detalhado da simulação final.' +
                                 'Por exemplo, se este registro contém o valor 50 significa que do total de séries' +
                                 'sintéticas simuladas haverá impressão detalhada para n séries, a saber, série 1, ' +
                                 'série 51, ..., série 951 etc. Este campo só será considerado se' +
                                 'a flag de impressão da simulação final estiver ativa.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.num_min_iter = {
                    'descricao': 'Este campo contém o número mínimo de iterações para a convergência da política.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.iter_inic_zinf = {
                    'descricao': 'Este campo indica a iteração partir da qual será investigada a incerteza do' +
                                 'parametro: valor esperado do custo total de operação obtido da função de custo' +
                                 'futuro do primeiro estágio - ZINF',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }

        self.rac_prev = {
                    'descricao': 'Racionamento Preventivo. Este campo indica a adoção ou não de corte de carga por' +
                                 'otimização (CCO) na simulação final: 0 = não adota CCO; 1 = adota CCO na' +
                                 'simulação final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.nr_anos_mnut = {
                    'descricao': 'Números de anos de informações de manutenção programada de usinas térmicas a ' +
                                 'serem considerados no arquivo de dados de manutenção térmica',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.tend_hidr_pol = {
                    'descricao': 'Consideração da tendência hidrológica no cálculo da política: ' +
                                 '0 = não será lido arquivo com a tendência hidrológica' +
                                 '1 = será lido arquivo com a tendência hidrológica por REE' +
                                 '2 = será lido arquivo com a tendência hidrológica por posto de medição',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.tend_hidr_sim = {
                    'descricao': 'Consideração da tendência hidrológica na Simulação Final:' +
                                 '0 = não será lido arquivo com a tendência hidrológica' +
                                 '1 = será lido arquivo com a tendência hidrológica por REE' +
                                 '2 = será lido arquivo com a tendência hidrológica por posto de medição',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_itpu = {
                    'descricao': 'Flag para consideração das restrições de Itaipu (flag desabilitado). ' +
                                 '0 = não será considerado 1 = será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_bid_dem = {
                    'descricao': 'Flag para consideração do bid de demanda (função não implementada). ' +
                                 '0 = não será considerado 1 = será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_tran_loss = {
                    'descricao': 'Flag para consideração das perdas de transmissão. 0 = não será considerado, ' +
                                 '1 = será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_el_nino = {
                    'descricao': 'Flag para consideração do El Niño (função não implementada). ' +
                                 '0 = não será considerado 1 = será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_enso = {
                    'descricao': 'Índice de identificação ENSO (função não implementada).',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_pat = {
                    'descricao': 'Flag para tipo de duração do patamar. 0 = sazonal. 1 = variável por ano.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }

        self.flag_dsv_agua = {
                    'descricao': 'Flag para consideração de desvio de água. 0 = não será considerado' +
                                 '1 = será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_dsv_ena = {
                    'descricao': 'Flag para consideração da energia de desvio de água como função da energia ' +
                                 'armazenada: 0 = constante; 1 = variável com o armazenamento',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_curv_segu = {
                    'descricao': 'Flag para controle da curva de segurança: 0 = não considera - será usado o cálculo' +
                                 'feito para as entradas de VMINT; 1 = curva de aversão a risco / VMINP',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_gera_cen = {
                    'descricao': 'Flag para controle da geração de cenário de afluências para as simulações backward' +
                                 'e forward: 0 = utiliza resíduos iguais com compensação na correlação cruzada da' +
                                 ' população nas simulações backward e forward; ' +
                                 '1 = utiliza compensação na correlação cruzada da população na simulação backward; ' +
                                 '2 = utiliza compensação na correlação cruzada da população nas simulações backward ' +
                                 'e forward.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.prof_risc_1 = {
                    'descricao': 'Profundidade para cálculo do risco de déficit (%) – primeiro valor',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.prof_risc_2 = {
                    'descricao': 'Profundidade para cálculo do risco de déficit (%) – segundo valor',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.func_part_quen = {
                    'descricao': 'Funcionalidade pseudo-partida quente: número de iterações a ser considerada para a ' +
                                 'simulação final. Se for zero, serão consideradas todas as iterações realizadas.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_agru_int = {
                    'descricao': 'Flag para consideração de agrupamento livre de intercâmbios. ' +
                                 '0 – não será considerado 1 – será considerado',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_pen_int = {
                    'descricao': 'Flag para consideração de equalização de penalidades de intercâmbio ' +
                                 '(flag desabilitado) Os intercâmbios entre subsistemas / submercados reais são ' +
                                 'penalizados por P, os intercâmbios entre subsistemas / submercados reais e ' +
                                 'fictícios são penalizados por P/2 e os intercâmbios entre subsistemas / submercados' +
                                 ' ficícios não penalizados.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_sub_mot = {
                    'descricao': 'Flag para a consideração da representação da submotorização. ' +
                                 '0 – como função da potência instalada. ' +
                                 '1 – como função da potência instalada e das energias afluentes médias históricas. ' +
                                 '2 – como função da potência instalada, da energia afluente histórica da usina ' +
                                 'submotorizada e da regularização à montante da usina',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_ord_auto = {
                    'descricao': 'Flag para a consideração da ordenação automática de subsistemas/submercados ' +
                                 'e classes térmicas: 0 – não considera. 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_carg_adic = {
                    'descricao': 'Flag para consideração do arquivo de cargas adicionais: 0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.zsup_linf_perc = {
                    'descricao': 'Valor percentual de ZSUP a ser subtraído de LINF para o critério de parada' +
                                 'estatístico(%)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.delt_zinf = {
                    'descricao': 'Valor máximo percentual para delta de ZINF no critério de parada não estatístico (%)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.num_delt_zinf = {
                    'descricao': 'Número de deltas de ZINF consecutivos a serem considerados no critério não ' +
                                 'statístico',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_desp_gnl = {
                    'descricao': 'Flag para consideração de despacho antecipado de usinas térmicas a gás natural ' +
                                 'liquefeito (GNL): 0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_modi_gnl = {
                    'descricao': 'Flag para modificação automática do montante de antecipação de despacho de uma ' +
                                 'usina GNL quando a capacidade de geração máxima desta usina for inferior a este ' +
                                 'valor: 0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_ghid_min = {
                    'descricao': 'Flag para consideração de restrições de geração hidráulica mínima: ' +
                                 '0 - não considera 1 - considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.mini_sim_fin = {
                    'descricao': 'Mês de início para o cálculo da simulação final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.aini_sim_fin = {
                    'descricao': 'Ano de início para o cálculo da simulação final',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.vini_ree_sim_fin = {
                    'descricao': 'Volume armazenado inicial (%) por REE para cálculo da simulação final.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_ger_ext = {
                    'descricao': 'Flag para utilização do gerenciador externo de processos: ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_comu_2niv = {
                    'descricao': 'Flag para utilização da comunicação em dois níveis: 0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_armz_loc = {
                    'descricao': 'Flag para utilização de armazenamento local de arquivos temporários: ' +
                                 '0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_mem_ena = {
                    'descricao': 'Flag para utilização de alocação em memória da energia natural afluente: ' +
                                 '0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_mem_fcf = {
                    'descricao': 'Flag para utilização de alocação em memória dos cortes da função de custo futuro: ' +
                                 '0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_sar = {
                    'descricao': 'Flag para utilização de mecanismo de aversão a risco: SAR: ' +
                                 '0 – não considera; ' +
                                 '1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_cvar = {
                    'descricao': 'Flag para utilização de mecanismo de aversão a risco: CVaR ' +
                                 '0 – não considera; ' +
                                 '1 – considera, constante no tempo 2 – considera, variável no tempo',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_min_zsup = {
                    'descricao': 'Flag para consideração do critério de mínimo ZSUP para convergência ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_req_vmin = {
                    'descricao': 'Flag para não consideração do requisito de vazão mínima' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_elet_ree = {
                    'descricao': 'Flag para consideração de restrições elétricas internas aos REEs ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_sele_cort = {
                    'descricao': 'Flag para consideração do procedimento de Seleção de Cortes de Benders ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_jane_cort = {
                    'descricao': 'Flag para consideração de Janela de Cortes de Benders: 0 – não considera ' +
                                 '1 – considera janela fixa de 2*NREE',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_cons_ream = {
                    'descricao': 'Flag para consideração Reamostragem de Cenários ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_ream_cena = {
                    'descricao': 'Tipo de Reamostragem de Cenários: 0 – Recombinação 1 – Plena',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_pass_ream = {
                    'descricao': 'Passo para Reamostragem de Cenários. Permitido valores entre 1 e número máximo ' +
                                 'de iterações',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_no_zero = {
                    'descricao': 'Flag para consideração do Nó Zero no cálculo de ZINF: ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_fcf_pdde = {
                    'descricao': 'Consulta à função de custo futuro ao longo das iterações da PDDE: ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_imp_ena = {
                    'descricao': 'Flag para impressão dos cenários de ENA: 0 – não imprime; 1 – imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_imp_cor = {
                    'descricao': 'Flag para impressão dos cortes ativos: 0 – não imprime; 1 – imprime',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_proc_agre = {
                    'descricao': 'Flag para escolha do representante do processo agregação: 0 – mais próximo; ' +
                                 '1 – centróide',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_corr_espa = {
                    'descricao': 'Flag para escolha da matriz de correlação espacial: 0 – anual; 1 – mensal',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_conv_estat = {
                    'descricao': 'Desconsidera critério estatístico no processo de convergência: 0 – não 1 – sim',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_mom_ream = {
                    'descricao': 'Momento de realização da reamostragem' +
                                 '0 – Backward da iteração correspondente ao passo para a reamostragem de ' +
                                 'cenários +1; ' +
                                 '1 – Forward da iteração correspondente ao passo para a reamostragem de cenários',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_arq_ena = {
                    'descricao': 'Flag para manutenção dos arquivos de ENA gerados para reamostragem após a ' +
                                 'execução do programa: 0 – apaga; 1 – mantém',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_test_conv = {
                    'descricao': 'Flag para teste da convergência somente após iteração mínima (inclusive). ' +
                                 '0 – teste começa na primeira iteração ' +
                                 '1 – teste começa na iteração mínima (inclusive)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_vmint_sazo = {
                    'descricao': 'Flag para a consideração sazonal de volume mínimo, com data (VMINT) nos períodos ' +
                                 'estáticos (pré e pós): 0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_vmaxt_sazo = {
                    'descricao': 'Flag para a consideração sazonal de volume máximo, com data (VMAXT) nos períodos ' +
                                 'estáticos (pré e pós): 0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_vminp_sazo = {
                    'descricao': 'Flag para a consideração sazonal de volume mínimo com adoção de penalidade, ' +
                                 'com data (VMINP) nos períodos estáticos (pré e pós): ' +
                                 '0 – não considera 1 – considera.',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_cfuga_sazo = {
                    'descricao': 'Flag para a consideração sazonal de canal de fuga (CFUGA) e altura de montante ' +
                                 '(CMONT) nos períodos estáticos (pré e pós) ' +
                                 '0 – não considera 1 – considera',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_efei_estuf = {
                    'descricao': 'Flag para a consideração de restrições de emissão de gases de efeito estufa ' +
                                 '0 – não representa 1 – representa',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_esto_eolic = {
                    'descricao': 'Flag para a representação da incerteza na geração eólica ' +
                                 '0 – não representa; 1 – representa ' +
                                 '(funcionalidade não operacional nesta versão)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_esto_solar = {
                    'descricao': 'Flag para a representação da incerteza na geração solar: ' +
                                 '0 – não representa; 1 – representa ' +
                                 '(funcionalidade não operacional nesta versão)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_esto_sl_eo = {
                    'descricao': 'Flag para o tipo de representação da incerteza na geração eólica/solar: ' +
                                 '1 – ajuste a partir de registro histórico 1 – parâmetros da distribuição ' +
                                 '1 – cenários (funcionalidade não operacional nesta versão)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }
        self.flag_rest_gasn = {
                    'descricao': 'Flag para a consideração de restrições de fornecimento de combustível (GN) ' +
                                 '0 – não representa; 1 – representa ' +
                                 '(funcionalidade não operacional nesta versão)',
                    'resumo': None,
                    'comentarios': None,
                    'ordem': None,
                    'valor': None
                 }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """
        Metodo abstrato da ArquivoEntrada sendo repassado para as classes filhas
        :param args: conjunto de parametros obrigatorios
        :param kwargs: conjunto de parametros opcionais
        :return:
        """

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """
        Metodo abstrato da ArquivoEntrada sendo repassado para as classes filhas
        :param args: conjunto de parametros obrigatorios
        :param kwargs: conjunto de parametros opcionais
        :return:
        """
