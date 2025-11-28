## ♟️ IA para o Jogo de Damas

## 📝 Descrição do Projeto

Este projeto consiste no desenvolvimento de um **agente inteligente** capaz de jogar o **Jogo de Damas** de forma autônoma contra um usuário. O Jogo de Damas é classificado como um problema clássico de **tomada de decisão sequencial**, e o objetivo é utilizar a Inteligência Artificial (IA) para tomar decisões ótimas em cada jogada.

Os dados utilizados pelo agente incluem o registro das posições das peças, a validação das jogadas e a aplicação das regras oficiais do jogo.

---

## ✨ Recursos e Funcionalidades

* **Agente Inteligente:** Capacidade de tomar decisões estratégicas no jogo.
* **Níveis de Dificuldade:** O sistema oferece diferentes níveis de desafio para o usuário, implementados com base no algoritmo Minimax com Poda Alfa-Beta:
    * Fácil
    * Médio
    * Difícil
* **Interface Gráfica:** Ambiente visual para interação com o tabuleiro.

---

## 🛠️ Implementação Técnica

### Algoritmo Principal
A inteligência do agente é baseada no algoritmo **Minimax com Poda Alfa-Beta**. Este algoritmo é utilizado para simular o jogo, buscando a jogada que maximiza a pontuação do agente e minimiza a pontuação do oponente, de forma eficiente. 

### Linguagem e Ferramentas
* **Linguagem:** **Python**
* **Ferramentas:**
    * **Pygame:** Utilizado para a criação da interface do tabuleiro.
    * **NumPy:** Utilizado para possíveis cálculos ou manipulações de dados no backend da IA.