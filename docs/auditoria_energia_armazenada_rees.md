# Auditoria e plano de implementação da energia armazenada em REEs

**Projeto:** PySDDP  
**Data da auditoria:** 16 de agosto de 2026  
**Escopo:** Energia Armazenável Máxima (EARMÁX), Energia Armazenada Inicial (EAR inicial), agregação por sistema/submercado e acoplamento hidráulico entre REEs  
**Natureza deste documento:** auditoria e proposta para aprovação; nenhuma alteração funcional foi implementada

## 1. Resumo executivo

A funcionalidade é viável com uma alteração futura pequena e localizada. O PySDDP já lê todos os dados necessários, já calcula as produtibilidades próprias e acumuladas por configuração e já calcula a EARMÁX de cada REE. Falta calcular a EAR inicial a partir do volume inicial útil de cada reservatório, expor resultados coerentes por REE e sistema e cobrir o comportamento com testes analíticos e um benchmark oficial.

Os principais achados são:

1. A EARMÁX existente em `Ree._calc_earm_max` segue a equação (19) da tese: para cada reservatório do REE, multiplica o volume útil pela produtividade acumulada até o fim da cascata e divide por `2,63`. Portanto, **o total atual já considera usinas a jusante situadas em outros REEs e outros sistemas** por meio de `ro_acum`.
2. O campo real não se chama `voli`: em `Confhd` ele é exposto como **`vol_ini`**, é um `float` em porcentagem do **volume útil** e aceita de 0 a 100 com duas casas decimais. O volume que deve valorar a EAR é `(vol_ini / 100) × (VMAX - VMIN)`, em hm³. O volume morto não entra.
3. A EAR inicial correta deve ser calculada reservatório a reservatório. `média(vol_ini) × EARMÁX` não é válida em geral; o percentual do REE é uma média ponderada pelas contribuições energéticas máximas individuais.
4. `ro_acum` é o campo correto e suficiente para o primeiro incremento. Ele é a PDTARM: soma `ro_equiv` da própria UHE e de todas as UHEs motorizadas disponíveis a jusante, inclusive fio d'água, até `jusante == 0`.
5. Há uma divergência importante na decomposição de acoplamento: no algoritmo atual, `ro_acum_b_ree`/`ro_acum_b_sist` recebem a sequência fio d'água logo após a fronteira, e `C` recebe a partir do primeiro reservatório de jusante. A tese e a documentação CEPEL definem **B como parcela controlável** (do primeiro reservatório de jusante em diante) e **C como parcela fio d'água** anterior a esse reservatório. B e C estão, portanto, semanticamente invertidas. O erro não afeta `ro_acum` nem a EARMÁX total, mas deve ser corrigido e testado antes de expor A/B/C publicamente.
6. Somar EARMÁX e EAR dos REEs associados produz diretamente os valores do sistema/submercado, inclusive quando há acoplamento. A energia deve permanecer contabilizada no REE de origem do armazenamento; a contribuição de geração a jusante já está dentro de sua PDTARM e não deve ser adicionada novamente ao REE receptor.
7. A entrada NEWAVE tem duas possíveis fontes para a condição inicial. `DGER.flag_earm_inic == 1` manda usar os percentuais individuais do `CONFHD`; com valor 0, o NEWAVE usa os percentuais por REE de `DGER.vol_earm_inic`. Uma API que pretenda reproduzir a condição efetiva do caso precisa respeitar essa seleção. Uma API explicitamente “a partir do CONFHD” pode forçar a primeira fonte, mas deve identificá-la no resultado.
8. O fator `2,63` é a convenção mensal já adotada pelo código e pelos artefatos NEWAVE para MWmês. A tese também mostra a formulação física `0,0864 × número de dias`, usando `2,6784` num mês de 31 dias. Essa diferença deve ser resolvida por aprovação e benchmark oficial; a recomendação de compatibilidade é manter `2,63` em uma constante central, sem variar pelo número de dias no primeiro incremento.

Risco geral: **baixo** para o cálculo total da EAR inicial reutilizando `ro_acum`; **médio** para tornar A/B/C público; **alto** se o escopo inicial for ampliado para EAR mensal genérica, mudanças de configuração, desvios hidráulicos ou decomposição por REE de destino.

## 2. Fontes analisadas

### 2.1 Código e dados do repositório

- `PySDDP/Pen.py`: composição e ordem de leitura da classe `Newave`.
- `PySDDP/newave/script/confhd.py`: leitura de `CONFHD`, aplicação de dados de `HIDR`, cálculo das produtibilidades e percurso da cascata.
- `PySDDP/newave/script/templates/confhd.py`: semântica documentada dos campos calculados.
- `PySDDP/newave/script/ree.py`: associação de UHEs a REEs e cálculo atual de EARMÁX.
- `PySDDP/newave/script/sistema.py`: cadastro dos sistemas/submercados, inclusive o indicador de sistema fictício.
- `PySDDP/newave/script/dger.py` e seu template: `flag_earm_inic`, `vol_earm_inic`, mês e ano inicial.
- `PySDDP/newave/script/hidr.py`, `modif.py`, `exph.py` e respectivos templates: cadastro, modificações, expansão e topologia.
- `PySDDP/hidr.py`, `PySDDP/resequiv.py`, `PySDDP/submercado.py` e `PySDDP/PowerSystem.py`: implementação legada paralela, útil apenas para identificar dívida técnica e a nomenclatura histórica de B/C.
- Caso real `PySDDP/pmo`: carregado sem alteração. O caso possui 162 UHEs, 12 REEs, 5 sistemas e `flag_earm_inic = 1`; foi usado como verificação estrutural, não como referência numérica oficial.
- Testes existentes em `tests`: não foram encontrados resultados “golden” de NEWAVE/NWLISTOP para EAR inicial por REE ou sistema.

