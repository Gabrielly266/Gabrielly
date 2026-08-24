#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#endif
#define MAX 100

void limparBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void limparBufferStr(char * str) {
    int tam = strlen(str);

    if (tam > 0 && str[tam-1] == '\n') {
        str[tam-1] = '\0';
    } else {
        limparBuffer();
    }
}

typedef struct {
    char nome[50];
    char telefone[20];
    char email[50];
} Aluno;

typedef struct {
    int numeroMatricula;
    char curso[50];
    float coeficiente;
    Aluno aluno;
} Matricula;

void imprimirMatricula(Matricula vetor) {
    printf("\n");
    printf("  Matrícula  = %d\n", vetor.numeroMatricula);
    printf("  Nome       = %s\n", vetor.aluno.nome);
    printf("  Curso      = %s\n", vetor.curso);
    printf("  Coeficiente= %.2f\n", vetor.coeficiente);
    printf("  Telefone   = %s\n", vetor.aluno.telefone);
    printf("  E-mail     = %s\n", vetor.aluno.email);
}

int pesquisarPorMatricula(Matricula vetor[], int qtd, int matricula){
    int i;
    for (i = 0; i < qtd; i++) {
        if (vetor[i].numeroMatricula == matricula) {
            printf("\nDados encontrados\n");
            return i;
        }
    }
    printf("Dados não encontrados!\n");
    return -1;
}
void inserirAluno(Matricula vetor[], int *qtd){
    int i;
    Matricula novo;
    if (*qtd >= MAX) {
        printf("\nLimite de matrículas atingido.\n");
        return;
    }
    printf("\nNúmero da matrícula: ");
    scanf(" %d", &novo.numeroMatricula);
    limparBuffer();
    i = pesquisarPorMatricula(vetor, *qtd, novo.numeroMatricula);
    if (i != -1) {
        printf("\nMatrícula já cadastrada!");
        return;
    }
    printf("\nProssiga com a matrícula");
    printf("\nNome: ");
    fgets(novo.aluno.nome, sizeof(novo.aluno.nome), stdin);
    limparBufferStr(novo.aluno.nome);
    printf("\nTelefone: ");
    fgets(novo.aluno.telefone, sizeof(novo.aluno.telefone), stdin);
    limparBufferStr(novo.aluno.telefone);
    printf("\nE-mail: ");
    fgets(novo.aluno.email, sizeof(novo.aluno.email), stdin);
    limparBufferStr(novo.aluno.email);
    printf("\nCurso: ");
    fgets(novo.curso, sizeof(novo.curso), stdin);
    limparBufferStr(novo.curso);
    do {
        printf("\nCoeficiente (0 a 100): ");
        scanf(" %f", &novo.coeficiente);
        limparBuffer();
        if (novo.coeficiente < 0 || novo.coeficiente > 100) {
            printf("\nValor inválido. Digite um número entre 0 e 100.");
        }
    } while (novo.coeficiente < 0 || novo.coeficiente > 100);
    vetor[*qtd] = novo;
    (*qtd)++;
    printf("\nAluno inserido com sucesso!\n");
}

void pesquisarPorNome(Matricula vetor[], int qtd, char nome[]){
    int i, achou = 0;
    for (i = 0; i < qtd; i++) {
        if (strcmp(vetor[i].aluno.nome, nome) == 0) {
            imprimirMatricula (vetor[i]);
            achou = 1;
        }
    }
    if (achou == 0) {
        printf("\nNenhum aluno encontrado com esse nome.\n");
    }
}
void atualizarCoeficiente(Matricula vetor[], int qtd){
    int matricula, pos;
    printf("\nDigite a matrícula: ");
    scanf(" %d", &matricula);
    limparBuffer();
    pos = pesquisarPorMatricula(vetor, qtd, matricula);
    if (pos == -1) {
        return;
    }
    do {
        printf("\nNovo coeficiente (0 a 100): ");
        scanf(" %f", &vetor[pos].coeficiente);
        limparBuffer();
        if (vetor[pos].coeficiente < 0 || vetor[pos].coeficiente > 100) {
            printf("\nValor inválido.\n");
        }
    } while (vetor[pos].coeficiente < 0 || vetor[pos].coeficiente> 100);
    printf("Coeficiente atualizado com sucesso!\n");
}
void maiorCoeficiente(Matricula vetor[], int qtd){
    float maior = 0;
    int pos = 0, i;
    if (qtd == 0) {
        printf("\nNenhum aluno cadastrado.\n");
        return;
    }
    for (i = 0; i < qtd; i++) {
        if (vetor[i].coeficiente >= maior) {
            maior = vetor[i].coeficiente;
            pos = i;
        }
    }
    printf("\nAluno com maior coeficiente:\n");
    imprimirMatricula (vetor[pos]);
}
void excluirAluno(Matricula vetor[], int *qtd){
    int matricula, pos, i;
    printf("\nDigite a matrícula a excluir: ");
    scanf(" %d", &matricula);
    limparBuffer();
    pos = pesquisarPorMatricula(vetor, *qtd, matricula);
    if (pos == -1) {
        return;
    }
    for (i = pos; i < (*qtd) - 1; i++) {
        vetor[i] = vetor[i + 1];
    }
    (*qtd)--;
    printf("\nAluno excluído com sucesso!\n");
}
void listar(Matricula vetor[], int qtd){
    int i;
    printf("\nLISTA DE ALUNOS\n");
    for (i = 0; i < qtd; i++) {
        printf("\nAluno %d:\n", i + 1);
        imprimirMatricula (vetor[i]);
    }
    printf("Total de alunos cadastrados: %d\n", qtd);
}

