import os
from datetime import date

import pandas as pd

from src.excel_exporter import to_excel_formatted
from src.folhas_efetivos import FolhasEfetivos
from src.folhas_pia import FolhasPIA
from src.importador_excel import ImportadorProjecaoExcel


class CMBH:

    def __init__(self, folhas_efetivos=FolhasEfetivos, folhas_pia=FolhasPIA):
        """Inicializa a classe CMBH."""
        self.funcionarios = {}  # {cm: Funcionario}
        self.folhas_efetivos = folhas_efetivos()
        self.folhas_pia = folhas_pia()

    @classmethod
    def from_excel(cls, caminho_excel: str, importa_folhas: bool = True) -> "CMBH":
        """Cria uma instância de CMBH a partir de um arquivo Excel."""

        return ImportadorProjecaoExcel().importa(
            caminho_excel, importa_folhas=importa_folhas
        )

    def calcula_projecao(self, ano_inicio: int, ano_fim: int):
        """Calcula as folhas de pagamento e PIAs para o intervalo de anos especificado."""
        comp_inicio = date(ano_inicio, 1, 1)
        comp_fim = date(ano_fim, 12, 1)

        funcionarios = list(self.funcionarios.values())
        self.folhas_efetivos.calcula_folhas(funcionarios, comp_inicio, comp_fim)
        self.folhas_pia.calcula_pias(funcionarios)

    def escreve_totais_mensais(
        self, ano_inicio: int, ano_fim: int, writer: pd.ExcelWriter
    ) -> None:
        """Exporta os totais das folhas para uma única planilha do Excel, juntando por competência."""
        df_efetivos = self.folhas_efetivos.total_mensal_no_intervalo(
            ano_inicio, ano_fim
        )
        df_pia = self.folhas_pia.total_mensal_no_intervalo(ano_inicio, ano_fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on=["ano", "competencia"], how="outer")

        to_excel_formatted(df_total, writer, sheet_name="Totais Mensais", index=False)

    def escreve_totais_anuais(
        self, ano_inicio: int, ano_fim: int, writer: pd.ExcelWriter
    ) -> None:
        """Exporta os totais anuais das folhas para uma única planilha do Excel, juntando por ano."""
        df_efetivos = self.folhas_efetivos.total_anual_no_intervalo(ano_inicio, ano_fim)
        df_pia = self.folhas_pia.total_anual_no_intervalo(ano_inicio, ano_fim)

        # Merge usando a coluna 'competencia'
        df_total = pd.merge(df_efetivos, df_pia, on=["ano"], how="outer")

        to_excel_formatted(df_total, writer, sheet_name="Totais Anuais", index=True)

    def escreve_folhas_servidores_efetivos(
        self, ano_inicio: int, ano_fim: int, writer: pd.ExcelWriter
    ) -> None:
        """Exporta cada funcionário para uma planilha do Excel, contendo folhas do PIA e mensal."""
        comp_inicio = date(ano_inicio, 1, 1)
        comp_fim = date(ano_fim, 12, 1)

        for funcionario in self.funcionarios.values():
            cm = funcionario.cm
            df_folhas = self.folhas_efetivos.exporta_folhas_do_funcionario(
                cm, comp_inicio, comp_fim
            )
            df_pia = self.folhas_pia.exporta_pia_do_funcionario(
                cm, comp_inicio, comp_fim
            )

            df_total = pd.merge(df_folhas, df_pia, on=["Competência"], how="outer")
            to_excel_formatted(df_total, writer, sheet_name=str(cm), index=False)

    def escreve_servidores(self, writer: pd.ExcelWriter) -> None:
        """Exporta os dados dos servidores para uma planilha do Excel."""
        dados = []
        for funcionario in self.funcionarios.values():
            dados.append(funcionario.to_dict())

        df = pd.DataFrame(dados)
        to_excel_formatted(df, writer, sheet_name="Efetivos", index=False)

    def escreve_metricas(
        self, ano_inicio: int, ano_fim: int, writer: pd.ExcelWriter
    ) -> None:
        """Exporta as métricas das folhas para uma planilha do Excel."""
        comp_inicio = date(ano_inicio, 1, 1)
        comp_fim = date(ano_fim, 12, 1)

        df_metricas_efetivos = self.folhas_efetivos.calcula_metricas(
            comp_inicio, comp_fim
        )
        to_excel_formatted(
            df_metricas_efetivos, writer, sheet_name="Métricas", index=False
        )

    def exporta(
        self,
        diretorio_resultado: str,
        ano_inicio: int,
        ano_fim: int,
        dados_servidores: bool = True,
        totalizadores: bool = True,
    ):
        if not dados_servidores and not totalizadores:
            print("Nenhum dado selecionado para exportação.")
            return
        if dados_servidores:
            arquivo_servidores = os.path.join(diretorio_resultado, "servidores.xlsx")
            with pd.ExcelWriter(arquivo_servidores, engine="openpyxl") as writer:
                self.escreve_servidores(writer=writer)
                self.escreve_metricas(
                    ano_inicio=ano_inicio, ano_fim=ano_fim, writer=writer
                )
                self.escreve_folhas_servidores_efetivos(
                    ano_inicio=ano_inicio, ano_fim=ano_fim, writer=writer
                )
        if totalizadores:
            arquivo_totalizadores = os.path.join(
                diretorio_resultado, "totalizadores.xlsx"
            )
            with pd.ExcelWriter(arquivo_totalizadores, engine="openpyxl") as writer:
                self.escreve_totais_mensais(
                    ano_inicio=ano_inicio, ano_fim=ano_fim, writer=writer
                )
                self.escreve_totais_anuais(
                    ano_inicio=ano_inicio, ano_fim=ano_fim, writer=writer
                )

    def exporta_progressoes(self, diretorio_resultado: str) -> None:
        """Exporta as progressões dos funcionários para um arquivo Excel."""
        arquivo_progressoes = os.path.join(diretorio_resultado, "progressoes.xlsx")
        with pd.ExcelWriter(arquivo_progressoes, engine="openpyxl") as writer:
            for funcionario in self.funcionarios.values():
                dados = []
                for prog in funcionario.progressoes:
                    dados.append(
                        {
                            "Data Progressão": prog.data,
                            "Novo Nível": str(prog.nivel),
                            "No progressões sem especial": prog.progs_sem_especial,
                        }
                    )

                df = pd.DataFrame(dados)
                to_excel_formatted(
                    df, writer, sheet_name=str(funcionario.cm), index=False
                )
