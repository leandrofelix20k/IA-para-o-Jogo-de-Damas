import pygame
import menuJogo
from constantes import LARGURA, ALTURA

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Damas - Inteligência Artificial")
    
    menuJogo.executar(tela)

if __name__ == "__main__":
    main()