FILE* abrirArquivo(char *nome, char *modo) {
    FILE *arq = fopen(nome, modo);
    if (arq == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nome);
        exit(1);
    }
    return arq;
}

void carregarArquivo(Matricula vetor[], int *qtd) {
    FILE *arquivo = fopen("matricula.bin", "rb");
    if (arquivo == NULL) {
        *qtd = 0; 
        return;
    }
    if (fread(qtd, sizeof(int), 1, arquivo) != 1 || *qtd < 0 || *qtd > MAX) {
        *qtd = 0;
        fclose(arquivo);
        return;
    }
    if (fread(vetor, sizeof(Matricula), (size_t)*qtd, arquivo) != (size_t)*qtd) {
        *qtd = 0;
    }
    fclose(arquivo);
}

void gravarArquivo(Matricula vetor[], int *qtd) {
    FILE *arquivo = abrirArquivo("matricula.bin", "wb");
    fwrite(qtd, sizeof(int), 1, arquivo);             
    fwrite(vetor, sizeof(Matricula), *qtd, arquivo);   
    fclose(arquivo);
}

int menu() {
	int op;

	printf("\n\nSISTEMA ACADEMICO\n\n");
	printf("1 - Inserir aluno\n");
	printf("2 - Pesquisar por matricula\n");
	printf("3 - Pesquisar por nome\n");
	printf("4 - Atualizar coeficiente\n");
	printf("5 - Maior coeficiente\n");
	printf("6 - Excluir aluno\n");
	printf("7 - Listar\n");
	printf("0 - Sair\n");
	do {
		printf("Escolha sua opcao: ");
		scanf(" %d", &op);
		limparBuffer();
	} while(op < 0 || op > 7);
	return op;
}

int main() {
    #ifdef _WIN32
    SetConsoleOutputCP(65001);
    #endif
    int qtd = 0;
    Matricula vetor[MAX];
    int matricula;
    char nome[50];
    int op;
    int i;
    carregarArquivo(vetor, &qtd);
    do{
        op = menu();
        switch (op) {
            case 1:
                inserirAluno(vetor, &qtd);
                break;
            case 2:
                printf("\nDigite o número da matrícula: ");
                scanf(" %d", &matricula);
                limparBuffer();
                i = pesquisarPorMatricula(vetor, qtd, matricula);
                if (i >=0) {
                    imprimirMatricula (vetor[i]);
                }
                break;
            case 3:
                printf("\nNome do aluno: ");
                fgets(nome, sizeof(nome), stdin);
                limparBufferStr(nome);
                pesquisarPorNome(vetor, qtd, nome);
                break;
            case 4:
                atualizarCoeficiente(vetor, qtd);
                break;
            case 5:
                maiorCoeficiente(vetor, qtd);
                break;
            case 6:
                excluirAluno(vetor, &qtd);
                break;
            case 7:
                listar(vetor, qtd);
                break;
            case 0:
                printf("\nSaindo...\n");
                break;
            default:
                printf("\nOpção inválida. Digite um número entre 0 e 7.\n");
        }
        #ifdef _WIN32
        system("PAUSE");
        #endif
    } while (op != 0);
    gravarArquivo(vetor, &qtd);
    return 0;
}