### 2.2 Documentos locais

- `docs/manuais/doutorado_marcato.pdf`, especialmente capítulo 3, seção 3.3, equações (19) a (21), e capítulo 5, seção 5.2, equações (105) a (108) e Tabela 29.
- `docs/manuais/ManualUsuario_v31.pdf`. Apesar do nome do arquivo, seus metadados internos o identificam como Manual do Usuário NEWAVE versão 30.0.2, setembro de 2025. Foram verificados `CONFHD`, registros de condição inicial do `DGER`, blocos de EARMÁX/EAR e saídas por REE/submercado.
- `docs/manuais/versaofinal.doc`, versão complementar da tese. O PDF foi usado como fonte paginada principal.

### 2.3 Fontes oficiais CEPEL consultadas na web

- [Portal de documentação técnica do CEPEL](https://www.cepel.br/produtos/documentacao-tecnica/).
- [Manual de Metodologia — Libs/SEE, versão publicada mais recente no portal](https://see.cepel.br/manual/libs/latest/index.html).
- [Manual do Usuário do NEWAVE disponibilizado pelo CEPEL](https://www.cepel.br/wp-content/uploads/2024/10/ManualUsuario-2.pdf).
- [Manual de Referência do NEWAVE](https://www.cepel.br/wp-content/uploads/2022/02/NEWAVE_Manual-de-Refer_ncia_2001-07_v8-1.pdf).
- [Relatório CEPEL 097/2001 — acoplamento hidráulico entre sistemas equivalentes](https://www.cepel.br/wp-content/uploads/2022/02/Rel-097_2001.pdf).
- [Relatório CEPEL 27538/2017 — representação por 12 REEs e validação das parcelas de acoplamento](https://www.cepel.br/wp-content/uploads/2022/02/Rel-27538_2017.pdf).
- [Apresentação CEPEL “Desmistificando o REE”](https://cepel.br/wp-content/uploads/2024/01/2021-12-13-ApresentacaoCEPEL_Workshop-GTMet_Desmistificando-o-REE.pdf).
- [Relatório CEPEL NW2DS](https://www.cepel.br/wp-content/uploads/2022/05/Rel-2568_2021.pdf), que registra o volume inicial do `CONFHD` como percentual do volume útil e emprega PDTARM no cálculo individual por UHE.
- [Evolução e características do NEWAVE](https://www.cepel.br/linhas-de-pesquisa/newave-saiba-mais/), incluindo a evolução de 4 para 9 e 12 REEs e a possibilidade de múltiplos REEs por submercado.
- [Topologia de UHEs no Manual de Metodologia](https://see.cepel.br/manual/libs/latest/usinas_hidreletricas/curso_rios/topologia_usinas_hidreletricas.html).
- [Função de produção hidrelétrica no Manual de Metodologia](https://see.cepel.br/manual/libs/latest/usinas_hidreletricas/geracao_energia/funcao_producao_hidreletrica.html).

Consulta web realizada em 16 de agosto de 2026. O portal oficial deve ser novamente verificado na implementação, pois versões de manuais e executáveis evoluem independentemente do nome dos arquivos locais.

## 3. Modelo matemático

### 3.1 Definições

Para a UHE de reservatório `u`, pertencente ao REE `r`, no período/configuração `t`:

- `VMIN_u`, `VMAX_u`: volumes mínimo e máximo, em hm³;
- `VU_u = VMAX_u - VMIN_u`: volume útil, em hm³;
- `p_u = vol_ini_u / 100`: fração inicial do volume útil;
- `VA_u(0) = p_u × VU_u`: volume útil armazenado inicial, em hm³;
- `rho_acum_u(t)`: PDTARM, no código `ro_acum[u][ano][mês]`, em MW/(m³/s);
- `F`: fator de conversão de `(hm³ × MW/(m³/s))` para MWmês.

Apenas UHEs com armazenamento (`vol_util > 0`), pertencentes ao REE e disponíveis na configuração entram como origens da soma. UHEs fio d'água não possuem parcela própria de volume armazenado, mas suas produtibilidades entram na PDTARM dos reservatórios a montante.

### 3.2 EARMÁX por REE

A equação (19) da tese se traduz diretamente em:

```text
EARMX_r(t) = Σ[u reservatório do REE r, disponível em t]
             VU_u × rho_acum_u(t) / F
```

`rho_acum_u(t)` deve incluir a produtividade equivalente da própria UHE e das UHEs motorizadas disponíveis a jusante até o final da cascata pertinente à representação. Na configuração NEWAVE lida atualmente, esse valor é `ro_acum`; não se deve recalculá-lo na nova funcionalidade.

### 3.3 EAR inicial por REE a partir do CONFHD

Conforme a afirmação posterior à equação (19), substitui-se o volume útil máximo pelo volume útil efetivamente armazenado:

```text
EAR_INICIAL_r = Σ[u reservatório do REE r, disponível em t0]
                ((vol_ini_u / 100) × VU_u) × rho_acum_u(t0) / F
```

O volume é o que está **acima de VMIN**. Não se deve usar `VMIN + p × VU`, pois isso valoraria o volume morto como energia controlável.

O caso de percentuais distintos deixa clara a ponderação correta. Definindo

```text
w_u = VU_u × rho_acum_u(t0) / F,
```

tem-se:

```text
100 × EAR_INICIAL_r / EARMX_r = Σ(vol_ini_u × w_u) / Σ(w_u).
```

Portanto, trata-se de média ponderada pela energia armazenável individual, não da média aritmética dos percentuais. A igualdade “EAR inicial = p × EARMÁX” só vale quando todos os reservatórios relevantes têm o mesmo `p` ou quando, por coincidência, a média aritmética e a ponderada são iguais.

### 3.4 Semântica de `vol_ini`

O campo público de `Confhd._get` é `vol_ini`, não `voli`:

- origem: colunas 36–41 do registro `CONFHD`, formato F6.2;
- tipo em Python: `float`;
- unidade: porcentagem;
- base: volume útil da UHE, `VMAX - VMIN`;
- faixa validada pelo PySDDP: `[0, 100]`, duas casas decimais;
- transformação: `volume_útil_armazenado_hm3 = vol_ini / 100 × vol_util`;
- volume morto: não incluído na grandeza armazenável;
- fio d'água: `Confhd` força `vol_util = 0` quando `tipo_reg != "M"`; seu `vol_ini` não gera EAR própria;
- nulos/especiais: o parser executa `float(...)`; vazio, `None`, NaN ou texto não constituem entrada válida. A API futura deve rejeitá-los explicitamente, em vez de propagar NaN.

Há ainda uma distinção de fonte: com `DGER.flag_earm_inic == 0`, a condição inicial efetiva do NEWAVE vem de `DGER.vol_earm_inic`, por REE, e o campo individual do `CONFHD` é ignorado. Com flag 1, usa-se o `CONFHD`. Para a fonte DGER, sob a representação em operação paralela:

```text
EAR_INICIAL_r = (percentual_DGER_r / 100) × EARMX_r(t0).
```

### 3.5 Agregação por sistema/submercado

Usando a associação `REE.DAT: submercado`:

```text
EARMX_s = Σ[r associado a s] EARMX_r
EAR_INICIAL_s = Σ[r associado a s] EAR_INICIAL_r
PERCENTUAL_s = 100 × EAR_INICIAL_s / EARMX_s
```

O percentual do sistema é a razão das somas, não a média dos percentuais dos REEs. Se `EARMX == 0` dentro de tolerância, o percentual é matematicamente indefinido e deve ser retornado como `NaN`/`None` acompanhado de estado explícito, não como zero.

A associação normativa para agregar REEs é o campo `submercado` de `REE.DAT`, presente em `Ree.bloco_ree['df']`. O campo `sist` de cada UHE, originado no `HIDR`, deve servir para validação de consistência, não para reconstruir silenciosamente a associação do REE.

### 3.6 Unidade e fator temporal

`VU [hm³] × rho [MW/(m³/s)]` é convertido em energia média mensal dividindo por um fator em `hm³/(m³/s)` por mês. Fisicamente:

```text
F_dias = 86.400 × dias / 1.000.000 = 0,0864 × dias.
```

A tese usa `F = 2,6784` no exemplo de 31 dias. O PySDDP atual usa literalmente `2,63`, aproximadamente o mês médio convencional de 30,44 dias, e seus resultados são denominados MWmês. Para manter compatibilidade com o NEWAVE e com a EARMÁX existente, a primeira implementação deve:

- usar `float64` e MWmês;
- centralizar `F_NEWAVE_MWMES = 2.63` em um único local documentado;
- não variar `F` com o calendário na API inicial;
- validar o valor contra uma saída oficial da mesma versão do NEWAVE antes da liberação.

Se futuramente houver modo físico por período civil, ele deve ser uma convenção explicitamente nomeada e não uma mudança silenciosa do resultado compatível.

### 3.7 Período inicial

Os vetores de `Confhd` são indexados como `[índice_de_ano][mês_calendário_0_a_11]`. A configuração inicial deve usar o primeiro ano de estudo e o mês indicado em `DGER.mesi_est`, isto é, conceitualmente `(0, mesi_est - 1)`, observando a regra específica do manual para eventual período pré-estudo. Não se deve assumir sempre `[0][0]`.

## 4. Tratamento do acoplamento hidráulico

### 4.1 Interpretação das equações (105)–(108)

O capítulo 5 não redefine a EARMÁX total: ele particiona a produtividade acumulada da água armazenada a montante. Para uma origem `u`:

- **A — própria:** geração na parte da cascata ainda pertencente ao REE/sistema de origem;
- **B — controlável a jusante:** geração a partir do primeiro reservatório pertencente ao REE/sistema de jusante e nas usinas posteriores;
- **C — fio d'água a jusante:** geração nas UHEs fio d'água consecutivas depois da fronteira e antes desse primeiro reservatório.

Assim, para a mesma origem, `rho_acum = A + B + C`. A Tabela 29 conserva a EARMÁX total do conjunto: as parcelas qualificam onde a água armazenada poderá gerar, mas não criam um segundo estoque de energia.

### 4.2 Sem acoplamento entre REEs

Se “sem acoplamento” significa que a topologia/modelagem configurada torna os REEs hidraulicamente independentes, a produtividade acumulada deve terminar na fronteira do REE. Isso deve decorrer da topologia ou de uma política metodológica explícita; não é recomendável cortar uma cascata NEWAVE real por um booleano genérico.

Para o comportamento atual e compatível do deck, a nova EAR deve simplesmente usar `ro_acum`. Se futuramente for necessário comparar formulações, é mais seguro um parâmetro nomeado, por exemplo `escopo_produtibilidade="cascata_configurada" | "limite_ree"`, com o primeiro como padrão, do que `considerar_acoplamento=True/False`.

### 4.3 Com acoplamento entre REEs

Sim: a energia potencial da água armazenada no REE de montante deve incluir sua geração futura nas UHEs dos REEs de jusante. Essa é precisamente a PDTARM acumulada usada na equação (19) e na decomposição do capítulo 5.

Não há dupla contagem quando cada termo permanece atribuído ao **reservatório/REE de origem do volume**. O reservatório de jusante tem sua própria EARMÁX, calculada apenas sobre seu volume útil próprio; ele não recebe novamente o volume de montante. Haveria dupla contagem se B/C fossem somadas como novo estoque no REE de destino além do total já atribuído à origem.

### 4.4 REEs acoplados no mesmo sistema

Somam-se diretamente as EARMÁX/EAR por origem de todos os REEs associados. A fronteira hidráulica entre eles não exige ajuste adicional. As parcelas A/B/C entre esses REEs são internas ao sistema e só interessam a um relatório de decomposição; o total do sistema permanece a soma simples.

### 4.5 REEs acoplados em sistemas diferentes

Também se somam diretamente os REEs associados a cada sistema. A água armazenada no sistema de montante continua sendo estoque desse sistema, embora parte de sua geração futura ocorra no sistema de jusante. B/C podem informar essa geração futura por destino, mas não devem ser transferidas nem somadas ao estoque do sistema receptor.

### 4.6 Problema encontrado nas parcelas B/C

Em `Confhd._prod_acum`, linhas 903–926, a variável `FioRee`/`FioSist` começa verdadeira após a fronteira. Enquanto encontra UHEs sem volume útil, o código acumula em B; ao encontrar o primeiro reservatório, muda a variável para falsa **antes** de acumular e passa a registrar em C. Isso produz:

```text
B_atual = fio d'água antes do primeiro reservatório a jusante
C_atual = primeiro reservatório de jusante e trecho posterior
```

A semântica CEPEL é a oposta. A implementação legada confirma que não se trata apenas de documentação: gráficos de `resequiv.py`/`submercado.py` rotulam historicamente B como “FioJusante” e C como “ContJusante”. O Relatório CEPEL 27538/2017, ao descrever casos com parcelas A e C associadas a geração fio d'água em Itaipu, oferece evidência externa adicional.

Consequências:

- `ro_acum`, EARMÁX e a futura EAR total não são afetados;
- A/B/C não devem ser expostas pela primeira versão da API;
- antes de expô-las, é necessário corrigir a classificação, decidir compatibilidade e criar regressão;
- os campos atuais são escalares por UHE de origem e não têm índice do REE/sistema de destino `l` das equações (107)–(108). Uma decomposição completa por destino exige estrutura nova, fora do escopo mínimo.

## 5. Inventário da implementação atual

| Elemento | Classe/arquivo e método | Unidade/dimensão | Reutilizável? | Observação |
|---|---|---:|---|---|
| `vol_ini` | `Confhd`, leitura e `_validate_values` | `% VU`, escalar/UHE | Sim | Campo real correspondente a `voli`; faixa 0–100 |
| `vol_min`, `vol_max`, `vol_util` | `Confhd`, dados `HIDR` e ajustes | hm³, escalar/UHE | Sim | `vol_util=VMAX-VMIN` apenas para reservatório |
| `ro_65` | `Confhd._calc_produtibs` | MW/(m³/s), `[ano][12]` | Não para EARMÁX | Produtividade na cota de 65% VU (`PDTMED`) |
| `ro_50` | `Confhd._calc_produtibs` | MW/(m³/s), `[ano][12]` | Não | Produtividade na cota de 50% VU |
| `ro_min`, `ro_max` | `Confhd._calc_produtibs` | MW/(m³/s), `[ano][12]` | Não para EARMÁX | Produtividade nas cotas mínima/máxima |
| `ro_equiv` | `Confhd._calc_produtibs` | MW/(m³/s), `[ano][12]` | Indiretamente | `PRODT`: produtividade própria na altura equivalente integrada de VMIN a VMAX |
| `ro_equiv65` | `Confhd._calc_produtibs` | MW/(m³/s), `[ano][12]` | Não para EARMÁX | `PRODTM`: altura equivalente de VMIN a 65% VU |
| `ro_acum` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | **Sim, diretamente** | `PDTARM`; própria + UHEs disponíveis/motorizadas a jusante até o fim |
| `ro_acum_65` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não para fórmula máxima | `PDAMED`, soma `ro_equiv65` |
| `ro_acum_max` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não | Soma `ro_max` |
| `ro_acum_med` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não | Soma `ro_65` |
| `ro_acum_min` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não | Soma `ro_min` |
| `ro_acum_a/b/c_ree` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não na v1 | A funciona como parcela própria; B/C estão invertidas e não indexam destino |
| `ro_acum_a/b/c_sist` | `Confhd._prod_acum` | MW/(m³/s), `[ano][12]` | Não na v1 | Mesmo problema em fronteira de sistema |
| EARMÁX por REE | `Ree._calc_earm_max` | MWmês, `[ano][12]`, `float32` | Sim, após encapsular | Já usa `ro_acum × vol_util / 2.63` |
| Associação REE→sistema | `Ree.bloco_ree['df'].submercado` | código inteiro | Sim | Fonte normativa para agregação |
| Sistema fictício | `Sistema.bloco_sistema['df'].tipo` | `0` real, `1` fictício | Sim | Política de exposição precisa ser aprovada |
| Topologia | `Confhd`: `codigo`, `jusante`, `ree`, `sist` | códigos escalares | Parcial | `jusante == 0` termina; percurso linear por origem |
| Condição inicial | `Dger.flag_earm_inic`, `vol_earm_inic` | flag e `%` por REE | Sim | Hoje apenas lidos/escritos; não alimentam um cálculo de EAR |

Detalhes relevantes:

- `_calc_produtibs` considera a cota do canal de fuga temporal (`cfugat`) e o tipo de perda hidráulica. As matrizes são `float64`.
- `_prod_acum` inclui uma UHE na soma quando `status_vol_morto == 2` e sua produtividade quando `status_motoriz == 2`. UHE fio d'água disponível contribui para a produtividade de montante.
- `Ree._calc_earm_max` cria o resultado com dtype `float32`; a API nova deve acumular em `float64` para reduzir erro numérico.
- O cálculo atual de EARMÁX é executado durante a leitura de `REE.DAT` e armazenado no DataFrame de REEs. Não há cálculo de EAR inicial.

### 5.1 Topologia e estruturas especiais

O percurso principal segue um único ponteiro `jusante` por UHE até zero. A detecção de mudança compara `uhe['ree']` e `uhe['sist']` aos códigos da origem. Não há objeto de grafo compartilhado nem validação explícita de ciclo, código de jusante inexistente ou reentrada de fronteira; existem percursos separados em `_prod_acum`, `vaz_inc` e `vaz_inc_entre_res`.

O cadastro contém `desvio`, e `MODIF` reconhece conceitualmente `CDESVIO`, mas a rotina atual que aplica modificações não incorpora `CDESVIO` no percurso da PDTARM. Bifurcações/desvios não são representados por `jusante` sozinho. Para a v1, criar outra travessia seria duplicação e risco: deve-se reutilizar `ro_acum`. Em evolução posterior, recomenda-se extrair um helper de topologia validada, com detecção de ciclos, alvos ausentes e política documentada para desvios.

Usinas e sistemas fictícios precisam ser preservados quando façam parte da representação oficial do deck; algumas UHEs fictícias são usadas justamente para modelar fronteiras/acoplamentos. Não se deve excluí-las do cálculo hidráulico sem benchmark. Na tabela pública por submercado, sistemas `tipo == 1` devem aparecer marcados ou ser excluídos apenas por opção explícita.

### 5.2 Configuração temporal e FDIN

As produtividades e estados são mensais. `Confhd` possui séries como `status_vol_morto`, `status_motoriz`, `cfugat`, `vol_mint` e `vol_maxt`, enquanto `vol_util` usado pela EARMÁX é hoje uma base escalar depois de ajustes cadastrais. Entrada de UHE, motorização e canal de fuga já afetam `ro_acum` por período; nem toda modificação de volume é refletida de maneira uniforme no `vol_util` da EARMÁX.

A tese define FDIN para corrigir a EAR quando muda a configuração equivalente. O PySDDP não implementa essa cadeia. Isso não impede a EAR inicial, que usa somente a primeira configuração, mas impede prometer uma API mensal genérica correta apenas generalizando o índice.

Conclusão temporal:

- **v1 — EAR inicial:** basta a primeira configuração efetiva do estudo, selecionada pelo mês inicial do DGER;
- **evolução:** uma API para qualquer período deve receber período/configuração, definir volumes úteis temporais, entradas/saídas, espera de enchimento e FDIN, e ser validada separadamente.

## 6. Lacunas identificadas

1. Não existe cálculo nem API de EAR inicial.
2. `DGER.flag_earm_inic` e `vol_earm_inic` são lidos, mas não conectados ao domínio.
3. Não há agregação pronta de EARMÁX/EAR por sistema com validação de REEs e sistemas fictícios.
4. O fator `2,63` está literal dentro de `Ree._calc_earm_max`, sem constante/unidade central.
5. O resultado atual de EARMÁX usa `float32`.
6. B/C estão semanticamente invertidas em REE e sistema.
7. A/B/C não identificam o destino, embora a formulação teórica tenha índice `l`.
8. Não há validação robusta da topologia hidráulica nem tratamento completo de desvio/bifurcação.
9. A ativação temporal do REE e algumas modificações de volume não são consideradas explicitamente no cálculo de EARMÁX.
10. Não há implementação de FDIN para uma série genérica de EAR.
11. Não há benchmark oficial versionado no repositório para EARMÁX/EAR inicial.
12. Há duas arquiteturas paralelas (classes atuais em `newave/script` e classes legadas na raiz de `PySDDP`); duplicar o cálculo nelas agravaria a divergência.

## 7. Plano de implementação proposto

### Etapa 0 — decisões e caso de referência

- **Objetivo:** congelar convenção, fonte inicial e comportamento de sistemas fictícios.
- **Arquivos:** documentação/testes; nenhum cálculo ainda.
- **Ações:** obter uma saída oficial NEWAVE/NWLISTOP da mesma versão para um deck imutável com `flag_earm_inic=1`; registrar EARMÁX e EARMI por REE e submercado.
- **Testes:** script de comparação tolerante versionado como fixture, se a licença permitir.
- **Risco:** baixo; bloqueia ambiguidades antes do código.

### Etapa 1 — testes analíticos do contrato

- **Objetivo:** definir resultados antes de implementar.
- **Arquivos prováveis:** novos testes em `tests/newave` ou estrutura equivalente.
- **Ações:** construir fixtures mínimas em memória para os casos A–K da seção 9; incluir mês inicial diferente de janeiro e fontes DGER/CONFHD.
- **Risco:** baixo.

### Etapa 2 — cálculo puro por origem

- **Objetivo:** calcular EARMÁX e EAR inicial em `float64`, sem alterar parsers.
- **Arquivos prováveis:** novo módulo de domínio, por exemplo `PySDDP/newave/energia_armazenada.py`, mais uma fachada fina em `PySDDP/Pen.py`/`Newave`.
- **Ações:** reutilizar `Confhd._get`, `vol_util`, `vol_ini` e `ro_acum`; centralizar fator/unidades; filtrar disponibilidade; validar percentuais e dimensões.
- **Testes:** A–F, K, fator/unidade, não janeiro.
- **Risco:** baixo. Não criar uma segunda rotina de cascata.

### Etapa 3 — seleção da fonte efetiva

- **Objetivo:** reproduzir o caso NEWAVE.
- **Ações:** implementar `fonte="efetiva"`, respeitando `flag_earm_inic`; oferecer fontes explícitas `confhd` e `dger`; registrar a fonte no resultado.
- **Testes:** flag 0, flag 1, percentuais inválidos, quantidade incompatível com REEs.
- **Risco:** médio, por diferenças de formato/versão do DGER.

### Etapa 4 — agregação por REE e sistema

- **Objetivo:** tabelas estáveis e dinâmicas, sem hardcode de quatro sistemas.
- **Ações:** associar pelo `REE.DAT.submercado`; validar sistema inexistente; definir política de fictícios; calcular percentuais como razão de somas.
- **Testes:** G–I, REE sem reservatório, REE sem associação válida e sistema fictício.
- **Risco:** baixo a médio.

### Etapa 5 — benchmark e documentação pública

- **Objetivo:** autorizar liberação.
- **Ações:** comparar por REE e submercado contra NEWAVE/NWLISTOP; documentar MWmês, fator, período, fonte e tolerância; testar round-trip dos decks sem alteração.
- **Risco:** médio enquanto não houver executável/saída oficial disponível.

### Etapa 6 — correção de B/C em mudança separada

- **Objetivo:** alinhar as parcelas de acoplamento com CEPEL.
- **Ações:** primeiro criar testes que demonstrem A+B+C=`ro_acum`; corrigir a atribuição B/C; avaliar impacto em consumidores legados; documentar eventual quebra semântica.
- **Testes:** fronteira seguida de fio d'água e depois reservatório, fronteiras múltiplas, REE e sistema, comparação com relatório CEPEL.
- **Risco:** médio/alto por compatibilidade. Não é pré-requisito para a EAR total, mas é pré-requisito para publicar parcelas.

### Etapa 7 — evolução mensal, somente em tarefa futura

- **Objetivo:** EAR em qualquer configuração.
- **Ações:** definir volumes úteis temporais, ativação de REE/UHE, alterações MODIF/EXPH, FDIN e desvios; aceitar período explícito.
- **Testes:** J e séries de configuração completas.
- **Risco:** alto; fora do incremento inicial.

## 8. Proposta de API

A lógica precisa simultaneamente de DGER, CONFHD, REE e SISTEMA. Por isso, a entrada pública mais coerente é a fachada `Newave`, com um calculador de domínio puro internamente; colocá-la apenas em `Ree` forçaria dependências externas e efeitos durante parsing.

Proposta conceitual, sem implementação:

```python
resultado = newave.calcular_energia_armazenada_inicial(
    fonte="efetiva",       # "efetiva" | "confhd" | "dger"
    periodo=None,          # None = primeiro estágio; reservado para evolução
    incluir_ficticios=True,
)
```

Retorno compatível com o estilo pandas atual:

```python
{
    "por_ree": pandas.DataFrame,
    "por_submercado": pandas.DataFrame,
    "metadados": {
        "unidade": "MWmes",
        "fonte": "confhd",
        "fator_conversao": 2.63,
        "ano": 2018,
        "mes": 1,
        "escopo_produtibilidade": "cascata_configurada",
    },
}
```

Colunas mínimas de `por_ree`:

```text
codigo_ree, nome_ree, codigo_submercado, nome_submercado,
earm_max_mwmes, ear_inicial_mwmes, percentual_earm
```

Colunas mínimas de `por_submercado`:

```text
codigo_submercado, nome_submercado, codigos_rees,
earm_max_mwmes, ear_inicial_mwmes, percentual_earm, ficticio
```

Comportamento de erro recomendado:

- `ValueError` com código/posição para `vol_ini` fora de `[0,100]`, NaN ou dimensão temporal incompatível;
- erro explícito para REE ligado a sistema inexistente; opcionalmente modo diagnóstico que crie grupo “não associado”, nunca descarte silencioso;
- percentual `NaN` quando EARMÁX for nula, mantendo EAR/EARMÁX numéricas;
- não mutar `Confhd`, `Ree.bloco_ree` ou `Sistema` durante o cálculo;
- resultados `float64` e cópias independentes.

Não se recomenda um booleano `considerar_acoplamento_hidraulico`. A topologia configurada e a escolha da PDTARM já definem o comportamento. Se a comparação sem acoplamento for realmente requisito, usar enum explícito e documentado; omiti-lo da v1 reduz a chance de produzir números incompatíveis com o deck.

As parcelas A/B/C não devem estar no retorno mínimo. Uma API posterior pode expor tabela separada, com origem, destino, tipo de parcela e unidade, depois da correção de B/C e da inclusão do índice de destino.

## 9. Estratégia de validação

### 9.1 Testes analíticos indispensáveis

| Caso | Montagem | Asserção principal |
|---|---|---|
| A | Um REE, um reservatório | Fórmula fechada de EARMÁX e EAR |
| B | Um REE, vários reservatórios em cascata | Cada volume usa sua própria PDTARM acumulada |
| C | Percentuais iniciais diferentes | Resultado individual; rejeitar média aritmética × EARMÁX |
| D | Fio d'água a jusante | Zero de armazenamento próprio, produtividade incluída a montante |
| E | Dois REEs sem ligação | Resultados independentes |
| F | Dois REEs acoplados | Montante inclui jusante; soma por origem sem duplicação |
| G | Dois REEs do mesmo sistema | Soma direta e percentual como razão de somas |
| H | REEs acoplados em sistemas distintos | Estoque permanece no sistema de origem |
| I | Vários sistemas, inclusive códigos não sequenciais | Agregação dinâmica, sem quatro sistemas fixos |
| J | Entrada de UHE/mudança de configuração | Reservado à API mensal/FDIN |
| K | 0%, 100%, fio d'água, REE vazio, inconsistências | Limites, NaN percentual e erros claros |

Testes adicionais obrigatórios:

- `DGER.flag_earm_inic` 0 e 1;
- mês inicial diferente de janeiro;
- igualdade entre implementação atual e nova EARMÁX dentro de tolerância;
- `float64` e tolerância numérica declarada;
- jusante inexistente e ciclo detectados por validador futuro;
- regressão específica demonstrando a inversão B/C atual;
- invariantes `A+B+C=ro_acum` e soma por origem;
- sistemas fictícios e REE com associação inválida.

### 9.2 Benchmark oficial

Procedimento recomendado:

1. selecionar deck licenciado e imutável com `flag_earm_inic=1`, múltiplos REEs e pelo menos uma fronteira hidráulica;
2. executar a versão identificada do NEWAVE e NWLISTOP/NWLISTCF;
3. capturar EARMÁX e EARMI da primeira configuração por REE;
4. comparar valores do PySDDP em MWmês, com tolerância absoluta e relativa justificadas;
5. agregar os mesmos REEs por submercado e comparar as tabelas oficiais, que documentam a soma dos REEs associados;
6. repetir com `flag_earm_inic=0` para validar a seleção da fonte DGER;
7. versionar somente os resultados permitidos/licenciados e metadados do executável.

O caso `PySDDP/pmo` demonstrou que os campos e dimensões necessários estão presentes, mas o repositório não contém uma saída oficial correspondente de EAR inicial. Seus valores calculados não devem ser promovidos a “golden” sem essa comparação.

### 9.3 Estado da suíte atual

`pytest` não está instalado no ambiente. A execução de `python -m unittest discover -s tests -v` iniciou 138 testes, mas terminou com 149 erros de limpeza/acesso em diretórios temporários sob `tests/tmp...` no ambiente Windows restrito. Não houve base confiável para interpretar isso como falha funcional da biblioteca. Antes da implementação, a suíte deve ser executada em ambiente com diretório temporário gravável e o isolamento de temporários deve ser corrigido/confirmado.

## 10. Riscos técnicos

| Risco | Impacto | Mitigação |
|---|---|---|
| Recontar B/C no REE de destino | Dupla contagem | Contabilizar estoque exclusivamente por origem; parcelas em tabela separada |
| Interpretar `vol_ini` como volume total | Superestimação pelo volume morto | Converter `% × (VMAX-VMIN)` |
| Média simples de percentuais | EAR incorreta em REE heterogêneo | Soma individual/ponderação energética |
| Troca semântica B/C atual | Relatório de acoplamento incorreto | Corrigir em mudança separada com teste e análise de compatibilidade |
| Usar `ro_65` ou `ro_equiv` isolado | Ignorar parte da cascata | Reutilizar `ro_acum`/PDTARM |
| Fator 2,63 versus dias civis | Divergência de unidade/benchmark | Convenção central e benchmark oficial |
| Assumir janeiro | Configuração inicial errada | Usar `DGER.mesi_est` e ano inicial |
| Ignorar `flag_earm_inic` | Não reproduzir caso NEWAVE | Fonte `efetiva` explícita |
| Somar percentuais | Resultado por sistema incorreto | Razão entre EAR e EARMÁX agregadas |
| REE sem reservatório | Divisão por zero | EARMÁX/EAR zero e percentual indefinido |
| Fio d'água com `vol_ini` | Estoque fictício | Exigir `vol_util > 0`; manter produtividade a jusante |
| Sistema/REE fictício | Exclusão indevida de modelagem | Marcar e configurar exposição; não retirar da cascata sem validação |
| Topologia inválida/desvio | Loop, erro ou PDTARM incompleta | Reusar PDTARM na v1; validador/grafo em evolução |
| Mudanças de configuração/FDIN | Série mensal conceitualmente errada | Limitar v1 ao primeiro estágio |
| `float32` no EARMÁX atual | Arredondamento acumulado | Calcular/retornar em `float64` |
| Arquiteturas paralelas | Resultados divergentes | Implementar apenas na arquitetura `Newave` atual |

## 11. Decisões que exigem aprovação

1. **Convenção temporal:** aprovar `2,63` como fator NEWAVE em MWmês na v1, condicionado ao benchmark, ou exigir fator por dias.
2. **Fonte padrão:** recomenda-se `fonte="efetiva"`, respeitando `DGER.flag_earm_inic`; confirmar se o produto também deve oferecer modo forçado `confhd`.
3. **Local da API:** aprovar fachada em `Newave` com calculador puro de domínio, em vez de adicionar lógica ao parser `Ree`.
4. **Sistemas fictícios:** recomenda-se preservar no cálculo e retornar marcados por padrão; aprovar política de filtragem apenas na apresentação.
5. **Associação inválida:** recomenda-se erro em modo normal e relatório diagnóstico opcional, sem descarte silencioso.
6. **Acoplamento:** aprovar uso invariável de `ro_acum`/cascata configurada na v1 e ausência de booleano.
7. **B/C:** aprovar correção em mudança separada e decidir política de compatibilidade para consumidores dos nomes antigos.
8. **Escopo temporal:** aprovar que a v1 calcula somente a condição inicial; período arbitrário e FDIN ficam fora.
9. **Benchmark:** definir deck, versão do executável CEPEL, tolerâncias e possibilidade de versionar saídas.

## 12. Recomendações finais e respostas obrigatórias

### 12.1 Respostas diretas

1. **Fórmula de EARMÁX do REE:** soma, sobre reservatórios disponíveis do REE, de `vol_util × ro_acum(t0) / F`.
2. **Fórmula de EAR inicial a partir de `voli`:** o campo real é `vol_ini`; soma de `(vol_ini/100) × vol_util × ro_acum(t0) / F` por reservatório.
3. **Semântica de `voli`:** `Confhd.vol_ini`, `float`, porcentagem do volume útil, 0–100, F6.2.
4. **Volume usado:** somente volume útil acima de `VMIN`; não o volume total e não o volume morto.
5. **Produtibilidades reutilizáveis:** diretamente `ro_acum`; `ro_equiv` é sua parcela elementar. As demais atendem outros níveis/cotas.
6. **Melhor campo acumulado:** `ro_acum`, documentado no código como PDTARM.
7. **Incluir UHEs a jusante de outros REEs:** sim, quando fazem parte da cascata configurada, inclusive fio d'água.
8. **Efeito do acoplamento:** a fórmula total não muda; a PDTARM passa pela fronteira. A/B/C apenas decompõem a mesma produtividade.
9. **Evitar dupla contagem:** atribuir toda EAR/EARMÁX ao REE de origem do volume; nunca readicionar B/C ao destino como estoque.
10. **Soma das EAR dos REEs do sistema:** sim, diretamente, usando a associação do `REE.DAT`.
11. **Soma das EARMÁX:** sim, pelo mesmo princípio.
12. **Unidade:** `float64` em MWmês na API; percentual apenas como coluna derivada.
13. **FATOR inicial:** recomendação `2,63` para compatibilidade NEWAVE, centralizado e validado; a alternativa física é `0,0864 × dias` e não deve ser misturada silenciosamente.
14. **Primeiro mês:** primeiro ano do estudo e mês `DGER.mesi_est`, não `[0][0]` fixo.
15. **Cálculo já existente:** EARMÁX inteira já existe em `Ree._calc_earm_max`; EAR inicial e agregação pública ainda não.
16. **Divergências tese versus NEWAVE atual:** o núcleo EARM/PDTARM e A/B/C permanece compatível; evoluíram número de REEs, fontes da condição inicial e representações individualizadas/híbridas. Há diferença de convenção visível no fator mensal. A divergência B/C encontrada é do PySDDP, não da tese.
17. **Menor alteração futura:** testes de contrato, calculador puro que reutilize `ro_acum`, fachada em `Newave`, seleção de fonte e duas tabelas pandas. Sem nova travessia hidráulica e sem API mensal.
18. **Testes indispensáveis:** A–K, flag DGER, mês não janeiro, regressão EARMÁX existente, B/C, invariantes de soma, sistemas fictícios/inválidos e benchmark NEWAVE/NWLISTOP.

### 12.2 Sequência mais segura

1. Aprovar as nove decisões da seção 11.
2. Obter primeiro o benchmark oficial.
3. Escrever testes analíticos A–K para o escopo inicial aplicável.
4. Implementar o calculador `float64` reutilizando `ro_acum` e o fator aprovado.
5. Integrar fontes CONFHD/DGER e agregar pelo `REE.DAT`.
6. Comparar com NEWAVE/NWLISTOP e somente então estabilizar a API.
7. Corrigir e expor A/B/C em tarefa independente.
8. Tratar período arbitrário, FDIN e topologia especial apenas em evolução posterior.

### 12.3 Critério de encerramento desta auditoria

Esta auditoria termina neste documento. Nenhuma classe, método, teste, dependência, versão ou API foi alterada; nenhum commit, push ou publicação foi realizado. A implementação deve aguardar aprovação explícita em tarefa posterior.
