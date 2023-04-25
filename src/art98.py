from datetime import date

from dateutil.relativedelta import relativedelta


class Art98:
    def __init__(
        self, data_inicio: date, usufruto: int, media_usufruto_cmbh: int = None
    ) -> None:
        self.data_inicio = data_inicio
        self.usufruto = usufruto
        self._media_usufruto_cmbh = media_usufruto_cmbh

    def media_usufruto_por_ano(self) -> int:
        """Calcula média de usufruto, caso não informado.

        Se for informada, na instanciação da classe, a média de usufruto da CMBH, essa
        média será retornada por essa funçõa. Caso contrário, será calculada a média
        anual de usufruto, sendo considerada como a divisão inteira entre o usufruto do
        servidor pelo número de anos completos desde o início do art. 98 e a data de
        execução dessa função.
        """
        if self._media_usufruto_cmbh:
            return self._media_usufruto_cmbh

        anos = relativedelta(date.today(), self.data_inicio).years
        return self.usufruto // anos

    def obtem_num_art98_para(self, data: date) -> int:
        """Calcula o número de dias de art. 98 para uma determinada data.

        Essa função calcula o número de concessões do art. 98 desde o início, e subtrai
        o usufruto efetivo, para o período anterior à projeção. Já para o período desde
        o momento de execução da função até a data informada, será subtraída, a cada
        ano projetado, a média de usufruto por ano, na forma da função
        `media_usufruto_por_ano`.
        """
        total_anos = relativedelta(data, self.data_inicio).years
        concessao = total_anos * 8 + (total_anos // 3) * 16 + (total_anos // 5) * 24

        media_usufruto = self.media_usufruto_por_ano()
        anos_projetados = relativedelta(data, date.today()).years
        usufruto_projetado = media_usufruto * anos_projetados

        num_art_98 = concessao - self.usufruto - usufruto_projetado

        if num_art_98 < 0:
            return 0
        return num_art_98
