PySDDP
###################
Python package applied to the planning of the operation of energy systems in the medium term horizon. This package also has classes applied to rain-to-flow

USAGE
###################

from PySDDP import sistema

EXAMPLE
###################

from PySDDP import sistema

q = sistema.PySDDP('pmo/')

Classroom
###################
from PySDDP import sistema

q = sistema.Classroom()

q.sistema["DGer"]["Nr_Disc"] = 41

resultado_pdd41 = q.pdd(0, imprime=False)

resultado_plu = q.pl_unico(0, imprime=False)

resultado_pddd = q.pddd(0, imprime=False)

DEPLOY SCRIPT
###################

Para publicar uma nova versão do pacote, você pode usar o script de deploy localizado em ``deploy.sh``.

No PowerShell, execute:

.. code-block:: powershell

   .\deploy.ps1 0.0.66 "Release 0.0.66"

O script:

- atualiza a versão em ``setup.py``;
- cria um commit;
- faz push para o repositório remoto;
- cria e envia a tag com o mesmo número da versão;
- dispara o fluxo de deploy no CircleCI.

Se você quiser que o script pergunte a versão, execute:

.. code-block:: powershell

   bash ./deploy.sh
