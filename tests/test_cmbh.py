import pandas as pd
from src.cmbh import CMBH

class DummyFolhasEfetivos:
    def total_mensal_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "competencia": ["01"], "valor_efetivos": [100]})
    def total_anual_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "total_efetivos": [1200]})

class DummyFolhasPIA:
    def total_mensal_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "competencia": ["01"], "valor_pia": [200]})
    def total_anual_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "total_pia": [2400]})


class TestCMBH:
    def test_exporta_totais_mensais_para(self, tmp_path):
        cmbh = CMBH(folhas_efetivos=DummyFolhasEfetivos, folhas_pia=DummyFolhasPIA)
        output_file = tmp_path / "totais_mensais.xlsx"
        cmbh.exporta_totais_mensais_para(2023, 2023, str(output_file))
        df = pd.read_excel(output_file, sheet_name="Totais Mensais")
        assert df.iloc[0]["valor_efetivos"] == 100
        assert df.iloc[0]["valor_pia"] == 200

    def test_exporta_totais_anuais_para(self, tmp_path):
        cmbh = CMBH(folhas_efetivos=DummyFolhasEfetivos, folhas_pia=DummyFolhasPIA)
        output_file = tmp_path / "totais_anuais.xlsx"
        cmbh.exporta_totais_anuais_para(2023, 2023, str(output_file))
        df = pd.read_excel(output_file, sheet_name="Totais Anuais")
        assert df.iloc[0]["total_efetivos"] == 1200
        assert df.iloc[0]["total_pia"] == 2400