from datetime import date

import config
from src.classe import Classe
from src.folha import CalculaFolha, DadosFolha
from src.funcionario import Funcionario, TipoPrevidencia
from src.nivel import Nivel
from src.tabela_salario import Tabela

# Definindo parâmetros para os testes
config.param.VALOR_BASE_E2 = 5758.83
config.param.VALOR_BASE_E3 = 10047.80
config.param.TETO_PREFEITO = 34604.05
config.param.TETO_PROCURADORES = 41845.49
config.param.TETO_INSS = 8157.41

p = config.param


class DummyFuncionario(Funcionario):
    def __init__(self, dados_folha: DadosFolha, nivel: Nivel = None):
        self.dados_folha = dados_folha
        self.nivel = nivel

    def obtem_nivel_para(self, competencia: date) -> Nivel:
        return self.nivel


class DummyTabela(Tabela):
    def valor_do_nivel_para_classe(self, nivel: Nivel, classe: Classe, competencia: date) -> float:
        if nivel == Nivel(1, "0") and classe == Classe.E2:
            return 1000
        if nivel == Nivel(25, "B") and classe == Classe.E2:
            return 2000
        if nivel == Nivel(30, "C") and classe == Classe.E2:
            return p.TETO_PREFEITO
        if nivel == Nivel(36, "D") and classe == Classe.E3:
            return p.TETO_PROCURADORES
        return 0.0


class TestCalculoFolha:

    def test_nivel(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(25, "B")
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        assert calculadora.calcula(funcionario, date(2023, 10, 1)).nivel == nivel

    def test_salario(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(25, "B")  # Valor: 2.000
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )

        assert calculadora.calcula(funcionario, date(2023, 10, 1)).salario == 2000

    def test_calcula_anuenio(self):
        calculadora = CalculaFolha(
            tabela=DummyTabela(),
        )
        funcionario = DummyFuncionario(
            DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=Nivel(25, "B"), # Valor: 2.000, não usado no cálculo do anuênio
        )
        competencia = date(2008, 2, 1)  # 8 anos. Valor do nível(1, "0") é 1000
        assert calculadora.calcula(funcionario, competencia).anuenio == 80

    def test_calcula_ats(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(25, "B")  # Valor: 2.000
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=None,
                num_ats=3,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        assert calculadora.calcula(funcionario, date(2023, 10, 1)).ats == 60

    def test_calcula_total_antes_limite_prefeito(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(25, "B")  # Valor: 2.000
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=3,  # R$ 60 de ats
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        competencia = date(2008, 2, 1)  # 8 anos = 80 reais de anuênio
        assert (
            calculadora.calcula(funcionario, competencia).total_antes_limite_prefeito
            == 2140
        )

    def test_calcula_total_quando_nao_atinge_teto(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(25, "B")  # Valor: 2.000
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        competencia = date(2008, 2, 1)  # 8 anos = 80 reais de anuênio
        assert calculadora.calcula(funcionario, competencia).total == 2080

    def test_total_respeita_limite_do_prefeito(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(30, "C")  # Valor: TETO_PREFEITO
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        competencia = date(2008, 2, 1)  # 8 anos: R$ 80 de anuênio > passa do limite
        assert calculadora.calcula(funcionario, competencia).total == p.TETO_PREFEITO

    def test_total_respeita_limite_do_procurador(self):
        calculadora = CalculaFolha(DummyTabela())
        nivel = Nivel(36, "D")  # Valor: TETO_PROCURADORES
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E3,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=True,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        competencia = date(2008, 2, 1)  # 8 anos: R$ 80 de anuênio > passa do limite
        assert (
            calculadora.calcula(funcionario, competencia).total == p.TETO_PROCURADORES
        )

    def test_fufin_eh_zero_se_bh_prev(self):
        calculadora = CalculaFolha(DummyTabela())
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=Nivel(1, "0"),
        )
        assert calculadora.calcula(funcionario, date(2023, 10, 1)).fufin_patronal == 0

    def test_fufin_eh_zero_se_bh_prev_complementar(self):
        calculadora = CalculaFolha(DummyTabela())
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2000, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
            nivel=Nivel(1, "0"),
        )
        assert calculadora.calcula(funcionario, date(2023, 10, 1)).fufin_patronal == 0

    def test_fufin(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.Fufin,
            ),
            nivel=Nivel(1, "0"),  # Valor: 1.000
        )
        assert (
            calculadora.calcula(funcionario, competencia).fufin_patronal
            == 1000 * p.ALIQUOTA_PATRONAL
        )

    def test_bhprev_patronal_passa_teto_inss_se_bhprev(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        nivel = Nivel(30, "C")  # Valor: TETO_PREFEITO
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=nivel,
        )
        assert calculadora.calcula(funcionario, competencia).bhprev_patronal == round(
            p.TETO_PREFEITO * p.ALIQUOTA_PATRONAL, 2
        )

    def test_bhprev_patronal_limitado_ao_inss_se_bhprev_complementar(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
            nivel=Nivel(30, "C"),  # Valor: TETO_PREFEITO
        )
        assert calculadora.calcula(funcionario, competencia).bhprev_patronal == round(
            p.TETO_INSS * p.ALIQUOTA_PATRONAL, 2
        )

    def test_bhprev_complementar_zerada_se_fufin(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.Fufin,
            ),
            nivel=Nivel(1, "0"),  # Valor: 1.000
        )
        assert calculadora.calcula(funcionario, competencia).bhprev_patronal == 0

    def test_bhprev_complementar_zerada_se_bhprev(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrev,
            ),
            nivel=Nivel(1, "0"),  # Valor: 1.000
        )
        assert (
            calculadora.calcula(funcionario, competencia).bhprev_complementar_patronal
            == 0
        )

    def test_bhprev_complementar_zerada_se_nao_atinge_teto_inss(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
            nivel=Nivel(1, "0"),  # Valor: 1.000
        )
        assert (
            calculadora.calcula(funcionario, competencia).bhprev_complementar_patronal
            == 0
        )

    def test_bhprev_complementar_somente_acima_teto_inss(self):
        calculadora = CalculaFolha(DummyTabela())
        competencia = date(2023, 10, 1)
        funcionario = DummyFuncionario(
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=competencia,
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.BHPrevComplementar,
            ),
            nivel=Nivel(30, "C"),  # Valor: LIMITE_PREFEITO
        )
        assert calculadora.calcula(
            funcionario, competencia
        ).bhprev_complementar_patronal == round(
            (p.TETO_PREFEITO - p.TETO_INSS) * p.ALIQUOTA_PATRONAL_COMPLEMENTAR, 2
        )
