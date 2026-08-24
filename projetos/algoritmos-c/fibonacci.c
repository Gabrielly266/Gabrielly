#include <stdio.h>
#include <stdlib.h>
#ifdef _WIN32
#include <windows.h>
#endif

int fibonacci(int n){
    if (n==0){
        return 0;
    }
    if (n==1){
        return 1;
    }
    return fibonacci (n-1) + fibonacci(n-2);
}

int main() {
    int n, f;
    #ifdef _WIN32
    SetConsoleOutputCP(65001);
    #endif
    printf("Escreva um valor para n:");
    if (scanf("%d", &n) != 1 || n < 0 || n > 46) {
        printf("Digite um número entre 0 e 46.\n");
        return 1;
    }
    f=fibonacci(n);
    printf("%d", f);
    return 0;
}
