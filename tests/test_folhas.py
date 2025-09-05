import pandas as pd
from datetime import date
from src.folhas import Folhas


class DummyFolhas(Folhas):
    def total_por_competencia(self, competencia: date):
        return {"competencia": self.formata_data(competencia), "valor": 100}

    def total_anual(self, ano: int) -> pd.DataFrame:
        # Simula um DataFrame anual com 2 competências + extras
        dados = [
            {"competencia": self.formata_data(date(ano, 1, 1)), "valor": 100},
            {"competencia": self.formata_data(date(ano, 2, 1)), "valor": 200},
            {"competencia": self.formata_13o(ano), "valor": 300},
            {"competencia": self.formata_terco_ferias(ano), "valor": 400},
        ]
        return pd.DataFrame(dados)


def test_total_no_intervalo():
    folhas = DummyFolhas()
    df = folhas.total_no_intervalo(2020, 2021)
    # Deve ter 8 linhas (4 por ano)
    assert df.shape[0] == 8
    # Checa se as competências estão corretas
    expected = [
        "2020-01",
        "2020-02",
        "13o 2020",
        "1/3 férias 2020",
        "2021-01",
        "2021-02",
        "13o 2021",
        "1/3 férias 2021",
    ]
    assert list(df["competencia"]) == expected
    # Checa valores
    assert list(df["valor"]) == [100, 200, 300, 400, 100, 200, 300, 400]
