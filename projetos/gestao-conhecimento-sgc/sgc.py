import json
import os

# Caminho para o arquivo da Camada de Dados (Persistência)
ARQUIVO_DADOS = "base_conhecimento.json"

def carregar_dados():

    # cria base inicial caso o arquivo não exista
    if not os.path.exists(ARQUIVO_DADOS):
        return [
            {
                "id":1,
                "titulo":"Primeiros passos no sistema",
                "conteudo":"Consulte o guia introdutório da aplicação.",
                "acessos":120
            },

            {
                "id":2,
                "titulo":"Consultas em banco de dados",
                "conteudo":"Exemplo didático de consulta SQL.",
                "acessos":45
            },

            {
                "id":3,
                "titulo":"Organização de documentos",
                "conteudo":"Padronizar nomes e categorias de arquivos.",
                "acessos":89
            }
        ]

    with open(ARQUIVO_DADOS,"r",encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(base):

    # salva no arquivo json
    with open(ARQUIVO_DADOS,"w",encoding="utf-8") as f:
        json.dump(base,f,indent=4,ensure_ascii=False)

def exibir_dashboard(base):

    print("\n--- DASHBOARD DE POPULARIDADE ---\n")

    for item in base:

        # barra proporcional aos acessos
        barra = "█" * (item["acessos"] // 10)

        print(item["id"],"-",item["titulo"])
        print(barra,"(",item["acessos"],"acessos)")
        print()

def buscar_conhecimento(base,termo):

    # busca no título ou conteúdo
    resultados = [
        item for item in base
        if termo.lower() in item["titulo"].lower()
        or termo.lower() in item["conteudo"].lower()
    ]

    return resultados

def adicionar_conhecimento(base):

    print("\nNovo conhecimento")

    titulo = input("Título: ")
    conteudo = input("Conteúdo: ")

    novo_id = max(item["id"] for item in base) + 1

    novo = {
        "id":novo_id,
        "titulo":titulo,
        "conteudo":conteudo,
        "acessos":0
    }

    base.append(novo)

    salvar_dados(base)

    print("Conhecimento salvo com sucesso!")

def menu():

    base = carregar_dados()

    while True:

        print("\n1-Dashboard")
        print("2-Pesquisar")
        print("3-Adicionar conhecimento")
        print("4-Sair")

        op = input("Opção: ")

        if op=="1":
            exibir_dashboard(base)

        elif op=="2":

            termo = input("Digite a busca: ")

            resultados = buscar_conhecimento(base,termo)

            if len(resultados)>0:

                for r in resultados:

                    print("\nTítulo:",r["titulo"])
                    print("Conteúdo:",r["conteudo"])

                    r["acessos"] +=1

                salvar_dados(base)

            else:
                print("Nenhum resultado encontrado")

        elif op=="3":
            adicionar_conhecimento(base)

        elif op=="4":
            salvar_dados(base)
            print("Sistema encerrado")
            break

        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu()
