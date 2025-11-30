# 🚀 Teoria da Complexidade e Análise de Tempo do Algoritmo KMP

Este repositório apresenta uma análise completa do desempenho do algoritmo Knuth–Morris–Pratt (KMP), incluindo simulações práticas, comparações entre implementações em C e Python, gráficos, tabelas e validação da sua complexidade assintótica.
---
## 📘 Descrição do Algoritmo

O algoritmo KMP resolve o problema de pattern matching exato, encontrando todas as ocorrências de um padrão P dentro de um texto T.

Seu diferencial é evitar retrocessos no texto, graças à construção da tabela LPS (Longest Prefix which is also a Suffix), que permite ao algoritmo saber automaticamente quanto deslocar o padrão após um mismatch.
---
🔧 Aplicações do KMP

O KMP é amplamente utilizado em:

📌 Padrões grandes com repetições

⚙️ Sistemas embarcados com tempo crítico

📚 Buscas constantes em textos extensos

❌ Cenários com muitos mismatches

⏱️ Processamento em tempo real

O algoritmo é ideal quando é necessário desempenho estável e previsível.

---
📊 Simulação com Dados
<img width="630" height="298" alt="image" src="https://github.com/user-attachments/assets/9b41cc14-e31d-49fc-a1bc-4f3addc235f7" />
---
⚖️ Comparação de Performance: C x Python
➡️ C domina em velocidade absoluta, especialmente para entradas grandes.
➡️ Python é mais lento, mas ainda mantém o comportamento linear esperado.
➡️ O KMP demonstra alta eficiência e estabilidade em ambas as implementações.
---

