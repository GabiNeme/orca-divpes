from enum import Enum


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
        if value < 1 or value > 45:
            raise ValueError("O número do nível deve estar entre 1 e 45")
        self._numero = value

    @property
    def letra(self) -> str:
        return self._letra

    @letra.setter
    def letra(self, value: int) -> None:
        possiveis_letras = ["0", "A", "B", "C", "D", "E"]
        if value not in possiveis_letras:
            raise ValueError("A letra deve ser 0, A, B, C, D ou E")
        self._letra = value

    def __str__(self) -> str:
        return str(self.numero) + "." + self.letra


class Cargo:
    def __init__(self, classe: Classe, nivel: Nivel, e_procurador: bool) -> None:
        self.classe = classe
        self.nivel = nivel
        self.e_procurador = e_procurador
