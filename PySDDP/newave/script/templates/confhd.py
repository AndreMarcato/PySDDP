# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Optional

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class ConfhdTemplate(ArquivoEntrada):
    """
    Classe que contem os dados de cadastro de todas as Usinas Hidrelétricas do newave.
    Esta classe tem como intuito fornecer duck typing para a classe Newave e ainda adicionar um nivel de especificacao
    dentro da fabrica. Alem disso esta classe deve passar adiante a responsabilidade da implementacao dos metodos de
    leitura e escrita
    """
    def __init__(self):

        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_postos = None
        self.const = None

        self._numero_registros_ = None
        self.nuhe = 0
        self.lista: Optional[list] = None
        self.lista_entrada: Optional[list] = None
        self.lista_resultados: Optional[list] = None
        self._copiavazoes = None

        # Dados de cadastro das usinas hidreletricas (presentes no HIDR.DAT)

        self._codigo = {
                    'descricao': 'Codigo da UHE',
                    'valor': list()
                 }
        self._nome = {
                    'descricao': 'Nome da UHE',
                    "valor": list()
               }
        self._posto = {
                    'descricao': 'Numero do Posto',
                    "valor": list()
               }
        self._bdh = {
                    'descricao': 'Banco de Dados Hidrometeorologico',
                    "valor": list()
               }
        self._sist = {
                    'descricao': 'Submercado',
                    "valor": list()
               }
        self._empr = {
                    'descricao': 'Codigo da empresa',
                    "valor": list()
               }
        self._jusante = {
                    'descricao': 'Codigo de Jusante',
                    "valor": list()
               }
        self._desvio = {
                    'descricao': 'Desvio de água',
                    "valor": list()
               }
        self._vol_min = {
                    'descricao': 'Volume Minimo',
                    "valor": list()
               }
        self._vol_max = {
                    'descricao': 'Volume Maximo',
                    "valor": list()
               }
        self._vol_vert = {
                    'descricao': 'Volume Vertimento',
                    "valor": list()
               }
        self._vol_min_desv = {
                    'descricao': 'Volume Minimo para Desvio',
                    "valor": list()
               }
        self._cota_min = {
                    'descricao': 'Cota Minima',
                    "valor": list()
               }
        self._cota_max = {
                    'descricao': 'Cota Maxima',
                    "valor": list()
               }
        self._pol_cota_vol = {
                    'descricao': 'Polinomio Cota-Volume',
                    "valor": list()
               }
        self._pol_cota_area = {
                    'descricao': 'Polinomio Cata-Area',
                    "valor": list()
               }
        self._coef_evap = {
                    'descricao': 'Coeficientes de Evaporacao',
                    "valor": list()
               }
        self._num_conj_maq = {
                    'descricao': 'Numero de Conjuntos de Maquinas',
                    "valor": list()
               }
        self._maq_por_conj = {
                    'descricao': 'Numero de Maquinas por Conjunto',
                    "valor": list()
               }
        self._pef_por_conj = {
                    'descricao': 'Potencia Efetiva por Maquina do Conjunto',
                    "valor": list()
               }
        self._cf_hbqt = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
        }
        self._cf_hbqg = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._cf_hbpt = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._alt_efet_conj = {
                    'descricao': 'Altura de Queda Efetiva do Conjunto',
                    "valor": list()
               }
        self._vaz_efet_conj = {
                    'descricao': 'Vazao Efetiva do Conjunto',
                    "valor": list()
               }
        self._prod_esp = {
                    'descricao': 'Produtibilidade Especifica',
                    "valor": list()
               }
        self._perda_hid = {
                    'descricao': 'Perda Hidraulica - (1) Percentual; (2) Metros',
                    "valor": list()
               }
        self._num_pol_vnj = {
                    'descricao': 'Numero de Polinomios Vazao Nivel Jusante',
                    "valor": list()
               }
        self._pol_vaz_niv_jus = {
                    'descricao': 'Polinomios Vazao Nivel Jusante',
                    "valor": list(),
                    "valor_2": list(),
                    "valor_3": list(),
                    "valor_4": list(),
                    "valor_5": list()
               }
        self._cota_ref_nivel_jus = {
                    'descricao': 'Cota Referencia Nivel de Jusante',
                    "valor": list()
               }
        self._cfmed = {
                    'descricao': 'Cota Media do Canal de Fuga',
                    "valor": list()
               }
        self._inf_canal_fuga = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._fator_carga_max = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._fator_carga_min = {
                    'descricao': 'Fator de Caga Minimo - Checar esta informacao ??????',
                    "valor": list()
               }
        self._vaz_min = {
                    'descricao': 'Vazao Minima Obrigatoria',
                    "valor": list()
               }
        self._unid_base = {
                    'descricao': 'Numero de Unidades de Base',
                    "valor": list()
               }
        self._tipo_turb = {
                    'descricao': 'Tipo de Turbina Hidraulica',
                    "valor": list()
               }
        self._repres_conj = {
                    'descricao': 'Representacao Conjunto de Maquina - Nao sei qual e esta informacao ?????',
                    "valor": list()
               }
        self._teifh = {
                    'descricao': 'Taxa Equivalente de Indisponibilidade Forcada Hidraulica',
                    "valor": list()
               }
        self._ip = {
                    'descricao': 'Indisponibilidade Programada',
                    "valor": list()
               }
        self._tipo_perda = {
                    'descricao': 'Tipo Perda Hidraulica',
                    "valor": list()
               }
        self._data = {
                    'descricao': 'Checar esta informacao ??????',
                    "valor": list()
               }
        self._observ = {
                    'descricao': 'Observacao',
                    "valor": list()
               }
        self._vol_ref = {
                    'descricao': 'Volume de Referencia',
                    "valor": list()
               }
        self._tipo_reg = {
                    'descricao': 'Tipo de Regularizacao',
                    "valor": list()
               }

        # Dados Adicionais Especificados no arquivo de configuracao hidraulica (CONFHD)
        self._ree = {
                        'descricao': 'Codigo do Reservatorio Equivalente de Energia',
                        'valor': list()
                    }
        self._status = {
                        'descricao': 'Status UHE (EX-Existente, EE-Exist em Expansão, NE-Nao Exist, NC-Nao Considerar',
                        'valor': list()
                      }
        self._vol_ini = {
                        'descricao': 'Percentual do Volume Util da UHE Disponivel no Inicio do Estudo',
                        'valor': list()
                      }
        self._modif = {
                        'descricao': 'Quandidade de modificacoes nos dados cadastrais do HIDR (verifica MODIF)',
                        'valor':  list()
                      }
        self._ano_i = {
                        'descricao': 'Primeiro ano do historico de afluencias (inclusive)',
                        'valor':  list()
                      }
        self._ano_f = {
                        'descricao': 'Ultimo ano do historico de afluencias (inclusive',
                        'valor':  list()
                      }

        # Dados Adicinais Calculados para as Usinas pertecentes a configuracao hidraulica (CONFHD)
        self._vol_util = {
                        'descricao': 'Volume Util da Usina Hidreletrica',
                        'valor': list(),
                        }
        self._vaz_efet = {
                        'descricao': 'Vazao Efetiva da Usina Hidreletrica',
                        'valor': list(),
                        }
        self._pot_efet = {
                        'descricao': 'Potencia Efetiva da Usina Hidreletrica',
                        'valor': list(),
                        }
        self._ro_65 = {
                        'descricao': 'PDTMED (NEWAVE) - PROD. ASSOCIADA A ALTURA CORRESPONDENTE A 65% DO VOLUME UTIL',
                        'valor': list(),
                    }
        self._ro_50 = {
                        'descricao': 'PROD. ASSOCIADA A ALTURA CORRESPONDENTE A 50% DO VOLUME UTIL',
                        'valor': list(),
                    }
        self._ro_max = {
                        'descricao': 'PDTMAX (NEWAVE) - PROD. ASSOCIADA A ALTURA MAXIMA',
                        'valor': list(),
                    }
        self._ro_min = {
                        'descricao': 'PDTMIN (NEWAVE) - PROD. ASSOCIADA A ALTURA MINIMA',
                        'valor': list(),
                    }
        self._ro_equiv = {
                        'descricao': 'PRODT (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO AO VOL. MAXIMO )',
                        'valor': list(),
                    }
        self._ro_equiv65 = {
                        'descricao': 'PRODTM (NEWAVE) - PROD. EQUIVALENTE ( DO VOL. MINIMO A 65% DO V.U. )',
                        'valor': list(),
                    }
        self._engolimento = {
                        'descricao': 'Engolimento da Usina Hidreletrica',
                        'valor': list(),
                    }
        self._ro_acum = {
                        'descricao': 'PDTARM (NEWAVE) - PROD. ACUM. PARA CALCULO DA ENERGIA ARMAZENADA',
                        'valor': list(),
                    }
        self._ro_acum_65 = {
                    'descricao': 'PDAMED (NEWAVE) - PROD. ACUM. PARA CALCULO E.ARMAZENADA CORRESP A 65% volume util',
                    'valor': list(),
                    }
        self._ro_acum_max = {
                        'descricao': 'PDCMAX e PDVMAX (NEWAVE) - PROD. ACUM.',
                        'valor': list(),
                    }
        self._ro_acum_med = {
                        'descricao': 'PDTCON, PDCMED e PDVMED (NEWAVE) - PROD. ACUM.',
                        'valor': list(),
                    }
        self._ro_acum_min = {
                        'descricao': 'PDCMIN e PDVMIN (NEWAVE) - PROD. ACUM.',
                        'valor': list(),
                        }
        self._ro_acum_a_ree = {
                        'descricao': 'Parcela A da Prod. Acumulada - Intercambio Hidraulico entre REE',
                        'valor': list(),
                        }
        self._ro_acum_b_ree = {
                        'descricao': 'Parcela B da Prod. Acumulada - Intercambio Hidraulico entre REE',
                        'valor': list(),
                        }
        self._ro_acum_c_ree = {
                        'descricao': 'Parcela C da Prod. Acumulada - Intercambio Hidraulico entre REE',
                        'valor': list(),
                        }
        self._ro_acum_a_sist = {
                        'descricao': 'Parcela A da Prod. Acumulada - Intercambio Hidraulico entre Submercados',
                        'valor': list(),
                        }
        self._ro_acum_b_sist = {
                        'descricao': 'Parcela B da Prod. Acumulada - Intercambio Hidraulico entre Submercados',
                        'valor': list(),
                        }
        self._ro_acum_c_sist = {
                        'descricao': 'Parcela C da Prod. Acumulada - Intercambio Hidraulico entre Submercados',
                        'valor': list(),
                        }
        self._ro_acum_entre_res_ree = {
                        'descricao': 'Produtibilidade Acumulada entre Reservatorios - REE',
                        'valor': list(),
                        }
        self._ro_acum_entre_res_sist = {
                        'descricao': 'Produtibilidade Acumulada entre Reservatorios - Submercados',
                        'valor': list(),
                        }

        # Vazoes Naturais, Incrementais e Par(p)
        self._vazoes = {
                        'descricao': 'Historico de Vazoes naturais (imes, ilag)',
                        'valor': list()
                      }
        self._fac = {
                     'descricao': 'Funcao de Autocorrelacao (imes, ilag)',
                     'valor': list()
                   }
        self._facp = {
                      'descricao': 'Funcao de Autocorrelacao Parcial (imes, ilag)',
                      'valor': list()
                    }
        self._coef_parp = {
                           'descricao': 'Coeficientes do Modelo par(p) (imes,ilag)',
                           'valor': list()
                         }
        self._coef_ind_parp = {
                        'descricao': 'Coeficientes indep. do Modelo par(p) (imes) - Aditivo = 0 - Multiplicativo > 0',
                        'valor': list()
                            }
        self._ordem = {
                       'descricao': 'Ordem do modelo par(p) para todos os meses (mes)',
                       'valor': list()
                     }

        # Parametros da usina Dependentes do Tempo - Especificados (MODIF.DAT)
        self._vol_mint = {
                          'descricao': 'Volume Mínimo Operativo (pode variar mes a mes)',
                          'valor': list()
                        }
        self._vol_maxt = {
                          'descricao': 'Volume Maximo Operativo (pode variar mes a mes)',
                          'valor': list()
                        }
        self._vol_minp = {
                          'descricao': 'Volume Mínimo com adocao de penalidade (pode variar mes a mes)',
                          'valor': list()
                        }
        self._vaz_mint = {
                          'descricao': 'Vazao Minima pode variar mes a mes',
                          'valor': list()
                        }
        self._cfugat = {
                        'descricao': 'Cota do Canal de Fuga em metros(pode variar mes a mes)',
                        'valor': list()
                        }
        self._cmont = {
                        'descricao': 'Nível de Montante em metros (pode variar mes a mes)',
                        'valor': list()
                        }

        # Parametros relativos a expansao hidrica que variam no tempo para usinas 'EE' e 'NE' (EXPH)
        self._status_vol_morto = {
                                'descricao': 'Status do Volume Morto - 0: Nao Comecou Encher - 1: Enchendo - 2: Cheio',
                                'valor': list()
                                }
        self._vol_morto_tempo = {
                                 'descricao': 'Evolucao do Volume Minimo da Usina',
                                 'valor': list()
                               }
        self._status_motoriz = {
                        'descricao': 'Status Motorizacao - 0: Nao Comecou Motorizar - 1: Motorizando - 3: Motorizada',
                        'valor': list()
                              }
        self._unidades_tempo = {
                                'descricao': 'Numero de Unidades em cada mes',
                                'valor': list()
                              }
        self._engol_tempo = {
                            'descricao': 'Evolucao do Engolimento Maximo da Usina',
                            'valor': list()
                           }
        self._potencia_tempo = {
                            'descricao': 'Evolucao da Potencia Instalada da Usina',
                            'valor': list()
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
