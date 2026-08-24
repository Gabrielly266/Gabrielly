"""Auditoria de acessos com bases de demonstração exclusivamente fictícias."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DIRETORIO = Path(__file__).resolve().parent
ARQUIVO_LOGS = DIRETORIO / "log_acessos_200_registros.csv"
ARQUIVO_USUARIOS = DIRETORIO / "usuarios_ativos_200_registros.csv"
ARQUIVO_GRAFICO = DIRETORIO / "riscos_seguranca.png"


def carregar_bases(arquivo_logs=ARQUIVO_LOGS, arquivo_usuarios=ARQUIVO_USUARIOS):
    logs = pd.read_csv(arquivo_logs)
    usuarios = pd.read_csv(arquivo_usuarios)
    esperadas = {"usuario_id", "data_hora", "status", "ip"}

    if not esperadas.issubset(logs.columns):
        raise ValueError("A base de acessos não possui todas as colunas necessárias.")
    if "usuario_id" not in usuarios.columns:
        raise ValueError("A base de usuários precisa da coluna 'usuario_id'.")

    logs["data_hora"] = pd.to_datetime(logs["data_hora"], errors="coerce")
    if logs["data_hora"].isna().any():
        raise ValueError("A base de acessos contém datas inválidas.")
    return logs, usuarios


def auditar_acessos(logs, usuarios):
    auditoria = logs.merge(usuarios, on="usuario_id", how="left", indicator=True)
    contas_orfas = auditoria.loc[auditoria["_merge"].eq("left_only")].copy()
    fora_horario = auditoria.loc[
        auditoria["data_hora"].dt.hour.lt(8)
        | auditoria["data_hora"].dt.hour.ge(18)
    ].copy()
    ips_externos = auditoria.loc[
        auditoria["status"].str.casefold().eq("sucesso")
        & ~auditoria["ip"].astype(str).str.startswith("192.168.")
    ].copy()

    indices_suspeitos = contas_orfas.index.union(fora_horario.index)
    return {
        "total": len(auditoria),
        "autorizados": len(auditoria) - len(indices_suspeitos),
        "contas_orfas": contas_orfas,
        "fora_horario": fora_horario,
        "ips_externos": ips_externos,
    }


def salvar_grafico(resultado, destino=ARQUIVO_GRAFICO):
    categorias = ["Autorizados", "Fora do horário", "Contas órfãs"]
    quantidades = [
        resultado["autorizados"],
        len(resultado["fora_horario"]),
        len(resultado["contas_orfas"]),
    ]
    figura, eixo = plt.subplots(figsize=(7, 4))
    eixo.bar(categorias, quantidades, color=["#2a9d8f", "#e9c46a", "#e76f51"])
    eixo.set_title("Resultado da auditoria de acessos")
    eixo.set_ylabel("Quantidade de registros")
    figura.tight_layout()
    figura.savefig(destino, dpi=150)
    plt.close(figura)


def main():
    logs, usuarios = carregar_bases()
    resultado = auditar_acessos(logs, usuarios)
    salvar_grafico(resultado)

    print(f'Registros analisados: {resultado["total"]}')
    print(f'Contas órfãs: {len(resultado["contas_orfas"])}')
    print(f'Acessos fora do horário: {len(resultado["fora_horario"])}')
    print(f'IPs externos: {len(resultado["ips_externos"])}')
    print(f"Gráfico salvo em {ARQUIVO_GRAFICO.name}.")


if __name__ == "__main__":
    main()
