from datetime import date

from src.classe import Classe
from src.nivel import Nivel
from src.carreira import Carreira2004
from src.desenvolvimento import Desenvolvimento


class TesteDesenvolvimento:
    def test_desenvolvimento_com_letras_concedidas(self):
        carreira = Carreira2004(Classe.E2)
        desenvolvimento = Desenvolvimento(
            carreira=carreira,
            nivel_atual=Nivel(3, "A"),
            dt_ult_prog_vert=date(2020, 1, 13),
            progs_sem_especial=1,
        )

        assert desenvolvimento.obtem_nivel_para(date(2021, 6, 1)) == Nivel(3, "A")
        assert desenvolvimento.obtem_nivel_para(date(2021, 7, 1)) == Nivel(5, "A")
        assert desenvolvimento.obtem_nivel_para(date(2021, 8, 1)) == Nivel(5, "A")
        assert desenvolvimento.obtem_nivel_para(date(2022, 12, 1)) == Nivel(5, "A")
        assert desenvolvimento.obtem_nivel_para(date(2023, 1, 1)) == Nivel(8, "B")
        assert desenvolvimento.obtem_nivel_para(date(2024, 9, 1)) == Nivel(8, "B")
        assert desenvolvimento.obtem_nivel_para(date(2024, 10, 1)) == Nivel(10, "B")
        assert desenvolvimento.obtem_nivel_para(date(2045, 9, 1)) == Nivel(31, "E")
        assert desenvolvimento.obtem_nivel_para(date(2045, 10, 1)) == Nivel(33, "E")

    def test_desenvolvimento_sem_letras_concedidas(self):
        carreira = Carreira2004(Classe.E3)
        desenvolvimento = Desenvolvimento(
            carreira=carreira,
            nivel_atual=Nivel(17, "A"),
            dt_ult_prog_vert=date(2019, 10, 16),
            progs_sem_especial=1,
        )

        assert desenvolvimento.obtem_nivel_para(date(2021, 9, 1)) == Nivel(17, "A")
        assert desenvolvimento.obtem_nivel_para(date(2021, 10, 1)) == Nivel(19, "A")
        assert desenvolvimento.obtem_nivel_para(date(2023, 9, 1)) == Nivel(19, "A")
        assert desenvolvimento.obtem_nivel_para(date(2023, 10, 1)) == Nivel(22, "A")
        assert desenvolvimento.obtem_nivel_para(date(2029, 9, 1)) == Nivel(26, "A")
        assert desenvolvimento.obtem_nivel_para(date(2029, 10, 1)) == Nivel(29, "A")
        assert desenvolvimento.obtem_nivel_para(date(2032, 3, 1)) == Nivel(29, "A")
        assert desenvolvimento.obtem_nivel_para(date(2032, 4, 1)) == Nivel(31, "A")

    def test_proxima_progressao_eh_especial(self):
        carreira = Carreira2004(Classe.E2)
        desenvolvimento = Desenvolvimento(
            carreira=carreira,
            nivel_atual=Nivel(5, "A"),
            dt_ult_prog_vert=date(2021, 7, 13),
            progs_sem_especial=2,
        )

        assert desenvolvimento.obtem_nivel_para(date(2022, 12, 1)) == Nivel(5, "A")
        assert desenvolvimento.obtem_nivel_para(date(2023, 1, 1)) == Nivel(8, "B")

    def test_nao_progride_depois_fim_carreira(self):
        carreira = Carreira2004(Classe.E2)
        desenvolvimento = Desenvolvimento(
            carreira=carreira,
            nivel_atual=Nivel(37, "E"),
            dt_ult_prog_vert=date(2023, 1, 1),
            progs_sem_especial=0,
        )

        assert desenvolvimento.obtem_nivel_para(date(2023, 1, 1)) == Nivel(37, "E")
        assert desenvolvimento.obtem_nivel_para(date(2025, 1, 1)) == Nivel(37, "E")
        assert desenvolvimento.obtem_nivel_para(date(2030, 1, 1)) == Nivel(37, "E")
