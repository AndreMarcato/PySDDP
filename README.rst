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
