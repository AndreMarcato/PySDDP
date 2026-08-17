# Energia armazenada em REEs e submercados

## API pública

A classe `PySDDP.Pen.Newave` expõe:

```python
resultado = newave.calcular_energia_armazenada_inicial()
```

O retorno contém:

- `por_ree`: `pandas.DataFrame` com EARMÁX, EAR inicial CONFHD, EAR inicial DGER e seus percentuais;
- `por_submercado`: `pandas.DataFrame` com as energias agregadas, a lista dinâmica de REEs e a identificação de sistema fictício;
- `metadados`: unidade, fator de conversão, período inicial, flag informativa e diagnósticos da fonte DGER.

Os cálculos e retornos energéticos usam `float64` e a unidade `MWmes`.

## Convenção de conversão

A constante `PySDDP.newave.energia_armazenada.FATOR_NEWAVE_MWMES` vale exatamente `2.63`. Ela converte o produto do volume útil em hm³ pela produtividade em MW/(m³/s) para a convenção NEWAVE de MWmês. O fator é fixo para todos os meses e não depende do calendário civil.

## EARMÁX

Para cada reservatório `u` disponível no primeiro período e pertencente ao REE `r`:

```text
EARMX_u = vol_util_u * ro_acum_u(t0) / 2.63
EARMX_r = soma(EARMX_u)
```

`ro_acum` é a PDTARM previamente calculada por `Confhd`: inclui a produtividade equivalente da própria UHE e das UHEs disponíveis e motorizadas a jusante. A API reutiliza esse campo e não percorre novamente a topologia hidráulica. UHE fio d'água tem `vol_util == 0` e não cria armazenamento próprio, embora sua produtividade possa compor `ro_acum` de um reservatório a montante.

## EAR inicial derivada do CONFHD

`CONFHD.vol_ini` é o percentual do volume útil, não do volume total. Para cada reservatório:

```text
EAR_CONFHD_u = (vol_ini_u / 100) * vol_util_u * ro_acum_u(t0) / 2.63
EAR_CONFHD_r = soma(EAR_CONFHD_u)
percentual_CONFHD_r = 100 * EAR_CONFHD_r / EARMX_r
```

O cálculo é individual por reservatório; não usa a média aritmética dos percentuais e não adiciona `VMIN`. Valores de `vol_ini` não numéricos, não finitos ou fora de `[0, 100]` são rejeitados.

## EAR inicial derivada do DGER

Os valores de `DGER.vol_earm_inic` são associados posicionalmente aos REEs na ordem do `REE.DAT`:

```text
EAR_DGER_r = (percentual_DGER_r / 100) * EARMX_r
```

As fontes CONFHD e DGER são calculadas em paralelo. `DGER.flag_earm_inic` é apenas retornada nos metadados; ela não seleciona nem elimina uma fonte nesta API.

Se o registro DGER estiver ausente ou sua quantidade não coincidir com a quantidade de REEs, a EAR CONFHD continua disponível, as colunas DGER recebem `NaN` e `metadados["diagnosticos"]` descreve a inconsistência. Quando a quantidade é coerente, cada percentual DGER deve ser numérico, finito e pertencer a `[0, 100]`.

## Primeiro período

A condição inicial usa:

```text
índice de ano = 0
índice de mês = DGER.mesi_est - 1
```

O ano e o mês civis são retornados nos metadados. A API não calcula EAR para períodos arbitrários, não aplica FDIN e não recompõe armazenamento após mudanças de configuração.

## Agregação por submercado

A associação normativa é `Ree.bloco_ree["df"]["submercado"]`, lida do `REE.DAT`. Para cada submercado:

```text
EARMX_s = soma(EARMX_r)
EAR_CONFHD_s = soma(EAR_CONFHD_r)
EAR_DGER_s = soma(EAR_DGER_r)
```

Os percentuais são razões das energias agregadas, nunca médias dos percentuais dos REEs. Quando EARMÁX é zero, o percentual é `NaN`. Sistemas sem REEs também são retornados, e `ficticio` reflete `Sistema.tipo == 1`. Uma associação REE→submercado inexistente gera erro explícito.

## Parcelas de acoplamento A/B/C

`Confhd._prod_acum` adota a convenção metodológica NEWAVE:

- A: produtividade no REE ou sistema da origem;
- B: produtividade controlável a jusante, começando no primeiro reservatório depois da fronteira e incluindo as UHEs posteriores;
- C: produtividade das UHEs fio d'água consecutivas depois da fronteira e antes do primeiro reservatório de jusante.

As parcelas satisfazem, dentro da precisão numérica:

```text
ro_acum = A_REE + B_REE + C_REE
ro_acum = A_SIST + B_SIST + C_SIST
```

A correção troca a classificação histórica invertida de B/C, sem modificar `ro_acum` total, EARMÁX ou EAR. Os campos decompõem o valor da água armazenada na origem; suas parcelas não devem ser adicionadas novamente ao estoque do REE ou submercado de destino.
