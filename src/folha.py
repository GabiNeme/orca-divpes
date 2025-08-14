from datetime import date

from dataclasses import dataclass
from src.anuenio import Anuenio
from src.funcionario import DadosFolha, TipoPrevidencia
from src.nivel import Nivel
from src.tabela_salario import Tabela

LIMITE_PREFEITO = 34604.05
LIMITE_PROCURADORES = 41845.49

FATOR_PATRONAL = 0.22
FATOR_PATRONAL_COMPLEMENTAR = 0.085
TETO_INSS = 8157.41


@dataclass
class Folha:
    """Representa os dados de folha de pagamento de um funcionário."""
    nivel: Nivel
    salario: float
    anuenio: float
    ats: float
    total_antes_limite_prefeito: float
    total: float
    fufin_patronal: float
    bhprev_patronal: float
    bhprev_complementar_patronal: float


class CalculaFolha:
    def __init__(self, funcionario: DadosFolha, tabela: Tabela):
        self.funcionario = funcionario
        self.tabela = tabela

    def _calcula_salario(self, nivel: Nivel) -> float:
        """Calcula o salário base do funcionário."""

        return self.tabela.valor_do_nivel_para_classe(
            nivel=nivel, classe=self.funcionario.classe
        )

    def _calcula_anuenio(self, competencia: date) -> float:
        """Calcula o anuenio do funcionário."""

        anuenio = Anuenio(self.funcionario.data_anuenio)
        qtde_anuenios = anuenio.obtem_numero_anuenios_para(competencia)

        valor_por_anuenio = 0.01 * self.tabela.valor_do_nivel_para_classe(
            nivel=Nivel(1, "0"), classe=self.funcionario.classe
        )
        return round(valor_por_anuenio * qtde_anuenios, 2)

    def _calcula_ats(self, nivel: Nivel) -> float:
        """Calcula o ATS do funcionário."""

        salario = self._calcula_salario(nivel)
        return round(self.funcionario.num_ats * salario * 0.01, 2)

    def _calcula_total_antes_limite_prefeito(
        self, nivel: Nivel, competencia: date
    ) -> float:
        """Calcula o total antes do limite preferencial."""
        salario = self._calcula_salario(nivel)
        anuenio = self._calcula_anuenio(competencia)
        ats = self._calcula_ats(nivel)
        return round(salario + anuenio + ats, 2)

    def _calcula_total(self, nivel: Nivel, competencia: date) -> float:
        """Calcula o total do funcionário."""
        if self.funcionario.procurador:
            limite = LIMITE_PROCURADORES
        else:
            limite = LIMITE_PREFEITO

        total_antes_limite_prefeito = self._calcula_total_antes_limite_prefeito(
            nivel, competencia
        )
        if total_antes_limite_prefeito > limite:
            return limite
        return total_antes_limite_prefeito

    def _calcula_fufin_patronal(self, nivel: Nivel, competencia: date) -> float:
        """Calcula a previdência patronal do funcionário."""
        if self.funcionario.tipo_previdencia != TipoPrevidencia.Fufin:
            return 0
        return round(self._calcula_total(nivel, competencia) * FATOR_PATRONAL, 2)

    def _calcula_bhprev_patronal(self, nivel: Nivel, competencia: date) -> float:
        """Calcula a previdência patronal do BHPrev do funcionário."""
        if self.funcionario.tipo_previdencia == TipoPrevidencia.Fufin:
            return 0
        elif self.funcionario.tipo_previdencia == TipoPrevidencia.BHPrev:
            return round(self._calcula_total(nivel, competencia) * FATOR_PATRONAL, 2)
        elif self.funcionario.tipo_previdencia == TipoPrevidencia.BHPrevComplementar:
            total = self._calcula_total(nivel, competencia)
            if total > TETO_INSS:
                return round(TETO_INSS * FATOR_PATRONAL, 2)
            return round(total * FATOR_PATRONAL, 2)

    def _calcula_bhprev_complementar_patronal(
        self, nivel: Nivel, competencia: date
    ) -> float:
        """Calcula a previdência patronal complementar do funcionário."""
        if self.funcionario.tipo_previdencia != TipoPrevidencia.BHPrevComplementar:
            return 0
        total = self._calcula_total(nivel, competencia)
        if total <= TETO_INSS:
            return 0
        return round((total - TETO_INSS) * FATOR_PATRONAL_COMPLEMENTAR, 2)

    def calcula(self, nivel: Nivel, competencia: date) -> Folha:
        return Folha(
            nivel=nivel,
            salario=self._calcula_salario(nivel),
            anuenio=self._calcula_anuenio(competencia),
            ats=self._calcula_ats(nivel),
            total_antes_limite_prefeito=self._calcula_total_antes_limite_prefeito(
                nivel, competencia
            ),
            total=self._calcula_total(nivel, competencia),
            fufin_patronal=self._calcula_fufin_patronal(nivel, competencia),
            bhprev_patronal=self._calcula_bhprev_patronal(nivel, competencia),
            bhprev_complementar_patronal=self._calcula_bhprev_complementar_patronal(
                nivel, competencia
            ),
        )
