import pytest
from datetime import date
from src.pia import CalculaPIA
from src.funcionario import Funcionario, DadosFolha, Aposentadoria, TipoPrevidencia
from src.nivel import Nivel
from src.classe import Classe


class MockTabela:
    def valor_do_nivel_para_classe(self, nivel, classe):
        return 30000


@pytest.fixture
def funcionario_fixture():
    def _make_funcionario(aderiu_pia=True, dias_pia=250, nivel=Nivel(1, "A")):
        dados_folha = DadosFolha(
            classe=Classe.E2,
            data_anuenio=date(2000, 1, 1),
            num_ats=0,
            procurador=False,
            tipo_previdencia=TipoPrevidencia.BHPrev,
        )
        aposentadoria = Aposentadoria(
            data_aposentadoria=date(2030, 1, 1),
            num_art_98_data_aposentadoria=dias_pia,
            aderiu_pia=aderiu_pia,
        )

        class DummyFuncionario(Funcionario):
            def __init__(self):
                self.dados_folha = dados_folha
                self.aposentadoria = aposentadoria

            def obtem_nivel_para(self, data):
                return nivel if data == aposentadoria.data_aposentadoria else None

        return DummyFuncionario()

    return _make_funcionario


class TestCalculaPIA:
    def test_pia_calcula_valor(self, funcionario_fixture):
        funcionario = funcionario_fixture(
            aderiu_pia=True, dias_pia=250, nivel=Nivel(1, "A")
        )
        tabela = MockTabela()
        pia = CalculaPIA(funcionario, tabela).calcula()
        assert pia is not None
        assert pia == 250000.00


    def test_pia_nao_aderiu(self, funcionario_fixture):
        funcionario = funcionario_fixture(aderiu_pia=False)
        tabela = MockTabela()
        pia = CalculaPIA(funcionario, tabela).calcula()
        assert pia is None


    def test_pia_nivel_none(self, funcionario_fixture):
        funcionario = funcionario_fixture(aderiu_pia=True)
        tabela = MockTabela()
        funcionario.obtem_nivel_para = lambda data: None
        pia = CalculaPIA(funcionario, tabela).calcula()
        assert pia is None
