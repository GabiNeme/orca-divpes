from datetime import date

import pandas as pd

from src.folha import Folha
from src.folhas_efetivos import FolhasEfetivos, GastoMensalEfetivos
from src.nivel import Nivel
from src.tabela_salario import Tabela


class DummyFolha(Folha):
    def __init__(
        self,
        total=100,
        fufin_patronal=10,
        bhprev_patronal=5,
        bhprev_complementar_patronal=2,
    ):
        self.nivel = Nivel(1, "A")
        self.salario = 1000
        self.total = total
        self.fufin_patronal = fufin_patronal
        self.bhprev_patronal = bhprev_patronal
        self.bhprev_complementar_patronal = bhprev_complementar_patronal


class DummyFuncionario:
    def __init__(self, cm, niveis):
        self.cm = cm
        self.niveis = niveis
        self.dados_folha = None

    def obtem_nivel_para(self, competencia):
        return self.niveis.get(competencia, None)


class DummyCalculaFolha:
    def __init__(self, tabela):
        pass

    def calcula(self, nivel, competencia):
        return DummyFolha()


class TestFolhasEfetivos:

    def test_calcula_folhas_e_total_por_competencia(self):
        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        inicio = date(2024, 1, 1)
        fim = date(2024, 1, 1)
        competencia = inicio

        funcionario1 = DummyFuncionario("001", {competencia: "nivel1"})
        funcionario2 = DummyFuncionario("002", {competencia: "nivel2"})
        funcionarios = [funcionario1, funcionario2]

        folhas.calcula_folhas(funcionarios, inicio, fim)

        # Verifica se as folhas foram calculadas corretamente
        assert competencia in folhas.folhas
        assert "001" in folhas.folhas[competencia]
        assert "002" in folhas.folhas[competencia]

        # Verifica o total por competencia
        gasto = folhas.total_por_competencia(competencia)
        assert isinstance(gasto, GastoMensalEfetivos)
        assert gasto.total_efetivos == 200
        assert gasto.fufin_patronal == 20
        assert gasto.bhprev_patronal == 10
        assert gasto.bhprev_complementar_patronal == 4

    def test_total_por_competencia_sem_folhas(self):
        tabela = Tabela()
        folhas = FolhasEfetivos(tabela, DummyCalculaFolha)
        competencia = date(2024, 1, 1)
        gasto = folhas.total_por_competencia(competencia)
        assert isinstance(gasto, GastoMensalEfetivos)
        assert gasto.total_efetivos == 0
        assert gasto.fufin_patronal == 0
        assert gasto.bhprev_patronal == 0
        assert gasto.bhprev_complementar_patronal == 0

    def test_total_anual(self):
        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        ano = 2024
        inicio = date(ano, 1, 1)
        fim = date(ano, 12, 1)
        competencias = folhas.gerar_periodos(inicio, fim)

        funcionario1 = DummyFuncionario("001", {c: "nivel1" for c in competencias})
        funcionario2 = DummyFuncionario("002", {c: "nivel2" for c in competencias})
        funcionarios = [funcionario1, funcionario2]

        folhas.calcula_folhas(funcionarios, inicio, fim)
        df = folhas.total_anual(ano)

        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {
            "ano",
            "competencia",
            "Total Efetivos",
            "Fufin Patronal",
            "BHPrev Patronal",
            "BHPrev Complementar Patronal",
        }
        # Deve ter 12 meses + 13o + 1/3 férias = 14 linhas
        assert df.shape[0] == 14
        assert all(df["ano"] == ano)
        # Os 12 primeiros são meses, depois "13o 2024" e "1/3 férias 2024"
        for i in range(12):
            assert df.iloc[i]["Total Efetivos"] == 200
            assert df.iloc[i]["Fufin Patronal"] == 20
            assert df.iloc[i]["BHPrev Patronal"] == 10
            assert df.iloc[i]["BHPrev Complementar Patronal"] == 4
        # 13o salário igual ao mês de dezembro
        assert df.iloc[12]["competencia"] == "2024-13o"
        assert df.iloc[12]["Total Efetivos"] == 200
        assert df.iloc[12]["Fufin Patronal"] == 20
        assert df.iloc[12]["BHPrev Patronal"] == 10
        assert df.iloc[12]["BHPrev Complementar Patronal"] == 4
        # 1/3 férias igual a 1/3 do mês de dezembro
        assert df.iloc[13]["competencia"] == "2024-férias"
        assert df.iloc[13]["Total Efetivos"] == round(200 / 3, 2)
        assert df.iloc[13]["Fufin Patronal"] == round(20 / 3, 2)
        assert df.iloc[13]["BHPrev Patronal"] == round(10 / 3, 2)
        assert df.iloc[13]["BHPrev Complementar Patronal"] == round(4 / 3, 2)

    def test_total_anual_sem_folhas(self):
        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        ano = 2024
        df = folhas.total_anual(ano)
        assert isinstance(df, pd.DataFrame)
        # Deve ter 14 linhas (12 meses + 13o + 1/3 férias)
        assert df.shape[0] == 14
        assert all(df["Total Efetivos"] == 0)
        assert all(df["Fufin Patronal"] == 0)
        assert all(df["BHPrev Patronal"] == 0)
        assert all(df["BHPrev Complementar Patronal"] == 0)

    def test_exporta_folhas_do_funcionario(self):

        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        competencia1 = date(2024, 1, 1)
        competencia2 = date(2024, 2, 1)
        cm = "001"
        # Adiciona folhas manualmente
        folhas.adiciona_folha(
            competencia1, cm, Folha(nivel=Nivel(1, "A"), salario=1000, total=100)
        )
        folhas.adiciona_folha(
            competencia2, cm, Folha(nivel=Nivel(3, "B"), salario=200, total=300)
        )
        # Exporta para DataFrame
        df = folhas.exporta_folhas_do_funcionario(cm, competencia1, competencia2)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 2
        assert df.iloc[0]["Competência"] == "2024-01"
        assert df.iloc[0]["Nível"] == "1.A"
        assert df.iloc[0]["Salário"] == 1000
        assert df.iloc[0]["Total"] == 100
        assert df.iloc[1]["Competência"] == "2024-02"
        assert df.iloc[1]["Nível"] == "3.B"
        assert df.iloc[1]["Salário"] == 200
        assert df.iloc[1]["Total"] == 300

    def test_exporta_folhas_do_funcionario_com_meses_sem_folha(self):

        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        competencia1 = date(2024, 1, 1)
        competencia2 = date(2024, 3, 1)
        cm = "001"
        df = folhas.exporta_folhas_do_funcionario(cm, competencia1, competencia2)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 3
        assert df.iloc[2]["Competência"] == "2024-03"
        assert df.iloc[2]["Total"] == 0

    def test_calcula_metricas(self):
        folhas = FolhasEfetivos(Tabela(), DummyCalculaFolha)
        inicio = date(2024, 1, 1)
        fim = date(2024, 3, 1)
        competencias = folhas.gerar_periodos(inicio, fim)

        funcionario1 = DummyFuncionario("001", {c: "nivel1" for c in competencias})
        funcionario2 = DummyFuncionario("002", {c: "nivel2" for c in competencias})
        funcionarios = [funcionario1, funcionario2]

        folhas.calcula_folhas(funcionarios, inicio, fim)
        df = folhas.calcula_metricas(inicio, fim)

        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {
            "CM",
            "Nível inicial",
            "Salário Inicial",
            "Valor Inicial lim. teto",
            "Valor Final lim. teto",
            "Média",
            "VPL (0,5%)",
            "Soma Total",
        }
        # Deve ter uma linha para cada funcionário
        assert df.shape[0] == 2
        # Checa valores esperados para DummyFolha (total sempre 100)
        for _, row in df.iterrows():
            assert row["Nível inicial"] == Nivel(1, "A")
            assert row["Salário Inicial"] == 1000
            assert row["Valor Inicial lim. teto"] == 100
            assert row["Valor Final lim. teto"] == 100
            assert row["Média"] == 100
            assert round(row["VPL (0,5%)"], 2) == round(
                100 / (1 + 0.005) ** 0
                + 100 / (1 + 0.005) ** 1
                + 100 / (1 + 0.005) ** 2,
                2,
            )
            assert row["Soma Total"] == 300
