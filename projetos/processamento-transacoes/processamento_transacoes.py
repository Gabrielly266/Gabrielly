from datetime import datetime
import random
import multiprocessing

def processar_transacao(evento, log_de_transacoes):
    agora = datetime.now().strftime("%H:%M:%S")

    print(
        f"[{agora}] NOVO EVENTO: Cliente {evento['cliente']} | "
        f"Valor: R${evento['valor']} | VIP: {evento['vip']}"
    )

    # --- REGRA DE NEGÓCIO ---
    if evento['valor'] > 1000:
        evento['valor'] *= 0.85
        print(f" [AUTOMAÇÃO]: Desconto aplicado. Novo valor: R${evento['valor']:.2f}")

    # --- REGRA DE FRAUDE (SOMENTE NÃO VIP) ---
    if not evento['vip']:
        compras_anteriores = [
            t for t in log_de_transacoes if t['cliente'] == evento['cliente']
        ]

        if len(compras_anteriores) >= 2:
            print(
                f" [ALERTA CEP]: Cliente {evento['cliente']} "
                f"com múltiplas transações rápidas."
            )
    else:
        print(f" [VIP]: Cliente {evento['cliente']} isento de verificação de fraude.")

    # Armazena o evento no log compartilhado
    log_de_transacoes.append(evento)

if __name__ == "__main__":
    multiprocessing.freeze_support()

    manager = multiprocessing.Manager()
    log_de_transacoes = manager.list()

    nomes_clientes = [f"Cliente_{i}" for i in range(1, 1001)]

    fluxo_entrada = []
    for _ in range(10000):
        fluxo_entrada.append({
            'cliente': random.choice(nomes_clientes),
            'valor': round(random.uniform(50, 5000), 2),
            'vip': random.choice([True, False])
        })

    num_processos = multiprocessing.cpu_count()
    print(f"Processando com {num_processos} processos...\n")

    with multiprocessing.Pool(processes=num_processos) as pool:
        pool.starmap(
            processar_transacao,
            [(evento, log_de_transacoes) for evento in fluxo_entrada]
        )

    print("\nProcessamento concluído!")
    print(f"Total de transações processadas: {len(log_de_transacoes)}")
