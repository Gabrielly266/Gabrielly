#include <stdio.h>

#define MAIOR_TERMO 46

int fibonacci(int n, int memoria[]) {
    if (n < 2) {
        return n;
    }

    if (memoria[n] == -1) {
        memoria[n] = fibonacci(n - 1, memoria) + fibonacci(n - 2, memoria);
    }

    return memoria[n];
}

int main(void) {
    int n;
    int memoria[MAIOR_TERMO + 1];

    for (int i = 0; i <= MAIOR_TERMO; i++) {
        memoria[i] = -1;
    }

    printf("Posição na sequência de Fibonacci: ");
    if (scanf("%d", &n) != 1 || n < 0 || n > MAIOR_TERMO) {
        fprintf(stderr, "Informe um número entre 0 e %d.\n", MAIOR_TERMO);
        return 1;
    }

    printf("Fibonacci(%d) = %d\n", n, fibonacci(n, memoria));
    return 0;
}
