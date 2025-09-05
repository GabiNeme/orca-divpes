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
        return f"13o {ano}"

    @staticmethod
    def formata_terco_ferias(ano: int) -> str:
        """Formata a competência do 1/3 de férias."""
        return f"1/3 férias {ano}"

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
