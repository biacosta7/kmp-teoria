import time
import random
import string
import statistics

def computeLPSArray(pattern):
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
    M = len(pattern)
    N = len(text)
    lps = computeLPSArray(pattern)
    
    i = 0  
    j = 0  

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
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def medir_execucao(func, *args):
    t0 = time.perf_counter()
    func(*args)
    t1 = time.perf_counter()
    return t1 - t0

def executar_experimento(tam_texto, tam_padrao, repeticoes=20):
    texto = gerar_string(tam_texto)
    padrao = gerar_string(tam_padrao)

    tempos = []

    for _ in range(repeticoes):
        tempo = medir_execucao(KMPSearch, texto, padrao)
        tempos.append(tempo)

    media = statistics.mean(tempos)
    desvio = statistics.stdev(tempos)

    return {
        "tamanho_texto": tam_texto,
        "tamanho_padrao": tam_padrao,
        "repeticoes": repeticoes,
        "media": media,
        "desvio": desvio,
        "tempos": tempos
    }


if __name__ == "__main__":
    tamanhos = [
        (1_000, 10), #pequeno
        (100_000, 50), #medio
        (1_000_000, 100),#grande
    ]

    for (T, P) in tamanhos:
        resultado = executar_experimento(T, P, repeticoes=20)

        print("\n-------------------------------")
        print(f"Texto: {T}, Padrão: {P}")
        print(f"Média: {resultado['media']:.6f} s")
        print(f"Desvio padrão: {resultado['desvio']:.6f} s")
        print("-------------------------------")