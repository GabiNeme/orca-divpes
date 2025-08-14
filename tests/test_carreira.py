from datetime import date
import pytest

from src.nivel import Nivel
from src.carreira import (
    Carreira,
    CarreiraConcurso2004,
    CarreiraConcurso2008,
    Progressao,
)


class TestCarreira:
    @pytest.mark.parametrize(
        "nivel_origem, nivel_destino",
        [
            (Nivel(1, "0"), Nivel(1, "A")),
            (Nivel(2, "0"), Nivel(2, "A")),
            (Nivel(3, "A"), Nivel(3, "B")),
            (Nivel(4, "0"), Nivel(4, "B")),
            (Nivel(5, "0"), Nivel(5, "C")),
            (Nivel(6, "A"), Nivel(6, "C")),
            (Nivel(7, "C"), Nivel(7, "D")),
            (Nivel(8, "A"), Nivel(8, "D")),
            (Nivel(9, "0"), Nivel(9, "E")),
            (Nivel(20, "B"), Nivel(20, "E")),
        ],
    )
    def test_concede_letras_ate_limite(self, nivel_origem, nivel_destino):
        assert Carreira().concede_letras_ate_limite(nivel_origem) == nivel_destino

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2020, 1, 1), Nivel(1, "A"), progs_sem_especial=0),
                Progressao(date(2021, 7, 1), Nivel(3, "A"), progs_sem_especial=1),
            ),
            (
                Progressao(date(2020, 1, 1), Nivel(6, "C"), progs_sem_especial=0),
                Progressao(date(2021, 7, 1), Nivel(8, "C"), progs_sem_especial=1),
            ),
            (
                Progressao(date(2020, 1, 1), Nivel(11, "E"), progs_sem_especial=0),
                Progressao(date(2022, 1, 1), Nivel(13, "E"), progs_sem_especial=1),
            ),
        ],
    )
    def test_progressao_vertical_nao_especia_progride_2_niveis(
        self, prog_antes, prog_depois
    ):
        carreira = Carreira()
        assert carreira.progride_verticalmente(prog_antes) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2021, 7, 13), Nivel(5, "A"), progs_sem_especial=1),
                Progressao(date(2023, 1, 13), Nivel(8, "A"), progs_sem_especial=0),
            ),
            (
                Progressao(date(2026, 10, 13), Nivel(12, "B"), progs_sem_especial=1),
                Progressao(date(2028, 10, 13), Nivel(15, "B"), progs_sem_especial=0),
            ),
        ],
    )
    def test_progressao_vertical_com_especial_progride_3_niveis(
        self, prog_antes, prog_depois
    ):
        carreira = Carreira()
        assert carreira.progride_verticalmente(prog_antes) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2021, 7, 13), Nivel(1, "A"), progs_sem_especial=0),
                Progressao(date(2023, 1, 13), Nivel(3, "B"), progs_sem_especial=1),
            ),
            (
                Progressao(date(2026, 10, 13), Nivel(8, "D"), progs_sem_especial=1),
                Progressao(date(2028, 7, 13), Nivel(11, "E"), progs_sem_especial=0),
            ),
        ],
    )
    def test_progressao_vertical_e_horizontal(self, prog_antes, prog_depois):
        carreira = Carreira()
        assert (
            carreira.progride_verticalmente_e_horizontalmente(prog_antes) == prog_depois
        )

    @pytest.mark.parametrize(
        "nivel",
        [
            (Nivel(1, "B")),
            (Nivel(4, "C")),
            (Nivel(6, "D")),
            (Nivel(8, "E")),
            (Nivel(34, "0")),
        ],
    )
    def test_checa_nivel_valido_lanca_excecao_se_invalido(self, nivel):
        with pytest.raises(ValueError):
            _ = Carreira().checa_nivel_valido(nivel)

    def test_progride_verticalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"), progs_sem_especial=0)
        with pytest.raises(ValueError):
            _ = Carreira().progride_verticalmente(progressao)

    def test_progride_verticalmente_e_horizontalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"), progs_sem_especial=0)
        with pytest.raises(ValueError):
            _ = Carreira().progride_verticalmente_e_horizontalmente(progressao)

    def test_concede_letra_verifica_nivel_invalido(self):
        nivel = Nivel(2, "E")
        with pytest.raises(ValueError):
            _ = Carreira().concede_letras_ate_limite(nivel)

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2020, 1, 1), Nivel(31, "D"), progs_sem_especial=1),
                Progressao(date(2022, 7, 1), Nivel(33, "D"), progs_sem_especial=0),
            ),
            (
                Progressao(date(2020, 1, 1), Nivel(32, "E"), progs_sem_especial=0),
                Progressao(date(2022, 7, 1), Nivel(33, "E"), progs_sem_especial=1),
            ),
        ],
    )
    def test_nao_progride_alem_do_fim_da_carreira(self, prog_antes, prog_depois):
        carreira = Carreira()
        assert carreira.progride_verticalmente(prog_antes) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes",
        [
            (Progressao(date(2020, 1, 1), Nivel(33, "0"), progs_sem_especial=0)),
            (Progressao(date(2020, 1, 1), Nivel(33, "E"), progs_sem_especial=1)),
        ],
    )
    def test_progressao_e_none_se_ja_esta_no_fim_da_carreira(self, prog_antes):
        carreira = Carreira()
        assert carreira.progride_verticalmente(prog_antes) is None


class TestCarreiraConcurso2008:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraConcurso2008()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(33, "E"), progs_sem_especial=1)
        prog_depois = Progressao(date(2022, 7, 1), Nivel(35, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraConcurso2004:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraConcurso2004()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(36, "E"), progs_sem_especial=0)
        prog_depois = Progressao(date(2022, 7, 1), Nivel(37, "E"), progs_sem_especial=1)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois
