from dataclasses import dataclass
from datetime import date
from enum import Enum

from dateutil.relativedelta import relativedelta

IDADE_COMPULSORIA = 75


class Sexo(Enum):
    FEMININO = 2
    MASCULINO = 1


@dataclass
class DadosPrevidenciarios:
    data_nascimento: date
    sexo: Sexo
    data_admissao: date
    tempo_INSS: int
    tempo_sevico_publico: int


class Aposentadoria:
    def __init__(
        self, servidor: DadosPrevidenciarios, t_min_serv_pub: int, t_min_camara: int
    ) -> None:
        self.servidor = servidor
        self.T_MIN_SEV_PUB = t_min_serv_pub
        self.T_MIN_CAMARA = t_min_camara
        self._data_aposentadoria = None
        self._compulsoria = None

        if servidor.sexo == Sexo.MASCULINO:
            self.ANOS_CONTRIB = 35
            self.IDADE_MINIMA = 60
        elif servidor.sexo == Sexo.FEMININO:
            self.ANOS_CONTRIB = 30
            self.IDADE_MINIMA = 55

    @property
    def data_aposentadoria(self) -> date:
        if not self._data_aposentadoria:
            self._calcula_aposentadoria()
        return self._data_aposentadoria

    @property
    def compulsoria(self) -> bool:
        if not self._compulsoria:
            self._calcula_aposentadoria()
        return self._compulsoria

    def _calcula_aposentadoria(self):
        data_completa_cond_aposentadoria = max(
            self._data_por_tempo_contribuicao(),
            self._data_por_idade_minima(),
            self._data_por_tempo_minimo_servico_publico(),
            self._data_por_tempo_minimo_de_camara(),
        )

        compulsoria = self._data_compulsoria()

        if data_completa_cond_aposentadoria > compulsoria:
            self._compulsoria = True
            self._data_aposentadoria = compulsoria
            return

        self._compulsoria = False
        self._data_aposentadoria = data_completa_cond_aposentadoria

    def _data_por_tempo_contribuicao(self) -> date:
        return (
            self.servidor.data_admissao
            + relativedelta(years=self.ANOS_CONTRIB)
            - relativedelta(days=self.servidor.tempo_INSS)
            - relativedelta(days=self.servidor.tempo_sevico_publico)
        )

    def _data_por_idade_minima(self) -> date:
        return self.servidor.data_nascimento + relativedelta(years=self.IDADE_MINIMA)

    def _data_por_tempo_minimo_servico_publico(self) -> date:
        return (
            self.servidor.data_admissao
            + relativedelta(years=self.T_MIN_SEV_PUB)
            - relativedelta(days=self.servidor.tempo_sevico_publico)
        )

    def _data_por_tempo_minimo_de_camara(self) -> date:
        return self.servidor.data_admissao + relativedelta(years=self.T_MIN_CAMARA)

    def _data_compulsoria(self) -> date:
        return self.servidor.data_nascimento + relativedelta(years=IDADE_COMPULSORIA)
