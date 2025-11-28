import pygame
from constantes import (
    PRETO, LINHAS, COLUNAS, TAMANHO_QUADRADO, 
    BEGE, MARROM_TABULEIRO, MARROM_PECA, DOURADO
)
from peca import Peca

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = []
        self.pecasDouradasRestantes = 12
        self.pecasMarronsRestantes = 12
        self.damaDourada = 0
        self.damaMarrom = 0
        self.criarTabuleiro()

    def desenharQuadrados(self, tela):
        tela.fill(BEGE)
        for linha in range(LINHAS):
            for coluna in range(linha % 2, COLUNAS, 2):
                pygame.draw.rect(
                    tela, 
                    MARROM_TABULEIRO, 
                    (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
                )

    def criarTabuleiro(self):
        for linha in range(LINHAS):
            self.tabuleiro.append([])
            for coluna in range(COLUNAS):
                if coluna % 2 == ((linha + 1) % 2):
                    if linha < 3:
                        self.tabuleiro[linha].append(Peca(linha, coluna, MARROM_PECA))
                    elif linha > 4:
                        self.tabuleiro[linha].append(Peca(linha, coluna, DOURADO)) 
                    else:
                        self.tabuleiro[linha].append(0)
                else:
                    self.tabuleiro[linha].append(0)

    def desenhar(self, tela):
        self.desenharQuadrados(tela)
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca != 0:
                    peca.desenhar(tela)

    def obter_peca(self, linha, coluna):
        return self.tabuleiro[linha][coluna]

    def mover_peca(self, peca, linha, coluna):
        # Atualiza a matriz do tabuleiro (Lógica)
        self.tabuleiro[peca.linha][peca.coluna], self.tabuleiro[linha][coluna] = self.tabuleiro[linha][coluna], self.tabuleiro[peca.linha][peca.coluna]
        
        # Atualiza a peça (Visual e atributos internos)
        peca.mover(linha, coluna)

        # Regra de Promoção à Dama
        if linha == LINHAS - 1 or linha == 0:
            if (peca.cor == MARROM_PECA and linha == LINHAS - 1) or (peca.cor == DOURADO and linha == 0):
                peca.tornar_dama()

    def remover(self, pecas):
        for peca in pecas:
            self.tabuleiro[peca.linha][peca.coluna] = 0
            if peca != 0:
                if peca.cor == DOURADO:
                    self.pecasDouradasRestantes -= 1
                else:
                    self.pecasMarronsRestantes -= 1

    def vencedor(self):
        if self.pecasDouradasRestantes <= 0:
            return MARROM_PECA
        elif self.pecasMarronsRestantes <= 0:
            return DOURADO
        return None

    def obter_movimentos_validos(self, peca):
        movimentos = {}
        esquerda = peca.coluna - 1
        direita = peca.coluna + 1
        linha = peca.linha

        if peca.cor == DOURADO or peca.dama:
            movimentos.update(self._atravessar_esquerda(linha - 1, max(linha - 3, -1), -1, peca.cor, esquerda, peca.dama))
            movimentos.update(self._atravessar_direita(linha - 1, max(linha - 3, -1), -1, peca.cor, direita, peca.dama))
        
        if peca.cor == MARROM_PECA or peca.dama:
            movimentos.update(self._atravessar_esquerda(linha + 1, min(linha + 3, LINHAS), 1, peca.cor, esquerda, peca.dama))
            movimentos.update(self._atravessar_direita(linha + 1, min(linha + 3, LINHAS), 1, peca.cor, direita, peca.dama))
    
        return movimentos

    def _atravessar_esquerda(self, inicio, fim, passo, cor, esquerda, dama, capturados=[]):
        movimentos = {}
        ultimo = []
        for r in range(inicio, fim, passo):
            if esquerda < 0:
                break
            
            atual = self.tabuleiro[r][esquerda]
            
            if atual == 0:
                if capturados and not ultimo:
                    break
                elif capturados:
                    movimentos[(r, esquerda)] = ultimo + capturados
                else:
                    movimentos[(r, esquerda)] = ultimo
                
                if capturados:
                    if passo == -1: row = max(r-3, -1)
                    else: row = min(r+3, LINHAS)
                    movimentos.update(self._atravessar_esquerda(r+passo, row, passo, cor, esquerda-1, dama, ultimo+capturados))
                    movimentos.update(self._atravessar_direita(r+passo, row, passo, cor, esquerda+1, dama, ultimo+capturados))
                break
            
            elif atual.cor == cor:
                break
            
            else:
                if ultimo: 
                    break 
                ultimo = [atual]

            esquerda -= 1
        
        return movimentos

    def _atravessar_direita(self, inicio, fim, passo, cor, direita, dama, capturados=[]):
        movimentos = {}
        ultimo = []
        for r in range(inicio, fim, passo):
            if direita >= COLUNAS:
                break
            
            atual = self.tabuleiro[r][direita]
            
            if atual == 0:
                if capturados and not ultimo:
                    break
                elif capturados:
                    movimentos[(r, direita)] = ultimo + capturados
                else:
                    movimentos[(r, direita)] = ultimo
                
                if capturados:
                    if passo == -1: row = max(r-3, -1)
                    else: row = min(r+3, LINHAS)
                    movimentos.update(self._atravessar_esquerda(r+passo, row, passo, cor, direita-1, dama, ultimo+capturados))
                    movimentos.update(self._atravessar_direita(r+passo, row, passo, cor, direita+1, dama, ultimo+capturados))
                break
            
            elif atual.cor == cor:
                break
            
            else:
                if ultimo:
                    break
                ultimo = [atual]

            direita += 1
        
        return movimentos