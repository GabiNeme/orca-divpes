from functools import lru_cache

from src.nivel import Nivel

INDICE_PROGRESSAO_VERTICAL = 0.0391
INDICE_PROGRESSAO_HORIZONTAL = 0.0797


class Tabela:
    @lru_cache(maxsize=None)
    def valor_do(self, nivel: Nivel, valor_inicial: float) -> float:
        """Calcula o valor do nível informado."""

        progressao_vertical_total = (1 + INDICE_PROGRESSAO_VERTICAL) ** (
            nivel.numero - 1
        )

        progressao_horizontal_total = (1 + INDICE_PROGRESSAO_HORIZONTAL) ** (
            nivel.numero_progressoes_horizontais
        )

        valor = valor_inicial * progressao_vertical_total * progressao_horizontal_total

        return round(valor, 2)
