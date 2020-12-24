from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class DadgerTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao do arquivo Entdados do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.comentarios = None
        self.tm = None
        self.sist = None
        self.ree = None
        self.uh = None
        self.tviag = None
        self.ut = None
        self.usie = None
        self.dp = None
        self.de = None
        self.cd = None
        self.ri = None
        self.ia = None
        self.rd = None
        self.rivar = None
        self.it = None
        self.gp = None
        self.ni = None
        self.ve = None
        self.ci_ce = None
        self.re = None
        self.lu = None
        self.fh = None
        self.ft = None
        self.fi = None
        self.fe = None
        self.fr = None
        self.fc = None
        self.ac = None
        self.da = None
        self.fp = None
        self.ez = None
        self.ag = None
        self.mh = None
        self.mt = None
        self.tx = None
        self.pq = None
        self.secr = None
        self.cr = None
        self.r11 = None
        self.vr = None
        self.pd = None
        self.vm = None
        self.df = None
        self.me = None
        self.meta_cjsist = None
        self.meta_sist = None
        self.meta_usit = None
        self.sh = None
        self.tf = None
        self.rs = None
        self.sp = None
        self.ps = None
        self.pp = None


        self.bloco_tm = {
            'descricao': 'Discretização do Estudo',
            'df': None,
            'formato':
                "{mne:>2}  {dd:>2}   {hr:>2} {mh:>3}    {durac:>4}     {rede:1}   {patamar:>5}\n",
        }

        self.bloco_sist = {
            'descricao': 'Definição dos Subsistemas',
            'df': None,
            'formato':
                "{mne:>6} {num:>2} {mne_iden:>2} {flag:1} {nome:>7}\n",
        }
        self.bloco_ree = {
            'descricao': 'Definição dos Reservatórios Equivalentes',
            'df': None,
            'formato':
                "{mne:>3}   {num_ree:>2} {num_sub:>2} {nome:>6}\n",
        }

        self.bloco_uh = {
            'descricao': 'Usinas Hidraulicas',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3}  {nome:>11}   {ss:>2}   {vinic:>9}{evap:1} {di:2} {hi:2} {m:1} {vmor:>9} {prod:1} "
                "{rest:1}\n",
        }
        self.bloco_tviag = {
            'descricao': 'Tempo de Viagem',
            'df': None,
            'formato':
                "{mne:>6}{mont:>3} {jus:>3} {tp:1}    {hr:>3}  {tpTviag:1}\n",
        }

        self.bloco_ut = {
            'descricao': 'Térmicas',
            'df': None,
            'formato':
                "{mne:>2}  {num:>3}  {nome:>11} {ss:>2} {flag:1} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {rest:1} "
                "  {gmin:>9}{gmax:>9} {g_anterior:>9}\n",
        }
        self.bloco_usie = {
            'descricao': 'Usinas Elevatórias',
            'df': None,
            'formato':
                "{mne:>4} {num:>3} {ss:>2}   {nome:>9}   {mont:>3}  {jus:>3}  {qmin:>9}{qmax:>9}{taxa_consumo:>9}\n",
        }

        self.bloco_dp = {
            'descricao': 'Carga',
            'df': None,
            'formato':
                "{mne:>2}  {ss:>2}  {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {demanda:>9}\n",
        }
        self.bloco_de = {
            'descricao': 'Demanda/Cargas Especiais',
            'df': None,
            'formato':
                "{mne:>2}  {nde:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {demanda:>9} {justific:>9}\n",
        }
        self.bloco_cd = {
            'descricao': 'Custo de Deficit',
            'df': None,
            'formato':
                "{mne:>2} {is:>2} {cd:>2} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {custo:>9}{limsup:>9}\n",
        }
        self.bloco_ri = {
            'descricao': 'Restrição de Itaipu 50HZ e 60HZ e Parcela da ANDE',
            'df': None,
            'formato':
                "{mne:>2}      {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1}   {gh50min:>9}{gh50max:>9}{gh60min:>9}"
                "{gh60max:>9}{ande:>9}\n",
        }
        self.bloco_ia = {
            'descricao': 'Intercâmbios de Energia entre Subsistemas',
            'df': None,
            'formato':
                "{mne:>2}  {ss1:>2}   {ss2:>2}  {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {ss1_ss2:>9}"
                "{ss2_ss1:>9}\n",
        }
        self.bloco_rd = {
            'descricao': 'Opções de representação da rede elétrica',
            'df': None,
            'formato':
                "{mne:>2}  {flag_fol:1}   {ncirc:>4}  {dbar:1} {lim:1} {dlin:1} {perd:1} {formato:1}\n",
        }
        self.bloco_rivar = {
            'descricao': 'Restrições internas soft de variação para variáveis do problema',
            'df': None,
            'formato':
                "{mne:>5}  {num:>3}{ss:>2} {cod:>2} {penalidade:>9}\n",
        }
        self.bloco_it = {
            'descricao': 'Coeficientes da Régua 11 de Itaipu',
            'df': None,
            'formato':
                "{mne:>2}  {num:>2}   {coef:>74}\n",
        }
        self.bloco_gp = {
            'descricao': 'Gap para Convergência',
            'df': None,
            'formato':
                "{mne:>2}  {tol_conv:>9} {tol_prob:>9}\n",
        }
        self.bloco_ni = {
            'descricao': 'Número máximo de Iterações',
            'df': None,
            'formato':
                "{mne:>2} {flag:>2}    {nmax:>2}\n",
        }
        self.bloco_ve = {
            'descricao': 'Volume de Espera',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {vol:>9}\n",
        }
        self.bloco_ci_ce = {
            'descricao': 'Dados de Importação/Exportação com Outros Subsistemas',
            'df': None,
            'formato':
                "{mne:>2} {num:>3} {nome:>9} {ss_busf:>5}{flag:1} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} "
                "{unid:1} {linf:>9}{lsup:>9}{custo:>9} {energia:>9}\n",
        }
        self.bloco_re = {
            'descricao': 'Restrições Elétricas Especiais',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3}  {di:>2} {hi:>2} {mi:1} {df:2} {hf:>2} {mf:1}\n",
        }
        self.bloco_lu = {
            'descricao': 'Limites da Restrição',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {linf:>9}{lsup:>9}\n",
        }
        self.bloco_fh = {
            'descricao': 'Fatores de Participação das Usinas Hidroelétricas na Restrição',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {ush:>3} {unh:>2}    {fator:>9}\n",
        }
        self.bloco_ft = {
            'descricao': 'Fator de Participação das Usina termoelétricas na Restrição',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {ust:>3}       {fator:>9}\n",
        }
        self.bloco_fi = {
            'descricao': 'Fator de Participação dos Intercâmbios na Restrição',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {ss1:>2}   {ss2:>2}   {fator:>9}\n",
        }
        self.bloco_fe = {
            'descricao': 'Fator de Participação dos Contratos de importação de energia',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {num_contrato:>3}       {fator:>9}\n",
        }
        self.bloco_fr = {
            'descricao': 'Fator de Participação das Fontes Renováveis Eólicas',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {useol:>5}     {fator:>8}\n",
        }
        self.bloco_fc = {
            'descricao': 'Fator de Participação Demandas/Cargas especiais',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3}   {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {demanda:>3}         {fator:>8}\n",
        }
        self.bloco_ac = {
            'descricao': 'Modificações no Cadastro de Usinas Hidroelétricas',
            'df': None,
            'formato':
                "{mne:>2}  {usi:>3}  {mneumonico:>5}{ind:1}{valor:>9}\n",
        }
        self.bloco_da = {
            'descricao': 'Retiradas de Água para Usos Alternativos',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {taxa:>9} {obs:>9}\n",
        }
        self.bloco_fp = {
            'descricao': 'Dados para a Modelagem da Função de Produção das Usinas Hidroelétricas',
            'df': None,
            'formato':
                "{mne:>2} {usi:>3} {f:1}  {nptQ:>3}  {nptV:>3} {concavidade:1} {min_quadraticos:1}     {deltaV:>9} "
                "{tr:>9}\n",
        }
        self.bloco_ez = {
            'descricao': 'Vinculo hidráulico entre Subsistemas',
            'df': None,
            'formato':
                "{mne:>2}  {usi:>3}  {perc_vol:>5}\n",
        }
        self.bloco_ag = {
            'descricao': 'Número de estágios da PDD',
            'df': None,
            'formato':
                "{mne:>2}{num_estagios:>3}\n",
        }
        self.bloco_mh = {
            'descricao': 'Unidades Geradoras Hidroelétricas',
            'df': None,
            'formato':
                "{mne:>2}  {num:>3}  {gr:>2} {id:>2}{di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {f:1}\n",
        }
        self.bloco_mt = {
            'descricao': 'Unidades Termoelétricas',
            'df': None,
            'formato':
                "{mne:>2}  {ute:>3} {ug:>3}  {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {f:1}\n",
        }
        self.bloco_tx = {
            'descricao': 'Taxa de juros anual',
            'df': None,
            'formato':
                "{mne:>2}{taxa_fcf:>7}\n",
        }
        self.bloco_pq = {
            'descricao': 'Geração em Pequenas Usinas',
            'df': None,
            'formato':
                "{mne:>2}  {ind:>3}  {nome:>9}{ss/b:>4}{di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {geracao:>9}\n",
        }
        self.bloco_secr = {
            'descricao': 'Definição das seções de rio',
            'df': None,
            'formato':
                "{mne:>4} {num:>3} {nome:>9}   {usi_1:>3} {fator_1:>5} {usi_2:>3} {fator_2:>5} {usi_3:>3} "
                "{fator_3:>5} {usi_4:>3} {fator_4:>5} {usi_5:>3} {fator_5:>5}\n",
        }
        self.bloco_cr = {
            'descricao': 'Polinômio CotaxVazão para as seções de rio',
            'df': None,
            'formato':
                "{mne:>2}  {num:>3}  {nome:>9}   {gr:>2} {A0:>12} {A1:>12} {A2:>12} {A3:>12} {A4:>12} {A5:>12} "
                "{A6:>12}\n",
        }
        self.bloco_r11 = {
            'descricao': 'Unidades Termoelétricas',
            'df': None,
            'formato':
                "{mne:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {cotaIni:>9}{varhora:>9}{vardia:>9} "
                "{coef:100}\n",
        }
        self.bloco_vr = {
            'descricao': 'Entrada/saída de Horário de verão',
            'df': None,
            'formato':
                "{mne:>3} {dia:>2} {mneumo_verao:>4}\n",
        }
        self.bloco_pd = {
            'descricao': 'Tolerância para as perdas nas linhas de transmissão',
            'df': None,
            'formato':
                "{mne:>3} {tol_perc:>5} {tol_MW:>10}\n",
        }
        self.bloco_vm = {
            'descricao': 'Taxa de enchimento do volume morto',
            'df': None,
            'formato':
                "{mne:>3} {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {taxa_enchimento:>9}\n",
        }
        self.bloco_df = {
            'descricao': 'Taxa de descarga de fundo (defluência) das usinas com enchimento de volume morto',
            'df': None,
            'formato':
                "{mne:>3} {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {taxa_descarga:>9}\n",
        }
        self.bloco_me = {
            'descricao': 'Usinas Elevatórias',
            'df': None,
            'formato':
                "{mne:>3} {ind:>3} {di:>2} {hi:>2} {mi:1} {df:>2} {hf:>2} {mf:1} {fator:>9}\n",

        }
        self.bloco_meta_cjsist = {
            'descricao': 'Definição dos conjuntos de subsistemas',
            'df': None,
            'formato':
                "{mneumo:>13} {ind:>3} {nome:>5}\n",
        }
        self.bloco_meta_sist = {
            'descricao': 'Metas semanais de recebimento para os subsistemas',
            'df': None,
            'formato':
                "{mne:>13} {ind:>3} {tp:>2} {num:1} {meta:>9} {tol_MW:>9} {tol_perc:>9}\n",
        }
        self.bloco_meta_usit = {
            'descricao': 'Metas semanais de recebimento para as usinas térmicas',
            'df': None,
            'formato':
                "{mne:>13} {ind:>3} {tp:>2} {num:1} {meta:>9} {tol_MW:>9} {tol_perc:>9}\n",
        }
        self.bloco_sh = {
            'descricao': 'Opções de execução para a Simulação Hidroelétrica',
            'df': None,
            'formato':
                "{mne:>3} {flag_simul:1} {flag_pl:1} {num_min:>3} {num_max:>3} {flag_quebra:1} {ind_1:>3} {ind_2:>3} "
                "{ind_3:>3} {ind_4:>3} {ind_5:>3}\n",
        }
        self.bloco_tf = {
            'descricao': 'Custo de geração termoelétrica mínima futuro',
            'df': None,
            'formato':
                "{mne:>3} {custo:>9}\n",
        }
        self.bloco_rs = {
            'descricao': 'Monitoramento das variáveis ao longo da resolução do problema',
            'df': None,
            'formato':
                "{mne:>3} {cod:>3} {ind:>4} {subs:>4} {tp:>4} {comentario:>9}\n",
        }
        self.bloco_sp = {
            'descricao': 'Flag para considerar os Arquivos de saída no formato SIPPOEE',
            'df': None,
            'formato':
                "{mne:>3} {flag:1}\n",
        }
        self.bloco_ps = {
            'descricao': 'Flag para interromper a execução do caso após os dados de entrada',
            'df': None,
            'formato':
                "{mne:>3} {flag:1}\n",
        }
        self.bloco_pp = {
            'descricao': 'Flag para realização de pré-processamnto na resolução do problema, antes de resolvê-lo de '
                         'forma definitiva',
            'df': None,
            'formato':
                "{mne:>3} {flag:1} {iteracoes:>3} {num:>3} {tp:1}\n",
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
