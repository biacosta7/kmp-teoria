#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double now() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void gerar_string(char *s, int n) {
    for (int i = 0; i < n; i++) {
        s[i] = 'a' + rand() % 26;
    }
    s[n] = '\0';
}

void computeLPSArray(const char* pattern, int M, int* lps) {
    int len = 0;
    lps[0] = 0;
    int i = 1;

    while (i < M) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
}

void KMPSearch(const char* pattern, const char* text) {
    int M = strlen(pattern);
    int N = strlen(text);

    int* lps = (int*)malloc(sizeof(int) * M);
    computeLPSArray(pattern, M, lps);

    int i = 0;
    int j = 0;

    while ((N - i) >= (M - j)) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        if (j == M) {
            j = lps[j - 1];
        }
        else if (i < N && pattern[j] != text[i]) {
            if (j != 0)
                j = lps[j - 1];
            else
                i++;
        }
    }

    free(lps);
}

void executar_experimento(int tam_texto, int tam_padrao, int repeticoes) {
    char *texto = malloc((tam_texto + 1) * sizeof(char));
    char *padrao = malloc((tam_padrao + 1) * sizeof(char));

    gerar_string(texto, tam_texto);
    gerar_string(padrao, tam_padrao);

    double *tempos = malloc(repeticoes * sizeof(double));

    for (int k = 0; k < repeticoes; k++) {
        double t0 = now();
        KMPSearch(padrao, texto);
        double t1 = now();
        tempos[k] = t1 - t0;
    }

    double soma = 0;
    for (int i = 0; i < repeticoes; i++) soma += tempos[i];
    double media = soma / repeticoes;

    double sd = 0;
    for (int i = 0; i < repeticoes; i++)
        sd += (tempos[i] - media) * (tempos[i] - media);
    sd = sqrt(sd / (repeticoes - 1));

    printf("\n==========================================\n");
    printf("TEXTO = %d caracteres\n", tam_texto);
    printf("PADRAO = %d caracteres\n", tam_padrao);
    printf("REPETICOES = %d\n", repeticoes);
    printf("MEDIA: %.6f s\n", media);
    printf("DESVIO PADRAO: %.6f s\n", sd);
    printf("==========================================\n");

    free(texto);
    free(padrao);
    free(tempos);
}

int main() {
    srand(time(NULL));

    int testes[][2] = {
        {1000, 10},// pequeno
        {100000, 50},// médio
        {1000000, 100},// grande
    };

    int repeticoes = 20;

    for (int i = 0; i < 3; i++) {
        executar_experimento(testes[i][0], testes[i][1], repeticoes);
    }

    return 0;
}
