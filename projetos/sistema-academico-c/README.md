# Sistema Acadêmico em C

Sistema de terminal para cadastro e acompanhamento de matrículas acadêmicas, com persistência dos registros em arquivo binário.

## Funcionalidades

- Cadastro, pesquisa e exclusão de estudantes.
- Consulta por número de matrícula ou nome.
- Atualização e comparação de coeficientes acadêmicos.
- Listagem dos registros e gravação em `matricula.bin`.
- Validação dos limites de entrada e execução em Windows, Linux ou macOS.

## Como executar

```bash
gcc -std=c11 -Wall -Wextra sistema_academico.c -o sistema_academico
./sistema_academico
```

**Conceitos:** structs, vetores, funções, operações CRUD, manipulação de arquivos e validação de dados.
