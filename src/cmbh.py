from src.folhas_efetivos import FolhasEfetivos
import pandas as pd

from src.folhas_pia import FolhasPIA
from src.importador_excel import ImportadorProjecaoExcel


class CMBH:

    def __init__(self, folhas_efetivos=FolhasEfetivos, folhas_pia=FolhasPIA):
        """Inicializa a classe CMBH."""
        self.funcionarios = {}  # {cm: Funcionario}
        self.folhas_efetivos = folhas_efetivos()
        self.folhas_pia = folhas_pia()

    @classmethod
    def from_excel(cls, caminho_excel: str, importa_folhas: bool = True) -> "CMBH":
        """Cria uma instância de CMBH a partir de um arquivo Excel."""

        return ImportadorProjecaoExcel().importa(
            caminho_excel, importa_folhas=importa_folhas
        )

    def exporta_totais_mensais_para(
        self, ano_inicio: int, ano_fim: int, caminho_excel: str
    ) -> None:
        """Exporta os totais das folhas para uma única planilha do Excel, juntando por competência."""
        df_efetivos = self.folhas_efetivos.total_mensal_no_intervalo(
            ano_inicio, ano_fim
        )
        df_pia = self.folhas_pia.total_mensal_no_intervalo(ano_inicio, ano_fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on=["ano", "competencia"], how="outer")

        with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
            df_total.to_excel(writer, sheet_name="Totais Mensais", index=False)

    def exporta_totais_anuais_para(
        self, ano_inicio: int, ano_fim: int, caminho_excel: str
    ) -> None:
        """Exporta os totais anuais das folhas para uma única planilha do Excel, juntando por ano."""
        df_efetivos = self.folhas_efetivos.total_anual_no_intervalo(ano_inicio, ano_fim)
        df_pia = self.folhas_pia.total_anual_no_intervalo(ano_inicio, ano_fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on=["ano"], how="outer")

        with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
            df_total.to_excel(writer, sheet_name="Totais Anuais", index=False)
