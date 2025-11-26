import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.dpi"] = 120

# teste.py
print("\n==============================")
print(">>> EXECUTANDO teste.py")
print("==============================\n")

saida_python = subprocess.check_output(
    ["python", "teste.py"],
    universal_newlines=True
)

print(">>> SAÍDA COMPLETA DO PYTHON:")
print("--------------------------------")
print(saida_python)
print("--------------------------------\n")

# teste.c
print("\n==============================")
print(">>> COMPILANDO E EXECUTANDO teste.c")
print("==============================\n")

subprocess.run(["gcc", "teste.c", "-o", "teste_c", "-lm"], check=True)

saida_c = subprocess.check_output(
    ["./teste_c"],
    universal_newlines=True
)

print(">>> SAÍDA COMPLETA DO C:")
print("--------------------------------")
print(saida_c)
print("--------------------------------\n")

# python
def extrair_python(logs):
    dados = []

    padrao = re.compile(
        r"Texto:\s*(\d+),\s*Padrão:\s*(\d+).*?Média:\s*([\d.]+).*?Desvio padrão:\s*([\d.]+)",
        re.S
    )

    for texto, padrao_tam, media, desvio in padrao.findall(logs):
        dados.append({
            "linguagem": "Python",
            "tamanho_texto": int(texto),
            "tamanho_padrao": int(padrao_tam),
            "tempo_medio": float(media),
            "desvio": float(desvio),
        })

    return dados

# C
def extrair_c(logs):
    dados = []

    blocos = logs.split("==========================================")

    for bloco in blocos:
        texto = re.search(r"TEXTO = (\d+)", bloco)
        padrao_tam = re.search(r"PADRAO = (\d+)", bloco)
        media = re.search(r"MEDIA: ([\d.]+)", bloco)
        desvio = re.search(r"DESVIO PADRAO: ([\d.]+)", bloco)

        if texto and padrao_tam and media and desvio:
            dados.append({
                "linguagem": "C",
                "tamanho_texto": int(texto.group(1)),
                "tamanho_padrao": int(padrao_tam.group(1)),
                "tempo_medio": float(media.group(1)),
                "desvio": float(desvio.group(1)),
            })

    return dados

# criar dataFrame
dados_python = extrair_python(saida_python)
dados_c = extrair_c(saida_c)

df = pd.DataFrame(dados_python + dados_c)

print("\n==============================")
print(">>> DADOS EXTRAÍDOS (TRATADOS)")
print("==============================\n")
print(df)

# 6. Curva teórica (O(n+m))
df_teorica = df.groupby("tamanho_texto")["tamanho_texto"].first()
# normaliza para a escala dos tempos reais
df_teorica_norm = df_teorica / df_teorica.max() * df["tempo_medio"].max()

# gráfico: Tempo real + desvio + curva teórica
plt.figure()

for linguagem in df["linguagem"].unique():
    dados = df[df["linguagem"] == linguagem]
    plt.errorbar(
        dados["tamanho_texto"],
        dados["tempo_medio"],
        yerr=dados["desvio"],
        marker='o',
        capsize=5,
        label=f"{linguagem} (prático)"
    )

plt.plot(
    df_teorica.index,
    df_teorica_norm,
    linestyle="--",
    label="Curva teórica O(n+m)"
)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Tamanho do Texto (log)")
plt.ylabel("Tempo (s, log)")
plt.title("Tempo de Execução - KMP (Python vs C)")
plt.grid(True, which="both")
plt.legend()
plt.savefig("curva_teorica_pratica.png")
plt.show()

# speedup (quantas vezes C é mais rápido)
df_speed = df.pivot(index="tamanho_texto", columns="linguagem", values="tempo_medio")
df_speed["speedup"] = df_speed["Python"] / df_speed["C"]

plt.figure()
plt.plot(df_speed.index, df_speed["speedup"], marker='o')

# curva sintética ~ linear para comparação de speedup
synthetic = df_speed.index / df_speed.index.min()
plt.plot(df_speed.index, synthetic, linestyle="--", label="Curva sintética (linear)")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Tamanho do Texto (log)")
plt.ylabel("Speedup (log)")
plt.title("Tempo de Execução - KMP (Python vs C) | Curva prática x sintética")
plt.grid(True, which="both")
plt.legend()
plt.savefig("curva_speedup.png")
plt.show()