import os
from PySDDP.PowerSystem import ImportaPmo, Classroom
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':
    sistema = ImportaPmo(os.path.join(os.getcwd(), 'pmo/'))
    CasoEstudo = Classroom()
    CasoEstudo.sistema[ "UHE"][0]["Afl"] += CasoEstudo.sistema[ "UHE"][0]["Afl"] + CasoEstudo.sistema[ "UHE"][0]["Afl"]
    CasoEstudo.sistema["DGer"]["Carga"] += CasoEstudo.sistema["DGer"]["Carga"] + CasoEstudo.sistema["DGer"]["Carga"]
    CasoEstudo.sistema["DGer"]["Nr_Est"] = 9
    #CasoEstudo.plot_tree(0,9,2,"/Users/andremarcato/Downloads/arvore")

    CasoEstudo.sistema["UHE"][0]["Afl"] = [[25, 20, 23, 28, 21, 24],
                                           [30, 22, 27, 32, 20, 26],
                                           [29, 18, 24, 30, 26, 28],
                                           [27, 20, 23, 26, 22, 24],
                                           [22, 14, 18, 25, 20, 23],
                                           [18, 13, 15, 20, 16, 18],
                                           [18, 12, 15, 19, 18, 20],
                                           [15, 9, 12, 13, 10, 11],
                                           [12, 8, 10, 14, 11, 13],
                                           [14, 12, 13, 11, 10, 16],
                                           [19, 17, 16, 25, 20, 22],
                                           [22, 18, 20, 24, 22, 23]]

    CasoEstudo.sistema["DGer"]["Nr_Est"] = 12
    CasoEstudo.sistema["DGer"]["Nr_Cen"] = 6
    CasoEstudo.sistema["DGer"]["Carga"] = [ 50., 50, 50,
                                            50., 50, 50,
                                            50., 50, 50,
                                            50., 50, 50 ]

    [ ZINF, ZSUP, LINF, LSUP, cortes] = CasoEstudo.pdde(6, 3, 5, imprime = False)

    x_axis = np.arange(1, len(ZINF)+1)
    plt.plot(x_axis, ZINF, 'c-')
    plt.plot(x_axis, ZSUP, 'r-', lw=3)
    plt.plot(x_axis, LINF, 'r-.', lw=2)
    plt.plot(x_axis, LSUP, 'r-.', lw=2)
    titulo = 'Convergência da PDDE'
    plt.title(titulo, fontsize=16)
    plt.xlabel('Iteração', fontsize=16)
    plt.ylabel('Custo ($)', fontsize=16)
    plt.show()

    CasoEstudo.despacho_pdde([40], [23], cortes, 2, imprime=True)

    # Exemplos de plots das árvores de decisão

    #CasoEstudo.plot_tree(0,4,2,"/Users/andremarcato/Downloads/arvore")
    # caminhos = [ 3, 7, 12, 15]
    #CasoEstudo.plot_tree_pdde(4,2, [ 3, 7, 12, 15], "/Users/andremarcato/Downloads/arvore")
    #CasoEstudo.plot_tree_pdde(6,3, [], "/Users/andremarcato/Downloads/arvore")
    #CasoEstudo.plot_pente_pdde(6, 6, 3, 4,"/Users/andremarcato/Downloads/arvore_pdde")

    #[ res_plu, fob_plu ] = CasoEstudo.pl_unico_tree(0,imprime=False)
    #print(round(fob_plu,2))

    #[ res_pddd, fob_pddd, zinf, zsup ] = CasoEstudo.pddd_tree(0, imprime=False)
    #print(round(fob_pddd,2))
    #print(zinf)
    #print(zsup)

    #print(res_pddd[0])
    #print(res_plu[0])


# ver downloads no PyPi
# https://pypistats.org/packages/pysddp

