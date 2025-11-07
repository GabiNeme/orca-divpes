from dataclasses import dataclass

from src.banco_de_dados import BancoDeDados


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
        )


param = Parametros()
