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
        if competencia.day != 1:
            competencia = competencia.replace(day=1)
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

    def total_anual(self, ano: int) -> pd.DataFrame:
        """Gera um DataFrame com os totais dos PIAs em um ano."""

        def append_gasto(ano, competencia_label, gasto: int):
            dados.append(
                {
                    "ano": ano,
                    "competencia": competencia_label,
                    "total_pia": gasto,
                }
            )

        periodos = self.gerar_periodos(date(ano, 1, 1), date(ano, 12, 1))

        dados = []
        for competencia in periodos:
            total = self.total_por_competencia(competencia)
            append_gasto(ano, Folhas.formata_data(competencia), total)

        # 13o e férias são zero para PIA
        append_gasto(ano, Folhas.formata_13o(ano), 0.0)
        append_gasto(ano, Folhas.formata_terco_ferias(ano), 0.0)

        return pd.DataFrame(dados)

    def exporta_pia_do_funcionario(
        self, cm: int, inicio: date, fim: date
    ) -> pd.DataFrame:
        """Exporta o PIA de um funcionário específico para um DataFrame."""
        dados = []
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.pias and cm in self.pias[competencia]:
                valor_pia = self.pias[competencia][cm]
                dados.append(
                    {"Competência": Folhas.formata_data(competencia), "PIA": valor_pia}
                )
            else:
                # Folha em branco para meses sem dados
                dados.append(
                    {
                        "Competência": Folhas.formata_data(competencia),
                        "PIA": 0.0,
                    }
                )

        return pd.DataFrame(dados)
