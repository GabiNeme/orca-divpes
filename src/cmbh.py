from datetime import date
from src.carreira import atribui_carreira
from src.classe import Classe
from src.folha import Folha
from src.folhas_efetivos import FolhasEfetivos
import pandas as pd

from src.banco_de_dados import BancoDeDados
from src.folhas_pia import FolhasPIA
from src.funcionario import Funcionario
from src.funcionario_factory import FuncionarioFactory
from src.nivel import Nivel
from src.regra_transicao import RegraTransicao


class CMBH:

    def __init__(self):
        """Inicializa a classe CMBH."""
        self.funcionarios = {}  # {cm: Funcionario}
        self.folhas_efetivos = FolhasEfetivos()
        self.folhas_pia = FolhasPIA()

    @classmethod
    def from_excel(cls, caminho_excel: str, importa_folhas: bool = True) -> "CMBH":
        """Cria uma instância de CMBH a partir de um arquivo Excel."""

        return ImportadorProjecaoExcel().importa(
            caminho_excel, importa_folhas=importa_folhas
        )

    def exporta_totais_para(self, inicio: date, fim: date, caminho_excel: str) -> None:
        """Exporta os totais das folhas para uma única planilha do Excel, juntando por competência."""
        df_efetivos = self.folhas_efetivos.total_no_intervalo_para_dataframe(
            inicio, fim
        )
        df_pia = self.folhas_pia.total_no_intervalo_para_dataframe(inicio, fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on="competencia", how="outer")

        with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
            df_total.to_excel(writer, sheet_name="Totais", index=False)


def obtem_tempos_licencas() -> dict[int, int]:
    """Obtém os tempos de licenças que interrompem contagem de progressão dos funcionários."""
    with open("sql/tempo_licencas.sql", "r", encoding="utf-8") as f:
        sql_query = f.read()
    df_licencas = BancoDeDados().realiza_consulta(sql_query)
    # Cria o dicionário indexado por cm
    return dict(zip(df_licencas["cm"], df_licencas["qtde_dias_licenca"]))


class ImportadorProjecaoExcel:

    def __init__(self, funcao_obtem_tempos_licencas=obtem_tempos_licencas):
        """Inicializa o importador de projeção Excel."""
        self.licencas = funcao_obtem_tempos_licencas()  # {cm: qtde_dias_licenca}
        self.cmbh = CMBH()

    def importa(self, caminho_excel: str, importa_folhas: bool = True) -> CMBH:
        """Importa os dados de funcionários de um arquivo Excel."""
        xls = pd.ExcelFile(caminho_excel)

        for sheet_name in xls.sheet_names:
            try:
                cm = int(sheet_name)
            except ValueError:
                continue  # Pula abas que não são Funcionario

            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

            # As duas primeiras linhas contêm dados do Funcionario
            funcionario_data = df.iloc[0:2].values
            funcionario = self._cria_funcionario_da_linha(funcionario_data)
            self.cmbh.funcionarios[cm] = funcionario

            if not importa_folhas:
                continue

            # Linhas 4 em diante são Folhas de pagamento
            folhas_data = df.iloc[3:]
            for _, linha in folhas_data.iterrows():
                if pd.isna(linha[4]):  # nível vazio, não tem folha
                    continue

                self._adiciona_folha_da_linha(funcionario.cm, linha)
                self._adiciona_pia_da_linha(funcionario.cm, linha)

        return self.cmbh

    def _cria_funcionario_da_linha(self, linha) -> Funcionario:

        def _parse_data(data):
            """Converte datetime to date."""
            return data.date()

        cm = int(linha[1][0])
        data_admissao = _parse_data(linha[1][1])
        classe = Classe(linha[1][2])
        data_anuenio = _parse_data(linha[1][6])
        num_ats = int(linha[1][7]) if not pd.isna(linha[1][7]) else 0
        procurador = linha[1][12] == "S"
        data_aposentadoria = _parse_data(linha[1][17])
        num_art_98_data_aposentadoria = (
            int(linha[1][18]) if not pd.isna(linha[1][18]) else 0
        )
        aderiu_pia = linha[1][20] == "S"
        ultima_progressao = RegraTransicao.primeira_progressao(
            data_admissao, procurador, self.licencas.get(cm, 0)
        )
        carreira = atribui_carreira(cm)
        grupo_de_controle = int(linha[1][15])

        return FuncionarioFactory.cria_funcionario(
            cm=cm,
            data_admissao=data_admissao,
            classe=classe,
            data_anuenio=data_anuenio,
            num_ats=num_ats,
            procurador=procurador,
            data_aposentadoria=data_aposentadoria,
            num_art_98_data_aposentadoria=num_art_98_data_aposentadoria,
            aderiu_pia=aderiu_pia,
            ultima_progressao=ultima_progressao,
            carreira=carreira,
            grupo_de_controle=grupo_de_controle,
        )

    def _adiciona_folha_da_linha(self, cm: int, linha) -> None:

        def _parse_float(valor_str):
            return round(float(valor_str), 2) if not pd.isna(valor_str) else 0.0

        competencia = date(year=int(linha[0]), month=int(linha[1]), day=1)
        folha = Folha(
            nivel=Nivel.from_string(linha[4]),
            salario=_parse_float(linha[5]),
            anuenio=_parse_float(linha[9]),
            ats=_parse_float(linha[7]),
            total_antes_limite_prefeito=_parse_float(linha[13]),
            total=_parse_float(linha[14]),
            fufin_patronal=_parse_float(linha[15]),
            bhprev_patronal=_parse_float(linha[16]),
            bhprev_complementar_patronal=_parse_float(linha[17]),
        )
        return self.cmbh.folhas_efetivos.adiciona_folha(competencia, cm, folha)

    def _adiciona_pia_da_linha(self, cm: int, linha) -> None:

        if pd.isna(linha[19]):
            return

        competencia = date(year=int(linha[0]), month=int(linha[1]), day=1)
        pia = round(float(linha[19]), 2)

        return self.cmbh.folhas_pia.adiciona_pia(competencia, cm, pia)
