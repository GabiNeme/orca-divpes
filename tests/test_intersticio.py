import pytest

from src.intersticio import IntersticioE2, IntersticioE3
from src.nivel import Nivel


class TestIntersticioE2:
    @pytest.mark.parametrize(
        "nivel, num_progs, tempo",
        [
            (Nivel(1, "0"), 1, 9),
            (Nivel(1, "A"), 2, 18),
            (Nivel(8, "B"), 2, 21),
            (Nivel(15, "C"), 2, 24),
            (Nivel(28, "D"), 2, 27),
            (Nivel(30, "E"), 2, 30),
            (Nivel(34, "0"), 2, 30),
            (Nivel(35, "0"), 2, 39),
            (Nivel(36, "0"), 2, 48),
            (Nivel(37, "0"), 2, 48),
        ],
    )
    def test_calcula_tempo_para_progredir(
        self, nivel: Nivel, num_progs: int, tempo: int
    ):
        assert IntersticioE2().tempo_para_progredir(nivel, num_progs) == tempo


class TestIntersticioE3:
    @pytest.mark.parametrize(
        "nivel, num_progs, tempo",
        [
            (Nivel(1, "0"), 1, 9),
            (Nivel(1, "A"), 2, 18),
            (Nivel(8, "B"), 2, 21),
            (Nivel(15, "C"), 2, 24),
            (Nivel(28, "D"), 2, 27),
            (Nivel(30, "E"), 2, 30),
            (Nivel(33, "0"), 2, 30),
            (Nivel(34, "0"), 2, 39),
            (Nivel(35, "0"), 2, 48),
            (Nivel(36, "0"), 2, 48),
        ],
    )
    def test_calcula_tempo_para_progredir(
        self, nivel: Nivel, num_progs: int, tempo: int
    ):
        assert IntersticioE3().tempo_para_progredir(nivel, num_progs) == tempo
