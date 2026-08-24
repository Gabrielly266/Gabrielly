#include <stdio.h>

#define QUANTIDADE_NOTAS 3

void limpar_entrada(void) {
    int caractere;
    while ((caractere = getchar()) != '\n' && caractere != EOF) {
    }
}

int ler_matricula(void) {
    int matricula;

    while (1) {
        printf("Matrícula: ");
        if (scanf("%d", &matricula) == 1 && matricula >= 0) {
            limpar_entrada();
            return matricula;
        }

        printf("Informe uma matrícula válida.\n");
        limpar_entrada();
    }
}

float ler_nota(int numero) {
    float nota;

    while (1) {
        printf("Nota %d: ", numero);
        if (scanf("%f", &nota) == 1 && nota >= 0.0f && nota <= 10.0f) {
            limpar_entrada();
            return nota;
        }

        printf("A nota deve estar entre 0 e 10.\n");
        limpar_entrada();
    }
}

float calcular_media(void) {
    float soma = 0.0f;

    for (int i = 1; i <= QUANTIDADE_NOTAS; i++) {
        soma += ler_nota(i);
    }

    return soma / QUANTIDADE_NOTAS;
}

int main(void) {
    int matricula = ler_matricula();
    float media = calcular_media();

    printf("\nMatrícula: %d\nMédia: %.2f\n", matricula, media);
    return 0;
}
