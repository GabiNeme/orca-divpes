from src.banco_de_dados import BancoDeDados


class ImportadorAeros:
    def __init__(self, banco_de_dados=BancoDeDados):
        """Inicializa o importador de projeção Excel."""
        self.banco_de_dados = banco_de_dados
        self.cmbh = None
        self._media_usufruto_art98_cmbh = None

    def importa(self):
        """Importa os dados de funcionários de um arquivo Excel."""
        return NotImplementedError


if __name__ == "__main__":
    importador = ImportadorAeros()
    importador.importa()
