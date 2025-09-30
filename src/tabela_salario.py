from functools import lru_cache

from src.nivel import Nivel
from src.classe import Classe
from src.parametros import parametros as p


class Tabela:
    @lru_cache(maxsize=None)
    @staticmethod
    def valor_do(nivel: Nivel, valor_inicial: float) -> float:
        """Calcula o valor do nível informado."""

        progressao_vertical_total = (1 + p.INDICE_PROGRESSAO_VERTICAL) ** (
            nivel.numero - 1
        )

        progressao_horizontal_total = (1 + p.INDICE_PROGRESSAO_HORIZONTAL) ** (
            nivel.numero_progressoes_horizontais
        )

        valor = valor_inicial * progressao_vertical_total * progressao_horizontal_total
        return round(valor, 2)

    @staticmethod
    def valor_do_nivel_para_classe(nivel: Nivel, classe: Classe) -> float:
        """Calcula o valor do nível informado para uma classe específica."""
        if classe == Classe.E1 or classe == Classe.E2:
            return Tabela.valor_do(nivel, p.VALOR_BASE_E2)

        return Tabela.valor_do(nivel, p.VALOR_BASE_E3)
