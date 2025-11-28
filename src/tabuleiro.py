import pygame
from constantes import (
    BEGE, MARROM_TABULEIRO, MARROM_PECA, DOURADO, 
    LINHAS, COLUNAS, TAMANHO_QUADRADO
)
from peca import Peca

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = []
        self.pecasDouradasRestantes = 12
        self.pecasMarronsRestantes = 12
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