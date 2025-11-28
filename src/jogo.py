import pygame
from constantes import PRETO, VERMELHO, BRANCO, AZUL, TAMANHO_QUADRADO, DOURADO, MARROM_PECA
from tabuleiro import Tabuleiro

class Jogo:
    def __init__(self, tela):
        self._init()
        self.tela = tela
    
    def update(self):
        self.tabuleiro.desenhar(self.tela)
        self.desenhar_movimentos_validos(self.movimentos_validos)
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.turno = DOURADO
        self.movimentos_validos = {}

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
        
        peca = self.tabuleiro.obter_peca(linha, coluna)
        if peca != 0 and peca.cor == self.turno:
            self.selecionado = peca
            # Lógica de Captura Obrigatória / Lei da Maioria
            todos_movimentos = self.tabuleiro.obter_movimentos_validos(peca)
            self.movimentos_validos = todos_movimentos
            return True
            
        return False

    def _mover(self, linha, coluna):
        peca = self.tabuleiro.obter_peca(linha, coluna)

        if self.selecionado and peca == 0 and (linha, coluna) in self.movimentos_validos:
            # Verifica se está obedecendo a Lei da Maioria (deve implementar globalmente)
            # Para simplificar neste passo, permitimos o movimento validado pelo tabuleiro
            
            self.tabuleiro.mover_peca(self.selecionado, linha, coluna)
            capturados = self.movimentos_validos[(linha, coluna)]
            if capturados:
                self.tabuleiro.remover(capturados)
            
            self.mudar_turno()
        else:
            return False

        return True

    def desenhar_movimentos_validos(self, movimentos):
        for movimento in movimentos:
            linha, coluna = movimento
            pygame.draw.circle(self.tela, AZUL, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2), 15)

    def mudar_turno(self):
        self.movimentos_validos = {}
        if self.turno == DOURADO:
            self.turno = MARROM_PECA
        else:
            self.turno = DOURADO

def iniciarJogo(tela, dificuldade):
    jogo = Jogo(tela)
    rodando = True
    relogio = pygame.time.Clock()

    while rodando:
        relogio.tick(60)

        if jogo.vencedor() != None:
            print(f"Vencedor: {jogo.vencedor()}")
            rodando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                linha, coluna = obter_linha_coluna_do_mouse(pos)
                jogo.selecionar(linha, coluna)
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        jogo.update()

def obter_linha_coluna_do_mouse(pos):
    x, y = pos
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna