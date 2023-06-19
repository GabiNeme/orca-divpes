from datetime import date

import pytest

from src.cargo import Classe, Nivel
from src.carreira import Carreira2004, CarreiraAntes2004, Progressao


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
                Progressao(date(2022, 7, 1), Nivel(37, "D"), 15),
            ),
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(36, "D")),
                False,
                Progressao(date(2022, 7, 1), Nivel(37, "D"), 15),
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
                Progressao(date(2022, 7, 1), Nivel(36, "D"), 15),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(35, "D")),
                False,
                Progressao(date(2022, 7, 1), Nivel(36, "D"), 15),
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


class TestCarreiraAntes2004:
    @pytest.mark.parametrize(
        "classe, nivel, limite_vertical",
        [
            (Classe.E2, Nivel(1, "0"), 47),
            (Classe.E2, Nivel(10, "A"), 45),
            (Classe.E2, Nivel(20, "B"), 43),
            (Classe.E2, Nivel(15, "C"), 41),
            (Classe.E2, Nivel(8, "D"), 39),
            (Classe.E2, Nivel(36, "E"), 37),
            (Classe.E3, Nivel(1, "0"), 46),
            (Classe.E3, Nivel(10, "A"), 44),
            (Classe.E3, Nivel(20, "B"), 42),
            (Classe.E3, Nivel(15, "C"), 40),
            (Classe.E3, Nivel(8, "D"), 38),
            (Classe.E3, Nivel(36, "E"), 36),
        ],
    )
    def test_limite(self, classe, nivel, limite_vertical):
        carreira = CarreiraAntes2004(classe)
        assert carreira.limite(nivel) == limite_vertical

    @pytest.mark.parametrize(
        "classe, numero_nivel, letra",
        [
            (Classe.E2, 1, "A"),
            (Classe.E2, 6, "A"),
            (Classe.E2, 7, "B"),
            (Classe.E2, 12, "B"),
            (Classe.E2, 13, "C"),
            (Classe.E2, 18, "C"),
            (Classe.E2, 19, "D"),
            (Classe.E2, 24, "D"),
            (Classe.E2, 25, "E"),
            (Classe.E2, 37, "E"),
            (Classe.E2, 38, "D"),
            (Classe.E2, 39, "D"),
            (Classe.E2, 40, "C"),
            (Classe.E2, 41, "C"),
            (Classe.E2, 42, "B"),
            (Classe.E2, 43, "B"),
            (Classe.E2, 44, "A"),
            (Classe.E2, 45, "A"),
            (Classe.E2, 46, "0"),
            (Classe.E2, 47, "0"),
            (Classe.E3, 36, "E"),
            (Classe.E3, 37, "D"),
            (Classe.E3, 38, "D"),
            (Classe.E3, 39, "C"),
            (Classe.E3, 40, "C"),
            (Classe.E3, 41, "B"),
            (Classe.E3, 42, "B"),
            (Classe.E3, 43, "A"),
            (Classe.E3, 44, "A"),
            (Classe.E3, 45, "0"),
            (Classe.E3, 46, "0"),
        ],
    )
    def test_letra_maxima_para_nivel(self, classe, numero_nivel, letra):
        carreira = CarreiraAntes2004(classe)
        assert carreira.letra_maxima_para_nivel(numero_nivel) == letra

    @pytest.mark.parametrize(
        "classe, prog_antes, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2020, 9, 25), Nivel(36, "A")),
                Progressao(date(2023, 3, 25), Nivel(38, "A")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 9, 25), Nivel(36, "D")),
                Progressao(date(2023, 3, 25), Nivel(38, "D")),
            ),
        ],
    )
    def test_progressao_vertical_nao_especial(self, classe, prog_antes, prog_depois):
        carreira = CarreiraAntes2004(classe)
        assert carreira.progride_verticalmente(prog_antes, False) == prog_depois

    @pytest.mark.parametrize(
        "classe, prog_antes, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2020, 9, 25), Nivel(38, "B")),
                Progressao(date(2023, 3, 25), Nivel(41, "B")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 9, 25), Nivel(36, "C")),
                Progressao(date(2023, 3, 25), Nivel(39, "C")),
            ),
        ],
    )
    def test_progressao_vertical_com_especial(self, classe, prog_antes, prog_depois):
        carreira = CarreiraAntes2004(classe)
        assert carreira.progride_verticalmente(prog_antes, True) == prog_depois

    @pytest.mark.parametrize(
        "prog_antes, especial, prog_depois",
        [
            (
                Progressao(date(2021, 7, 13), Nivel(37, "A")),
                True,
                Progressao(date(2024, 1, 13), Nivel(40, "C")),
            ),
            (
                Progressao(date(2026, 10, 13), Nivel(43, "0")),
                False,
                Progressao(date(2029, 4, 13), Nivel(45, "A")),
            ),
        ],
    )
    def test_progressao_vertical_e_horizontal(self, prog_antes, especial, prog_depois):
        carreira = CarreiraAntes2004(Classe.E2)
        assert (
            carreira.progride_verticalmente_e_horizontalmente(prog_antes, especial)
            == prog_depois
        )

    @pytest.mark.parametrize(
        "nivel",
        [
            (Nivel(43, "E")),
            (Nivel(45, "D")),
            (Nivel(48, "C")),
            (Nivel(49, "B")),
            (Nivel(51, "A")),
            (Nivel(53, "0")),
        ],
    )
    def test_checa_nivel_valido_lanca_excecao_se_invalido(self, nivel):
        with pytest.raises(ValueError):
            _ = CarreiraAntes2004(Classe.E2).checa_nivel_valido(nivel)
            _ = CarreiraAntes2004(Classe.E3).checa_nivel_valido(nivel)

    @pytest.mark.parametrize(
        "classe, prog_antes, especial, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(44, "A")),
                False,
                Progressao(date(2022, 7, 1), Nivel(45, "A"), 15),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(39, "C")),
                False,
                Progressao(date(2022, 7, 1), Nivel(40, "C"), 15),
            ),
            (
                Classe.E2,
                Progressao(date(2020, 1, 1), Nivel(41, "B")),
                True,
                Progressao(date(2022, 7, 1), Nivel(43, "B")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(44, "0")),
                True,
                Progressao(date(2022, 7, 1), Nivel(46, "0")),
            ),
        ],
    )
    def test_progressao_com_ganho_de_credito(
        self, classe, prog_antes, especial, prog_depois
    ):
        carreira = CarreiraAntes2004(classe)
        assert carreira.progride_verticalmente(prog_antes, especial) == prog_depois

    @pytest.mark.parametrize(
        "classe, prog_antes, especial, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2022, 7, 1), Nivel(45, "A"), 15),
                False,
                Progressao(date(2025, 4, 1), Nivel(46, "A")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(40, "C"), 15),
                False,
                Progressao(date(2022, 10, 1), Nivel(41, "C")),
            ),
        ],
    )
    def test_progressao_com_gasto_de_credito(
        self, classe, prog_antes, especial, prog_depois
    ):
        carreira = CarreiraAntes2004(classe)
        assert carreira.progride_verticalmente(prog_antes, especial) == prog_depois

    @pytest.mark.parametrize(
        "classe, prog_antes, prog_depois",
        [
            (
                Classe.E2,
                Progressao(date(2022, 7, 1), Nivel(50, "0")),
                Progressao(date(2026, 7, 1), Nivel(51, "0")),
            ),
            (
                Classe.E3,
                Progressao(date(2020, 1, 1), Nivel(41, "D")),
                Progressao(date(2024, 1, 1), Nivel(42, "D")),
            ),
        ],
    )
    def test_progressao_art_44(self, classe, prog_antes, prog_depois):
        carreira = CarreiraAntes2004(classe)
        assert carreira.progride_verticalmente(prog_antes, True) == prog_depois
        assert carreira.progride_verticalmente(prog_antes, False) == prog_depois

    @pytest.mark.parametrize(
        "classe, prog_antes",
        [
            (Classe.E2, Progressao(date(2020, 1, 1), Nivel(52, "0"))),
            (Classe.E2, Progressao(date(2020, 1, 1), Nivel(50, "A"))),
            (Classe.E2, Progressao(date(2020, 1, 1), Nivel(42, "E"))),
            (Classe.E3, Progressao(date(2020, 1, 1), Nivel(47, "B"))),
            (Classe.E3, Progressao(date(2020, 1, 1), Nivel(45, "C"))),
            (Classe.E3, Progressao(date(2020, 1, 1), Nivel(43, "D"))),
        ],
    )
    def test_progressao_e_none_se_ja_esta_no_fim_da_carreira(self, classe, prog_antes):
        carreira = CarreiraAntes2004(classe)
        prog = carreira.progride_verticalmente(prog_antes)

        assert prog is None
