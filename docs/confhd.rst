Contrato de Confhd
##################

Visão geral
===========

``Confhd.get()`` devolve o estado completo de uma UHE em um novo dicionário.
Listas e arrays são cópias independentes; alterá-los não modifica o caso antes
de ``put()``. ``Confhd.put()`` exige todas as chaves devolvidas por ``get()``,
valida os campos físicos e reincorpora explicitamente cada chave.

O fluxo suportado é:

.. code-block:: python

   from copy import deepcopy

   original = caso.confhd.get(codigo)
   atualizada = deepcopy(original)
   atualizada["ree"] = novo_ree
   atualizada["status"] = "EX"

   caso.confhd.put(atualizada)
   caso.confhd.escrever(caminho_confhd)
   caso.vazoes.escrever(caminho_vazoes)

``codigo`` identifica o registro e não é editável. ``get()`` acrescenta
``codigo_original`` ao dicionário para que ``put()`` consiga detectar uma
troca de identidade mesmo depois de ``deepcopy``. Por compatibilidade,
``put()`` ainda aceita um dicionário completo legado sem esse metadado, mas
todo novo dicionário obtido por ``get()`` o contém.

Mapa dos dados persistentes
===========================

Os intervalos abaixo são índices Python (início inclusivo, fim exclusivo) na
linha do arquivo. Não houve alteração de posição ou largura.

.. list-table::
   :header-rows: 1
   :widths: 11 13 11 15 9 11 10 10 13

   * - Campo
     - Chave
     - Tipo
     - Interno
     - Leitura
     - Atualização
     - Escrita
     - Round-trip
     - Posição/largura
   * - NUM
     - ``codigo``
     - ``int``
     - ``_codigo``
     - sim
     - identidade
     - sim
     - sim
     - ``[1:5]`` / 4
   * - NOME
     - ``nome``
     - ``str``
     - ``_nome``
     - sim
     - sim
     - sim
     - sim
     - ``[6:18]`` / 12
   * - POSTO
     - ``posto``
     - ``int``
     - ``_posto``
     - sim
     - sim
     - sim
     - sim
     - ``[19:23]`` / 4
   * - JUS
     - ``jusante``
     - ``int``
     - ``_jusante``
     - sim
     - sim
     - sim
     - sim
     - ``[25:29]`` / 4
   * - REE
     - ``ree``
     - ``int``
     - ``_ree``
     - sim
     - sim
     - sim
     - sim
     - ``[30:34]`` / 4
   * - V.INIC
     - ``vol_ini``
     - ``float``
     - ``_vol_ini``
     - sim
     - sim
     - sim
     - sim
     - ``[35:41]`` / 6
   * - U.EXIS
     - ``status``
     - ``str``
     - ``_status``
     - sim
     - sim
     - sim
     - sim
     - ``[44:46]`` / 2
   * - MODIF
     - ``modif``
     - ``int``
     - ``_modif``
     - sim
     - sim
     - sim
     - sim
     - ``[49:53]`` / 4
   * - INIC.HIST
     - ``ano_i``
     - ``int``
     - ``_ano_i``
     - sim
     - sim
     - sim
     - sim
     - ``[58:62]`` / 4
   * - FIM HIST
     - ``ano_f``
     - ``int``
     - ``_ano_f``
     - sim
     - sim
     - sim
     - sim
     - ``[67:71]`` / 4
   * - VAZOES.DAT
     - ``vazoes``
     - ``ndarray[int32]``
     - ``_vazoes`` / ``_copiavazoes``
     - sim
     - sim
     - por ``Vazoes.escrever()``
     - sim
     - ``(anos, 12)``

Política das demais chaves de get()
===================================

O mapa central ``Confhd._FIELD_MAP`` contém as 102 chaves históricas. Além
dos campos da tabela, elas têm as políticas explícitas abaixo:

