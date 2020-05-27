import os
from PySDDP.PowerSystem import ImportaPmo, Classroom

if __name__ == '__main__':
    sistema = ImportaPmo(os.path.join(os.getcwd(), 'pmo/'))
    CasoEstudo = Classroom()
    print(CasoEstudo.sistema['DGer'])
    resultado_pddd = CasoEstudo.pdd(0, imprime=False)

