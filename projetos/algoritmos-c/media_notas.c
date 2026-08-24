#include <stdio.h>
#include <stdlib.h>
#ifdef _WIN32
#include <windows.h>
#endif

int lerMatricula(){
    int matricula;
    printf("Digite sua matrícula:");
    scanf("%d", &matricula);
    while (matricula<0){
        printf("Digite novamente:");
        scanf("%d", &matricula);
    }
    return matricula;
}

float lerNota(){
    float n;
    printf("Digite sua nota:");
    scanf("%f", &n);
    while ((n<0)||(n>10)){
        printf("Digite novamente:");
        scanf("%f", &n);
    }
    return n;
}

float media(){
    int cont=0;
    float soma=0, n, media;

    while (cont<3){
        n=lerNota();
        soma=soma+n;
        cont=cont+1;
    }
    media=soma/3;
    return media;
} 

int main() {
    int matri;
    float m;

    #ifdef _WIN32
    SetConsoleOutputCP(65001);
    #endif

    matri=lerMatricula();
    m=media();
    printf("Matrícula %d | Média: %.2f\n", matri, m);
    
    return 0;
}
