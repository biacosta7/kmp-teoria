#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

/**
 * Obtém timestamp de alta precisão
 */
double now() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/**
 * Gera string aleatória de tamanho n
 */
void gerar_string_aleatoria(char *s, int n) {
    for (int i = 0; i < n; i++) {
        s[i] = 'a' + rand() % 26;
    }
    s[n] = '\0';
}

/**
 * Gera string conforme o tipo de caso
 */
void gerar_string_caso(char *s, int n, const char *tipo_caso) {
    if (strcmp(tipo_caso, "PIOR CASO") == 0) {
        // String cheia de 'A's com um 'B' no final
        for (int i = 0; i < n - 1; i++) {
            s[i] = 'A';
        }
        s[n - 1] = 'B';
    } else {
        // String aleatória (para melhor caso e caso médio)
        gerar_string_aleatoria(s, n);
    }
    s[n] = '\0';
}

/**
 * Computa o array LPS (Longest Proper Prefix which is also Suffix)
 * Complexidade: O(m)
 */
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

/**
 * Algoritmo KMP para busca de padrão em texto
 * Complexidade: O(n + m)
 * 
 * Retorna: número de ocorrências encontradas
 */
int KMPSearch(const char* pattern, const char* text) {
    int M = strlen(pattern);
    int N = strlen(text);

    int* lps = (int*)malloc(sizeof(int) * M);
    computeLPSArray(pattern, M, lps);

    int i = 0;  // índice para text
    int j = 0;  // índice para pattern
    int count = 0;  // contador de ocorrências

    while (i < N) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        if (j == M) {
            count++;  // Padrão encontrado
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
    return count;
}

/**
 * Executa experimento de performance
 */
void executar_experimento(int tam_texto, int tam_padrao, int repeticoes, const char *tipo_caso) {
    char *texto = malloc((tam_texto + 1) * sizeof(char));
    char *padrao = malloc((tam_padrao + 1) * sizeof(char));

    if (!texto || !padrao) {
        fprintf(stderr, "Erro de alocação de memória\n");
        exit(1);
    }

    // ============================================================
    // GERAR STRINGS CONFORME O TIPO DE CASO
    // ============================================================
    
    gerar_string_caso(texto, tam_texto, tipo_caso);
    gerar_string_caso(padrao, tam_padrao, tipo_caso);
    
    // Para MELHOR CASO, garantir que padrão não existe no texto
    if (strcmp(tipo_caso, "MELHOR CASO") == 0) {
        // Trocar primeira letra do padrão para algo diferente do texto
        padrao[0] = (texto[0] == 'z') ? 'a' : 'z';
    }

    // ============================================================
    // EXECUTAR MEDIÇÕES
    // ============================================================
    
    double *tempos = malloc(repeticoes * sizeof(double));
    int ocorrencias = 0;

    for (int k = 0; k < repeticoes; k++) {
        double t0 = now();
        int count = KMPSearch(padrao, texto);
        double t1 = now();
        tempos[k] = t1 - t0;
        
        if (k == 0) ocorrencias = count;
    }

    // Calcular média
    double soma = 0;
    for (int i = 0; i < repeticoes; i++) 
        soma += tempos[i];
    double media = soma / repeticoes;

    // Calcular desvio padrão
    double sd = 0;
    for (int i = 0; i < repeticoes; i++)
        sd += (tempos[i] - media) * (tempos[i] - media);
    sd = sqrt(sd / (repeticoes - 1));

    // ============================================================
    // IMPRIMIR NO FORMATO QUE comparacao_kmp.py ESPERA
    // ============================================================
    
    printf("\n==========================================\n");
    printf("TIPO: %s\n", tipo_caso);
    printf("TEXTO = %d\n", tam_texto);
    printf("PADRAO = %d\n", tam_padrao);
    printf("REPETICOES = %d\n", repeticoes);
    printf("MEDIA: %.6f\n", media);
    printf("DESVIO PADRAO: %.6f\n", sd);
    printf("OCORRENCIAS: %d\n", ocorrencias);
    printf("COMPLEXIDADE (n+m): %d\n", tam_texto + tam_padrao);
    printf("==========================================\n");

    free(texto);
    free(padrao);
    free(tempos);
}

int main() {
    srand(time(NULL));

    printf("==================================================\n");
    printf("TESTES DE PERFORMANCE - ALGORITMO KMP (C)\n");
    printf("==================================================\n");

    // Mesmos tamanhos do teste.py para comparação justa
    int testes[][2] = {
        {1000, 10},         // pequeno
        {10000, 20},        // médio-pequeno
        {50000, 30},        // médio
        {100000, 50},       // médio-grande
        {500000, 75},       // grande
        {1000000, 100},     // muito grande
    };

    int num_testes = sizeof(testes) / sizeof(testes[0]);
    int repeticoes = 20;
    
    // Array com os 3 tipos de casos
    const char *tipos[] = {"MELHOR CASO", "PIOR CASO", "CASO MEDIO"};
    int num_tipos = 3;

    // ============================================================
    // EXECUTAR OS 3 CASOS PARA CADA TAMANHO
    // ============================================================
    
    for (int i = 0; i < num_testes; i++) {
        for (int t = 0; t < num_tipos; t++) {
            executar_experimento(testes[i][0], testes[i][1], repeticoes, tipos[t]);
        }
    }

    return 0;
}