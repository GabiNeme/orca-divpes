import argparse
import json
import os
import sys

import config
from src.banco_de_dados import BancoDeDados
from src.cmbh import CMBH


def main(
    caminho_projecao_excel,
    ano_inicio,
    ano_fim,
    diretorio_resultado,
    recalcula_projecao=False,
):
    """Executa a lógica principal de exportação.

    Nota: essa função não carrega os parâmetros de configuração.
    Portanto, essa função espera que `config.param` já esteja definido pelo chamador.
    O helper CLI `run_from_argv` realiza o carregamento de parâmetros (do Aeros ou JSON)
    antes de chamar esta função.
    """
    cmbh: CMBH = CMBH.from_excel(
        caminho_projecao_excel, importa_folhas=not recalcula_projecao
    )
    if recalcula_projecao:
        cmbh.calcula_projecao(ano_inicio, ano_fim)
        cmbh.exporta_progressoes(diretorio_resultado)

    cmbh.exporta(diretorio_resultado, ano_inicio, ano_fim)
    print(
        f"Exportação concluída para {diretorio_resultado} "
        f"dos anos {ano_inicio} a {ano_fim}."
    )


def run_from_argv(argv=None):
    """Analisa os argumentos da CLI e executa.

    Retorna 0 em caso de sucesso, um número diferente de zero em caso de falha.
    Este helper pode ser testado passando uma lista de argumentos em `argv`
    (excluindo o nome do programa).
    """
    parser = argparse.ArgumentParser(
        description="Exporta projeções a partir de planilha e parâmetros"
    )
    parser.add_argument(
        "caminho_projecao_excel", help="Caminho do arquivo de projeção (xlsx)"
    )
    parser.add_argument("ano_inicio", type=int, help="Ano inicial da projeção")
    parser.add_argument("ano_fim", type=int, help="Ano final da projeção")
    parser.add_argument(
        "diretorio_resultado", help="Diretório onde os resultados serão salvos"
    )
    parser.add_argument(
        "--recalcula-projecao",
        action="store_true",
        help="Se informado, recalcula a projeção antes de exportar",
    )
    parser.add_argument(
        "--parametros-json",
        dest="parametros_json",
        help="Caminho para um arquivo JSON com parâmetros (usará Parametros.from_json)",
    )

    args = parser.parse_args(argv)

    # Load parameters: from JSON if provided, else from Aeros database
    if args.parametros_json:
        json_path = args.parametros_json
        if not os.path.exists(json_path):
            print(f"Arquivo de parâmetros JSON não encontrado: {json_path}")
            return 1
        try:
            with open(json_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:  # json decode error, permission error, etc.
            print(f"Falha ao ler/parsing do JSON de parâmetros: {exc}")
            return 1
        try:
            config.param = config.Parametros.from_json(data)
        except Exception as exc:
            print(f"Falha ao construir Parametros a partir do JSON: {exc}")
            return 1
    else:
        # fallback: load from Aeros DB
        try:
            config.param = config.Parametros.from_aeros(BancoDeDados())
        except Exception as exc:
            print(f"Falha ao carregar parâmetros do Aeros: {exc}")
            return 1

    try:
        main(
            args.caminho_projecao_excel,
            args.ano_inicio,
            args.ano_fim,
            args.diretorio_resultado,
            recalcula_projecao=args.recalcula_projecao,
        )
    except Exception as exc:
        print(f"Erro ao executar exportação: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    rv = run_from_argv(sys.argv[1:])
    sys.exit(rv)
