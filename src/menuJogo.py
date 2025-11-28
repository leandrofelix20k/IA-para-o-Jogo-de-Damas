import pygame
import sys
import jogo
from constantes import (
    LARGURA, ALTURA, PRETO, BRANCO, CINZA, CINZA_CLARO,
    FACIL, MEDIO, DIFICIL
)

pygame.font.init()

def desenharTexto(texto, fonte, cor, superficie, x, y):
    objetoTexto = fonte.render(texto, True, cor)
    retanguloTexto = objetoTexto.get_rect(center=(x, y))
    superficie.blit(objetoTexto, retanguloTexto)

def desenharBotao(tela, retangulo, texto, fonte, posicaoMouse):
    corBotao = CINZA
    if retangulo.collidepoint(posicaoMouse):
        corBotao = CINZA_CLARO
    
    pygame.draw.rect(tela, corBotao, retangulo)
    desenharTexto(texto, fonte, PRETO, tela, retangulo.centerx, retangulo.centery)

def selecionarDificuldade(tela):
    rodando = True
    fonteTitulo = pygame.font.SysFont("arial", 50, bold=True)
    fonteBotao = pygame.font.SysFont("arial", 40)
    fonteVoltar = pygame.font.SysFont("arial", 20)
    
    botaoLargura = 400
    botaoAltura = 80
    centroX = LARGURA // 2

    retanguloFacil = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloFacil.center = (centroX, 300)

    retanguloMedio = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloMedio.center = (centroX, 420)

    retanguloDificil = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloDificil.center = (centroX, 540)
    
    retanguloVoltar = pygame.Rect(10, 10, 100, 50)

    while rodando:
        tela.fill(PRETO)
        posicaoMouse = pygame.mouse.get_pos()

        desenharTexto("SELECIONE A DIFICULDADE", fonteTitulo, BRANCO, tela, centroX, 150)

        desenharBotao(tela, retanguloFacil, "FÁCIL", fonteBotao, posicaoMouse)
        desenharBotao(tela, retanguloMedio, "MÉDIO", fonteBotao, posicaoMouse)
        desenharBotao(tela, retanguloDificil, "DIFÍCIL", fonteBotao, posicaoMouse)
        desenharBotao(tela, retanguloVoltar, "VOLTAR", fonteVoltar, posicaoMouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if retanguloFacil.collidepoint(posicaoMouse):
                    return FACIL
                if retanguloMedio.collidepoint(posicaoMouse):
                    return MEDIO
                if retanguloDificil.collidepoint(posicaoMouse):
                    return DIFICIL
                if retanguloVoltar.collidepoint(posicaoMouse):
                    return None

        pygame.display.update()

def executar(tela):
    rodando = True
    fonteTitulo = pygame.font.SysFont("arial", 60, bold=True)
    fonteBotao = pygame.font.SysFont("arial", 40)

    botaoLargura = 400
    botaoAltura = 80
    centroX = LARGURA // 2

    retanguloNovaPartida = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloNovaPartida.center = (centroX, 300)

    retanguloRegras = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloRegras.center = (centroX, 420)

    retanguloSair = pygame.Rect(0, 0, botaoLargura, botaoAltura)
    retanguloSair.center = (centroX, 540)

    while rodando:
        tela.fill(PRETO)
        posicaoMouse = pygame.mouse.get_pos()

        desenharTexto("DAMAS IA", fonteTitulo, BRANCO, tela, centroX, 150)

        desenharBotao(tela, retanguloNovaPartida, "NOVA PARTIDA", fonteBotao, posicaoMouse)
        desenharBotao(tela, retanguloRegras, "REGRAS DO JOGO", fonteBotao, posicaoMouse)
        desenharBotao(tela, retanguloSair, "SAIR", fonteBotao, posicaoMouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if retanguloNovaPartida.collidepoint(posicaoMouse):
                    dificuldade = selecionarDificuldade(tela)
                    if dificuldade is not None:
                        jogo.iniciarJogo(tela, dificuldade)
                        
                if retanguloRegras.collidepoint(posicaoMouse):
                    pass
                    
                if retanguloSair.collidepoint(posicaoMouse):
                    rodando = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()