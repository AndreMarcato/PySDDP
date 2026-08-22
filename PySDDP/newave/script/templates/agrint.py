from abc import abstractmethod

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class AgrintTemplate(ArquivoEntrada):
    """Estrutura comum ao arquivo de agrupamentos livres de interligacoes."""

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_patamares = None
        self.numero_registros_composicao = 0
        self.numero_registros_limites = 0

        self.bloco_composicao = {
            "df": None,
            "descricao": "Interligacoes e coeficientes de cada agrupamento",
            "cabecalho": [],
        }
        self.bloco_limites = {
            "df": None,
            "descricao": "Vigencias e limites por patamar dos agrupamentos",
            "cabecalho": [],
        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """Le o arquivo de agrupamentos livres de interligacoes."""

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """Mantem o contrato de ``ArquivoEntrada``."""
