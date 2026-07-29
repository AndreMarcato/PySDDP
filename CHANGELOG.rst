Changelog
#########

0.0.74 (não publicado)
=======================

* Corrige a simetria entre ``Confhd.get()`` e ``Confhd.put()``.
* Persiste ``ree``, ``vol_ini``, ``status``, ``modif``, ``ano_i`` e
  ``ano_f``, além dos campos comuns do registro CONFHD.
* Valida identidade, larguras fixas, tipos, domínio de ``status`` e séries de
  vazões antes de modificar as estruturas internas.
* Passa a devolver cópias dos arrays públicos e mantém a associação das
  vazões por posto, inclusive quando o posto é compartilhado.
* Adiciona testes de caracterização, round-trip de ``CONFHD.DAT`` e
  ``VAZOES.DAT`` e regressão da API existente.

Não há alteração das assinaturas públicas de ``get()``, ``put()`` ou
``escrever()``. A chave de metadado ``codigo_original`` foi acrescentada ao
dicionário completo para proteger a identidade durante uma edição.
