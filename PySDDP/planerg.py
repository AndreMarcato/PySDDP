import os
from PySDDP.PowerSystem import ImportaPmo, Classroom
import plotly.graph_objects as go

if __name__ == '__main__':
    sistema = ImportaPmo(os.path.join(os.getcwd(), 'pmo/'))
    CasoEstudo = Classroom()
    CasoEstudo.sistema[ "UHE"][0]["Afl"] += CasoEstudo.sistema[ "UHE"][0]["Afl"] + CasoEstudo.sistema[ "UHE"][0]["Afl"]
    CasoEstudo.sistema["DGer"]["Carga"] += CasoEstudo.sistema["DGer"]["Carga"] + CasoEstudo.sistema["DGer"]["Carga"]
    CasoEstudo.sistema["DGer"]["Nr_Est"] = 9
    #CasoEstudo.plot_tree(0,9,2,"/Users/andremarcato/Downloads/arvore")

    CasoEstudo.sistema["UHE"][0]["Afl"] = [[25, 20, 23],
                                           [30, 22, 27],
                                           [29, 18, 24],
                                           [27, 20, 23],
                                           [22, 14, 18],
                                           [18, 13, 15],
                                           [18, 12, 15],
                                           [15, 9, 12],
                                           [12, 8, 10],
                                           [14, 12, 13],
                                           [19, 17, 16],
                                           [22, 18, 20]]

    CasoEstudo.sistema["DGer"]["Nr_Est"] = 7
    CasoEstudo.sistema["DGer"]["Nr_Cen"] = 2
    CasoEstudo.sistema["DGer"]["Carga"] = [ 50., 60, 45,
                                            50., 60, 45,
                                            50., 60, 45,
                                            50., 60, 45 ]

    CasoEstudo.plot_tree(0,4,2,"/Users/andremarcato/Downloads/arvore")


    [ res_plu, fob_plu ] = CasoEstudo.pl_unico_est(0,imprime=False)
    print(round(fob_plu,2))

    [ res_pddd, fob_pddd, zinf, zsup ] = CasoEstudo.pddd_est(0, imprime=False)
    print(round(fob_pddd,2))
    print(zinf)
    print(zsup)

    print(res_pddd[0])
    print(res_plu[0])


# ver downloads no PyPi
# https://pypistats.org/packages/pysddp

