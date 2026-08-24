# Auditoria de Acessos e Logs

Script de auditoria que cruza registros de acesso com uma base de usuários ativos para identificar riscos de segurança.

## Verificações realizadas

- Contas presentes nos logs, mas ausentes da base de usuários ativos.
- Acessos registrados fora do horário comercial, das 8h às 18h.
- Acessos bem-sucedidos provenientes de endereços IP externos.
- Geração de um gráfico com a distribuição dos riscos identificados.

## Como executar

```bash
pip install -r requirements.txt
python auditoria.py
```

Os arquivos CSV incluídos contêm **exclusivamente dados sintéticos**, criados para demonstrar a execução sem expor informações pessoais ou registros reais. O gráfico é salvo como `riscos_seguranca.png`.

**Tecnologias:** Python, pandas, matplotlib e arquivos CSV.
