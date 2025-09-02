from src.funcionario import Funcionario
from src.tabela_salario import Tabela


class CalculaPIA:
    def __init__(self, funcionario: Funcionario, tabela: Tabela):
        self.funcionario = funcionario
        self.tabela = tabela

    def calcula(self) -> float | None:
        """Calcula o valor do PIA para o funcionário, se aplicável."""
        if not self.funcionario.aposentadoria.aderiu_pia:
            return None

        dias_pia = self.funcionario.aposentadoria.num_art_98_data_aposentadoria
        nivel_aposentadoria = self.funcionario.obtem_nivel_para(
            self.funcionario.aposentadoria.data_aposentadoria
        )
        if not nivel_aposentadoria:
            return None

        valor_do_nivel = self.tabela.valor_do_nivel_para_classe(
            nivel=nivel_aposentadoria, classe=self.funcionario.dados_folha.classe
        )

        return dias_pia * valor_do_nivel / 30
