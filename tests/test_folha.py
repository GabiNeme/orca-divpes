from datetime import date
from src.classe import Classe
from src.funcionario import TipoPrevidencia
from src.nivel import Nivel
from src.folha import *
from src.tabela_salario import Tabela


class MockTabela(Tabela):
    def valor_do_nivel_para_classe(self, nivel: Nivel, classe: Classe) -> float:
        if nivel == Nivel(1, "0") and classe == Classe.E2:
            return 1000
        if nivel == Nivel(25, "B") and classe == Classe.E2:
            return 2000
        if nivel == Nivel(30, "C") and classe == Classe.E2:
            return LIMITE_PREFEITO
        if nivel == Nivel(36, "D") and classe == Classe.E3:
            return LIMITE_PROCURADORES
        return 0.0


class TestCalculoFolha:

    def test_nivel(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(25, "B")
        assert calculadora.calcula(nivel, date(2023, 10, 1)).nivel == nivel

    def test_salario(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(25, "B")  # Valor: 2.000
        assert calculadora.calcula(nivel, date(2023, 10, 1)).salario == 2000

    def test_calcula_anuenio(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        competencia = date(2008, 2, 1)  # 8 anos. Nível(1, "0") é 1000
        assert calculadora.calcula(Nivel(1, "0"), competencia).anuenio == 80

    def test_calcula_ats(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=3,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(25, "B")  # Valor: 2.000
        assert calculadora.calcula(nivel, date(2023, 10, 1)).ats == 60

    def test_calcula_total_antes_limite_prefeito(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=3,  # R$ 60 de ats
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(25, "B")  # Valor: 2.000
        competencia = date(2008, 2, 1)  # 8 anos = 80 reais de anuênio
        assert (
            calculadora.calcula(nivel, competencia).total_antes_limite_prefeito == 2140
        )

    def test_calcula_total_quando_nao_atinge_teto(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(25, "B")  # Valor: 2.000
        competencia = date(2008, 2, 1)  # 8 anos = 80 reais de anuênio
        assert calculadora.calcula(nivel, competencia).total == 2080

    def test_total_respeita_limite_do_prefeito(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(30, "C")  # Valor: LIMITE_PREFEITO
        competencia = date(
            2008, 2, 1
        )  # 8 anos = 80 reais de anuênio -> passa do limite
        assert calculadora.calcula(nivel, competencia).total == LIMITE_PREFEITO

    def test_total_respeita_limite_do_procurador(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E3,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=True,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(36, "D")  # Valor: LIMITE_PROCURADORES
        competencia = date(
            2008, 2, 1
        )  # 8 anos = 80 reais de anuênio -> passa do limite
        assert calculadora.calcula(nivel, competencia).total == LIMITE_PROCURADORES

    def test_fufin_eh_zero_se_bh_prev(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        assert calculadora.calcula(Nivel(1, "0"), date(2023, 10, 1)).fufin_patronal == 0

    def test_fufin_eh_zero_se_bh_prev_complementar(self):
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
        )
        assert calculadora.calcula(Nivel(1, "0"), date(2023, 10, 1)).fufin_patronal == 0

    def test_fufin(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.Fufin,
            ),
        )
        nivel = Nivel(1, "0")  # Valor: 1.000
        assert (
            calculadora.calcula(nivel, competencia).fufin_patronal
            == 1000 * FATOR_PATRONAL
        )

    def test_bhprev_patronal_passa_teto_inss_se_bhprev(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(30, "C")  # Valor: LIMITE_PREFEITO
        assert calculadora.calcula(nivel, competencia).bhprev_patronal == round(
            LIMITE_PREFEITO * FATOR_PATRONAL, 2
        )

    def test_bhprev_patronal_limitado_ao_inss_se_bhprev_complementar(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
        )
        nivel = Nivel(30, "C")  # Valor: LIMITE_PREFEITO
        assert calculadora.calcula(nivel, competencia).bhprev_patronal == round(
            TETO_INSS * FATOR_PATRONAL, 2
        )

    def test_bhprev_complementar_zerada_se_fufin(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.Fufin,
            ),
        )
        nivel = Nivel(1, "0")  # Valor: 1.000
        assert calculadora.calcula(nivel, competencia).bhprev_patronal == 0

    def test_bhprev_complementar_zerada_se_bhprev(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
        )
        nivel = Nivel(1, "0")  # Valor: 1.000
        assert calculadora.calcula(nivel, competencia).bhprev_complementar_patronal == 0

    def test_bhprev_complementar_zerada_se_nao_atinge_teto_inss(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
        )
        nivel = Nivel(1, "0")  # Valor: 1.000
        assert calculadora.calcula(nivel, competencia).bhprev_complementar_patronal == 0

    def test_bhprev_complementar_somente_acima_teto_inss(self):
        competencia = date(2023, 10, 1)
        calculadora = CalculaFolha(
            tabela=MockTabela(),
            funcionario=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
        )
        nivel = Nivel(30, "C")  # Valor: LIMITE_PREFEITO
        assert calculadora.calcula(
            nivel, competencia
        ).bhprev_complementar_patronal == round(
            (LIMITE_PREFEITO - TETO_INSS) * FATOR_PATRONAL_COMPLEMENTAR, 2
        )
