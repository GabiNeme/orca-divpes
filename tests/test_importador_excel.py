from datetime import date
import pytest
from src.carreira import CarreiraConcurso2004
from src.classe import Classe
from src.cmbh import CMBH, ImportadorProjecaoExcel
from src.funcionario import TipoPrevidencia
from src.nivel import Nivel


def dummy_obtem_tempos_licencas():
    return {1: 30, 2: 731}


@pytest.fixture
def cmbh_fixture() -> CMBH:
    # Setup code: create an ImportadorProjecaoExcel instance
    return ImportadorProjecaoExcel(
        funcao_obtem_tempos_licencas=dummy_obtem_tempos_licencas
    ).importa("tests/exemplo_projecao_atual.xlsx")


class TestImportadorProjecaoExcel:

    def test_funcionario_e2(self, cmbh_fixture: CMBH):
        assert cmbh_fixture is not None

        funcionario = cmbh_fixture.funcionarios.get(2)
        assert funcionario.data_admissao == date(2018, 7, 13)

        # DadosFolha
        assert funcionario.dados_folha.classe == Classe.E2
        assert funcionario.dados_folha.data_anuenio == date(2018, 7, 13)
        assert funcionario.dados_folha.num_ats == 0
        assert not funcionario.dados_folha.procurador
        assert funcionario.dados_folha.tipo_previdencia == TipoPrevidencia.BHPrev

        # Aposentadoria
        assert funcionario.aposentadoria.data_aposentadoria == date(2049, 3, 31)
        assert funcionario.aposentadoria.num_art_98_data_aposentadoria == 393
        assert funcionario.aposentadoria.aderiu_pia

    def test_progressao_funcionario_com_licenca(self, cmbh_fixture: CMBH):

        ultima_progressao = cmbh_fixture.funcionarios.get(2).progressoes[-1]
        # Ultima progressao (primeira da carreira nova)
        assert ultima_progressao.data == date(2020, 7, 13)
        assert ultima_progressao.nivel == Nivel(1, "A")
        assert ultima_progressao.progs_sem_especial == 0

    def test_funcionario_e3_procurador(self, cmbh_fixture: CMBH):
        funcionario = cmbh_fixture.funcionarios.get(4)
        assert funcionario.dados_folha.classe == Classe.E3
        assert funcionario.dados_folha.data_anuenio == date(2006, 2, 23)
        assert funcionario.dados_folha.num_ats == 0
        assert funcionario.dados_folha.procurador

    def test_progressao_funcionario_procurador(self, cmbh_fixture: CMBH):
        funcionario = cmbh_fixture.funcionarios.get(4)
        ultima_progressao = funcionario.progressoes[-1]
        assert ultima_progressao.data == date(2006, 2, 23)
        assert ultima_progressao.nivel == Nivel(10, "A")
        assert ultima_progressao.progs_sem_especial == 0

    def test_numero_ats(self, cmbh_fixture: CMBH):
        funcionario = cmbh_fixture.funcionarios.get(1)
        assert funcionario.dados_folha.num_ats == 2

    def test_tipo_carreira(self, cmbh_fixture: CMBH):
        funcionario = cmbh_fixture.funcionarios.get(1)
        assert isinstance(funcionario.carreira, CarreiraConcurso2004)

    def test_nao_aderiu_pia(self, cmbh_fixture: CMBH):
        funcionario = cmbh_fixture.funcionarios.get(1)
        assert not funcionario.aposentadoria.aderiu_pia

    def test_folha(self, cmbh_fixture: CMBH):
        competencia = date(2025, 11, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas[competencia][1]

        assert folha.nivel == Nivel(36, "C")
        assert folha.salario == 27751.45
        assert folha.ats == 555.03
        assert folha.anuenio == 1670.06
        assert folha.total_antes_limite_prefeito == 29976.54
        assert folha.total == 29976.54
        assert folha.fufin_patronal == 6594.84
        assert folha.bhprev_patronal == 0.0
        assert folha.bhprev_complementar_patronal == 0.0

    def test_limite_ao_teto(self, cmbh_fixture: CMBH):
        competencia = date(2027, 1, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas.get(competencia, {}).get(4)

        assert folha.total_antes_limite_prefeito == 56480.83
        assert folha.total == 41845.49

    def test_bhprev(self, cmbh_fixture: CMBH):
        competencia = date(2028, 7, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas.get(competencia, {}).get(2)

        assert folha.bhprev_patronal == 2378.94

    def test_bhprev_complementar(self, cmbh_fixture: CMBH):
        competencia = date(2041, 12, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas.get(competencia, {}).get(3)

        assert folha.bhprev_patronal == 1794.63
        assert folha.bhprev_complementar_patronal == 72.62

    def test_folha_vazia_antes_admissao(self, cmbh_fixture: CMBH):
        competencia = date(2026, 2, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas.get(competencia, {}).get(3)

        assert folha is None

    def test_folha_vazia_apos_aposentadoria(self, cmbh_fixture: CMBH):
        competencia = date(2050, 1, 1)
        folha = cmbh_fixture.folhas_efetivos.folhas.get(competencia, {}).get(1)

        assert folha is None

    def test_existencia_pia(self, cmbh_fixture: CMBH):
        competencia = date(2049, 3, 1)
        pia = cmbh_fixture.folhas_pia.pias[competencia][2]

        assert pia == 446457.03

    def test_nao_existencia_pia(self, cmbh_fixture: CMBH):
        competencia = date(2049, 2, 1)
        total_pia = cmbh_fixture.folhas_pia.total_por_competencia(competencia)

        assert total_pia == 0

    def test_folhas_vazias_se_importa_folhas_falso(self):
        cmbh = ImportadorProjecaoExcel().importa(
            "tests/exemplo_projecao_atual.xlsx", importa_folhas=False
        )

        assert not cmbh.folhas_efetivos.folhas
        assert not cmbh.folhas_pia.pias
