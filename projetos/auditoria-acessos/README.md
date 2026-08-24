# Auditoria de acessos

Análise de registros de acesso para encontrar três situações: usuários ausentes da base de contas ativas, acessos fora do horário comercial e conexões bem-sucedidas por IP externo.

O projeto usa pandas para cruzar os arquivos CSV e matplotlib para gerar um gráfico com o resultado.

## Executar

```bash
pip install -r requirements.txt
python auditoria.py
```

O gráfico é salvo como `riscos_seguranca.png`. Os arquivos CSV do repositório contêm apenas dados fictícios.
