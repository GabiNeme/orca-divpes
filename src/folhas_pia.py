import pandas as pd
from datetime import date

from src.folhas import Folhas
from src.funcionario import Funcionario
from src.pia import CalculaPIA
from src.tabela_salario import Tabela


class FolhasPIA(Folhas):
    """Representa as folhas do PIA de todos os funcionários."""

    def __init__(self, tabela: Tabela = Tabela, calcula_pia: CalculaPIA = CalculaPIA):
        """Inicializa a classe as folhas."""
        self.pias = {}  # {competencia: {cm: valor}}
        self.tabela = tabela
        self.calcula_pia = calcula_pia

    def adiciona_pia(self, competencia: date, cm: int, pia: float | None):
        """Adiciona um PIA para um funcionário em uma competência específica."""
        if pia is None:
            return
        if competencia not in self.pias:
            self.pias[competencia] = {}
        self.pias[competencia][cm] = pia

    def _calcula_pia_funcionario(self, funcionario: Funcionario) -> float | None:
        """Calcula o PIA para um funcionário específico."""
        cm = funcionario.cm
        calculadora_pia = self.calcula_pia(funcionario, self.tabela)

        self.adiciona_pia(
            funcionario.aposentadoria.data_aposentadoria,
            cm,
            calculadora_pia.calcula(),
        )

    def calcula_pias(self, funcionarios: list[Funcionario]):
        """Calcula os PIAs para uma lista de funcionários."""
        for funcionario in funcionarios:
            self._calcula_pia_funcionario(funcionario)

    def total_por_competencia(self, competencia: date) -> float:
        """Calcula o total dos PIAs para uma competência específica."""
        if competencia not in self.pias:
            return 0.0

        return sum(self.pias[competencia].values())

    def total_no_intervalo_para_dataframe(
        self, inicio: date, fim: date
    ) -> pd.DataFrame:
        """Gera um DataFrame com os totais dos PIAs entre duas competências."""
        periodos = self._gerar_periodos(inicio, fim)

        dados = []
        for competencia in periodos:
            total = self.total_por_competencia(competencia)
            dados.append(
                {
                    "competencia": competencia,
                    "total_pia": total,
                }
            )

        return pd.DataFrame(dados)
