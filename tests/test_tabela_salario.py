import pytest

from src.classe import Classe
from src.nivel import Nivel
from src.tabela_salario import Tabela

INICIAL_E2 = 4759.37


class TestTabelaE2:
    @pytest.mark.parametrize(
        "nivel, valor",
        [
            ("1.0", INICIAL_E2),
            ("5.A", 5990.76),
            ("10.B", 7835.59),
            ("15.C", 10248.53),
            ("20.D", 13404.52),
            ("30.E", 21238.7),
        ],
    )
    def test_valor_do_nivel(self, nivel: str, valor: float):
        tabela = Tabela
        nivel_ = Nivel.from_string(nivel)
        assert tabela.valor_do(nivel_, INICIAL_E2) == valor

    def test_valor_do_nivel_E2(self):
        tabela = Tabela()
        INICIAL_E2 = 5758.83
        assert tabela.valor_do_nivel_para_classe(Nivel(1, "0"), Classe.E2) == INICIAL_E2
        assert tabela.valor_do_nivel_para_classe(Nivel(20, "A"), Classe.E2) == 12886.26
        assert tabela.valor_do_nivel_para_classe(Nivel(31, "E"), Classe.E2) == 26703.62

    def test_valor_do_nivel_E3(self):
        tabela = Tabela()
        INICIAL_E3 = 10047.80
        assert tabela.valor_do_nivel_para_classe(Nivel(1, "0"), Classe.E3) == INICIAL_E3
        assert tabela.valor_do_nivel_para_classe(Nivel(16, "B"), Classe.E3) == 20822.72
        assert tabela.valor_do_nivel_para_classe(Nivel(33, "E"), Classe.E3) == 50306.2
