import os
from PySDDP.PowerSystem import ImportaPmo, Classroom

if __name__ == '__main__':
    sistema = ImportaPmo(os.path.join(os.getcwd(), 'pmo/'))
    CasoEstudo = Classroom()
    CasoEstudo.sistema["DGer"]["Carga"] = [ 50, 60, 70 ]
    print(CasoEstudo.sistema['DGer'])
    resultado = CasoEstudo.pddd(0, imprime=False)
    print(resultado["DGer"]["CustoTotal"])



