from datetime import date

import pytest

from src.cargo import Classe, Nivel
from src.carreira import Carreira2004, Progressao


class TestCarreira2004:
    @pytest.mark.parametrize(
        "nivel_origem, nivel_destino",
        [
            (Nivel(1, "0"), Nivel(1, "A")),
            (Nivel(6, "0"), Nivel(6, "A")),
            (Nivel(7, "A"), Nivel(7, "B")),
            (Nivel(12, "0"), Nivel(12, "B")),
            (Nivel(13, "0"), Nivel(13, "C")),
            (Nivel(18, "A"), Nivel(18, "C")),
            (Nivel(19, "C"), Nivel(19, "D")),
            (Nivel(24, "A"), Nivel(24, "D")),
            (Nivel(25, "0"), Nivel(25, "E")),
            (Nivel(36, "B"), Nivel(36, "E")),
        ],
    )
    def test_concede_letras_ate_limite(self, nivel_origem, nivel_destino):
        assert (
            Carreira2004(Classe.E2).concede_letras_ate_limite(nivel_origem)
            == nivel_destino
        )

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2020, 9, 25), Nivel(3, "A")),
                Progressao(date(2022, 3, 25), Nivel(5, "A")),
            ),
            (
                Progressao(date(2020, 1, 1), Nivel(8, "B")),
                Progressao(date(2021, 10, 1), Nivel(10, "B")),
            ),
            (
                Progressao(date(2021, 10, 20), Nivel(16, "C")),
                Progressao(date(2023, 10, 20), Nivel(18, "C")),
            ),
            (
                Progressao(date(2021, 1, 1), Nivel(28, "0")),
                Progressao(date(2023, 4, 1), Nivel(30, "0")),
            ),
            (
                Progressao(date(2020, 10, 3), Nivel(32, "A")),
                Progressao(date(2023, 4, 3), Nivel(34, "A")),
            ),
        ],
    )
    def test_progressao_vertical_nao_especial(self, prog_antes, prog_depois):
        carreira = Carreira2004(Classe.E2)
        assert carreira.progride_verticalmente(prog_antes, False) == prog_depois
        assert carreira.progressao_vertical_anterior(prog_depois) == prog_antes

    @pytest.mark.parametrize(
        "prog_antes, prog_depois",
        [
            (
                Progressao(date(2021, 7, 13), Nivel(5, "A")),
                Progressao(date(2023, 1, 13), Nivel(8, "A")),
            ),
            (
                Progressao(date(2026, 10, 13), Nivel(12, "B")),
                Progressao(date(2028, 10, 13), Nivel(15, "B")),
            ),
            (
                Progressao(date(2032, 10, 13), Nivel(19, "D")),
                Progressao(date(2034, 10, 13), Nivel(22, "D")),
            ),
        ],
    )
    def test_progressao_vertical_com_especial(self, prog_antes, prog_depois):
        carreira = Carreira2004(Classe.E2)
        assert carreira.progride_verticalmente(prog_antes, True) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes, especial, prog_depois",
        [
            (
                Progressao(date(2021, 7, 13), Nivel(5, "A")),
                True,
                Progressao(date(2023, 1, 13), Nivel(8, "B")),
            ),
            (
                Progressao(date(2026, 10, 13), Nivel(18, "C")),
                False,
                Progressao(date(2028, 10, 13), Nivel(20, "D")),
            ),
        ],
    )
    def test_progressao_vertical_e_horizontal(self, prog_antes, especial, prog_depois):
        carreira = Carreira2004(Classe.E2)
        assert (
            carreira.progride_verticalmente_e_horizontalmente(prog_antes, especial)
            == prog_depois
        )

    @pytest.mark.parametrize(
        "classe, prog_antes, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(25, "D")),
                Progressao(date(2022, 1, 1), Nivel(27, "E")),
            ),
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(26, "D")),
                Progressao(date(2022, 1, 1), Nivel(28, "E")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(23, "D")),
                Progressao(date(2022, 1, 1), Nivel(25, "E")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(24, "D")),
                Progressao(date(2022, 1, 1), Nivel(26, "E")),
            ),
        ],
    )
    def test_limite_letras_D_e_E(self, classe, prog_antes, prog_depois):
        carreira = Carreira2004(classe)
        assert (
            carreira.progride_verticalmente_e_horizontalmente(prog_antes, False)
            == prog_depois
        )

    @pytest.mark.parametrize(
        "nivel",
        [
            (Nivel(1, "B")),
            (Nivel(6, "B")),
            (Nivel(12, "C")),
            (Nivel(18, "D")),
            (Nivel(24, "E")),
            (Nivel(10, "E")),
            (Nivel(40, "0")),
        ],
    )
    def test_checa_nivel_valido_lanca_excecao_se_invalido(self, nivel):
        with pytest.raises(ValueError):
            _ = Carreira2004(Classe.E2).checa_nivel_valido(nivel)

    def test_progride_verticalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"))
        with pytest.raises(ValueError):
            _ = Carreira2004(Classe.E2).progride_verticalmente(progressao, False)

    def test_progride_verticalmente_e_horizontalmente_verifica_nivel_invalido(self):
        progressao = Progressao(date.today(), Nivel(2, "E"))
        with pytest.raises(ValueError):
            _ = Carreira2004(Classe.E2).progride_verticalmente_e_horizontalmente(
                progressao, False
            )

    def test_concede_letra_verifica_nivel_invalido(self):
        nivel = Nivel(2, "E")
        with pytest.raises(ValueError):
            _ = Carreira2004(Classe.E2).concede_letras_ate_limite(nivel)

    @pytest.mark.parametrize(
        "classe, prog_antes, especial, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(35, "D")),
                True,
                Progressao(date(2022, 7, 1), Nivel(37, "D")),
            ),
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(36, "D")),
                True,
                Progressao(date(2022, 7, 1), Nivel(37, "D")),
            ),
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(36, "D")),
                False,
                Progressao(date(2022, 7, 1), Nivel(37, "D")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(34, "D")),
                True,
                Progressao(date(2022, 7, 1), Nivel(36, "D")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(35, "D")),
                True,
                Progressao(date(2022, 7, 1), Nivel(36, "D")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(35, "D")),
                False,
                Progressao(date(2022, 7, 1), Nivel(36, "D")),
            ),
        ],
    )
    def test_nao_progride_alem_do_fim_da_carreira(
        self, classe, prog_antes, especial, prog_depois
    ):
        carreira = Carreira2004(classe)
        assert carreira.progride_verticalmente(prog_antes, especial) == prog_depois

    @pytest.mark.parametrize(
        "classe, prog_antes, especial",
        [
            (Classe.E2, Progressao(date(2020, 1, 1), Nivel(37, "E")), True),
            (Classe.E2, Progressao(date(2020, 1, 1), Nivel(37, "B")), False),
            (Classe.E3, Progressao(date(2020, 1, 1), Nivel(36, "E")), True),
            (Classe.E3, Progressao(date(2020, 1, 1), Nivel(36, "B")), False),
        ],
    )
    def test_progressao_e_none_se_ja_esta_no_fim_da_carreira(
        self, classe, prog_antes, especial
    ):
        carreira = Carreira2004(classe)
        assert carreira.progride_verticalmente(prog_antes, especial) is None
