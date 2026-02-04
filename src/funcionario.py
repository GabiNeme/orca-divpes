from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

from src.carreira import Carreira, Progressao
from src.classe import Classe
from src.nivel import Nivel
from src.progressoes_horizontais import progressoes_horizontais


class TipoPrevidencia(Enum):
    Fufin = "Fufin"
    BHPrev = "BHPrev"
    BHPrevComplementar = "BHPrevComplementar"


@dataclass
class DadosFolha:
    classe: Classe
    data_anuenio: date
    num_ats: int
    procurador: bool
    tipo_previdencia: TipoPrevidencia


@dataclass
class Aposentadoria:
    data_condicao_aposentadoria: date
    data_aposentadoria: date
    num_art_98_data_aposentadoria: int
    aderiu_pia: bool


class Funcionario:
    def __init__(
        self,
        cm: int,
        data_admissao: date,
        dados_folha: DadosFolha,
        aposentadoria: Aposentadoria,
        ultima_progressao: Progressao,
        carreira: Carreira,
    ):
        self.cm = cm
        self.data_admissao = data_admissao
        self.dados_folha = dados_folha
        self.aposentadoria = aposentadoria
        self.progressoes = [ultima_progressao]
        self.carreira = carreira

    def _calcula_progressoes_ate(self, data: date):
        ultima_progressao = self.progressoes[-1]

        while ultima_progressao and data > ultima_progressao.data:
            # Sempre progride verticalmente e horizontalmente respeitando a letra máxima.
            # Quando a letra máxima for None, progride até o máximo permitido.
            ultima_progressao = self.carreira.progride_verticalmente_e_horizontalmente(
                ultima_progressao,
                letra_maxima=progressoes_horizontais.obtem_letra_maxima(self.cm),
                data_condicao_aposentadoria=self.aposentadoria.data_condicao_aposentadoria,
            )

            if ultima_progressao:
                self.progressoes.append(ultima_progressao)

    def obtem_nivel_para(self, data: date) -> Optional[Nivel]:
        """Retorna o nível que o servidor estará em determinada data.
        Se tiver aposentado, retorna None"""

        # Se a data for após o dia 1o, muda para o dia 1o
        if data.day > 1:
            data = date(data.year, data.month, 1)
        if data <= self.data_admissao:  # Funcionário não admitido
            return None
        if data > self.aposentadoria.data_aposentadoria:  # Funcionário aposentado
            return None

        self._calcula_progressoes_ate(data)

        for progressao in reversed(self.progressoes):
            dt_prog = progressao.data
            if dt_prog < data or (
                dt_prog.month == data.month and dt_prog.year == data.year
            ):
                return progressao.nivel

    def to_dict(self):
        return {
            "CM": self.cm,
            "Data admissão": self.data_admissao,
            "Classe": self.dados_folha.classe.value,
            "Data anuênio": self.dados_folha.data_anuenio,
            "Num ATS": self.dados_folha.num_ats,
            "Procurador": self.dados_folha.procurador,
            "Tipo Previdência": self.dados_folha.tipo_previdencia.value,
            "Data Condição Aposentadoria": self.aposentadoria.data_condicao_aposentadoria,
            "Data Aposentadoria": self.aposentadoria.data_aposentadoria,
            "Num Art 98 Data Aposentadoria": self.aposentadoria.num_art_98_data_aposentadoria,
            "Aderiu PIA": self.aposentadoria.aderiu_pia,
        }
