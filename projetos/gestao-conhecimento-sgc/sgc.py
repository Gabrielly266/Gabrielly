"""Base de conhecimento simples, com pesquisa e armazenamento em JSON."""

import json
from pathlib import Path


ARQUIVO_DADOS = Path(__file__).with_name("base_conhecimento.json")

BASE_INICIAL = [
    {
        "id": 1,
        "titulo": "Primeiros passos no sistema",
        "conteudo": "Consulte o guia introdutório da aplicação.",
        "acessos": 12,
    },
    {
        "id": 2,
        "titulo": "Consultas em banco de dados",
        "conteudo": "Exemplo didático de consulta SQL.",
        "acessos": 5,
    },
    {
        "id": 3,
        "titulo": "Organização de documentos",
        "conteudo": "Padronize os nomes e as categorias dos arquivos.",
        "acessos": 8,
    },
]


def carregar_dados(caminho=ARQUIVO_DADOS):
    caminho = Path(caminho)
    if not caminho.exists():
        return [item.copy() for item in BASE_INICIAL]

    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as erro:
        raise ValueError(f"Não foi possível carregar a base: {erro}") from erro


def salvar_dados(base, caminho=ARQUIVO_DADOS):
    caminho = Path(caminho)
    caminho.write_text(
        json.dumps(base, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def buscar_conhecimento(base, termo):
    termo = termo.strip().casefold()
    if not termo:
        return []

    return [
        item
        for item in base
        if termo in item["titulo"].casefold()
        or termo in item["conteudo"].casefold()
    ]


def adicionar_conhecimento(base, titulo, conteudo):
    titulo = titulo.strip()
    conteudo = conteudo.strip()
    if not titulo or not conteudo:
        raise ValueError("Título e conteúdo são obrigatórios.")

    registro = {
        "id": max((item["id"] for item in base), default=0) + 1,
        "titulo": titulo,
        "conteudo": conteudo,
        "acessos": 0,
    }
    base.append(registro)
    return registro


def exibir_dashboard(base):
    print("\nArtigos mais consultados")
    print("-" * 32)
    for item in sorted(base, key=lambda registro: registro["acessos"], reverse=True):
        print(f'{item["titulo"]:<30} {item["acessos"]:>3} acessos')


def menu():
    try:
        base = carregar_dados()
    except ValueError as erro:
        print(erro)
        return

    while True:
        print("\n1. Ver dashboard")
        print("2. Pesquisar")
        print("3. Adicionar artigo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            exibir_dashboard(base)
        elif opcao == "2":
            resultados = buscar_conhecimento(base, input("Pesquisar por: "))
            if not resultados:
                print("Nenhum artigo encontrado.")
                continue

            for artigo in resultados:
                artigo["acessos"] += 1
                print(f'\n{artigo["titulo"]}\n{artigo["conteudo"]}')
            salvar_dados(base)
        elif opcao == "3":
            try:
                adicionar_conhecimento(
                    base,
                    input("Título: "),
                    input("Conteúdo: "),
                )
            except ValueError as erro:
                print(erro)
                continue
            salvar_dados(base)
            print("Artigo salvo.")
        elif opcao == "4":
            salvar_dados(base)
            print("Até a próxima.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
