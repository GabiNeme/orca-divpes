from datetime import date
from dateutil.relativedelta import relativedelta

from src.carreira import Progressao
from src.nivel import Nivel


class RegraTransicao:

    @staticmethod
    def primeira_progressao(
        data_admissao: date, procurador: bool, dias_licenca: int
    ) -> Progressao:
        """Aplica a regra de transição para determinar a primeira
        progressão na nova carreira."""
        if procurador:
            nivel_inicial = Nivel(10, "A")
        else:
            nivel_inicial = Nivel(1, "A")

        data_primeira_progressao = data_admissao + relativedelta(days=dias_licenca)

        return Progressao(
            data=data_primeira_progressao, nivel=nivel_inicial, progs_sem_especial=0
        )
