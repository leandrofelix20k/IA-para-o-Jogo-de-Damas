import pygame
import sys
from constantes import (
    PRETO, CINZA, CINZA_CLARO, AZUL, 
    TAMANHO_QUADRADO, DOURADO, MARROM_PECA,
    LARGURA, ALTURA
)
from tabuleiro import Tabuleiro

class Jogo:
    def __init__(self, tela):
        self._init()
        self.tela = tela
    
    def update(self):
        self.tabuleiro.desenhar(self.tela)
        self.desenharMovimentosValidos(self.movimentosValidos)
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.turno = DOURADO
        self.movimentosValidos = {}

    def vencedor(self):
        return self.tabuleiro.vencedor()

    def reset(self):
        self._init()

    def selecionar(self, linha, coluna):
        if self.selecionado:
            resultado = self._mover(linha, coluna)
            if not resultado:
                self.selecionado = None
                self.selecionar(linha, coluna)
        
        peca = self.tabuleiro.obterPeca(linha, coluna)
        if peca != 0 and peca.cor == self.turno:
            self.selecionado = peca
            self.movimentosValidos = self.tabuleiro.obterMovimentosValidos(peca)
            return True
            
        return False

    def _mover(self, linha, coluna):
        peca = self.tabuleiro.obterPeca(linha, coluna)

        if self.selecionado and peca == 0 and (linha, coluna) in self.movimentosValidos:
            self.tabuleiro.moverPeca(self.selecionado, linha, coluna)
            capturados = self.movimentosValidos[(linha, coluna)]
            if capturados:
                self.tabuleiro.remover(capturados)
            
            self.mudarTurno()
        else:
            return False

        return True

    def desenharMovimentosValidos(self, movimentos):
        for movimento in movimentos:
            linha, coluna = movimento
            pygame.draw.circle(self.tela, AZUL, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2), 15)

    def mudarTurno(self):
        self.movimentosValidos = {}
        if self.turno == DOURADO:
            self.turno = MARROM_PECA
        else:
            self.turno = DOURADO

def desenharTextoCentralizado(tela, texto, tamanho, cor, y):
    fonte = pygame.font.SysFont("arial", tamanho, bold=True)
    objetoTexto = fonte.render(texto, True, cor)
    rectTexto = objetoTexto.get_rect(center=(LARGURA // 2, y))
    tela.blit(objetoTexto, rectTexto)

def desenharBotao(tela, rect, texto, mousePos):
    cor = CINZA
    if rect.collidepoint(mousePos):
        cor = CINZA_CLARO
    
    pygame.draw.rect(tela, cor, rect)
    fonte = pygame.font.SysFont("arial", 30)
    textoSurf = fonte.render(texto, True, PRETO)
    textoRect = textoSurf.get_rect(center=rect.center)
    tela.blit(textoSurf, textoRect)

def telaFinal(tela, vencedor):
    rodando = True
    if vencedor == DOURADO:
        mensagem = "VITÓRIA!"
        corMensagem = DOURADO
    else:
        mensagem = "DERROTA!"
        corMensagem = MARROM_PECA

    larguraBotao = 300
    alturaBotao = 60
    centroX = LARGURA // 2

    rectReiniciar = pygame.Rect(0, 0, larguraBotao, alturaBotao)
    rectReiniciar.center = (centroX, 400)

    rectMenu = pygame.Rect(0, 0, larguraBotao, alturaBotao)
    rectMenu.center = (centroX, 500)

    sombra = pygame.Surface((LARGURA, ALTURA))
    sombra.set_alpha(200)
    sombra.fill(PRETO)
    tela.blit(sombra, (0,0))

    while rodando:
        mousePos = pygame.mouse.get_pos()
        desenharTextoCentralizado(tela, mensagem, 80, corMensagem, 200)
        desenharBotao(tela, rectReiniciar, "JOGAR NOVAMENTE", mousePos)
        desenharBotao(tela, rectMenu, "VOLTAR AO MENU", mousePos)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SAIR"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectReiniciar.collidepoint(mousePos):
                    return "RESTART"
                if rectMenu.collidepoint(mousePos):
                    return "MENU"

def obterLinhaColunaMouse(pos):
    x, y = pos
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

def iniciarJogo(tela, dificuldade):
    jogo = Jogo(tela)
    rodando = True
    relogio = pygame.time.Clock()

    while rodando:
        relogio.tick(60)

        vencedor = jogo.vencedor()
        if vencedor is not None:
            acao = telaFinal(tela, vencedor)
            if acao == "SAIR":
                rodando = False
                pygame.quit()
                sys.exit()
            elif acao == "MENU":
                rodando = False
            elif acao == "RESTART":
                jogo.reset()
                
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                linha, coluna = obterLinhaColunaMouse(pos)
                jogo.selecionar(linha, coluna)
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w: 
                   jogo.tabuleiro.pecasMarronsRestantes = 0

        jogo.update()