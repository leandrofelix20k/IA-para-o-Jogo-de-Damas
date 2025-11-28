import pygame
from constantes import TAMANHO_QUADRADO, CINZA, DOURADO

class Peca:
    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.dama = False
        self.x = 0
        self.y = 0
        self.calcularPosicao()

    def calcularPosicao(self):
        self.x = TAMANHO_QUADRADO * self.coluna + TAMANHO_QUADRADO // 2
        self.y = TAMANHO_QUADRADO * self.linha + TAMANHO_QUADRADO // 2

    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.calcularPosicao()

    def tornarDama(self):
        self.dama = True

    def desenhar(self, tela):
        raio = TAMANHO_QUADRADO // 2 - 15
        pygame.draw.circle(tela, CINZA, (self.x, self.y), raio + 2)
        pygame.draw.circle(tela, self.cor, (self.x, self.y), raio)
        
        if self.dama:
            pygame.draw.circle(tela, CINZA, (self.x, self.y), raio // 2)
    
    def __repr__(self):
        return str(self.cor)