# IA para o Jogo de Damas

**Disciplina:** Introdução à Inteligência Artificial<br>
**Semestre:** 2025.2<br>
**Professor:** Andre Luis Fonseca Faustino<br>
**Turma:** T04<br>

## Integrantes do Grupo

* Vinicios David Martins Bezerra (20220062699)
* Jose Kaua de Lima Souza (20240038645)
* Leandro Felix de Almeida Silva (20210055289)

## Descrição do Projeto

Este projeto consiste no desenvolvimento de um agente inteligente capaz de jogar Damas seguindo as regras oficiais brasileiras (CBJD). O objetivo principal é a implementação do algoritmo **Minimax com Poda Alfa-Beta** para a tomada de decisão sequencial em um ambiente competitivo adversário.

A aplicação foi desenvolvida utilizando a linguagem **Python**. Para a interface gráfica e gerenciamento de eventos, utilizou-se a biblioteca **Pygame**.

## Guia de Instalação e Execução

Siga os passos abaixo para configurar o ambiente e executar o jogo em sua máquina local.

### 1. Instalação das Dependências

Certifique-se de ter o **Python 3.x** instalado. Recomenda-se o uso de um ambiente virtual (venv). Clone o repositório e instale as bibliotecas listadas no `requirements.txt`:

```bash
# Clone o repositório
git clone [https://github.com/leandrofelix20k/IA-para-o-Jogo-de-Damas.git](https://github.com/leandrofelix20k/IA-para-o-Jogo-de-Damas.git)

# Entre na pasta do projeto
cd IA-para-o-Jogo-de-Damas

# Crie e ative o ambiente virtual
# Linux/Mac:
python3 -m venv venv
source venv/bin/activate
# Windows:
# python -m venv venv
# .\venv\Scripts\activate

# Instale as dependências
pip install -r src/requirements.txt

# Execute o jogo
python src/main.py