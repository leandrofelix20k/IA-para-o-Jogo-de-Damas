import pygame
import sys
from tabuleiro import Tabuleiro

def iniciarJogo(tela, dificuldade):
    rodando = True
    relogio = pygame.time.Clock()
    
    tabuleiroJogo = Tabuleiro()
    
    while rodando:
        relogio.tick(60)

        tabuleiroJogo.desenhar(tela)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False