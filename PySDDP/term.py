class term(object):
    # Dados de cadastro das usinas termeletrica (presentes no TERM.DAT)
    Codigo = None
    Nome = None
    Potencia = None
    FCMax = None
    TEIF = None
    IP = None
    GTMin = None

    # Dados Adicionais Especificados no arquivo de configuracao termica (CONFT)
    Sist = None
    Status = None
    Classe = None

    # Dados Adicionais Especificados no arquivo de classe termica (CLAST)
    Custo = None
    NomeClasse = None
    TipoComb = None

    def insere(self, custo, gmax):
        self.custo = custo
        self.gmax = gmax
