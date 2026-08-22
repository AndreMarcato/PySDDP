from abc import abstractmethod

from PySDDP.newave.script.templates.arquivo_entrada import ArquivoEntrada


class PatamarTemplate(ArquivoEntrada):
    """Estrutura comum ao arquivo de patamares de mercado do NEWAVE."""

    def __init__(self):
        super().__init__()

        self.dir_base = None
        self.nome_arquivo = None
        self.numero_patamares = None
        self.tipo = None
        self.tem_bloco_5 = False
        self.finalizacao_bloco_4_por_eof = False

        self.bloco_numero_patamares = {
            "valor": None,
            "descricao": "Numero de patamares de mercado",
            "cabecalho": [],
        }
        self.bloco_duracao = {
            "df": None,
            "descricao": "Duracao mensal dos patamares de mercado",
            "cabecalho": [],
        }
        self.bloco_mercado = {
            "df": None,
            "descricao": "Fatores de mercado por submercado e patamar",
            "cabecalho": [],
        }
        self.bloco_intercambio = {
            "df": None,
            "descricao": "Fatores de intercambio por interligacao e patamar",
            "cabecalho": [],
        }
        self.bloco_nao_simuladas = {
            "df": None,
            "descricao": "Fatores de geracao nao simulada por bloco e patamar",
            "cabecalho": [],
        }

    @abstractmethod
    def ler(self, *args, **kwargs) -> None:
        """Le o arquivo de patamares de mercado."""

    @abstractmethod
    def escrever(self, *args, **kwargs) -> None:
        """Mantem o contrato de ``ArquivoEntrada``."""
