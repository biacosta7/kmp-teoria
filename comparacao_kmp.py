import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import sys
import io
import platform

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXECUTAVEL_C = "teste_c.exe" if platform.system() == "Windows" else "./teste_c"

plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 10
plt.style.use('ggplot')

print("="*70)
print("ANÁLISE COMPLETA - ALGORITMO KMP")
print("Curva teórica independente + visualização aprimorada")
print("="*70)

# ============================================================
# EXECUTAR TESTES
# ============================================================

print("\n[1/4] Executando testes em Python...")
saida_python = subprocess.check_output(
    ["python", "teste.py"],
    encoding='utf-8',
    errors='replace'
)

print("[2/4] Compilando e executando testes em C...")
subprocess.run(["gcc", "teste.c", "-o", "teste_c", "-lm"], 
               check=True, capture_output=True)
saida_c = subprocess.check_output(
    [EXECUTAVEL_C],
    encoding='utf-8',
    errors='replace'
)

# ============================================================
# EXTRAIR DADOS
# ============================================================

def extrair_dados(logs, linguagem):
    dados = []
    blocos = logs.split("==========================================")
    
    for bloco in blocos:
        tipo_match = re.search(r"TIPO:\s*(.+)", bloco)
        texto_match = re.search(r"TEXTO = (\d+)", bloco)
        padrao_match = re.search(r"PADRAO = (\d+)", bloco)
        media_match = re.search(r"MEDIA: ([\d.]+)", bloco)
        desvio_match = re.search(r"DESVIO PADRAO: ([\d.]+)", bloco)
        
        if all([tipo_match, texto_match, padrao_match, media_match, desvio_match]):
            dados.append({
                "linguagem": linguagem,
                "tipo_caso": tipo_match.group(1).strip(),
                "n": int(texto_match.group(1)),
                "m": int(padrao_match.group(1)),
                "tempo_medio": float(media_match.group(1)),
                "desvio": float(desvio_match.group(1)),
            })
    
    return dados

print("[3/4] Processando resultados...")
dados_python = extrair_dados(saida_python, "Python")
dados_c = extrair_dados(saida_c, "C")
df = pd.DataFrame(dados_python + dados_c)
df['n_mais_m'] = df['n'] + df['m']

# ============================================================
# TABELA DE RESULTADOS
# ============================================================

print("\n" + "="*70)
print("TABELA DE RESULTADOS - TODOS OS CASOS")
print("="*70)

# Criar tabela pivot
tabela = df.pivot_table(
    index=['n', 'tipo_caso'],
    columns='linguagem',
    values=['tempo_medio', 'desvio'],
    aggfunc='first'
)

print(tabela.to_string())

# ============================================================
# ANÁLISE DE DIFERENÇA ENTRE CASOS
# ============================================================

print("\n" + "="*70)
print("ANÁLISE: DIFERENÇA ENTRE MELHOR E PIOR CASO")
print("="*70)

