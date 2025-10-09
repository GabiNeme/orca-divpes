from dataclasses import dataclass
from datetime import date

import config
from src.anuenio import Anuenio
from src.funcionario import DadosFolha, Funcionario, TipoPrevidencia
from src.nivel import Nivel
from src.tabela_salario import Tabela


@dataclass
class Folha:
    """Representa os dados de folha de pagamento de um funcionário."""

    nivel: Nivel = None
    salario: float = 0.0
    anuenio: float = 0.0
    ats: float = 0.0
    total_antes_limite_prefeito: float = 0.0
    total: float = 0.0
    fufin_patronal: float = 0.0
    bhprev_patronal: float = 0.0
    bhprev_complementar_patronal: float = 0.0

    def to_dict(self) -> dict:
        return {
            "Nível": str(self.nivel),
            "Salário": self.salario,
            "Anuênio": self.anuenio,
            "ATS": self.ats,
            "Total Antes Limite Prefeito": self.total_antes_limite_prefeito,
            "Total": self.total,
            "Fufin Patronal": self.fufin_patronal,
            "BHPrev Patronal": self.bhprev_patronal,
            "BHPrev Complementar Patronal": self.bhprev_complementar_patronal,
        }


class CalculaFolha:
    def __init__(self, tabela: Tabela):
        self.tabela = tabela

    def calcula(self, funcionario: Funcionario, competencia: date) -> Folha | None:
        nivel = funcionario.obtem_nivel_para(competencia)
        if not nivel:  # Funcionário não admitido ou exonerado
            return None
        dados_folha = funcionario.dados_folha
        return Folha(
            nivel=nivel,
            salario=self._calcula_salario(dados_folha, nivel, competencia),
            anuenio=self._calcula_anuenio(dados_folha, competencia),
            ats=self._calcula_ats(dados_folha, nivel, competencia),
            total_antes_limite_prefeito=self._calcula_total_antes_limite_prefeito(
                dados_folha, nivel, competencia
            ),
            total=self._calcula_total(dados_folha, nivel, competencia),
            fufin_patronal=self._calcula_fufin_patronal(dados_folha, nivel, competencia),
            bhprev_patronal=self._calcula_bhprev_patronal(dados_folha, nivel, competencia),
            bhprev_complementar_patronal=self._calcula_bhprev_complementar_patronal(
                dados_folha, nivel, competencia
            ),
        )

    def _calcula_salario(self, funcionario: DadosFolha, nivel: Nivel, competencia: date) -> float:
        """Calcula o salário base do funcionário."""

        return self.tabela.valor_do_nivel_para_classe(
            nivel=nivel, classe=funcionario.classe, competencia=competencia
        )

    def _calcula_anuenio(self, funcionario: DadosFolha, competencia: date) -> float:
        """Calcula o anuenio do funcionário."""

        anuenio = Anuenio(funcionario.data_anuenio)
        qtde_anuenios = anuenio.obtem_numero_anuenios_para(competencia)

        valor_por_anuenio = 0.01 * self.tabela.valor_do_nivel_para_classe(
            nivel=Nivel(1, "0"), classe=funcionario.classe, competencia=competencia
        )
        return round(valor_por_anuenio * qtde_anuenios, 2)

    def _calcula_ats(self, funcionario: DadosFolha, nivel: Nivel, competencia: date) -> float:
        """Calcula o ATS do funcionário."""

        salario = self._calcula_salario(funcionario, nivel, competencia)
        return round(funcionario.num_ats * salario * 0.01, 2)

    def _calcula_total_antes_limite_prefeito(
        self, funcionario: DadosFolha, nivel: Nivel, competencia: date
    ) -> float:
        """Calcula o total antes do limite preferencial."""
        salario = self._calcula_salario(funcionario, nivel, competencia)
        anuenio = self._calcula_anuenio(funcionario, competencia)
        ats = self._calcula_ats(funcionario, nivel, competencia)
        return round(salario + anuenio + ats, 2)

    def _calcula_total(
        self, funcionario: DadosFolha, nivel: Nivel, competencia: date
    ) -> float:
        """Calcula o total do funcionário."""
        if funcionario.procurador:
            limite = config.param.TETO_PROCURADORES
        else:
            limite = config.param.TETO_PREFEITO

        total_antes_limite_prefeito = self._calcula_total_antes_limite_prefeito(
            funcionario, nivel, competencia
        )
        if total_antes_limite_prefeito > limite:
            return limite
        return total_antes_limite_prefeito

    def _calcula_fufin_patronal(self, funcionario: DadosFolha, nivel: Nivel, competencia: date) -> float:
        """Calcula a previdência patronal do funcionário."""
        if funcionario.tipo_previdencia != TipoPrevidencia.Fufin:
            return 0
        return round(
            self._calcula_total(funcionario, nivel, competencia) * config.param.ALIQUOTA_PATRONAL,
            2,
        )

    def _calcula_bhprev_patronal(self, funcionario: DadosFolha, nivel: Nivel, competencia: date) -> float:
        """Calcula a previdência patronal do BHPrev do funcionário."""
        if funcionario.tipo_previdencia == TipoPrevidencia.Fufin:
            return 0
        elif funcionario.tipo_previdencia == TipoPrevidencia.BHPrev:
            return round(
                self._calcula_total(funcionario, nivel, competencia)
                * config.param.ALIQUOTA_PATRONAL,
                2,
            )
        elif funcionario.tipo_previdencia == TipoPrevidencia.BHPrevComplementar:
            total = self._calcula_total(funcionario, nivel, competencia)
            if total > config.param.TETO_INSS:
                return round(config.param.TETO_INSS * config.param.ALIQUOTA_PATRONAL, 2)
            return round(total * config.param.ALIQUOTA_PATRONAL, 2)

    def _calcula_bhprev_complementar_patronal(
        self, funcionario: DadosFolha, nivel: Nivel, competencia: date
    ) -> float:
        """Calcula a previdência patronal complementar do funcionário."""
        if funcionario.tipo_previdencia != TipoPrevidencia.BHPrevComplementar:
            return 0
        total = self._calcula_total(funcionario, nivel, competencia)
        if total <= config.param.TETO_INSS:
            return 0
        return round(
            (total - config.param.TETO_INSS)
            * config.param.ALIQUOTA_PATRONAL_COMPLEMENTAR,
            2,
        )
