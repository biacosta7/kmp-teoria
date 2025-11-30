import time
import random
import string
import statistics

def computeLPSArray(pattern):
    """
    Computa o array LPS (Longest Proper Prefix which is also Suffix)
    Complexidade: O(m) onde m = len(pattern)
    """
    M = len(pattern)
    lps = [0] * M
    length = 0
    i = 1
    
    while i < M:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def KMPSearch(text, pattern):
    """
    Algoritmo KMP para busca de padrão em texto
    Complexidade: O(n + m) onde n = len(text), m = len(pattern)
    
    Retorna: lista de índices onde o padrão foi encontrado
    """
    M = len(pattern)
    N = len(text)
    lps = computeLPSArray(pattern)
    
    i = 0  # índice para text
    j = 0  # índice para pattern
    indices = []

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == M:
            indices.append(i - j)
            j = lps[j - 1]
        
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return indices


def gerar_string(n):
    """Gera string aleatória de tamanho n com letras minúsculas"""
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def medir_execucao(func, *args):
    """Mede tempo de execução de uma função"""
    t0 = time.perf_counter()
    resultado = func(*args)
    t1 = time.perf_counter()
    return t1 - t0, resultado


def executar_experimento(tam_texto, tam_padrao, repeticoes=20, tipo_caso='CASO MEDIO'):
    """
    Executa experimento de performance do KMP
    
    Args:
        tam_texto: tamanho do texto (n)
        tam_padrao: tamanho do padrão (m)
        repeticoes: número de execuções (15-30 recomendado)
        tipo_caso: 'MELHOR CASO', 'PIOR CASO' ou 'CASO MEDIO'
    
    Returns:
        dict com estatísticas do experimento
    """
    
    # GERAR STRINGS CONFORME O TIPO DE CASO
    if tipo_caso == 'PIOR CASO':
        # Texto cheio de 'A's com um 'B' no final
        # Força máximo de comparações em algoritmos naive (mas KMP resiste)
        texto = 'A' * (tam_texto - 1) + 'B'
        padrao = 'A' * (tam_padrao - 1) + 'B'
        
    elif tipo_caso == 'MELHOR CASO':
        # Texto aleatório + padrão que NÃO existe
        # Padrão começa com letra diferente de qualquer no texto
        texto = gerar_string(tam_texto)
        # Garantir que primeira letra do padrão não existe no texto
        primeiro_char = texto[0]
        chars_disponiveis = string.ascii_lowercase.replace(primeiro_char, '')
        padrao = random.choice(chars_disponiveis) + gerar_string(tam_padrao - 1)
        
    else:  # CASO MEDIO
        # Strings completamente aleatórias
        texto = gerar_string(tam_texto)
        padrao = gerar_string(tam_padrao)
    
    tempos = []
    ocorrencias = None

    for _ in range(repeticoes):
        tempo, resultado = medir_execucao(KMPSearch, texto, padrao)
        tempos.append(tempo)
        if ocorrencias is None:
            ocorrencias = len(resultado)

    media = statistics.mean(tempos)
    desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0

    return {
        "tipo_caso": tipo_caso,
        "tamanho_texto": tam_texto,
        "tamanho_padrao": tam_padrao,
        "repeticoes": repeticoes,
        "media": media,
        "desvio": desvio,
        "ocorrencias": ocorrencias,
        "tempos": tempos
    }


if __name__ == "__main__":
    # Tamanhos de teste (mesmos do teste.c para comparação justa)
    tamanhos = [
        (1_000, 10),        # pequeno
        (10_000, 20),       # médio-pequeno
        (50_000, 30),       # médio
        (100_000, 50),      # médio-grande
        (500_000, 75),      # grande
        (1_000_000, 100),   # muito grande
    ]

    print("="*50)
    print("TESTES DE PERFORMANCE - ALGORITMO KMP (Python)")
    print("="*50)
    
    # EXECUTAR OS 3 CASOS PARA CADA TAMANHO
    for (T, P) in tamanhos:
        for tipo in ['MELHOR CASO', 'PIOR CASO', 'CASO MEDIO']:
            resultado = executar_experimento(T, P, repeticoes=20, tipo_caso=tipo)

            # FORMATO QUE comparacao_kmp.py ESPERA
            print("\n" + "="*50)
            print(f"TIPO: {tipo}")
            print(f"TEXTO = {T}")
            print(f"PADRAO = {P}")
            print(f"REPETICOES = {resultado['repeticoes']}")
            print(f"MEDIA: {resultado['media']:.6f}")
            print(f"DESVIO PADRAO: {resultado['desvio']:.6f}")
            print(f"OCORRENCIAS: {resultado['ocorrencias']}")
            print(f"COMPLEXIDADE (n+m): {T + P}")
            print("="*50)