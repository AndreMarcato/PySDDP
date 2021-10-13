from abc import abstractmethod

from PySDDP.dessem.script.templates.arquivo_entrada import ArquivoEntrada


class DadosEletricosTemplate(ArquivoEntrada):
    """
    Classe que contem todos os elementos comuns a qualquer versao dos arquivos contendo os casos bases e os arquivos de
    modificacoes sobre os casos bases do Dessem.
    Esta classe tem como intuito fornecer duck typing para a classe Dessem e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """

    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.const = None

        self.titu = None
        self.dbar = None
        self.dlin = None
        self.dare = None
        self.danc = None
        self.dusi = None
        self.dcsc = None
        self.dref = None
        self.dgbt = None

        self.comentarios = None

        self.bloco_titu = {
            'df': None,
            'descricao':
                "titu\n",
            'formato':
                "{titu:<80}\n"
        }

        self.bloco_dbar = {
            'df': None,
            'descricao':
                "(Num)OETGb(   nome   )Gl( V)( A)( Pg)( Qg)( Qn)( Qm)(Bc  )( Pl)( Ql)( Sh)Are(Vf)M(1)(2)(3)(4)(5)(6)("
                "7)(8)(9)(10\n",
            'formato':
                "{num:<5}{cod_oper:1}{status:1}{tipo:1}{tensao:<2}{nome:>12}      {angulo:<4}{ger_ativa:>5}            "
                "         {carga_ativa:>5}          {area:>3}                    {num_subs}\n"
        }

        self.bloco_dlin = {
            'df': None,
            'descricao':
                "(De )d O d(Pa )NcEP ( R% )( X% )(Mvar)(Tap)(Tmn)(Tmx)(Phs)(Bc  )(Cn)(Ce)Ns(Cq)(1)(2)(3)(4)(5)(6)(7)("
                "8)(9)(10\n",
            'formato':
                "{barra_de:>5}  {cod_oper:1}  {barra_para:>5}{circ:>2}{status:1}{cod_ident:1} {resist:>6}{reat:>6}     "
                " {tap:>5}          {defasagem:>5}      {capac_norm:>4}{capac_emerg:>4}                        "
                "{flag_viol:1} {flag_perd:1}\n"
        }

        self.bloco_dare = {
            'df': None,
            'descricao':
                "(Ar    (Xchg)     (      Identificacao da area       ) (Xmin) (Xmax)\n",
            'formato':
                "{num_area:>3}  {cod_oper:1}            {nome_area:<36}\n"
        }

        self.bloco_danc = {
            'df': None,
            'descricao':
                "\n",
            'formato':
                "{num_area:<3} {fator:<6}\n"
        }

        self.bloco_dusi = {
            'df': None,
            'descricao':
                "(No) O (No) (Nome      )  ## DD (Pmin)(Pmax)(Qmin)(Qmax)    (Dumm)(Dumm)(No)#t\n"
                "(xxx  XXXXX xxxxxxxxxxxx  xx                                            xxxxXx\n",
            'formato':
                "{num_elem:>4} {cod_oper:1}{num_barra:>5} {nome_elem:<12}  {num_unid:>3}   {pmin:>6}{pmax:>6}          "
                "                  {num_cad:>4}{num_grupo:1}{tipo:1}\n"
        }

        self.bloco_dcsc = {
            'df': None,
            'descricao':
                "(De ) O  (Pa )NcEPB      (Xmin)(Xmax)( Xv )C ( Vsp) (Ext)Nst(Cn)(Ce)(Cq)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10"
                "\n",
            'formato':
                "{barra_de:>5} {cod_oper:1}  {barra_para:>5}{circ:>2}                     {reat_csc:>6}\n"
        }

        self.bloco_dref = {
            'df': None,
            'descricao_resp':
                "(RES O Nume       LInf      LSup  F                      Nome/Observacao para o restricao\n"
                "(xxx x xxxx xxxxxxxxxxXXXXXXXXXX  x    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n",
            'formato_resp':
                "{id:<4} {cod_oper:1} {num_restr:>4} {lim_inf:>10}{lim_sup:>10}  {flag_lim:1}    {obs:>50}\n",
            'descricao':
                "(E O  from   tonc   FatorPart\n"
                "(x x xxxxxxxxxxxx  xxxxxxxxxx\n",
            'formato':
                " {cod_elem:1} {cod_oper_real:1} {barra_de:>5}{barra_para:>5}{circ:>2}  {fator:>10}\n"
        }

        self.bloco_dgbt = {
            'df': None,
            'descricao':
                "(G ( kV)\n",
            'formato':
                "{niv_tensao:>2} {tensao_nom:>5}  {flag_lim:1}    {flag_perdas:1}\n"
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