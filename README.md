<div align="center">

# ParseMathExpression 

**Um analisador léxico e sintático de expressões matemáticas com uma interface gráfica moderna e robusta, construída em Python e PySide6.**

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/PySide-6-orange?style=for-the-badge&logo=qt)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>



---

##  Demonstração

<div align="center">

![GIF da Aplicação](https://github.com/Junior-jrp/ParseMathExpression/blob/main/ReadmeAssets/gif_PME.gif?raw=true)



</div>

---

##  Funcionalidades Principais

- **Análise Completa:** Implementação de um **Analisador Léxico (Lexer)** para tokenizar a expressão e um **Analisador Sintático (Parser)** de descida recursiva para construir a árvore de operações.
- **Precedência de Operadores:** Respeita a ordem matemática correta das operações (`^` antes de `*`/`/` antes de `+`/`-`).
- **Associatividade de Operadores:** Lida corretamente com a associatividade, incluindo a associatividade à direita para potenciação (`2 ^ 3 ^ 2` é calculado como `2 ^ (3 ^ 2)`).
- **Suporte a Parênteses:** Permite o agrupamento de expressões com parênteses para alterar a ordem de prioridade.
- **Operadores Unários:** Reconhece e calcula corretamente números negativos (ex: `-5 + 10`).
- **Interface Gráfica Moderna:** UI elegante e intuitiva construída com **PySide6**, com tema escuro e design focado na usabilidade.
- **Tratamento de Erros:** Fornece feedback claro e específico para erros de sintaxe, erros matemáticos (como divisão por zero) e caracteres inválidos.
- **Painel de Exemplos:** Uma aba dedicada que demonstra a capacidade do parser com uma vasta gama de expressões válidas e inválidas.

---

## Screenshots

<table align="center">
  <tr>
    <td align="center"><strong>Calculadora</strong></td>
    <td align="center"><strong>Exemplos de Uso</strong></td>
    <td align="center"><strong>Sobre</strong></td>
  </tr>
  <tr>
    <td><img src="https://github.com/Junior-jrp/ParseMathExpression/blob/main/ReadmeAssets/Image2.png?raw=true" alt="Screenshot da Calculadora" width="400"/></td>
    <td><img src="https://github.com/Junior-jrp/ParseMathExpression/blob/main/ReadmeAssets/Image3.png?raw=true" alt="Screenshot dos Exemplos" width="400"/></td>
    <td><img src="https://github.com/Junior-jrp/ParseMathExpression/blob/main/ReadmeAssets/Image1.png?raw=true" alt="Screenshot Sobre" width="400"/></td>
  </tr>
</table>

---

## Tecnologias e Conceitos Aplicados

- **Linguagem:** **Python 3**
- **Interface Gráfica:** **PySide6 (Qt for Python)**
- **Conceitos de Teoria da Computação:**
  - **Análise Léxica:** Uso de expressões regulares para dividir a string de entrada em uma sequência de *tokens* (números, operadores, etc.).
  - **Análise Sintática:** Construção de uma **Árvore Sintática Abstrata (AST)** para representar a estrutura hierárquica da expressão.
  - **Parser de Descida Recursiva:** A técnica de parsing implementada.
  - **Avaliação de AST:** O processo de "resolver" a árvore para encontrar o resultado final.

---

## Possíveis Melhorias


- **Suporte a Funções Matemáticas:**
  - Implementar funções como `sqrt()`, `log()`, `sin()`, `cos()`, `tan()`, etc.
  - Exemplo: `sqrt(4) + sin(pi / 2)`

- **Inclusão de Constantes:**
  - Adicionar suporte a constantes matemáticas conhecidas, como `pi` e `e`.

- **Variáveis Definidas pelo Usuário:**
  - Permitir que o usuário defina e utilize variáveis (`x = 5`, `y = 10`, `x * y`).
  - Isso transformaria a calculadora em um ambiente de script simples.

- **Histórico de Cálculos:**
  - Adicionar uma nova aba ou painel para exibir um histórico dos cálculos realizados na sessão.

- **Plotagem de Gráficos:**
  - Integrar a biblioteca `Matplotlib` para plotar gráficos de funções com uma variável (ex: plotar `f(x) = x^2`).

---

##  Como Executar

Siga os passos abaixo para executar o projeto em sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Junior-jrp/ParseMathExpression.git
    cd ParseMathExpression
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências necessárias:**
    ```bash
    pip install PySide6
    ```

4.  **Execute a aplicação:**
    ```bash
    python main_app.py
    ```


---

Este projeto foi desenvolvido como requisito avaliativo da disciplina de **Teoria da Computação** no **Instituto Federal do Ceará  - Campus Maracanaú**

<div align="center">
  <img src="https://github.com/Junior-jrp/ParseMathExpression/blob/main/logo.png?raw=true" alt="Logo" width="150"/>
</div>
