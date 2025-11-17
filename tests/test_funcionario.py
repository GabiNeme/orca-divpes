from datetime import date

from dateutil.relativedelta import relativedelta

from src.carreira import Carreira, Progressao
from src.classe import Classe
from src.funcionario import Aposentadoria, DadosFolha, Funcionario, TipoPrevidencia
from src.nivel import Nivel


class DummyCarreira(Carreira):
    # Implementação para testes
    def progride_verticalmente_e_horizontalmente(
        self, ultima_progressao, letra_maxima=None
    ):
        progs_horizontais = 1
        if ultima_progressao.nivel.numero >= 5:
            progs_horizontais = 0
        return Progressao(
            data=ultima_progressao.data + relativedelta(years=1),  # soma um ano
            nivel=ultima_progressao.nivel.proximo(1, progs_horizontais),
            progs_sem_especial=ultima_progressao.progs_sem_especial + 1,
        )

    def progride_verticalmente(self, ultima_progressao):
        return Progressao(
            data=ultima_progressao.data + relativedelta(years=1),  # soma um ano
            nivel=ultima_progressao.nivel.proximo(1, 0),
            progs_sem_especial=ultima_progressao.progs_sem_especial + 1,
        )


class TesteFuncionario:

    def default_funcionario(self, nivel_inicial: Nivel = Nivel(1, "A")) -> Funcionario:
        return Funcionario(
            cm=12345,
            data_admissao=date(2020, 1, 1),
            dados_folha=DadosFolha(
                classe=Classe.E2,
                data_anuenio=date(2021, 1, 1),
                num_ats=0,
                procurador=False,
                tipo_previdencia=TipoPrevidencia.Fufin,
            ),
            aposentadoria=Aposentadoria(
                data_condicao_aposentadoria=date(2045, 10, 1),
                data_aposentadoria=date(2045, 10, 20),
                num_art_98_data_aposentadoria=0,
                aderiu_pia=True,
            ),
            ultima_progressao=Progressao(
                data=date(2021, 1, 1), nivel=nivel_inicial, progs_sem_especial=1
            ),
            carreira=DummyCarreira(),
        )

    def test_retorna_nivel_correto_se_concede_todas_as_letras(self):
        funcionario = self.default_funcionario()

        assert funcionario.obtem_nivel_para(date(2021, 1, 1)) == Nivel(1, "A")
        assert funcionario.obtem_nivel_para(date(2022, 1, 2)) == Nivel(2, "B")
        assert funcionario.obtem_nivel_para(date(2025, 8, 1)) == Nivel(5, "E")
        assert funcionario.obtem_nivel_para(date(2030, 12, 1)) == Nivel(10, "E")

    def test_retorna_nivel_correto_se_nao_concede_todas_as_letras(self):
        funcionario = self.default_funcionario(
            Nivel(11, "A")
        )  # Na carreira atual, não concede letras

        assert funcionario.obtem_nivel_para(date(2021, 1, 1)) == Nivel(11, "A")
        assert funcionario.obtem_nivel_para(date(2022, 1, 2)) == Nivel(12, "A")
        assert funcionario.obtem_nivel_para(date(2025, 8, 1)) == Nivel(15, "A")
        assert funcionario.obtem_nivel_para(date(2030, 12, 1)) == Nivel(20, "A")

    def retorna_none_se_aposentado(self):
        funcionario = self.default_funcionario()

        assert funcionario.obtem_nivel_para(date(2045, 10, 1)) is None
        assert funcionario.obtem_nivel_para(date(2050, 1, 1)) is None

    def retorna_progressao_mes_anterior_aposentadoria(self):
        funcionario = self.default_funcionario()

        assert funcionario.obtem_nivel_para(date(2045, 9, 30)) is not None

    def retorna_nivel_correto_no_dia_da_aposentadoria(self):
        funcionario = self.default_funcionario()

        assert funcionario.obtem_nivel_para(date(2045, 10, 31)) is not None

    def retorna_none_se_antes_da_admissao(self):
        funcionario = self.default_funcionario()
        assert funcionario.obtem_nivel_para(date(2019, 12, 31)) is None
