import pytest

from src.cargo import Classe, Nivel


class TestClasse:
    def test_classe_E1(self):
        classe = Classe["E1"]
        assert classe == Classe.E1

    def test_classe_E2(self):
        classe = Classe["E2"]
        assert classe == Classe.E2

    def test_classe_E3(self):
        classe = Classe["E3"]
        assert classe == Classe.E3

    def test_classe_nao_aceita_outra_classe(self):
        with pytest.raises(KeyError):
            _ = Classe["E4"]


class TestNivel:
    @pytest.mark.parametrize("nivel_str", ["", " ", "0.A", "1.F", "60.E", "1.1.A"])
    def test_nao_aceita_niveis_incorretos(self, nivel_str):
        with pytest.raises(ValueError):
            _ = Nivel.from_string(nivel_str)

    @pytest.mark.parametrize("nivel_str", ["1.0", " 20.D "])
    def test_aceita_niveis_corretos(self, nivel_str):
        _ = Nivel.from_string(nivel_str)

    def test_impressao_nivel(self):
        nivel = Nivel.from_string(" 36.E ")
        assert str(nivel) == "36.E"

    def test_numero(self):
        nivel = Nivel.from_string("13.C")
        assert nivel.numero == 13

    def test_letra(self):
        nivel = Nivel.from_string("13.C")
        assert nivel.letra == "C"

    @pytest.mark.parametrize(
        "letra, numero_progs",
        [("0", 0), ("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)],
    )
    def test_correspondencia_letra_e_num_prog_horizontal(self, letra, numero_progs):
        nivel = Nivel(1, letra)

        assert nivel.numero_progressoes_horizontais == numero_progs

    @pytest.mark.parametrize(
        "nivel, passo_vert, passo_hor, proximo_nivel",
        [
            (Nivel(1, "0"), 0, 0, Nivel(1, "0")),
            (Nivel(5, "A"), 0, 1, Nivel(5, "B")),
            (Nivel(10, "B"), 1, 0, Nivel(11, "B")),
            (Nivel(15, "C"), 3, 2, Nivel(18, "E")),
            (Nivel(15, "A"), 2, 3, Nivel(17, "D")),
        ],
    )
    def test_proximo_nivel_retorna_nivel_correto(
        self, nivel: Nivel, passo_vert, passo_hor, proximo_nivel
    ):
        assert nivel.proximo(passo_vert, passo_hor) == proximo_nivel

    @pytest.mark.parametrize(
        "nivel, passo_vert, passo_hor, nivel_anterior",
        [
            (Nivel(1, "0"), 0, 0, Nivel(1, "0")),
            (Nivel(5, "A"), 0, 1, Nivel(5, "0")),
            (Nivel(10, "B"), 1, 0, Nivel(9, "B")),
            (Nivel(15, "C"), 3, 2, Nivel(12, "A")),
            (Nivel(15, "C"), 2, 3, Nivel(13, "0")),
        ],
    )
    def test_nivel_anterior_retorna_nivel_correto(
        self, nivel: Nivel, passo_vert, passo_hor, nivel_anterior
    ):
        assert nivel.anterior(passo_vert, passo_hor) == nivel_anterior
