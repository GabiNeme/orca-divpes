import pandas as pd
from src.cmbh import CMBH


class DummyFolhasEfetivos:
    def total_mensal_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame(
            {"ano": [2023], "competencia": ["01"], "valor_efetivos": [100]}
        )

    def total_anual_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "total_efetivos": [1200]})

    def exporta_folhas_do_funcionario(self, cm, inicio, fim):
        # Simula um DataFrame de folhas para o funcionário
        return pd.DataFrame(
            {"Competência": ["2023-01", "2023-02"], "Salário": [1000, 1100]}
        )


class DummyFolhasPIA:
    def total_mensal_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "competencia": ["01"], "valor_pia": [200]})

    def total_anual_no_intervalo(self, ano_inicio, ano_fim):
        return pd.DataFrame({"ano": [2023], "total_pia": [2400]})

    def exporta_pia_do_funcionario(self, cm, inicio, fim):
        # Simula um DataFrame de PIA para o funcionário
        return pd.DataFrame({"Competência": ["2023-01", "2023-02"], "PIA": [200, 0]})


class DummyFuncionario:
    def __init__(self, cm, nome):
        self.cm = cm
        self.nome = nome

    def to_dict(self):
        return {"cm": self.cm, "nome": self.nome}


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

    def test_exporta_folhas_servidores_efetivos_para(self, tmp_path):
        cmbh = CMBH(folhas_efetivos=DummyFolhasEfetivos, folhas_pia=DummyFolhasPIA)
        # Adiciona dois funcionários fictícios
        cmbh.funcionarios = {
            1: DummyFuncionario(1, "Alice"),
            2: DummyFuncionario(2, "Bob"),
        }
        output_file = tmp_path / "folhas_servidores.xlsx"
        cmbh.exporta_folhas_servidores_efetivos_para(2023, 2023, str(output_file))

        # Verifica se as abas dos funcionários existem e os dados estão corretos
        xls = pd.ExcelFile(output_file)
        assert "1" in xls.sheet_names
        assert "2" in xls.sheet_names

        df1 = pd.read_excel(output_file, sheet_name="1")
        df2 = pd.read_excel(output_file, sheet_name="2")

        # Verifica dados do funcionário 1
        assert list(df1["Competência"]) == ["2023-01", "2023-02"]
        assert list(df1["Salário"]) == [1000, 1100]
        assert list(df1["PIA"]) == [200, 0]

        # Verifica dados do funcionário 2
        assert list(df2["Competência"]) == ["2023-01", "2023-02"]
        assert list(df2["Salário"]) == [1000, 1100]
        assert list(df2["PIA"]) == [200, 0]

    def test_exporta_servidores_para(self, tmp_path):
        cmbh = CMBH()
        # Adiciona dois funcionários fictícios
        cmbh.funcionarios = {
            1: DummyFuncionario(1, "Alice"),
            2: DummyFuncionario(2, "Bob"),
        }
        output_file = tmp_path / "servidores.xlsx"
        cmbh.exporta_servidores_para(str(output_file))

        # Verifica se os dados exportados estão corretos
        df = pd.read_excel(output_file, sheet_name="Efetivos")
        assert set(df.columns) == {"cm", "nome"}
        assert set(df["cm"]) == {1, 2}
        assert set(df["nome"]) == {"Alice", "Bob"}
