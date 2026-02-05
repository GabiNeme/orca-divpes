from dataclasses import dataclass
from enum import Enum

from src.banco_de_dados import BancoDeDados


class ConcessaoLetras(Enum):
    NAO_CONCEDE = "NAO_CONCEDE"
    CONCEDE_UMA = "CONCEDE_UMA"
    CONCEDE_TODAS = "CONCEDE_TODAS"


@dataclass
class Parametros:
    # Tabela de salários
    VALOR_BASE_E2: float = None  # Importado do Aeros
    VALOR_BASE_E3: float = None  # Importado do Aeros
    INDICE_PROGRESSAO_VERTICAL: float = 0.04
    INDICE_PROGRESSAO_HORIZONTAL: float = 0.0816
    # Reajustes
    REAJUSTE_ANUAL: float = 0.0
    DATA_BASE_REAJUSTE: int = 5  # Maio
    # Tetos
    TETO_PREFEITO: float = None  # Importado do Aeros
    TETO_PROCURADORES: float = None  # Importado do Aeros
    # Previdência
    ALIQUOTA_PATRONAL: float = 0.22
    ALIQUOTA_PATRONAL_COMPLEMENTAR: float = 0.085
    TETO_INSS: float = None  # Importado do Aeros
    # Parâmetros de cálculo
    CONCESSAO_LETRAS: ConcessaoLetras = ConcessaoLetras.CONCEDE_TODAS

    @classmethod
    def from_aeros(cls, aeros: BancoDeDados):
        aeros_df = aeros.realiza_consulta_arquivo("parametros_aeros.sql")

        if aeros_df.empty:
            raise ValueError(
                "Não foi possível carregar parâmetros do Aeros: DataFrame vazio"
            )

        required_columns = [
            "valor_base_e2",
            "valor_base_e3",
            "teto_prefeito",
            "teto_procuradores",
            "teto_inss",
        ]

        # Extrai valores e checa se estão presentes e não são nulos
        valores = {}
        for col in required_columns:
            valor = aeros_df[col].iloc[0]
            if valor is None or (hasattr(valor, "isna") and valor.isna()):
                raise ValueError(
                    f"Coluna '{col}' tem valor nulo ou ausente no banco de dados."
                )
            valores[col] = float(valor)

        return cls(
            VALOR_BASE_E2=valores["valor_base_e2"],
            VALOR_BASE_E3=valores["valor_base_e3"],
            TETO_PREFEITO=valores["teto_prefeito"],
            TETO_PROCURADORES=valores["teto_procuradores"],
            TETO_INSS=valores["teto_inss"],
        )

    @classmethod
    def from_json(cls, json_data: dict):
        # Lê o parâmetro CONCESSAO_LETRAS como enum
        concessao_letras_bruto = json_data.get("CONCESSAO_LETRAS", None)
        if concessao_letras_bruto is None:
            concessao_letras = ConcessaoLetras.CONCEDE_TODAS
        if isinstance(concessao_letras_bruto, str):
            try:
                concessao_letras = ConcessaoLetras(concessao_letras_bruto)
            except ValueError:
                # Se não for um valor válido do enum, usa o padrão CONCEDE_TODAS
                concessao_letras = ConcessaoLetras.CONCEDE_TODAS
        else:
            concessao_letras = ConcessaoLetras.CONCEDE_TODAS

        return cls(
            VALOR_BASE_E2=json_data.get("VALOR_BASE_E2", None),
            VALOR_BASE_E3=json_data.get("VALOR_BASE_E3", None),
            INDICE_PROGRESSAO_VERTICAL=json_data.get(
                "INDICE_PROGRESSAO_VERTICAL", None
            ),
            INDICE_PROGRESSAO_HORIZONTAL=json_data.get(
                "INDICE_PROGRESSAO_HORIZONTAL", None
            ),
            REAJUSTE_ANUAL=json_data.get("REAJUSTE_ANUAL", None),
            DATA_BASE_REAJUSTE=json_data.get("DATA_BASE_REAJUSTE", None),
            TETO_PREFEITO=json_data.get("TETO_PREFEITO", None),
            TETO_PROCURADORES=json_data.get("TETO_PROCURADORES", None),
            ALIQUOTA_PATRONAL=json_data.get("ALIQUOTA_PATRONAL", None),
            ALIQUOTA_PATRONAL_COMPLEMENTAR=json_data.get(
                "ALIQUOTA_PATRONAL_COMPLEMENTAR", None
            ),
            TETO_INSS=json_data.get("TETO_INSS", None),
            CONCESSAO_LETRAS=concessao_letras,
        )


param = Parametros()
