import pygame
import sys
import jogo
from constantes import (
    LARGURA, ALTURA, PRETO, BRANCO, CINZA, CINZA_CLARO,
    FACIL, MEDIO, DIFICIL, DOURADO
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

def exibirRegras(tela):
    rodando = True
    fonteTitulo = pygame.font.SysFont("arial", 35, bold=True)
    fonteTexto = pygame.font.SysFont("arial", 20) 
    fonteDestaque = pygame.font.SysFont("arial", 20, bold=True)
    fonteBotao = pygame.font.SysFont("arial", 25)

    regras = [
        ("1. TABULEIRO & INÍCIO:", True),
        ("   - Tabuleiro 64 casas. Grande diagonal escura à esquerda.", False),
        ("   - As Brancas sempre fazem o lance inicial.", False),
        ("", False),
        ("2. MOVIMENTAÇÃO:", True),
        ("   - Pedra: Move 1 casa na diagonal, sempre para frente.", False),
        ("   - Dama: Ao atingir a casa de coroação (última linha), vira Dama.", False),
        ("   - A Dama move-se livremente na diagonal (frente e trás).", False),
        ("", False),
        ("3. CAPTURA (OBRIGATÓRIA):", True),
        ("   - Não existe sopro. Captura p/ frente e p/ trás (Pedra e Dama).", False),
        ("   - A Dama pode parar em qualquer casa após a peça capturada.", False),
        ("", False),
        ("4. LEI DA MAIORIA (REGRA CRUCIAL):", True),
        ("   - Se houver mais de uma opção de captura, é OBRIGATÓRIO", False),
        ("     escolher o lance que captura o MAIOR número de peças.", False),
        ("   - Pedra e Dama têm o mesmo valor na contagem (valem 1).", False),
        ("", False),
        ("5. REGRAS TÉCNICAS:", True),
        ("   - Captura em Cadeia: Peças capturadas só saem no fim do lance.", False),
        ("   - Se passar pela casa de coroação capturando, NÃO vira Dama.", False),
        ("   - Empate: 20 lances sucessivos de Dama sem captura.", False)
    ]

    rectVoltar = pygame.Rect(0, 0, 200, 50)
    rectVoltar.center = (LARGURA // 2, 720)

    while rodando:
        tela.fill(PRETO)
        posicaoMouse = pygame.mouse.get_pos()

        desenharTexto("REGRAS OFICIAIS (CBJD)", fonteTitulo, DOURADO, tela, LARGURA // 2, 60)

        yInicial = 120
        espacamento = 26
        
        for texto, destaque in regras:
            if destaque:
                textoObj = fonteDestaque.render(texto, True, DOURADO)
            else:
                textoObj = fonteTexto.render(texto, True, BRANCO)
            
            tela.blit(textoObj, (50, yInicial))
            yInicial += espacamento

        desenharBotao(tela, rectVoltar, "VOLTAR", fonteBotao, posicaoMouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectVoltar.collidepoint(posicaoMouse):
                    return

        pygame.display.update()

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
                    exibirRegras(tela)
                    
                if retanguloSair.collidepoint(posicaoMouse):
                    rodando = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()