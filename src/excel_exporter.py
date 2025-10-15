import pandas as pd
from openpyxl.styles import Alignment, NamedStyle


class ExcelExporter:
    """Classe para exportar DataFrames para Excel com formatação personalizada."""

    def __init__(self):
        self._setup_number_style()

    def _setup_number_style(self):
        """Configura o estilo de formatação para números."""
        self.number_style = NamedStyle(name="number_format")
        self.number_style.number_format = "#,##0.00"

    def to_excel(
        self,
        df: pd.DataFrame,
        writer: pd.ExcelWriter,
        sheet_name: str,
        index: bool = False,
        **kwargs
    ) -> None:
        """
        Exporta DataFrame para Excel com formatação automática de números.

        Args:
            df: DataFrame a ser exportado
            writer: ExcelWriter do pandas
            sheet_name: Nome da planilha
            index: Se deve incluir o índice
            **kwargs: Argumentos adicionais para to_excel
        """
        # Primeiro, escreve o DataFrame normalmente
        df.to_excel(writer, sheet_name=sheet_name, index=index, **kwargs)

        # Depois aplica a formatação
        self._format_worksheet(writer, sheet_name, df, index, **kwargs)

    def _format_worksheet(
        self,
        writer: pd.ExcelWriter,
        sheet_name: str,
        df: pd.DataFrame,
        index: bool,
        **kwargs
    ) -> None:
        """Aplica formatação de números, quebra de linha automática e ajuste de colunas."""
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Adiciona o estilo ao workbook se não existir
        if "number_format" not in workbook.named_styles:
            workbook.add_named_style(self.number_style)

        # Determina a primeira coluna de dados
        start_col = 2 if index else 1
        start_row = 2  # Linha após o cabeçalho

        # Aplica formatação para números float
        for row_idx in range(len(df)):
            for col_idx, _ in enumerate(df.columns):
                cell = worksheet.cell(
                    row=start_row + row_idx, column=start_col + col_idx
                )

                # Verifica se o valor é um float
                if self._is_float_value(df.iloc[row_idx, col_idx]):
                    cell.style = "number_format"

        # Aplica wrap text na primeira linha (cabeçalhos)
        self._apply_header_wrap_text(worksheet, df, index)

        # Aplica auto-fit na altura das linhas
        self._enhance_first_row_height(worksheet)

        # Aplica auto-fit na largura das colunas
        self._auto_fit_columns_width(worksheet, df, index)

    def _apply_header_wrap_text(
        self,
        worksheet,
        df: pd.DataFrame,
        index: bool,
    ) -> None:
        """Aplica wrap text automático nos cabeçalhos."""
        header_row = 1
        start_col = 2 if index else 1

        # Aplica wrap text nos cabeçalhos das colunas
        for col_idx in range(len(df.columns)):
            cell = worksheet.cell(row=header_row, column=start_col + col_idx)
            cell.alignment = Alignment(
                wrap_text=True, vertical="center", horizontal="center"
            )

    def _enhance_first_row_height(self, worksheet) -> None:
        """Aplica auto-fit apenas na primeira linha."""

        worksheet.row_dimensions[1].height = 45

    def _auto_fit_columns_width(self, worksheet, df: pd.DataFrame, index: bool) -> None:
        """Aplica auto-fit na largura das colunas."""
        start_col = 2 if index else 1

        for col_idx, col in enumerate(df.columns):
            # Comprimento máximo dos dados
            max_data_length = df[col].astype(str).map(len).max()

            # Comprimento do cabeçalho com regra especial
            header_length = len(str(col))
            if header_length > 15:
                header_constraint = 15
            else:
                header_constraint = header_length

            # Largura final é o máximo entre dados e constraint do cabeçalho
            max_length = max(max_data_length, header_constraint)

            adjusted_width = (max_length + 2) * 1.1  # Ajuste para melhor visualização
            worksheet.column_dimensions[chr(64 + start_col + col_idx)].width = (
                adjusted_width
            )

    def _is_float_value(self, value) -> bool:
        """Verifica se um valor é um número float."""
        import numpy as np

        # Verifica se é None ou NaN
        if value is None or pd.isna(value):
            return False

        # Verifica se é um tipo float (exclui int, bool, etc.)
        return isinstance(value, (float, np.floating))


# Instância global para uso conveniente
exporter = ExcelExporter()


# Função de conveniência
def to_excel_formatted(
    df: pd.DataFrame,
    writer: pd.ExcelWriter,
    sheet_name: str,
    index: bool = False,
    **kwargs
) -> None:
    """
    Função de conveniência para exportar DataFrame com formatação.

    Args:
        df: DataFrame a ser exportado
        writer: ExcelWriter do pandas
        sheet_name: Nome da planilha
        index: Se deve incluir o índice
        **kwargs: Argumentos adicionais para to_excel
    """
    exporter.to_excel(df, writer, sheet_name, index, **kwargs)
