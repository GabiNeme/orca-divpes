import pytest

from src.cargo import Classe, Nivel


class TestClasse:
    def test_classe_E2(self):
        classe = Classe["E2"]
        assert classe == Classe.E2

    def test_classe_E3(self):
        classe = Classe["E3"]
        assert classe == Classe.E3

    def test_classe_nao_aceita_outra_classe(self):
        with pytest.raises(KeyError):
            _ = Classe["E1"]


class TestNivel:
    @pytest.mark.parametrize("nivel_str", ["", " ", "0.A", "1.F", "50.E", "1.1.A"])
    def test_nao_aceita_niveis_incorretos(self, nivel_str):
        with pytest.raises(ValueError):
            _ = Nivel(nivel_str)

    @pytest.mark.parametrize("nivel_str", ["1.0", " 20.D "])
    def test_aceita_niveis_corretos(self, nivel_str):
        _ = Nivel(nivel_str)

    def test_impressao_nivel(self):
        nivel = Nivel(" 36.E ")
        assert str(nivel) == "36.E"

    def test_numero(self):
        nivel = Nivel("13.C")
        assert nivel.numero == 13

    def test_letra(self):
        nivel = Nivel("13.C")
        assert nivel.letra == "C"
