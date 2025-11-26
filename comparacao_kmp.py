import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt

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
        r"Texto:\s*(\d+),\s*Padrão:\s*(\d+).*?Média:\s*([\d.]+)",
        re.S
    )

    for texto, padrao_tam, media in padrao.findall(logs):
        dados.append({
            "linguagem": "Python",
            "tamanho_texto": int(texto),
            "tamanho_padrao": int(padrao_tam),
            "tempo_medio": float(media),
            "complexidade": "O(n + m)"
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

        if texto and padrao_tam and media:
            dados.append({
                "linguagem": "C",
                "tamanho_texto": int(texto.group(1)),
                "tamanho_padrao": int(padrao_tam.group(1)),
                "tempo_medio": float(media.group(1)),
                "complexidade": "O(n + m)"
            })

    return dados

# criar dataFrame
dados_python = extrair_python(saida_python)
dados_c = extrair_c(saida_c)

df = pd.DataFrame(dados_python + dados_c)

print("\n==============================")
print(">>> DADOS EXTRAÍDOS (LOGS TRATADOS)")
print("==============================\n")
print(df)

# criar tabela comparativa
tabela = df.pivot(
    index=["tamanho_texto", "tamanho_padrao"],
    columns="linguagem",
    values="tempo_medio"
)

if "Python" in tabela.columns and "C" in tabela.columns:
    tabela["C_vezes_mais_rapido"] = tabela["Python"] / tabela["C"]

print("\n==============================")
print(">>> TABELA COMPARATIVA FINAL")
print("==============================\n")
print(tabela)

# grafico - tempo de execuçao
plt.figure()
for linguagem in df["linguagem"].unique():
    dados = df[df["linguagem"] == linguagem]
    plt.plot(
        dados["tamanho_texto"],
        dados["tempo_medio"],
        marker='o',
        label=linguagem
    )

plt.xlabel("Tamanho do Texto")
plt.ylabel("Tempo Médio (s)")
plt.title("Tempo de Execução - KMP (Python vs C)")
plt.legend()
plt.grid(True)
plt.savefig("tempo_execucao_kmp.png")
plt.show()

# grafico - velocidade relativa
if "C_vezes_mais_rapido" in tabela.columns:
    plt.figure()
    plt.plot(
        tabela.index.get_level_values(0),
        tabela["C_vezes_mais_rapido"],
        marker='o'
    )

    plt.xlabel("Tamanho do Texto")
    plt.ylabel("Python é X vezes mais lento que C")
    plt.title("Velocidade Relativa - KMP")
    plt.grid(True)
    plt.savefig("velocidade_relativa_kmp.png")
    plt.show()
