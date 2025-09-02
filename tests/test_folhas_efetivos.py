from datetime import date
from src.folhas_efetivos import FolhasEfetivos, GastoMensalEfetivos
from src.tabela_salario import Tabela


class DummyFolha:
    def __init__(
        self,
        total=100,
        fufin_patronal=10,
        bhprev_patronal=5,
        bhprev_complementar_patronal=2,
    ):
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
    def __init__(self, dados_folha, tabela):
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
