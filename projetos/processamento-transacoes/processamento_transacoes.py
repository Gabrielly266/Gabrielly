"""Processamento paralelo de transações fictícias com regras de negócio."""

import argparse
import multiprocessing
import random
from collections import Counter


LIMITE_DESCONTO = 1_000.0
PERCENTUAL_DESCONTO = 0.15


def gerar_transacoes(quantidade, seed=None):
    gerador = random.Random(seed)
    return [
        {
            "cliente": f"Cliente_{gerador.randint(1, 1_000)}",
            "valor": round(gerador.uniform(50, 5_000), 2),
            "vip": gerador.choice((True, False)),
        }
        for _ in range(quantidade)
    ]


def processar_transacao(evento):
    resultado = evento.copy()
    resultado["desconto_aplicado"] = evento["valor"] > LIMITE_DESCONTO
    if resultado["desconto_aplicado"]:
        resultado["valor"] = round(evento["valor"] * (1 - PERCENTUAL_DESCONTO), 2)
    return resultado


def identificar_alertas(transacoes):
    compras_por_cliente = Counter(
        transacao["cliente"] for transacao in transacoes if not transacao["vip"]
    )
    return {
        cliente: quantidade
        for cliente, quantidade in compras_por_cliente.items()
        if quantidade > 2
    }


def processar_lote(eventos, processos=None):
    if not eventos:
        return []

    quantidade_processos = min(processos or multiprocessing.cpu_count(), len(eventos))
    if quantidade_processos == 1:
        return [processar_transacao(evento) for evento in eventos]

    with multiprocessing.Pool(processes=quantidade_processos) as pool:
        return pool.map(processar_transacao, eventos)


def main():
    argumentos = argparse.ArgumentParser(
        description="Simula o processamento paralelo de transações."
    )
    argumentos.add_argument("--quantidade", type=int, default=1_000)
    argumentos.add_argument("--processos", type=int, default=None)
    argumentos.add_argument("--seed", type=int, default=None)
    opcoes = argumentos.parse_args()

    if opcoes.quantidade < 1:
        argumentos.error("--quantidade precisa ser maior que zero")
    if opcoes.processos is not None and opcoes.processos < 1:
        argumentos.error("--processos precisa ser maior que zero")

    eventos = gerar_transacoes(opcoes.quantidade, seed=opcoes.seed)
    resultados = processar_lote(eventos, processos=opcoes.processos)
    alertas = identificar_alertas(resultados)
    descontos = sum(transacao["desconto_aplicado"] for transacao in resultados)

    print(f"Transações processadas: {len(resultados)}")
    print(f"Descontos aplicados: {descontos}")
    print(f"Clientes não VIP com compras recorrentes: {len(alertas)}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
