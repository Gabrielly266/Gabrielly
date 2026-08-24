# Processamento Paralelo de Transações

Simulação de processamento de eventos com regras de negócio, tratamento diferenciado de clientes VIP e identificação de padrões suspeitos.

## Funcionalidades

- Geração de transações sintéticas.
- Processamento paralelo com `multiprocessing`.
- Aplicação automática de desconto para transações acima do limite configurado.
- Detecção de compras repetidas para clientes não VIP.
- Registro compartilhado das transações processadas.

## Como executar

```bash
python processamento_transacoes.py
```

A configuração original simula 10 mil eventos e pode consumir recursos consideráveis. Para testes rápidos, reduza o valor de `range(10000)` no código.

**Conceitos:** concorrência, automação de regras, processamento de eventos e monitoramento.
