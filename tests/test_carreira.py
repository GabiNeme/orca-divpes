from datetime import date

import pytest

from src.carreira import (
    CarreiraE2,
    CarreiraE2Concurso2004,
    CarreiraE2Concurso2008,
    CarreiraE2PassaDoTetoAtual,
    CarreiraE3,
    CarreiraE3Concurso2004,
    CarreiraE3Concurso2008,
    CarreiraE3PassaDoTetoAtual,
    Progressao,
)
from src.nivel import Nivel


class TestCarreiraE2:
    @pytest.mark.parametrize(
        "nivel_origem, nivel_destino",
        [
            (Nivel(1, "0"), Nivel(1, "A")),
            (Nivel(2, "0"), Nivel(2, "A")),
            (Nivel(3, "A"), Nivel(3, "B")),
            (Nivel(4, "0"), Nivel(4, "B")),
            (Nivel(5, "0"), Nivel(5, "B")),
            (Nivel(6, "A"), Nivel(6, "C")),
            (Nivel(7, "C"), Nivel(7, "C")),
            (Nivel(8, "A"), Nivel(8, "D")),
            (Nivel(9, "0"), Nivel(9, "D")),
            (Nivel(10, "0"), Nivel(10, "D")),
            (Nivel(11, "0"), Nivel(11, "E")),
            (Nivel(20, "B"), Nivel(20, "E")),
        ],
    )
    def test_concede_letras_ate_limite(self, nivel_origem, nivel_destino):
        assert CarreiraE2().concede_letras_ate_limite(nivel_origem) == nivel_destino

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
        carreira = CarreiraE2()
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
        carreira = CarreiraE2()
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
        carreira = CarreiraE2()
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
            (Nivel(33, "0")),
        ],
    )
    def test_checa_nivel_valido_lanca_excecao_se_invalido(self, nivel):
        with pytest.raises(ValueError):
            _ = CarreiraE2().checa_nivel_valido(nivel)

    def test_progride_verticalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"), progs_sem_especial=0)
        with pytest.raises(ValueError):
            _ = CarreiraE2().progride_verticalmente(progressao)

    def test_progride_verticalmente_e_horizontalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"), progs_sem_especial=0)
        with pytest.raises(ValueError):
            _ = CarreiraE2().progride_verticalmente_e_horizontalmente(progressao)

    def test_progride_vert_e_hor_nao_ultrapassa_letra_maxima(self):
        ultima_progressao = Progressao(
            date.today(), Nivel(8, "B"), progs_sem_especial=1
        )
        letra_maxima = "D"
        progressao_esperada = Progressao(
            date.today(), Nivel(11, "D"), progs_sem_especial=0
        )  # No nivel 11 poderia ir até E

        progressao = CarreiraE2().progride_verticalmente_e_horizontalmente(
            ultima_progressao, letra_maxima
        )
        assert progressao.nivel == progressao_esperada.nivel

    def test_concede_letra_verifica_nivel_invalido(self):
        nivel = Nivel(2, "E")
        with pytest.raises(ValueError):
            _ = CarreiraE2().concede_letras_ate_limite(nivel)

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2020, 1, 1), Nivel(30, "D"), progs_sem_especial=1),
                Progressao(date(2022, 7, 1), Nivel(32, "D"), progs_sem_especial=0),
            ),
            (
                Progressao(date(2020, 1, 1), Nivel(31, "E"), progs_sem_especial=0),
                Progressao(date(2022, 7, 1), Nivel(32, "E"), progs_sem_especial=1),
            ),
        ],
    )
    def test_nao_progride_alem_do_fim_da_carreira(self, prog_antes, prog_depois):
        carreira = CarreiraE2()
        assert carreira.progride_verticalmente(prog_antes) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes",
        [
            (Progressao(date(2020, 1, 1), Nivel(32, "0"), progs_sem_especial=0)),
            (Progressao(date(2020, 1, 1), Nivel(32, "E"), progs_sem_especial=1)),
        ],
    )
    def test_progressao_e_none_se_ja_esta_no_fim_da_carreira(self, prog_antes):
        carreira = CarreiraE2()
        assert carreira.progride_verticalmente(prog_antes) is None

    def test_progride_ate_letra_respeita_letra_maxima(self):
        carreira = CarreiraE2()
        nivel_origem = Nivel(5, "A")
        letra = "B"
        nivel_destino = Nivel(5, "B")  # No 5, letra C é o máximo
        assert carreira.progride_ate_letra(nivel_origem, letra) == nivel_destino

    def test_progride_ate_letra_vai_ate_maximo_se_limite_e_maior(self):
        carreira = CarreiraE2()
        nivel_origem = Nivel(3, "A")
        letra = "C"
        nivel_destino = Nivel(3, "B")  # No 3, letra B é o máximo
        assert carreira.progride_ate_letra(nivel_origem, letra) == nivel_destino

    def test_progride_ate_letra_vai_nao_volta_nivel(self):
        carreira = CarreiraE2()
        nivel_origem = Nivel(5, "B")
        letra = "A"
        nivel_destino = Nivel(5, "B")  # No 5, letra C é o máximo
        assert carreira.progride_ate_letra(nivel_origem, letra) == nivel_destino

    def test_progride_mesmo_depois_de_completar_condicao_aposentadoria(self):
        carreira = CarreiraE2()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(30, "E"), progs_sem_especial=0)
        prog_depois_esperada = Progressao(
            date(2022, 7, 1), Nivel(32, "E"), progs_sem_especial=1
        )

        prog_depois = carreira.progride_verticalmente(prog_antes, date(2020, 2, 1))
        assert prog_depois == prog_depois_esperada

        prog_depois = carreira.progride_verticalmente_e_horizontalmente(
            prog_antes, None, date(2018, 1, 1)
        )
        assert prog_depois == prog_depois_esperada


