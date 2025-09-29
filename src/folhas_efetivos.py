import pandas as pd

from dataclasses import dataclass
from datetime import date
from src.folha import CalculaFolha, Folha
from src.folhas import Folhas
from src.funcionario import Funcionario
from src.tabela_salario import Tabela

TAXA_DESCONTO = 0.005  # 0,5% ao mês

@dataclass
class GastoMensalEfetivos:
    total_efetivos: float
    fufin_patronal: float
    bhprev_patronal: float
    bhprev_complementar_patronal: float


class FolhasEfetivos(Folhas):
    def __init__(
        self, tabela: Tabela = Tabela, calcula_folha: CalculaFolha = CalculaFolha
    ):
        """Inicializa a classe as folhas."""
        self.servidores = set()  # Conjunto para armazenar CMs únicos
        self.folhas = {}  # {competencia: {cm: Folha}}
        self.tabela = tabela
        self.calcula_folha = calcula_folha

    def adiciona_folha(self, competencia: date, cm: int, folha: Folha):
        """Adiciona uma folha de pagamento para um funcionário em uma competência específica."""
        self.servidores.add(cm)
        if competencia not in self.folhas:
            self.folhas[competencia] = {}
        self.folhas[competencia][cm] = folha

    def _calcula_folhas_funcionario(
        self, funcionario: Funcionario, inicio: date, fim: date
    ) -> Folha | None:
        """Calcula a folha de pagamento para um funcionário específico."""
        cm = funcionario.cm
        calculadora_folha = self.calcula_folha(funcionario.dados_folha, self.tabela)

        for competencia in self.gerar_periodos(inicio, fim):
            nivel = funcionario.obtem_nivel_para(competencia)
            if not nivel:  # Funcionário não admitido ou exonerado
                continue
            folha = calculadora_folha.calcula(nivel, competencia)
            self.adiciona_folha(competencia, cm, folha)

    def calcula_folhas(self, funcionarios: list[Funcionario], inicio: date, fim: date):
        """Calcula as folhas de pagamento para uma lista de funcionários."""
        for funcionario in funcionarios:
            self.servidores.add(funcionario.cm)
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

    def total_anual(self, ano: int) -> pd.DataFrame:
        """Gera um DataFrame com os totais de um ano, incluindo 13º e 1/3 férias."""

        def append_gasto(ano, competencia_label, gasto: GastoMensalEfetivos):
            dados.append(
                {
                    "ano": ano,
                    "competencia": competencia_label,
                    "Total Efetivos": gasto.total_efetivos,
                    "Fufin Patronal": gasto.fufin_patronal,
                    "BHPrev Patronal": gasto.bhprev_patronal,
                    "BHPrev Complementar Patronal": gasto.bhprev_complementar_patronal,
                }
            )

        periodos = self.gerar_periodos(date(ano, 1, 1), date(ano, 12, 1))
        dados = []
        for competencia in periodos:
            gasto = self.total_por_competencia(competencia)
            append_gasto(ano, Folhas.formata_data(competencia), gasto)

        # Adiciona o 13º salário
        append_gasto(ano, Folhas.formata_13o(ano), self._calcula_13o(ano))

        # Adiciona o 1/3 de férias
        append_gasto(
            ano, Folhas.formata_terco_ferias(ano), self._calcula_terco_ferias(ano)
        )

        df = pd.DataFrame(dados)
        return df

    def _calcula_13o(self, ano: int) -> GastoMensalEfetivos:
        """Calcula o total do 13º salário para o ano especificado - igual ao valor de dezembro."""

        competencia = date(ano, 12, 1)

        return self.total_por_competencia(competencia)

    def _calcula_terco_ferias(self, ano: int) -> GastoMensalEfetivos:
        """Calcula o total do 1/3 de férias para o ano especificado - 1/3 do valor de dezembro."""

        competencia = date(ano, 12, 1)
        tot_dez = self.total_por_competencia(competencia)

        return GastoMensalEfetivos(
            total_efetivos=round(tot_dez.total_efetivos / 3, 2),
            fufin_patronal=round(tot_dez.fufin_patronal / 3, 2),
            bhprev_patronal=round(tot_dez.bhprev_patronal / 3, 2),
            bhprev_complementar_patronal=round(
                tot_dez.bhprev_complementar_patronal / 3, 2
            ),
        )

    def exporta_folhas_do_funcionario(
        self, cm: int, inicio: date, fim: date
    ) -> pd.DataFrame:
        """Exporta as folhas de um funcionário específico para um dataframe."""
        dados = []
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                dados.append(
                    {"Competência": Folhas.formata_data(competencia), **folha.to_dict()}
                )
            else:
                # Folha em branco para meses sem dados
                dados.append(
                    {
                        "Competência": Folhas.formata_data(competencia),
                        **Folha().to_dict(),
                    }
                )

        return pd.DataFrame(dados)
    
    def calcula_metricas(self, inicio: date, fim: date) -> pd.DataFrame:
        """Calcula métricas adicionais para as folhas de pagamento no intervalo especificado."""
        # Exemplo de métrica: total anual por funcionário
        metricas = []
        for cm in sorted(self.servidores):
            dados = {
                "CM": cm,
                "Valor Inicial": self._calcula_valor_inicial(cm, inicio, fim),
                "Valor Final": self._calcula_valor_final(cm, inicio, fim),
                "Média": self._calcula_media(cm, inicio, fim),
                "VPL (0,5%)": self._calcula_vpl(cm, inicio, fim),
                "Soma Total": self._calcula_soma(cm, inicio, fim),
            }
            metricas.append(dados)
        return pd.DataFrame(metricas)

    def _calcula_valor_inicial(self, cm: int, inicio: date, fim: date) -> float:
        """Calcula o valor inicial para um funcionário na primeira competência que ele/a aparece."""
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                return folha.total
        return 0.0
    
    def _calcula_valor_final(self, cm: int, inicio: date, fim: date) -> float:
        """Calcula o valor final para um funcionário na última competência que ele/a aparece."""
        for competencia in reversed(list(self.gerar_periodos(inicio, fim))):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                return folha.total
        return 0.0

    def _calcula_media(self, cm: int, inicio: date, fim: date) -> float:
        """Calcula a média para um funcionário no intervalo especificado."""
        total = 0.0
        count = 0
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                total += folha.total
                count += 1
        return round(total / count, 2) if count > 0 else 0.0
    
    def _calcula_vpl(self, cm: int, inicio: date, fim: date) -> float:
        """Calcula o Valor Presente Líquido (VPL) para um funcionário no intervalo especificado."""
        vpl = 0.0
        meses = 0
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                vpl += folha.total / ((1 + TAXA_DESCONTO) ** meses)
            meses += 1
        return round(vpl, 2)

    def _calcula_soma(self, cm: int, inicio: date, fim: date) -> float:
        """Calcula a soma total para um funcionário no intervalo especificado."""
        total = 0.0
        for competencia in self.gerar_periodos(inicio, fim):
            if competencia in self.folhas and cm in self.folhas[competencia]:
                folha = self.folhas[competencia][cm]
                total += folha.total
        return total
