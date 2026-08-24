# Cenário exclusivamente fictício para demonstração acadêmica.
# Os indicadores e valores não pertencem a nenhuma organização real.

dados_auditoria = {
    "IND_01": {
        "nome": "Transparencia de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    },
    "IND_02": {
        "nome": "Estrategia de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    },
    "IND_03": {
        "nome": "Projeto de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    },
    "IND_04": {
        "nome": "Operacao de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    },
    "IND_05": {
        "nome": "Conformidade de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    },
    "IND_06": {
        "nome": "Inovacao de exemplo",
        "valor_atual": 3.0,
        "meta": 4.0
    }
}

# Atividade 1: Classificação Automatizada
def classificar_dominio_cobit(indicador_nome):
    indicador = indicador_nome.lower()

    if "board" in indicador or "transparencia" in indicador or "meta_conselho" in indicador:
        return "EDM"
    elif "estrategia" in indicador or "orcamento" in indicador or "arquitetura" in indicador or "inovacao" in indicador:
        return "APO"
    elif "projeto" in indicador or "requisito" in indicador or "mudanca" in indicador:
        return "BAI"
    elif "operacao" in indicador or "suporte" in indicador or "seguranca" in indicador:
        return "DSS"
    elif "auditoria" in indicador or "conformidade" in indicador or "leis" in indicador:
        return "MEA"
    else:
        return "Nao Identificado"

print("--- Teste Atividade 1: Classificação de Domínios ---")
print(classificar_dominio_cobit("Seguranca de Operacoes Diarias"))  # DSS
print(classificar_dominio_cobit("Nivel de Transparencia do Board")) # EDM
print(classificar_dominio_cobit("ROI em Iniciativas de Inovacao"))  # APO
print()

# Atividade 2: Avaliação de Valor
def avaliar_geracao_de_valor(beneficios, custos, riscos):
    score_valor = (beneficios * 0.5) - (custos * 0.2) - (riscos * 0.3)

    if score_valor >= 5.0:
        status = "Aprovado pelo Conselho (Gera Valor Alinhado)"
    else:
        status = "Rejeitado: Alto risco/custo ou baixo retorno estratégico"

    return score_valor, status

print("--- Teste Atividade 2: Avaliação de Geração de Valor ---")
score, msg = avaliar_geracao_de_valor(beneficios=9.0, custos=4.0, riscos=3.0)
print(f"Score do Projeto: {score:.2f} | Decisão do Board: {msg}")
print()

# Atividade 3: Maturidade Customizada
def calcular_maturidade_customizada(pontuacoes_dominios, fator_foco):
    if fator_foco == 'seguranca':
        pesos = {"EDM": 0.20, "APO": 0.10, "BAI": 0.10, "DSS": 0.30, "MEA": 0.30}
    elif fator_foco == 'inovacao':
        pesos = {"EDM": 0.15, "APO": 0.30, "BAI": 0.35, "DSS": 0.10, "MEA": 0.10}
    else:
        pesos = {"EDM": 0.20, "APO": 0.20, "BAI": 0.20, "DSS": 0.20, "MEA": 0.20}

    nota_final = sum(pontuacoes_dominios.get(dom, 0) * pesos[dom] for dom in pesos)
    return nota_final

print("--- Teste Atividade 3: Maturidade por Fator de Desenho ---")
auditoria_atual = {"EDM": 3.0, "APO": 3.0, "BAI": 3.0, "DSS": 3.0, "MEA": 3.0}
print(f"Maturidade com foco INOVAÇÃO:  {calcular_maturidade_customizada(auditoria_atual, 'inovacao'):.2f}")
print(f"Maturidade com foco SEGURANÇA: {calcular_maturidade_customizada(auditoria_atual, 'seguranca'):.2f}")
print()

# Execução do Relatório Final
medias_dominios = {"EDM": [], "APO": [], "BAI": [], "DSS": [], "MEA": []}

for id_ind, info in dados_auditoria.items():
    dominio = classificar_dominio_cobit(info["nome"])
    if dominio != "Nao Identificado":
        medias_dominios[dominio].append(info["valor_atual"])

medias_finais = {k: (sum(v) / len(v) if v else 0) for k, v in medias_dominios.items()}

foco = input("Escolha o Foco Estratégico (inovacao/seguranca): ").strip().lower()

if foco not in ["inovacao", "seguranca"]:
    print(f"Entrada inválida. Usando foco padrão.")
    foco = "padrao"

nota_final = calcular_maturidade_customizada(medias_finais, foco)

print()
print("--- Relatório Executivo: Cenário Acadêmico Fictício ---")

# Visão do Board (Governança - EDM)
print("\n--- Visão do Board (Governança - EDM) ---")
nota_edm = medias_finais.get("EDM", 0)
print(f"Nota EDM: {nota_edm:.2f} / 5.00")

if nota_edm >= 4.0:
    status_edm = "Em Conformidade"
elif nota_edm >= 2.5:
    status_edm = "Abaixo do esperado pelo Conselho"
else:
    status_edm = "Critico"

print(f"Status: {status_edm}")
print(f"Indice de Maturidade Geral ({foco}): {nota_final:.2f} / 5.00")

# Visão Operacional (Gestão - APO/BAI/DSS/MEA)
print("\n--- Analise de Gaps (Gestão) ---")

encontrou_gap = False
for id_ind, info in dados_auditoria.items():
    dominio = classificar_dominio_cobit(info["nome"])
    if dominio != "EDM" and info["valor_atual"] < info["meta"]:
        gap = info["meta"] - info["valor_atual"]
        print(f"Alerta: {info['nome']} | Atual: {info['valor_atual']} < Meta: {info['meta']} (Abaixo da Meta - Critico)")
        encontrou_gap = True

if not encontrou_gap:
    print("Todos os indicadores operacionais estão dentro da meta.")