class TestCarreiraConcurso2008:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE2Concurso2008()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(32, "E"), progs_sem_especial=1)
        prog_depois = Progressao(date(2022, 7, 1), Nivel(34, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraConcurso2004:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE2Concurso2004()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(35, "E"), progs_sem_especial=0)
        prog_depois = Progressao(date(2023, 4, 1), Nivel(36, "E"), progs_sem_especial=1)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraE2PassaDoTetoAtual:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE2PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(40, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == None

    def test_progride_ate_36_mesmo_depois_de_completar_condicao_aposentadoria(self):
        carreira = CarreiraE2PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(34, "E"), progs_sem_especial=0)
        prog_depois_esperada = Progressao(
            date(2022, 7, 1), Nivel(36, "E"), progs_sem_especial=1
        )
        prog_depois = carreira.progride_verticalmente(prog_antes, date(2018, 2, 1))
        assert prog_depois == prog_depois_esperada

    def test_nao_progride_apos_36_se_completou_condicao_aposentadoria(self):
        carreira = CarreiraE2PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(35, "E"), progs_sem_especial=1)
        prog_depois_esperada = Progressao(
            date(2023, 4, 1), Nivel(36, "E"), progs_sem_especial=0
        )
        prog_depois = carreira.progride_verticalmente(prog_antes, date(2018, 2, 1))
        assert prog_depois == prog_depois_esperada
        assert prog_depois == prog_depois_esperada

    def test_nao_progride_mais_apos_completar_condicao_aposentadoria(self):
        carreira = CarreiraE2PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(38, "E"), progs_sem_especial=1)

        assert carreira.progride_verticalmente(prog_antes, date(2021, 1, 1)) == None


class TestCarreiraE3:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE3()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(30, "E"), progs_sem_especial=1)
        prog_depois = Progressao(date(2022, 7, 1), Nivel(31, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraE3Concurso2008:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE3Concurso2008()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(31, "E"), progs_sem_especial=1)
        prog_depois = Progressao(date(2022, 7, 1), Nivel(33, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraE3Concurso2004:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE3Concurso2004()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(34, "E"), progs_sem_especial=1)
        prog_depois = Progressao(date(2023, 4, 1), Nivel(35, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == prog_depois


class TestCarreiraE3PassaDoTetoAtual:
    def test_nao_progride_alem_do_fim_da_carreira(self):
        carreira = CarreiraE3PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(39, "E"), progs_sem_especial=0)
        assert carreira.progride_verticalmente(prog_antes) == None

    def test_progride_ate_35_mesmo_depois_de_completar_condicao_aposentadoria(self):
        carreira = CarreiraE3PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(32, "E"), progs_sem_especial=0)
        prog_depois_esperada = Progressao(
            date(2022, 7, 1), Nivel(34, "E"), progs_sem_especial=1
        )
        prog_depois = carreira.progride_verticalmente(prog_antes, date(2018, 2, 1))
        assert prog_depois == prog_depois_esperada

    def test_nao_progride_apos_35_se_completou_condicao_aposentadoria(self):
        carreira = CarreiraE3PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(34, "E"), progs_sem_especial=1)
        prog_depois_esperada = Progressao(
            date(2023, 4, 1), Nivel(35, "E"), progs_sem_especial=0
        )
        prog_depois = carreira.progride_verticalmente(prog_antes, date(2018, 2, 1))
        assert prog_depois == prog_depois_esperada
        assert prog_depois == prog_depois_esperada

    def test_nao_progride_mais_apos_completar_condicao_aposentadoria(self):
        carreira = CarreiraE3PassaDoTetoAtual()
        prog_antes = Progressao(date(2020, 1, 1), Nivel(37, "E"), progs_sem_especial=1)

        assert carreira.progride_verticalmente(prog_antes, date(2021, 1, 1)) == None
