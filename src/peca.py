import pygame
from constantes import TAMANHO_QUADRADO, CINZA, DOURADO
import pygame
from constantes import TAMANHO_QUADRADO, CINZA, DOURADO
from copy import deepcopy # <--- NOVO IMPORT
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
  
    # método para cópia profunda
    def __deepcopy__(self, memo):
        cls = self.__class__
        nova_peca = cls.__new__(cls)
        memo[id(self)] = nova_peca

        # Copiar todos os atributos necessários
        nova_peca.linha = self.linha
        nova_peca.coluna = self.coluna
        nova_peca.cor = self.cor
        nova_peca.dama = self.dama
        nova_peca.x = self.x
        nova_peca.y = self.y

        return nova_peca