* Dados cadastrais carregados de HIDR:
  ``bdh``, ``sist``, ``empr``, ``desvio``, ``vol_min``, ``vol_max``,
  ``vol_vert``, ``vol_min_desv``, ``cota_min``, ``cota_max``,
  ``pol_cota_vol``, ``pol_cota_area``, ``coef_evap``, ``num_conj_maq``,
  ``maq_por_conj``, ``pef_por_conj``, ``cf_hbqt*``, ``cf_hbqg*``,
  ``cf_hbpt*``, ``alt_efet_conj``, ``vaz_efet_conj``, ``prod_esp``,
  ``perda_hid``, ``num_pol_vnj``, ``pol_vaz_niv_jus*``,
  ``cota_ref_nivel_jus``, ``cfmed``, ``inf_canal_fuga``,
  ``fator_carga_max``, ``fator_carga_min``, ``vaz_min``, ``unid_base``,
  ``tipo_turb``, ``repres_conj``, ``teifh``, ``ip``, ``tipo_perda``,
  ``data``, ``observ``, ``vol_ref`` e ``tipo_reg``.
* Valores temporais incorporados de MODIF/EXPH:
  ``vol_mint``, ``vol_maxt``, ``vol_minp``, ``vaz_mint``, ``cfugat``,
  ``cmont``, ``status_vol_morto``, ``status_motoriz``,
  ``vol_morto_tempo``, ``engol_tempo``, ``potencia_tempo`` e
  ``unidades_tempo``.
* Valores calculados:
  ``vol_util``, ``pot_efet``, ``vaz_efet``, ``ro_65``, ``ro_50``,
  ``ro_equiv``, ``ro_equiv65``, ``ro_min``, ``ro_max``, ``engolimento`` e
  todas as chaves ``ro_acum*``.

Por compatibilidade, ``put()`` atualiza essas chaves no estado em memória;
nenhuma é ignorada. Elas não pertencem ao registro físico de ``CONFHD.DAT`` e
``Confhd.escrever()`` não tenta persistir dados cujo arquivo proprietário é
HIDR, MODIF ou EXPH. Valores calculados são derivados na leitura e também não
possuem campo físico no CONFHD.

Validações e normalizações
==========================

* ``nome`` deve ser uma string Latin-1 de até 12 caracteres e é preenchido à
  direita;
* ``status`` é normalizado para maiúsculas e aceita ``EX``, ``EE``, ``NE`` ou
  ``NC``;
* ``vol_ini`` deve estar entre 0 e 100 e é normalizado para duas casas;
* inteiros aceitam escalares Python ou NumPy sem truncamento;
* ``codigo`` deve existir; ``posto`` deve apontar para uma coluna existente
  da matriz; os demais inteiros devem caber em quatro posições;
* ``ano_i`` não pode ser posterior a ``ano_f``;
* ``vazoes`` deve ter forma ``(anos, 12)``, conter inteiros finitos dentro de
  ``int32`` e é copiada para a coluna do posto;
* chaves ausentes e desconhecidas geram ``KeyError``; tipos incompatíveis
  geram ``TypeError``; valores ou identidades inválidos geram ``ValueError``.

Vazões e postos compartilhados
==============================

CONFHD associa a UHE a uma série por ``posto``. Se duas UHEs usam o mesmo
posto, elas compartilham necessariamente a mesma coluna de ``VAZOES.DAT``.
Atualizar uma delas atualiza a série observada pela outra. Ao mudar ``posto``,
a série fornecida no dicionário é gravada na nova coluna; a coluna antiga não
é apagada.

Limites estruturais
===================

Não há limite fixo de quantidade de registros na classe: as listas crescem
conforme o arquivo. O código é limitado a quatro dígitos pelo CONFHD e o posto
é limitado simultaneamente a quatro dígitos e ao número de colunas lido de
``VAZOES.DAT``. No deck real de regressão há 162 UHEs e 320 postos possíveis.
