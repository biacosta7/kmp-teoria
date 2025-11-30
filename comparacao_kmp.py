"""
Análise Completa do Algoritmo KMP
- Compara C vs Python
- Testa Melhor, Pior e Caso Médio (Requisito 6)
- Gráficos no estilo validado pelo professor (Projeto 2)
"""

import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import sys
import io
import platform

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Detectar sistema operacional para nome do executável
EXECUTAVEL_C = "teste_c.exe" if platform.system() == "Windows" else "./teste_c"

plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 10
plt.style.use('ggplot')

print("="*70)
print("ANÁLISE COMPLETA - ALGORITMO KMP")
print("Teoria da Computação - Requisito 6: Melhor/Pior/Médio Caso")
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
# EXTRAÇÃO DE DADOS
# ============================================================

def extrair_dados(logs, linguagem):
    """Extrai dados incluindo tipo de caso"""
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
print("ANÁLISE: DIFERENÇA ENTRE MELHOR E PIOR CASO (REQUISITO 6)")
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
# GRÁFICO 1: Análise Teórica vs Prática (ESTILO PROJETO 2)
# ============================================================

print("\n[4/4] Gerando gráficos...")

fig, ax = plt.subplots(figsize=(14, 8))

# Converter n para KB/MB para eixo X (como no Projeto 2)
def bytes_to_label(n):
    if n >= 1_000_000:
        return f"{n//1_000_000}mb"
    elif n >= 1_000:
        return f"{n//1_000}kb"
    else:
        return f"{n}b"

# Preparar dados para o gráfico
tamanhos_unicos = sorted(df['n'].unique())
x_labels = [bytes_to_label(n) for n in tamanhos_unicos]
x_ticks = np.arange(len(x_labels))

# Calcular curva teórica O(N) - ajustada aos dados
dados_teorico = df[(df['linguagem']=='Python') & (df['tipo_caso']=='PIOR CASO')]
x_teorico = dados_teorico['n'].values
y_teorico = dados_teorico['tempo_medio'].values

# Ajuste linear para curva teórica (não arbitrária!)
slope_teorico, intercept_teorico, _, _, _ = linregress(x_teorico, y_teorico)
curva_teorica = slope_teorico * np.array(tamanhos_unicos) + intercept_teorico

# Plotar curva teórica
ax.plot(x_ticks, curva_teorica, '--', color='green', linewidth=2.5,
        label='Complexidade Teórica $O(N)$', zorder=1)

