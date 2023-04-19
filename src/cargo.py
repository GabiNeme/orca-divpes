from enum import Enum

NIVEL_MINIMO = 1
NIVEL_MAXIMO = 47
POSSIVEIS_LETRAS = ["0", "A", "B", "C", "D", "E"]


class Classe(Enum):
    E2 = "E2"
    E3 = "E3"


class Nivel:
    def __init__(self, nivel: str) -> None:
        """Espera receber o nível no formato 5.A, por exemplo."""

        nivel_separado = nivel.strip().split(".")

        if len(nivel_separado) != 2:
            raise ValueError(
                "O nível informado não está no formato correto. "
                + "Deve ser 8.B, por exemplo."
            )

        self.numero = int(nivel_separado[0])
        self.letra = nivel_separado[1]

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, value: int) -> None:
        if value < NIVEL_MINIMO or value > NIVEL_MAXIMO:
            raise ValueError("O número do nível deve estar entre 1 e 45")
        self._numero = value

    @property
    def letra(self) -> str:
        return self._letra

    @letra.setter
    def letra(self, value: int) -> None:
        if value not in POSSIVEIS_LETRAS:
            raise ValueError("A letra deve ser 0, A, B, C, D ou E")
        self._letra = value

    @property
    def numero_progressoes_horizontais(self) -> int:
        """Retorna o número de progressões horizontais que aquela letra representa."""
        return POSSIVEIS_LETRAS.index(self.letra)

    def __str__(self) -> str:
        return str(self.numero) + "." + self.letra


class Cargo:
    def __init__(self, classe: Classe, nivel: Nivel, e_procurador: bool) -> None:
        self.classe = classe
        self.nivel = nivel
        self.e_procurador = e_procurador
