from datetime import date
from src.funcionario import Aposentadoria
from src.folhas_pia import FolhasPIA
import pandas as pd


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

    def test_total_no_intervalo_para_dataframe(self):
        inicio = date(2030, 1, 1)
        fim = date(2030, 4, 1)
        competencia1 = inicio
        competencia2 = date(2030, 2, 1)
        competencia3 = date(2030, 3, 1)

        funcionario1 = DummyFuncionario(cm=1, data_aposentadoria=competencia1, valor_pia=1000)
        funcionario2 = DummyFuncionario(cm=2, data_aposentadoria=competencia2, valor_pia=2000)
        funcionario3 = DummyFuncionario(cm=3, data_aposentadoria=competencia3, valor_pia=3000)
        funcionarios = [funcionario1, funcionario2, funcionario3]

        folhas_pia = FolhasPIA(calcula_pia=DummyCalculaPIA)
        folhas_pia.calcula_pias(funcionarios)

        df = folhas_pia.total_no_intervalo_para_dataframe(inicio, fim)
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {"competencia", "total_pia"}
        expected = {
            competencia1: 1000,
            competencia2: 2000,
            competencia3: 3000,
            fim: 0,
        }
        for _, row in df.iterrows():
            assert row["total_pia"] == expected[row["competencia"]]

    def test_total_no_intervalo_para_dataframe_sem_pias(self):
        inicio = date(2030, 1, 1)
        fim = date(2030, 1, 1)
        folhas_pia = FolhasPIA()
        df = folhas_pia.total_no_intervalo_para_dataframe(inicio, fim)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 1
        assert all(df["total_pia"] == 0)
