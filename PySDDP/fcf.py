class fcf(object):
    nr_cortes = None
    coef_vf = None
    termo_i = None
    estagio = None

    def __init__(self, estagio):
        self.nr_cortes = 0
        self.coef_vf = []
        self.termo_i = []
        self.estagio = estagio

    def add_corte(self, coeficientes, constante, volume, nr_estagios):
        coeficientes = -(1/nr_estagios)*coeficientes
        for i in range(0,len(volume)):
            if coeficientes[i] > 0:
                coeficientes[i] = 0
        constante = constante/nr_estagios
        for i in range(0,len(volume)):
            constante = constante - volume[i]*coeficientes[i]
        self.coef_vf.append(coeficientes)
        self.termo_i.append(constante)
        self.nr_cortes = self.nr_cortes+1

    def get_fcf(self, vf, alpha):
        rest_cortes = []
        if self.nr_cortes == 0:
            return rest_cortes
        else:
            for icor in range(0,self.nr_cortes):
                funcao = self.termo_i[icor]
                for i in range(0,len(vf)):
                    funcao = funcao + self.coef_vf[icor][i]*vf[i]
                rest_cortes.append( alpha >= funcao)
            return rest_cortes
