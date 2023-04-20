import pytest

from src.cargo import Nivel
from src.intersticio import Intersticio


class TestIntersticio:
    @pytest.mark.parametrize(
        "nivel, num_progs, tempo",
        [
            (Nivel(1, "0"), 1, 9),
            (Nivel(1, "A"), 2, 18),
            (Nivel(8, "B"), 2, 21),
            (Nivel(15, "C"), 2, 24),
            (Nivel(28, "D"), 2, 27),
            (Nivel(30, "E"), 2, 30),
            (Nivel(48, "0"), 2, 48),
        ],
    )
    def test_calcula_tempo_para_progredir(
        self, nivel: Nivel, num_progs: int, tempo: int
    ):
        assert Intersticio().tempo_para_progredir(nivel, num_progs) == tempo
