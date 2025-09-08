from datetime import date
from src.folhas_efetivos import FolhasEfetivos
import pandas as pd

from src.folhas_pia import FolhasPIA
from src.importador_excel import ImportadorProjecaoExcel


class CMBH:

    def __init__(self):
        """Inicializa a classe CMBH."""
        self.funcionarios = {}  # {cm: Funcionario}
        self.folhas_efetivos = FolhasEfetivos()
        self.folhas_pia = FolhasPIA()

    @classmethod
    def from_excel(cls, caminho_excel: str, importa_folhas: bool = True) -> "CMBH":
        """Cria uma instância de CMBH a partir de um arquivo Excel."""

        return ImportadorProjecaoExcel().importa(
            caminho_excel, importa_folhas=importa_folhas
        )

    def exporta_totais_para(self, inicio: date, fim: date, caminho_excel: str) -> None:
        """Exporta os totais das folhas para uma única planilha do Excel, juntando por competência."""
        df_efetivos = self.folhas_efetivos.total_anual(inicio, fim)
        df_pia = self.folhas_pia.total_anual(inicio, fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on="competencia", how="outer")

        with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
            df_total.to_excel(writer, sheet_name="Totais", index=False)
