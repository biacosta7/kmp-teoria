# 🚀 Teoria da Complexidade e Análise de Tempo do Algoritmo KMP

Este repositório apresenta uma análise completa do desempenho do algoritmo **Knuth–Morris–Pratt (KMP)**, incluindo:

- Avaliação teórica e prática  
- Simulações com diferentes casos  
- Comparação entre implementações em **C** e **Python**  
- Gráficos e tabelas gerados automaticamente  
- Validação da complexidade assintótica  


## 📘 Descrição do Algoritmo

O algoritmo **KMP** resolve o problema de *pattern matching* exato, encontrando todas as ocorrências de um padrão `P` dentro de um texto `T`.

Seu diferencial é **evitar retrocessos no texto**, graças à **tabela LPS** (*Longest Prefix which is also a Suffix*), que indica quanto o padrão pode avançar após um mismatch — tornando a busca eficiente e previsível.


## 🔧 Aplicações do KMP

O KMP é amplamente utilizado em:

- 📌 Padrões grandes com repetições  
- ⚙️ Sistemas embarcados com tempo crítico  
- 📚 Buscas frequentes em textos extensos  
- ❌ Cenários com muitos mismatches  
- ⏱️ Processamento em tempo real  

É uma excelente escolha quando é necessário **desempenho estável e garantido**.

## 📊 Simulação com Dados

Para validar a complexidade O(n + m) do KMP na prática, foram realizadas simulações em C e Python, variando o tamanho do texto e do padrão.
Cada experimento foi repetido 20 vezes, registrando tempo médio e desvio padrão para garantir precisão estatística.

---

## 🧱 Arquitetura do Projeto

```bash
 📂 **kmp-teoria**  
 ├── `comparacao_kmp.py` — Executa todos os testes e gera gráficos/tabelas  
 ├── `teste.py` — Código e testes do KMP em Python  
 ├── `teste.c` — Código e testes do KMP em C  
 ├── `analise_teorica_vs_pratica.png` — Gráfico gerado automaticamente  
 ├── `comparacao_c_python_performance.png` — Gráfico gerado automaticamente  
 └── `README.md`
```

## 🚀 Como rodar o projeto

### 1) Instalar dependências Python
```bash
pip install pandas matplotlib scipy numpy
```

### 2) Compilar o código em C
#### 🪟 Windows
```bash
gcc teste.c -o teste_c.exe -lm
```

#### 🐧 Linux / macOS
```bash
gcc teste.c -o teste_c -lm
```

### 3) Rodar os testes individualmente
#### Python:
```bash
python teste.py
```

#### C:
Windows:
```bash
./teste_c.exe
```
Linux/macOS:
```bash
./teste_c
```

### 4) Rodar a análise completa 
```bash
python comparacao_kmp.py
```

Isso irá:

- compilar automaticamente o `teste.c`
- rodar os testes em C e Python  
- gerar tabelas comparativas  
- calcular diferenças entre casos  
- validar a complexidade O(n+m)  
- gerar os gráficos:  
  - `analise_teorica_vs_pratica.png`  
  - `comparacao_c_python_performance.png`

## ⏳ Análise de Complexidade

O KMP é composto por duas fases:
### Construção da Tabela LPS — O(m)
- Processa somente o padrão.
- Sempre linear, independente dos casos.
  
### Busca no texto — O(n)
- ⭐ Melhor Caso: textos e padrões aleatórios onde o primeiro caractere do padrão nunca aparece no texto, forçando mismatches imediatos.
- 🔥 Pior Caso: padrões e textos altamente repetitivos (aaaa...ab), projetados para maximizar o uso da tabela LPS — ainda assim mantendo crescimento linear.
- 📈 Caso Médio: texto e padrão totalmente aleatórios, representando o comportamento típico do algoritmo.

### Complexidade Total
- O(n + m)

## 👥 Equipe
- Beatriz Costa
- Nina França
- Sofia Gomes
