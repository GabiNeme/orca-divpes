from datetime import date

import pandas as pd
from src.folhas import Folhas
from src.funcionario import Aposentadoria
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

    def test_competencia_mantida_se_dia_diferente_de_1(self):
        competencia = date(2030, 1, 15)  # dia diferente de 1
        funcionario = DummyFuncionario(
            cm=1, data_aposentadoria=competencia, valor_pia=1000
        )
        folhas_pia = FolhasPIA(calcula_pia=DummyCalculaPIA)
        folhas_pia.calcula_pias([funcionario])
        # A competência deve ser armazenada como o primeiro dia do mês
        assert date(2030, 1, 1) in folhas_pia.pias
        assert folhas_pia.pias[date(2030, 1, 1)][1] == 1000


    def test_total_anual(self):
        ano = 2030
        competencia1 = date(ano, 12, 1)
        competencia2 = date(ano, 2, 1)
        competencia3 = date(ano, 3, 1)

        funcionario1 = DummyFuncionario(
            cm=1, data_aposentadoria=competencia1, valor_pia=1000
        )
        funcionario2 = DummyFuncionario(
            cm=2, data_aposentadoria=competencia2, valor_pia=2000
        )
        funcionario3 = DummyFuncionario(
            cm=3, data_aposentadoria=competencia3, valor_pia=3000
        )
        funcionarios = [funcionario1, funcionario2, funcionario3]

        folhas_pia = FolhasPIA(calcula_pia=DummyCalculaPIA)
        folhas_pia.calcula_pias(funcionarios)

        df = folhas_pia.total_anual(ano)

        # Deve ter 12 meses + 13o + 1/3 férias = 14 linhas
        assert df.shape[0] == 14
        assert set(df.columns) == {"ano", "competencia", "total_pia"}
        assert all(df["ano"] == ano)

        expected = {
            Folhas.formata_data(competencia1): 1000,
            Folhas.formata_data(competencia2): 2000,
            Folhas.formata_data(competencia3): 3000,
            Folhas.formata_13o(ano): 0,
            Folhas.formata_terco_ferias(ano): 0,
        }
        for mes in range(1, 13):
            competencia_str = Folhas.formata_data(date(ano, mes, 1))
            if competencia_str not in expected:
                expected[competencia_str] = 0

        for competencia_str, valor_esperado in expected.items():
            assert (
                df.loc[df["competencia"] == competencia_str, "total_pia"].iloc[0]
                == valor_esperado
            )

    def test_total_anual_sem_pias(self):
        folhas_pia = FolhasPIA()
        df = folhas_pia.total_anual(2030)
        # Deve ter 12 meses + 13o + 1/3 férias = 14 linhas
        assert df.shape[0] == 14
        assert all(df["total_pia"] == 0)

    def test_exporta_pia_do_funcionario(self):
        ano = 2030
        competencia1 = date(ano, 1, 1)
        competencia2 = date(ano, 2, 1)
        competencia3 = date(ano, 3, 1)
        funcionario = DummyFuncionario(cm=1, data_aposentadoria=competencia1, valor_pia=1000)

        folhas_pia = FolhasPIA(calcula_pia=DummyCalculaPIA)
        folhas_pia.calcula_pias([funcionario])

        # Exporta de janeiro a março
        df = folhas_pia.exporta_pia_do_funcionario(1, competencia1, competencia3)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Competência", "PIA"]
        # Deve ter 3 linhas (jan, fev, mar)
        assert df.shape[0] == 3
        # Janeiro tem valor, os outros meses são zero
        assert df.loc[df["Competência"] == Folhas.formata_data(competencia1), "PIA"].iloc[0] == 1000
        assert df.loc[df["Competência"] == Folhas.formata_data(competencia2), "PIA"].iloc[0] == 0.0
        assert df.loc[df["Competência"] == Folhas.formata_data(competencia3), "PIA"].iloc[0] == 0.0

    def test_exporta_pia_do_funcionario_sem_pia(self):
        ano = 2030
        competencia1 = date(ano, 1, 1)
        competencia2 = date(ano, 2, 1)
        folhas_pia = FolhasPIA()
        # Exporta para funcionário sem PIA
        df = folhas_pia.exporta_pia_do_funcionario(99, competencia1, competencia2)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Competência", "PIA"]
        assert df.shape[0] == 2
        assert df["PIA"].sum() == 0
