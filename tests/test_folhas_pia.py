import pytest
from datetime import date
from src.classe import Classe
from src.funcionario import Aposentadoria, DadosFolha
from src.folhas_pia import FolhasPIA


class DummyFuncionario:
    def __init__(self, cm, data_aposentadoria, valor_pia):
        self.cm = cm
        self.aposentadoria = Aposentadoria(
            data_aposentadoria=data_aposentadoria,
            num_art_98_data_aposentadoria=0,  # não é usado
            aderiu_pia=True,
        )
        self.valor_pia = valor_pia


class DummyCalculaPIA:
    def __init__(self, funcionario, tabela):
        self.valor_pia = funcionario.valor_pia

    def calcula(self):
        return self.valor_pia


class TestFolhasPIA:

    def test_calcula_pias_e_total_por_competencia(self):
        competencia = date(2030, 1, 1)
        funcionario1 = DummyFuncionario(
            cm=1, data_aposentadoria=competencia, valor_pia=1000
        )
        funcionario2 = DummyFuncionario(
            cm=2, data_aposentadoria=competencia, valor_pia=2000
        )
        funcionario3 = DummyFuncionario(
            cm=3, data_aposentadoria=competencia, valor_pia=None
        )
        funcionarios = [funcionario1, funcionario2, funcionario3]

        folhas_pia = FolhasPIA(tabela=None, calcula_pia=DummyCalculaPIA)
        folhas_pia.calcula_pias(funcionarios)

        assert folhas_pia.total_por_competencia(competencia) == 3000

    def test_total_por_competencia_sem_pias(self):
        competencia = date(2030, 1, 1)
        folhas_pia = FolhasPIA()
        total = folhas_pia.total_por_competencia(competencia)
        assert total == 0.0
