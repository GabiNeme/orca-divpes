from datetime import date

from src.classe import Classe
from src.nivel import Nivel
from src.carreira import Carreira, Progressao
from src.funcionario import Funcionario, Registro, Aposentadoria
from dateutil.relativedelta import relativedelta


class MockCarreira(Carreira):
    # Implementação mock para testes
    def progride_verticalmente_e_horizontalmente(self, ultima_progressao):
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
            registro=Registro(
                cm=12345,
                classe=Classe.E2,
                data_anuenio=date(2021, 1, 1),
                num_ats=0,
                procurador=False,
            ),
            aposentadoria=Aposentadoria(
                data_aposentadoria=date(2045, 10, 1), num_art_98_data_aposentadoria=0
            ),
            ultima_progressao=Progressao(
                data=date(2021, 1, 1), nivel=nivel_inicial, progs_sem_especial=1
            ),
            carreira=MockCarreira(),
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
