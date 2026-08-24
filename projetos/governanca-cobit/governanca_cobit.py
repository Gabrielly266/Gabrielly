"""Avaliação acadêmica dos domínios do COBIT com indicadores fictícios."""

from collections import defaultdict


INDICADORES_DE_EXEMPLO = [
    {"nome": "Transparência de exemplo", "valor_atual": 3.0, "meta": 4.0},
    {"nome": "Estratégia de exemplo", "valor_atual": 3.0, "meta": 4.0},
    {"nome": "Projeto de exemplo", "valor_atual": 3.0, "meta": 4.0},
    {"nome": "Operação de exemplo", "valor_atual": 3.0, "meta": 4.0},
    {"nome": "Conformidade de exemplo", "valor_atual": 3.0, "meta": 4.0},
    {"nome": "Inovação de exemplo", "valor_atual": 3.0, "meta": 4.0},
]

PALAVRAS_POR_DOMINIO = {
    "EDM": ("transparência", "conselho", "governança"),
    "APO": ("estratégia", "inovação", "planejamento"),
    "BAI": ("projeto", "requisito", "mudança"),
    "DSS": ("operação", "suporte", "segurança"),
    "MEA": ("auditoria", "conformidade", "monitoramento"),
}

PESOS_POR_FOCO = {
    "seguranca": {"EDM": 0.20, "APO": 0.10, "BAI": 0.10, "DSS": 0.30, "MEA": 0.30},
    "inovacao": {"EDM": 0.15, "APO": 0.30, "BAI": 0.35, "DSS": 0.10, "MEA": 0.10},
    "padrao": {"EDM": 0.20, "APO": 0.20, "BAI": 0.20, "DSS": 0.20, "MEA": 0.20},
}


def classificar_dominio_cobit(indicador):
    texto = indicador.casefold()
    for dominio, palavras in PALAVRAS_POR_DOMINIO.items():
        if any(palavra in texto for palavra in palavras):
            return dominio
    return None


def calcular_medias_por_dominio(indicadores):
    valores = defaultdict(list)
    for indicador in indicadores:
        dominio = classificar_dominio_cobit(indicador["nome"])
        if dominio is not None:
            valores[dominio].append(indicador["valor_atual"])

    return {
        dominio: sum(valores[dominio]) / len(valores[dominio]) if valores[dominio] else 0.0
        for dominio in PALAVRAS_POR_DOMINIO
    }


def calcular_maturidade_customizada(pontuacoes, foco="padrao"):
    pesos = PESOS_POR_FOCO.get(foco, PESOS_POR_FOCO["padrao"])
    return sum(pontuacoes.get(dominio, 0.0) * peso for dominio, peso in pesos.items())


def identificar_desvios(indicadores):
    return [
        {
            "nome": indicador["nome"],
            "dominio": classificar_dominio_cobit(indicador["nome"]),
            "diferenca": round(indicador["meta"] - indicador["valor_atual"], 2),
        }
        for indicador in indicadores
        if indicador["valor_atual"] < indicador["meta"]
    ]


def main():
    foco = input("Foco da análise (inovacao/seguranca): ").strip().casefold()
    if foco not in ("inovacao", "seguranca"):
        foco = "padrao"

    medias = calcular_medias_por_dominio(INDICADORES_DE_EXEMPLO)
    maturidade = calcular_maturidade_customizada(medias, foco)

    print("\nAvaliação de governança — cenário fictício")
    for dominio, media in medias.items():
        print(f"{dominio}: {media:.1f}/5")
    print(f"\nMaturidade geral ({foco}): {maturidade:.2f}/5")

    print("\nIndicadores abaixo da meta")
    for desvio in identificar_desvios(INDICADORES_DE_EXEMPLO):
        print(f'- {desvio["nome"]} ({desvio["dominio"]}): {desvio["diferenca"]:.1f}')


if __name__ == "__main__":
    main()
