import pygame
from constantes import (
    PRETO, LINHAS, COLUNAS, TAMANHO_QUADRADO, 
    BEGE, MARROM_TABULEIRO, MARROM_PECA, DOURADO
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

    def obterPeca(self, linha, coluna):
        if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
            return self.tabuleiro[linha][coluna]
        return None

    def moverPeca(self, peca, linha, coluna):
        # Atualiza a matriz
        self.tabuleiro[peca.linha][peca.coluna], self.tabuleiro[linha][coluna] = self.tabuleiro[linha][coluna], self.tabuleiro[peca.linha][peca.coluna]
        peca.mover(linha, coluna)

        # Regra de Promoção à Dama
        if not peca.dama:
            if (peca.cor == MARROM_PECA and linha == LINHAS - 1) or (peca.cor == DOURADO and linha == 0):
                peca.tornarDama()

    def remover(self, pecas):
        for peca in pecas:
            self.tabuleiro[peca.linha][peca.coluna] = 0
            if peca != 0:
                if peca.cor == DOURADO:
                    self.pecasDouradasRestantes -= 1
                else:
                    self.pecasMarronsRestantes -= 1

    def vencedor(self):
        if self.pecasDouradasRestantes <= 0:
            return MARROM_PECA
        elif self.pecasMarronsRestantes <= 0:
            return DOURADO
        return None

    def obterMovimentosValidos(self, peca):
        movimentos = {}
        
        # 1. Primeiro verificamos se há capturas (pois são obrigatórias)
        capturas = self._buscarTodasCapturas(peca)
        if capturas:
            return capturas
        
        # 2. Se não houver capturas, verificamos movimentos simples
        movimentos = self._buscarMovimentosSimples(peca)
        return movimentos

    def _buscarMovimentosSimples(self, peca):
        movimentos = {}
        linhaAtual = peca.linha
        colunaAtual = peca.coluna
        
        if peca.dama:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dLinha, dColuna in direcoes:
                for i in range(1, 8):
                    novaLinha = linhaAtual + (dLinha * i)
                    novaColuna = colunaAtual + (dColuna * i)
                    
                    if not self._posicaoValida(novaLinha, novaColuna):
                        break
                    
                    conteudo = self.tabuleiro[novaLinha][novaColuna]
                    if conteudo == 0:
                        movimentos[(novaLinha, novaColuna)] = []
                    else:
                        break
        else:
            direcaoFrente = -1 if peca.cor == DOURADO else 1
            opcoes = [(direcaoFrente, -1), (direcaoFrente, 1)]
            
            for dLinha, dColuna in opcoes:
                novaLinha = linhaAtual + dLinha
                novaColuna = colunaAtual + dColuna
                
                if self._posicaoValida(novaLinha, novaColuna):
                    if self.tabuleiro[novaLinha][novaColuna] == 0:
                        movimentos[(novaLinha, novaColuna)] = []

        return movimentos

    def _buscarTodasCapturas(self, peca):
        movimentos = {}
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self._capturaRecursiva(peca, peca.linha, peca.coluna, [], movimentos, direcoes)
        return movimentos

    def _capturaRecursiva(self, peca, linha, coluna, capturados, movimentosFinais, direcoes):
        for dLinha, dColuna in direcoes:
            if peca.dama:
                for i in range(1, 8):
                    linhaInimigo = linha + (dLinha * i)
                    colunaInimigo = coluna + (dColuna * i)
                    
                    if not self._posicaoValida(linhaInimigo, colunaInimigo):
                        break
                        
                    conteudo = self.tabuleiro[linhaInimigo][colunaInimigo]
                    
                    if conteudo == 0:
                        continue
                    
                    if conteudo in capturados or conteudo.cor == peca.cor:
                        break
                    
                    for j in range(i + 1, 8):
                        linhaPouso = linha + (dLinha * j)
                        colunaPouso = coluna + (dColuna * j)
                        
                        if not self._posicaoValida(linhaPouso, colunaPouso):
                            break
                        
                        if self.tabuleiro[linhaPouso][colunaPouso] != 0:
                            break
                        
                        novosCapturados = capturados + [conteudo]
                        
                        if (linhaPouso, colunaPouso) not in movimentosFinais or len(novosCapturados) > len(movimentosFinais.get((linhaPouso, colunaPouso), [])):
                             movimentosFinais[(linhaPouso, colunaPouso)] = novosCapturados

                        self._capturaRecursiva(peca, linhaPouso, colunaPouso, novosCapturados, movimentosFinais, direcoes)
                    break 

            else:
                linhaInimigo = linha + dLinha
                colunaInimigo = coluna + dColuna
                linhaPouso = linha + (dLinha * 2)
                colunaPouso = coluna + (dColuna * 2)
                
                if self._posicaoValida(linhaPouso, colunaPouso):
                    pecaInimiga = self.tabuleiro[linhaInimigo][colunaInimigo]
                    
                    if pecaInimiga != 0 and pecaInimiga.cor != peca.cor and pecaInimiga not in capturados:
                        if self.tabuleiro[linhaPouso][colunaPouso] == 0:
                            novosCapturados = capturados + [pecaInimiga]
                            movimentosFinais[(linhaPouso, colunaPouso)] = novosCapturados
                            self._capturaRecursiva(peca, linhaPouso, colunaPouso, novosCapturados, movimentosFinais, direcoes)

    def _posicaoValida(self, linha, coluna):
        return 0 <= linha < LINHAS and 0 <= coluna < COLUNAS