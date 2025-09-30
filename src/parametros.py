from dataclasses import dataclass
import json
import os


@dataclass
class Parametros:
    # Tabela de salários
    VALOR_BASE_E2: float = 5758.83
    VALOR_BASE_E3: float = 10047.80
    INDICE_PROGRESSAO_VERTICAL: float = 0.0391
    INDICE_PROGRESSAO_HORIZONTAL: float = 0.0797
    # Reajustes
    REAJUSTE_ANUAL: float = 0.1
    DATA_BASE_REAJUSTE: int = 5 # Maio
    # Tetos
    TETO_PREFEITO: float = 34604.05
    TETO_PROCURADORES: float = 41845.49
    # Previdência
    ALIQUOTA_PATRONAL: float = 0.22
    ALIQUOTA_PATRONAL_COMPLEMENTAR: float = 0.085
    TETO_INSS: float = 8157.41

    @classmethod
    def from_json(cls, json_path=None):
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), "parametros.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                params = json.load(f)
            return cls(
                indice_progressao_vertical=params.get(
                    "indice_progressao_vertical", cls.indice_progressao_vertical
                ),
                indice_progressao_horizontal=params.get(
                    "indice_progressao_horizontal", cls.indice_progressao_horizontal
                ),
                valor_base_e2=params.get("valor_base_e2", cls.valor_base_e2),
                valor_base_e3=params.get("valor_base_e3", cls.valor_base_e3),
            )
        return cls()

parametros = Parametros()
