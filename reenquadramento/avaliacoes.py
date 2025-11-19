from dataclasses import dataclass
from datetime import date


@dataclass
class Avaliacao:
    inicio_intersticio: date
    nota: float


class Avaliacoes:
    def __init__(self):
        self.avaliacoes = {}  # {cm: List[Avaliacao]}

    @classmethod
    def from_excel(cls, caminho_excel: str = "reenquadramento\\notas.xlsx"):
        """Carrega avaliações a partir de um arquivo Excel."""
        import pandas as pd

        df = pd.read_excel(caminho_excel, sheet_name="Sheet0")

        instancia = cls()

        for _, row in df.iterrows():
            cm: int = int(row["cm"])
            intersticio: date = row["inicio"]
            nota: float = float(row["nota"])

            instancia.avaliacoes.setdefault(cm, []).append(
                Avaliacao(inicio_intersticio=intersticio, nota=nota)
            )

        return instancia

    def do_cm(self, cm: int) -> list[Avaliacao]:
        """Retorna a avaliação de um funcionário pelo seu cm."""
        return self.avaliacoes.get(cm)
