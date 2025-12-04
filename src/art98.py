from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta


@dataclass
class DadosArt98:
    data_inicio: date
    usufruto: int


class Art98:
    def __init__(self, dados_art98: DadosArt98, media_usufruto_cmbh: int = 0) -> None:
        self.dados_art98 = dados_art98
        self._media_usufruto_cmbh = media_usufruto_cmbh

    def __init__(
        self, data_inicio: date, usufruto: int, media_usufruto_cmbh: int = 0
    ) -> None:
        self.dados_art98 = DadosArt98(data_inicio, usufruto)
        self._media_usufruto_cmbh = media_usufruto_cmbh

    def media_usufruto_por_ano(self) -> int:
        """Calcula média de usufruto, caso início do art 98 seja maior que a data atual.

        Se a data de início for maior que a data atual, retorna o usufruto médio do CMBH.
        Caso contrário, será calculada a média anual de usufruto, sendo considerada como
        a divisão inteira entre o usufruto do servidor pelo número de anos completos.
        """
        if self.dados_art98.data_inicio > date.today():
            return self._media_usufruto_cmbh
        return self.calcula_media_usufruto_por_ano(self.dados_art98)

    def obtem_num_art98_para(self, data: date) -> int:
        """Calcula o número de dias de art. 98 para uma determinada data.

        Essa função calcula o número de concessões do art. 98 desde o início, e subtrai
        o usufruto efetivo, para o período anterior à projeção. Já para o período desde
        o momento de execução da função até a data informada, será subtraída, a cada
        ano projetado, a média de usufruto por ano, na forma da função
        `media_usufruto_por_ano`.
        """
        total_anos = relativedelta(data, self.dados_art98.data_inicio).years
        concessao = total_anos * 8 + (total_anos // 3) * 16 + (total_anos // 5) * 24

        media_usufruto = self.media_usufruto_por_ano()
        anos_projetados = relativedelta(data, date.today()).years
        usufruto_projetado = media_usufruto * anos_projetados

        num_art_98 = concessao - self.dados_art98.usufruto - usufruto_projetado

        if num_art_98 < 0:
            return 0
        return num_art_98

    @staticmethod
    def calcula_media_usufruto_por_ano(dados_art98: DadosArt98) -> int:
        """Calcula a média de usufruto por ano, considerando o usufruto do servidor."""
        anos = relativedelta(date.today(), dados_art98.data_inicio).years
        if anos == 0:
            return 0
        return dados_art98.usufruto // anos

    @staticmethod
    def calcula_media_usufruto_art98_cmbh(dados_art98: list[DadosArt98]) -> int:
        """Calcula a média de usufruto do art. 98 da CMBH."""
        if not dados_art98 or len(dados_art98) == 0:
            return 0

        usufruto_anual_cmbh = 0
        for dados in dados_art98:
            usufruto_anual_cmbh += Art98.calcula_media_usufruto_por_ano(dados)
            print(dados.data_inicio, dados.usufruto, usufruto_anual_cmbh)

        return int(usufruto_anual_cmbh / len(dados_art98))
