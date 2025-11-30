import pygame
import sys
import time

from constantes import (
    PRETO, CINZA, CINZA_CLARO, AZUL, VERDE, VERMELHO,
    TAMANHO_QUADRADO, DOURADO, MARROM_PECA,
    LARGURA, ALTURA, LINHAS, COLUNAS,
    FACIL, MEDIO, DIFICIL 
)
from tabuleiro import Tabuleiro
from ia import minimax 



def obterLinhaColunaMouse(pos):
    x, y = pos
    # garantem que sempre retornará números inteiros
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

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


class Jogo:
    def __init__(self, tela, dificuldade): 
        self._init()
        self.tela = tela
        self.rectDesistir = pygame.Rect(3, 10, 80, 40)
        self.dificuldade = dificuldade
        self.profundidade = self._definir_profundidade(dificuldade)
        
        # Delay da IA
        self.aguardando_ia = False
        self.tempo_inicio_ia = 0
        self.delay_ia = 0.7   # tempo em segundos


    def _definir_profundidade(self, dificuldade):
        if dificuldade == FACIL:
            return 1
        elif dificuldade == MEDIO:
            return 3
        elif dificuldade == DIFICIL:
            return 5
        return 1

    def mudarTurno(self):
        self.movimentosValidos = {}
        self.selecionado = None
        
        # Inverte o turno no Tabuleiro
        if self.tabuleiro.turno == DOURADO:
            self.tabuleiro.turno = MARROM_PECA
        else:
            self.tabuleiro.turno = DOURADO
        
        # Recalcula movimentos (agora método de Tabuleiro)
        self.tabuleiro._calcularMovimentosObrigatorios()

    def lance_ia(self):
        avaliacao, tabuleiro_melhor_lance = minimax(
            self.tabuleiro, 
            self.profundidade, 
            float('-inf'), 
            float('inf'), 
            True,
            MARROM_PECA
        )

        if tabuleiro_melhor_lance:
            # O tabuleiro retornado já está no estado pós-lance da IA (turno trocado)
            self.tabuleiro = tabuleiro_melhor_lance
            
            # Reseta estado visual do Jogo
            self.movimentosValidos = {}
            self.selecionado = None
            
    def update(self):
        self.tabuleiro.desenhar(self.tela)
        self.desenharDicasVisuais() 
        self.desenharBotaoDesistir()
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        # O Tabuleiro agora gerencia o turno e os movimentos válidos globais
        self.tabuleiro = Tabuleiro() 
        self.movimentosValidos = {}
        
    def vencedor(self):
        return self.tabuleiro.vencedor()

    def reset(self):
        self._init()
        self.profundidade = self._definir_profundidade(self.dificuldade)

    def selecionar(self, linha, coluna):
        if self.selecionado:
            resultado = self._mover(linha, coluna)
            if not resultado:
                self.selecionado = None
                self.selecionar(linha, coluna)
                return True 
        
        peca = self.tabuleiro.obterPeca(linha, coluna)
        
        if peca != 0 and peca.cor == self.tabuleiro.turno:
            if peca in self.tabuleiro.movimentosValidosGlobais:
                self.selecionado = peca
                self.movimentosValidos = self.tabuleiro.movimentosValidosGlobais[peca]
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

    def desenharDicasVisuais(self):
        if self.selecionado:
            self._desenharBolinhasDestino(self.movimentosValidos)
            pygame.draw.circle(self.tela, VERDE, (self.selecionado.x, self.selecionado.y), 50, 4)
        
        elif self.tabuleiro.capturaObrigatoria:
            for peca, movimentos in self.tabuleiro.movimentosValidosGlobais.items():
                pygame.draw.circle(self.tela, VERDE, (peca.x, peca.y), 40, 3)
                self._desenharBolinhasDestino(movimentos)

    def _desenharBolinhasDestino(self, movimentos):
        for movimento in movimentos:
            linha, coluna = movimento
            cx = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            cy = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            pygame.draw.circle(self.tela, AZUL, (cx, cy), 15)

    def desenharBotaoDesistir(self):
        mousePos = pygame.mouse.get_pos()
        cor = VERMELHO
        if self.rectDesistir.collidepoint(mousePos):
            cor = (200, 0, 0)

        pygame.draw.rect(self.tela, cor, self.rectDesistir, border_radius=5)
        
        fonte = pygame.font.SysFont("arial", 20, bold=True)
        texto = fonte.render("DESISTIR", True, (255, 255, 255))
        rectTexto = texto.get_rect(center=self.rectDesistir.center)
        self.tela.blit(texto, rectTexto)


def iniciarJogo(tela, dificuldade):
    jogo = Jogo(tela, dificuldade) 
    rodando = True
    relogio = pygame.time.Clock()

    while rodando:
        relogio.tick(60)

        vencedor = jogo.vencedor()
        
        # --- Tela final ---
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

        # --- Lógica da IA (com delay) ---
        if jogo.tabuleiro.turno == MARROM_PECA and vencedor is None:

            # IA ainda não começou a esperar → inicia o timer
            if not jogo.aguardando_ia:
                jogo.aguardando_ia = True
                jogo.tempo_inicio_ia = time.time()

            # IA já está esperando → verifica se terminou o delay
            else:
                if time.time() - jogo.tempo_inicio_ia >= jogo.delay_ia:
                    jogo.lance_ia()
                    jogo.aguardando_ia = False

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Botão desistir
                if jogo.rectDesistir.collidepoint(pos):
                    acao = telaFinal(tela, MARROM_PECA)
                    if acao == "SAIR":
                        rodando = False
                        pygame.quit()
                        sys.exit()
                    elif acao == "MENU":
                        rodando = False
                    elif acao == "RESTART":
                        jogo.reset()
                
                # Jogador (DOURADO)
                elif jogo.tabuleiro.turno == DOURADO:
                    linha, coluna = obterLinhaColunaMouse(pos)
                    jogo.selecionar(linha, coluna)
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w: 
                    jogo.tabuleiro.pecasMarronsRestantes = 0

        jogo.update()
        