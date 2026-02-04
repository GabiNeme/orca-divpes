LETRAS = ["0", "A", "B", "C", "D", "E"]


class Nivel:
    def __init__(self, numero: int, letra: str) -> None:
        """Espera receber o número e a letra do nível, separadamente."""

        self.numero = numero
        self.letra = letra

    @classmethod
    def from_string(cls, nivel: str) -> None:
        """Espera receber o nível no formato 5.A, por exemplo."""

        nivel_separado = nivel.strip().split(".")

        if len(nivel_separado) != 2:
            raise ValueError(
                "O nível informado não está no formato correto. "
                + "Deve ser 8.B, por exemplo."
            )

        return cls(int(nivel_separado[0]), nivel_separado[1])

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, value: int) -> None:
        if value <= 0:
            raise ValueError("O número do nível deve ser maior que zero")
        self._numero = value

    @property
    def letra(self) -> str:
        return self._letra

    @letra.setter
    def letra(self, value: int) -> None:
        if value not in LETRAS:
            raise ValueError(
                f"Letra: {value} não reconhecido. As letras devem ser : "
                + ", ".join(LETRAS)
            )
        self._letra = value

    @property
    def numero_progressoes_horizontais(self) -> int:
        """Retorna o número de progressões horizontais que aquela letra representa."""
        return LETRAS.index(self.letra)

    def anterior(self, passos_verticais: int, passos_horizontais: int):
        prox_numero = self.numero - passos_verticais
        prox_letra = LETRAS[self.numero_progressoes_horizontais - passos_horizontais]
        return Nivel(prox_numero, prox_letra)

    def proximo(self, passos_verticais: int, passos_horizontais: int):
        prox_numero = self.numero + passos_verticais
        prox_letra = LETRAS[self.numero_progressoes_horizontais + passos_horizontais]
        return Nivel(prox_numero, prox_letra)

    def __str__(self) -> str:
        return str(self.numero) + "." + self.letra

    def __eq__(self, other):
        return self.numero == other.numero and self.letra == other.letra

    def __hash__(self) -> int:
        return self.numero * (self.numero_progressoes_horizontais + 1000)

    @staticmethod
    def nivel_horizontal_para_numero(letra: str) -> int:
        return LETRAS.index(letra)
