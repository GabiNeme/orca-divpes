from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta


class Folhas(ABC):
    def __init__(self) -> None:
        return

    def _gerar_periodos(self, inicio: date, fim: date) -> list[date]:
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
    def total_no_intervalo_para_dataframe(self, inicio: date, fim: date):
        """Gera um DataFrame com os totais entre duas competências."""
        return NotImplementedError
