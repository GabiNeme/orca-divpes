import pytest

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
        tabela = Tabela()
        nivel_ = Nivel.from_string(nivel)
        assert tabela.valor_do(nivel_, INICIAL_E2) == valor
