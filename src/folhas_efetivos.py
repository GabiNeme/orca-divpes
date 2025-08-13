from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta
from src.folha import CalculaFolha, Folha
from src.funcionario import Funcionario
from src.tabela_salario import Tabela

@dataclass
class GastoMensalEfetivos:
    total_efetivos: float
    fufin_patronal: float
    bhprev_patronal: float
    bhprev_complementar_patronal: float

class FolhasEfetivos:
    def __init__(self, tabela: Tabela = Tabela, calcula_folha: CalculaFolha = CalculaFolha):
        """Inicializa a classe as folhas."""
        self.folhas = {}  # {competencia: {cm: Folha}}
        self.tabela = tabela
        self.calcula_folha = calcula_folha

    def adiciona_folha(self, competencia: date, cm: int, folha: Folha):
        """Adiciona uma folha de pagamento para um funcionário em uma competência específica."""
        if competencia not in self.folhas:
            self.folhas[competencia] = {}
        self.folhas[competencia][cm] = folha

    def _calcula_folhas_funcionario(
        self, funcionario: Funcionario, inicio: date, fim: date
    ) -> Folha | None:
        """Calcula a folha de pagamento para um funcionário específico."""
        cm = funcionario.cm
        calculadora_folha = self.calcula_folha(funcionario.dados_folha, self.tabela)

        for competencia in self._gerar_periodos(inicio, fim):
            nivel = funcionario.obtem_nivel_para(competencia)
            if not nivel: # Funcionário não admitido ou exonerado
                continue
            folha = calculadora_folha.calcula(nivel, competencia)
            self.adiciona_folha(competencia, cm, folha)

    def _gerar_periodos(self, inicio: date, fim: date) -> list[date]:
        """Gera períodos mensais entre duas datas."""
        periodos = [inicio]
        while inicio <= fim:
            inicio += relativedelta(months=1)
            periodos.append(inicio)
        return periodos

    def calcula_folhas(self, funcionarios: list[Funcionario], inicio: date, fim: date):
        """Calcula as folhas de pagamento para uma lista de funcionários."""
        for funcionario in funcionarios:
            self._calcula_folhas_funcionario(funcionario, inicio, fim)

    def total_por_competencia(self, competencia: date) -> GastoMensalEfetivos:
        """Calcula o total das folhas de pagamento para uma competência específica."""
        gasto = GastoMensalEfetivos(
            total_efetivos=0.0,
            fufin_patronal=0.0,
            bhprev_patronal=0.0,
            bhprev_complementar_patronal=0.0,
        )
        if competencia not in self.folhas:
            return gasto

        for _, folha in self.folhas[competencia].items():
            gasto.total_efetivos += folha.total
            gasto.fufin_patronal += folha.fufin_patronal
            gasto.bhprev_patronal += folha.bhprev_patronal
            gasto.bhprev_complementar_patronal += folha.bhprev_complementar_patronal
        
        return gasto