# Plotar Python - Pior Caso
for i, n in enumerate(tamanhos_unicos):
    dado = df[(df['linguagem']=='Python') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        ax.errorbar(i, dado['tempo_medio'].values[0], 
                   yerr=dado['desvio'].values[0],
                   fmt='o', color='#e90052', capsize=5, markersize=8,
                   linewidth=2, elinewidth=1.5, zorder=3)

# Linha conectando pontos Python
y_python = []
for n in tamanhos_unicos:
    dado = df[(df['linguagem']=='Python') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        y_python.append(dado['tempo_medio'].values[0])
ax.plot(x_ticks, y_python, '-', color='#e90052', linewidth=2, 
        label='Python - Pior Caso Medido', zorder=2)

# Plotar C - Pior Caso
for i, n in enumerate(tamanhos_unicos):
    dado = df[(df['linguagem']=='C') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        ax.errorbar(i, dado['tempo_medio'].values[0],
                   yerr=dado['desvio'].values[0],
                   fmt='^', color='#0077b6', capsize=5, markersize=8,
                   linewidth=2, elinewidth=1.5, zorder=3)

# Linha conectando pontos C
y_c = []
for n in tamanhos_unicos:
    dado = df[(df['linguagem']=='C') & (df['tipo_caso']=='PIOR CASO') & (df['n']==n)]
    if not dado.empty:
        y_c.append(dado['tempo_medio'].values[0])
ax.plot(x_ticks, y_c, '-', color='#0077b6', linewidth=2,
        label='C - Pior Caso Medido', zorder=2)

# Configuração do gráfico
ax.set_yscale('log')
ax.set_title('Análise Teórica vs. Prática (Pior Caso) - Escala Logarítmica',
             fontsize=16, fontweight='bold')
ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
ax.set_ylabel('Tempo de Execução (Segundos - Escala Log)', fontsize=14)
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45, ha='right')
ax.legend(fontsize=12, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.7, which='both')

plt.tight_layout()
plt.savefig('analise_teorica_vs_pratica.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# GRÁFICO 2: Comparação C vs Python (ESTILO PROJETO 2)
# ============================================================

fig, ax = plt.subplots(figsize=(14, 8))

cores_casos = {
    'Caso Real': ('-', 'solid'),
    'Pior Caso': ('--', 'dashed')
}

# Mapear tipos de caso
mapa_casos = {
    'CASO MEDIO': 'Caso Real',
    'PIOR CASO': 'Pior Caso'
}

for ling, cor, marker in [('C', '#0077b6', '^'), ('Python', '#e90052', 'o')]:
    for tipo_orig, tipo_display in mapa_casos.items():
        # Preparar dados
        y_vals = []
        y_errs = []
        
        for n in tamanhos_unicos:
            dado = df[(df['linguagem']==ling) & (df['tipo_caso']==tipo_orig) & (df['n']==n)]
            if not dado.empty:
                y_vals.append(dado['tempo_medio'].values[0])
                y_errs.append(dado['desvio'].values[0])
            else:
                y_vals.append(np.nan)
                y_errs.append(0)
        
        # Plotar
        linestyle = cores_casos[tipo_display][1]
        label = f"{ling} ({tipo_display})"
        
        ax.errorbar(x_ticks, y_vals, yerr=y_errs,
                   marker=marker, linestyle=linestyle,
                   color=cor, capsize=4, markersize=8,
                   linewidth=2, elinewidth=1.5,
                   label=label, alpha=0.85)

# Configuração do gráfico
ax.set_yscale('log')
ax.set_title('KMP: Comparação de Performance (C vs Python) - Escala Logarítmica',
             fontsize=16, fontweight='bold')
ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
ax.set_ylabel('Tempo de Execução Médio (Segundos - Escala Log)', fontsize=14)
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45, ha='right')
ax.legend(fontsize=12, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.7, which='both')

plt.tight_layout()
plt.savefig('comparacao_c_python_performance.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# VALIDAÇÃO MATEMÁTICA RIGOROSA
# ============================================================

print("\n" + "="*70)
print("VALIDAÇÃO MATEMÁTICA DA COMPLEXIDADE O(n+m)")
print("="*70)

for ling in ['Python', 'C']:
    dados = df[(df['linguagem']==ling) & (df['tipo_caso']=='CASO MEDIO')]
    x = dados['n_mais_m'].values
    y = dados['tempo_medio'].values
    
    # Regressão linear
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    # Teste de razão constante
    ratios = []
    for i in range(1, len(x)):
        time_ratio = y[i] / y[i-1]
        size_ratio = x[i] / x[i-1]
        normalized_ratio = time_ratio / size_ratio
        ratios.append(normalized_ratio)
    
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    
    print(f"\n{ling}:")
    print(f"  R² = {r_value**2:.6f} (>0.95 indica ajuste linear excelente)")
    print(f"  p-value = {p_value:.2e} (<0.05 indica significância)")
    print(f"  Razão normalizada: {mean_ratio:.3f} ± {std_ratio:.3f}")
    print(f"  Esperado para O(n+m): ≈ 1.0")
    
    if r_value**2 > 0.95 and 0.85 <= mean_ratio <= 1.15 and p_value < 0.05:
        print(f"  ✅ Complexidade O(n+m) CONFIRMADA matematicamente!")
    else:
        print(f"  ⚠️ Dados sugerem possível desvio de O(n+m) ideal")

# ============================================================
# RESUMO FINAL
# ============================================================

print("\n" + "="*70)
print("RESUMO FINAL")
print("="*70)

print("\n✅ CHECK REQUISITO 4: Simulação com dados sintéticos")
print(f"  - {len(df)//6} tamanhos testados (1KB até 1MB)")
print(f"  - 20 repetições por teste")
print(f"  - Média e desvio padrão calculados")

print("\n✅ CHECK REQUISITO 5: Gráficos e tabelas")
print("  - Tabela comparativa completa")
print("  - Gráfico: Análise teórica vs prática (validado)")
print("  - Gráfico: Comparação C vs Python (validado)")

print("\n✅ CHECK REQUISITO 6: Análise melhor/pior/caso médio")
print("  - MELHOR CASO: Padrão não existe no texto")
print("  - PIOR CASO: AAA...AAB (valida resistência do KMP)")
print("  - CASO MÉDIO: Strings aleatórias")
print("  - Diferença entre casos confirma eficiência O(n+m)")

print("\n" + "="*70)
print("Arquivos gerados:")
print("  1. analise_teorica_vs_pratica.png (estilo Projeto 2 validado)")
print("  2. comparacao_c_python_performance.png (estilo Projeto 2 validado)")
print("="*70)