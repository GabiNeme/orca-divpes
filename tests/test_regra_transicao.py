from datetime import date

from src.regra_transicao import RegraTransicao
from src.nivel import Nivel

class TestRegraTransicao:
    def test_primeira_progressao_nao_procurador(self):
        data_admissao = date(2020, 1, 1)
        procurador = False
        dias_licenca = 0
        progressao = RegraTransicao.primeira_progressao(data_admissao, procurador, dias_licenca)
        assert progressao.nivel == Nivel(1, "A")
        assert progressao.data == date(2020, 1, 1)
        assert progressao.progs_sem_especial == 0

    def test_primeira_progressao_procurador(self):
        data_admissao = date(2020, 1, 1)
        procurador = True
        dias_licenca = 0
        progressao = RegraTransicao.primeira_progressao(data_admissao, procurador, dias_licenca)
        assert progressao.nivel == Nivel(10, "A")
        assert progressao.data == date(2020, 1, 1)
        assert progressao.progs_sem_especial == 0

    def test_primeira_progressao_com_licenca(self):
        data_admissao = date(2020, 1, 1)
        procurador = False
        dias_licenca = 30
        progressao = RegraTransicao.primeira_progressao(data_admissao, procurador, dias_licenca)
        assert progressao.nivel == Nivel(1, "A")
        assert progressao.data == date(2020, 1, 31)
        assert progressao.progs_sem_especial == 0
