from dataclasses import dataclass

from src.banco_de_dados import BancoDeDados


@dataclass
class Parametros:
    # Tabela de salários
    VALOR_BASE_E2: float = None  # Importado do Aeros
    VALOR_BASE_E3: float = None  # Importado do Aeros
    INDICE_PROGRESSAO_VERTICAL: float = 0.0391
    INDICE_PROGRESSAO_HORIZONTAL: float = 0.0797
    # Reajustes
    REAJUSTE_ANUAL: float = 0.1
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


param = Parametros()
