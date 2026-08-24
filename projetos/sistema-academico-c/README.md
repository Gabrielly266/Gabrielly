# Sistema acadêmico

Programa em C para cadastrar estudantes e acompanhar suas matrículas. Os dados ficam salvos em um arquivo binário, então continuam disponíveis na próxima execução.

O menu permite cadastrar, buscar por matrícula ou nome, atualizar o coeficiente, excluir e listar estudantes. Também mostra o maior coeficiente da turma.

## Executar

```bash
gcc -std=c11 -Wall -Wextra sistema_academico.c -o sistema_academico
./sistema_academico
```

O arquivo `matricula.bin` é criado automaticamente. O sistema aceita até 100 matrículas, evita cadastros repetidos e valida as entradas numéricas.
