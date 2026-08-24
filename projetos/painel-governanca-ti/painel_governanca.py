"""Consolida incidentes e problemas em um painel de serviços de TI."""

import pandas as pd


def criar_bases_de_exemplo():
    incidentes = pd.DataFrame(
        {
            "servico": [
                "Serviço A",
                "Serviço B",
                "Serviço A",
                "Serviço C",
                "Serviço B",
            ],
            "ticket_id": [1, 2, 3, 4, 5],
            "prioridade": ["Alta", "Baixa", "Média", "Alta", "Baixa"],
        }
    )
    problemas = pd.DataFrame({"servico": ["Serviço A", "Serviço C"]})
    return incidentes, problemas


def montar_painel(incidentes, problemas):
    colunas_incidentes = {"servico", "ticket_id", "prioridade"}
    if not colunas_incidentes.issubset(incidentes.columns):
        raise ValueError("A base de incidentes não possui todas as colunas esperadas.")
    if "servico" not in problemas.columns:
        raise ValueError("A base de problemas precisa da coluna 'servico'.")

    total = incidentes.groupby("servico")["ticket_id"].count()
    alta = (
        incidentes.loc[incidentes["prioridade"].str.casefold() == "alta"]
        .groupby("servico")["ticket_id"]
        .count()
    )

    painel = pd.DataFrame(
        {
            "total_incidentes": total,
            "incidentes_prioridade_alta": alta,
        }
    )
    painel["incidentes_prioridade_alta"] = (
        painel["incidentes_prioridade_alta"].fillna(0).astype(int)
    )
    painel["problema_aberto"] = painel.index.isin(problemas["servico"])
    return painel.sort_values(
        ["incidentes_prioridade_alta", "total_incidentes"],
        ascending=False,
    )


def resumir_painel(painel):
    total_servicos = len(painel)
    com_problema = int(painel["problema_aberto"].sum())
    percentual = round(com_problema / total_servicos * 100, 1) if total_servicos else 0.0
    return {
        "total_servicos": total_servicos,
        "servicos_com_problema": com_problema,
        "percentual_com_problema": percentual,
    }


def main():
    incidentes, problemas = criar_bases_de_exemplo()
    painel = montar_painel(incidentes, problemas)
    resumo = resumir_painel(painel)

    print("\nPainel de governança de TI")
    print(painel.to_string())
    print(f'\nServiços monitorados: {resumo["total_servicos"]}')
    print(f'Serviços com problema aberto: {resumo["servicos_com_problema"]}')
    print(f'Percentual impactado: {resumo["percentual_com_problema"]}%')


if __name__ == "__main__":
    main()
