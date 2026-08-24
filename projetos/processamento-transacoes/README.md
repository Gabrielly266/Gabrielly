# Processamento de transações

Simulação de transações com processamento paralelo em Python. Compras acima de R$ 1.000 recebem desconto, e compras recorrentes de clientes não VIP são sinalizadas para conferência.

A análise de recorrência acontece depois do processamento paralelo, evitando inconsistências no compartilhamento de dados entre processos.

## Executar

```bash
python processamento_transacoes.py
```

Para testar com menos registros ou reproduzir o mesmo resultado:

```bash
python processamento_transacoes.py --quantidade 30 --processos 2 --seed 42
```

Todos os clientes e valores são gerados aleatoriamente para a demonstração.