for ling in ['C', 'Python']:
    print(f"\n{ling}:")
    print(f"{'n (chars)':<12} {'Melhor (s)':<12} {'Pior (s)':<12} {'Diff (%)':<12}")
    print("-"*50)
    
    for n in sorted(df['n'].unique()):
        melhor = df[(df['linguagem']==ling) & (df['tipo_caso']=='MELHOR CASO') & (df['n']==n)]
        pior = df[(df['linguagem']==ling) & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
        
        if not melhor.empty and not pior.empty:
            t_melhor = melhor['tempo_medio'].values[0]
            t_pior = pior['tempo_medio'].values[0]
            diff_pct = ((t_pior - t_melhor) / t_melhor) * 100
            print(f"{n:<12,} {t_melhor:<12.6f} {t_pior:<12.6f} {diff_pct:<+12.2f}%")

print("\n-> Interpretação: Diferença < 25% confirma que KMP mantém O(n+m) no pior caso!")

# ============================================================
# SPEEDUP ENTRE LINGUAGENS
# ============================================================

print("\n" + "="*70)
print("SPEEDUP (Python / C) POR TIPO DE CASO")
print("="*70)

for caso in ['MELHOR CASO', 'PIOR CASO', 'CASO MEDIO']:
    print(f"\n{caso}:")
    df_caso = df[df['tipo_caso'] == caso]
    
    for n in sorted(df_caso['n'].unique()):
        dados_n = df_caso[df_caso['n'] == n]
        if len(dados_n) == 2:
            t_c = dados_n[dados_n['linguagem']=='C']['tempo_medio'].values[0]
            t_py = dados_n[dados_n['linguagem']=='Python']['tempo_medio'].values[0]
            speedup = t_py / t_c
            print(f"  n={n:>10,}: {speedup:>6.2f}x")


# ============================================================
# GRÁFICO 1: ANÁLISE TEÓRICA vs PRÁTICA
# ============================================================

print("\n[4/4] Gerando gráficos...")

def bytes_to_label(n):
    if n >= 1_000_000:
        return f"{n//1_000_000}mb"
    elif n >= 1_000:
        return f"{n//1_000}kb"
    else:
        return f"{n}b"

tamanhos_unicos = sorted(df['n'].unique())
x_labels = [bytes_to_label(n) for n in tamanhos_unicos]
x_ticks = np.arange(len(x_labels))

# ===========================================================
# APENAS PIOR CASO (substituido por todos os casos)
# ===========================================================

fig1, ax1 = plt.subplots(figsize=(14, 8))

# Python - Pior Caso
y_python = []
for i, n in enumerate(tamanhos_unicos):
    dado = df[(df['linguagem']=='Python') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        y_python.append(dado['tempo_medio'].values[0])
        ax1.errorbar(i, dado['tempo_medio'].values[0], 
                    yerr=dado['desvio'].values[0],
                    fmt='o', color="#e900e5", capsize=5, markersize=8,
                    linewidth=2, elinewidth=1.5, zorder=3)

ax1.plot(x_ticks, y_python, '-', color='#e900e5', linewidth=2, 
        label='Python - Pior Caso Medido', zorder=2)

# C - Pior Caso
y_c = []
for i, n in enumerate(tamanhos_unicos):
    dado = df[(df['linguagem']=='C') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        y_c.append(dado['tempo_medio'].values[0])
        ax1.errorbar(i, dado['tempo_medio'].values[0],
                    yerr=dado['desvio'].values[0],
                    fmt='^', color="#ffb255", capsize=5, markersize=8,
                    linewidth=2, elinewidth=1.5, zorder=3)

ax1.plot(x_ticks, y_c, '-', color='#ffb255', linewidth=2,
        label='C - Pior Caso Medido', zorder=2)


# ============================================================
# CÁLCULO DA CONSTANTE TEÓRICA
# ============================================================

primeiro_c = df[(df['linguagem']=='C') & (df['tipo_caso']=='PIOR CASO') & (df['n']==tamanhos_unicos[0])]
primeiro_py = df[(df['linguagem']=='Python') & (df['tipo_caso']=='PIOR CASO') & (df['n']==tamanhos_unicos[0])]

if not primeiro_c.empty and not primeiro_py.empty:
    t_c = primeiro_c['tempo_medio'].values[0]
    t_py = primeiro_py['tempo_medio'].values[0]
    CONSTANTE_BASE = np.sqrt(t_c * t_py)  #media geometrica
    print(f"\n[INFO] Constante teórica calculada: {CONSTANTE_BASE:.2e} segundos")
    print(f"       (Média geométrica entre C={t_c:.2e} e Python={t_py:.2e})")
else:
    CONSTANTE_BASE = 5e-5  #fallback
    print(f"\n[INFO] Usando constante padrão: {CONSTANTE_BASE:.2e} segundos")

#calcular curva teórica: T(n) = k * n (onde k é nossa constante)
n_teorico = np.array(tamanhos_unicos)
curva_teorica_corrigida = CONSTANTE_BASE * (n_teorico / n_teorico[0])

#plotar curva teórica
ax1.plot(x_ticks, curva_teorica_corrigida, '--', color='green', linewidth=2.5,
        label='Complexidade Teórica O(n+m) [referência]', zorder=1, alpha=0.7)

#configuração do gráfico
ax1.set_yscale('log')
ax1.set_title('Análise Teórica vs. Prática (Pior Caso)',
             fontsize=16, fontweight='bold')
ax1.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
ax1.set_ylabel('Tempo de Execução (Segundos - Escala Log)', fontsize=14)
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_labels, rotation=45, ha='right')
ax1.legend(fontsize=11, loc='upper left')
ax1.grid(True, linestyle='--', alpha=0.7, which='both')

plt.tight_layout()
plt.savefig('analise_teorica_vs_pratica.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================================================
# TODOS OS CASOS
# ===========================================================

fig2, ax2 = plt.subplots(figsize=(14, 8))

cores_config = {
    ('Python', 'MELHOR CASO'): ('#f9c74f', 'o', '--'), 
    ('Python', 'CASO MEDIO'): ('#f9844a', 's', '-'), 
    ('Python', 'PIOR CASO'): ('#f94144', '^', '-'), 
    ('C', 'MELHOR CASO'): ('#90dbf4', 'o', '--'), 
    ('C', 'CASO MEDIO'): ('#577590', 's', '-'),
    ('C', 'PIOR CASO'): ('#003049', '^', '-'),
}

#plotar Python e C para todos os casos
for ling in ['Python', 'C']:
    for caso in ['MELHOR CASO', 'CASO MEDIO', 'PIOR CASO']:
        cor, marker, linestyle = cores_config[(ling, caso)]
        y_vals = []
        
        for i, n in enumerate(tamanhos_unicos):
            dado = df[(df['linguagem']==ling) & (df['tipo_caso']==caso) & (df['n']==n)]
            if not dado.empty:
                y_vals.append(dado['tempo_medio'].values[0])
                ax2.errorbar(i, dado['tempo_medio'].values[0],
                            yerr=dado['desvio'].values[0],
                            fmt=marker, color=cor, capsize=4, markersize=8,
                            linewidth=2, elinewidth=1.5, alpha=0.85, zorder=3)
        
        if y_vals:
            ax2.plot(x_ticks[:len(y_vals)], y_vals, linestyle, 
                    color=cor, linewidth=2.5,
                    label=f'{ling} - {caso}', alpha=0.9, zorder=2)

#curva teórica
ax2.plot(x_ticks, curva_teorica_corrigida, '--', color='green', linewidth=3,
        label='Complexidade Teórica O(n+m)', zorder=1, alpha=0.6)

ax2.set_yscale('log')
ax2.set_title('Análise de Performance KMP: Todos os Casos vs. Teoria',
             fontsize=16, fontweight='bold')
ax2.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
ax2.set_ylabel('Tempo de Execução (Segundos - Escala Log)', fontsize=14)
ax2.set_xticks(x_ticks)
ax2.set_xticklabels(x_labels, rotation=45, ha='right')
ax2.legend(fontsize=9, loc='upper left', ncol=2)
ax2.grid(True, linestyle='--', alpha=0.7, which='both')

plt.tight_layout()
plt.savefig('analise_todos_casos_vs_teoria.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================================================
# ANÁLISE DE ADERÊNCIA À TEORIA
# ===========================================================

print("\n" + "="*70)
print("ANÁLISE DE ADERÊNCIA À COMPLEXIDADE TEÓRICA O(n+m)")
print("="*70)

for ling in ['Python', 'C']:
    print(f"\n{ling}:")
    print(f"{'Tipo Caso':<15} {'R² (ajuste)':<15} {'Inclinação':<15} {'Qualidade'}")
    print("-"*60)
    
    for caso in ['MELHOR CASO', 'CASO MEDIO', 'PIOR CASO']:
        dados = df[(df['linguagem']==ling) & (df['tipo_caso']==caso)]
        
        if len(dados) >= 3:
            x = dados['n_mais_m'].values
            y = dados['tempo_medio'].values
            
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            
            #determina qualidade do ajuste
            r2 = r_value**2
            if r2 > 0.98:
                qualidade = "Excelente"
            elif r2 > 0.95:
                qualidade = "Muito Boa"
            elif r2 > 0.90:
                qualidade = "Boa"
            else:
                qualidade = "Ruim"
            
            print(f"{caso:<15} {r2:<15.6f} {slope:<15.2e} {qualidade}")

print("\n" + "="*70)
print("INTERPRETAÇÃO:")
print("- R² > 0.95: Forte aderência à complexidade linear O(n+m)")
print("- R² < 0.90: Possível desvio (overhead, cache, GC, etc.)")
print("="*70)

print("\nArquivos gerados:")
print("  1. analise_teorica_vs_pratica.png (curva teórica independente)")
print("  2. analise_todos_casos_vs_teoria.png (visão completa)")
print("="*70)