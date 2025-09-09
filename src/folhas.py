from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd


class Folhas(ABC):
    def __init__(self) -> None:
        return

    @staticmethod
    def formata_data(dt: date) -> str:
        """Formata a competência como 'YYYY-MM'."""
        return dt.strftime("%Y-%m")

    @staticmethod
    def formata_13o(ano: int) -> str:
        """Formata a competência do 13º salário."""
        return f"{ano}-13o"

    @staticmethod
    def formata_terco_ferias(ano: int) -> str:
        """Formata a competência do 1/3 de férias."""
        return f"{ano}-férias"

    @staticmethod
    def gerar_periodos(inicio: date, fim: date) -> list[date]:
        """Gera períodos mensais entre duas datas, incluindo apenas até 'fim'."""
        periodos = []
        atual = inicio
        while atual <= fim:
            periodos.append(atual)
            atual += relativedelta(months=1)
        return periodos

    @abstractmethod
    def total_por_competencia(self, competencia: date):
        """Calcula o total gasto em uma determinada competência."""
        return NotImplementedError

    @abstractmethod
    def total_anual(self, ano: int) -> pd.DataFrame:
        """Gera um DataFrame com os totais de um ano."""
        return NotImplementedError

    def total_mensal_no_intervalo(self, ano_inicio: int, ano_fim: int) -> pd.DataFrame:
        """Calcula o total mensal gasto em um intervalo de anos."""

        df_total = pd.DataFrame()
        for ano in range(ano_inicio, ano_fim + 1):
            df_ano = self.total_anual(ano)
            if ano == ano_inicio:
                df_total = df_ano
            else:
                df_total = pd.concat([df_total, df_ano], ignore_index=True)
        return df_total

    def total_anual_no_intervalo(self, ano_inicio: int, ano_fim: int) -> pd.DataFrame:
        """Calcula o total anual gasto em um intervalo de anos, agrupando por ano."""

        df_total = self.total_mensal_no_intervalo(ano_inicio, ano_fim)
        # Faz o group by pelo ano e soma as colunas numéricas, ignorando 'competencia'
        df_grouped = (
            df_total.drop(columns=["competencia"])
            .groupby("ano", as_index=True)
            .sum(numeric_only=True)
        )
        return df_grouped
