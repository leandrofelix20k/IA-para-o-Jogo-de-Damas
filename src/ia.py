# ia.py
from copy import deepcopy
from constantes import MARROM_PECA, DOURADO, LINHAS, COLUNAS
import pygame

# --- Função de Avaliação (inalterada) ---
def avaliar_tabuleiro(tabuleiro):
    # ... (código inalterado) ...
    valor_peca = 1.0
    valor_dama = 2.0 

    pontuacao = (tabuleiro.pecasMarronsRestantes * valor_peca) - (tabuleiro.pecasDouradasRestantes * valor_peca)

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            peca = tabuleiro.obterPeca(linha, coluna)
            if peca != 0:
                if peca.dama:
                    if peca.cor == MARROM_PECA:
                        pontuacao += (valor_dama - valor_peca)
                    else:
                        pontuacao -= (valor_dama - valor_peca)

    return pontuacao


# --- Função de Simulação do MiniMax (inalterada) ---
def minimax(posicao, profundidade, alpha, beta, maximizando_jogador, cor_ia):
    if profundidade == 0 or posicao.vencedor() is not None:
        return avaliar_tabuleiro(posicao), None

    lances_validos = gerar_lances_validos(posicao)
    
    # ... (lógica minimax inalterada) ...
    if maximizando_jogador:
        max_avaliacao = float('-inf')
        melhor_lance = None
        
        for tabuleiro_simulado in lances_validos:
            avaliacao, _ = minimax(tabuleiro_simulado, profundidade - 1, alpha, beta, False, cor_ia)
            
            if avaliacao > max_avaliacao:
                max_avaliacao = avaliacao
                melhor_lance = tabuleiro_simulado
            
            alpha = max(alpha, max_avaliacao)
            if beta <= alpha:
                break
        
        if not lances_validos:
            return avaliar_tabuleiro(posicao), None
        
        return max_avaliacao, melhor_lance

    else:
        min_avaliacao = float('inf')
        melhor_lance = None
        
        for tabuleiro_simulado in lances_validos:
            avaliacao, _ = minimax(tabuleiro_simulado, profundidade - 1, alpha, beta, True, cor_ia)
            
            if avaliacao < min_avaliacao:
                min_avaliacao = avaliacao
                melhor_lance = tabuleiro_simulado
            
            beta = min(beta, min_avaliacao)
            if beta <= alpha:
                break

        if not lances_validos:
            return avaliar_tabuleiro(posicao), None

        return min_avaliacao, melhor_lance


# --- Geração de Lances Válidos (CORRIGIDO) ---
def gerar_lances_validos(tabuleiro):
    lances_tabuleiros = []
    
    # --- AGORA CHAMA O MÉTODO DA CLASSE TABULEIRO ---
    tabuleiro._calcularMovimentosObrigatorios() 
    
    movimentos_globais = tabuleiro.movimentosValidosGlobais

    for peca_origem, movimentos in movimentos_globais.items():
        for destino, capturadas in movimentos.items():
            linha_destino, coluna_destino = destino
            
            # 1. Cria uma cópia profunda para simulação
            tabuleiro_simulado = deepcopy(tabuleiro)
            
            # 2. Encontra a peça na cópia (a referência mudou)
            # Nota: É preciso garantir que peca_origem seja tratada corretamente
            # ao procurarmos na cópia do tabuleiro.
            peca_simulada = tabuleiro_simulado.obterPeca(peca_origem.linha, peca_origem.coluna)
            
            # 3. Move a peça na simulação
            tabuleiro_simulado.moverPeca(peca_simulada, linha_destino, coluna_destino)
            
            # 4. Remove as peças capturadas na simulação
            pecas_a_remover = []
            for peca_capturada in capturadas:
                 pecas_a_remover.append(tabuleiro_simulado.obterPeca(peca_capturada.linha, peca_capturada.coluna))
            
            tabuleiro_simulado.remover(pecas_a_remover)
            
            # 5. Muda o turno na simulação e calcula os movimentos do próximo jogador
            tabuleiro_simulado.turno = MARROM_PECA if tabuleiro_simulado.turno == DOURADO else DOURADO
            tabuleiro_simulado._calcularMovimentosObrigatorios() # NOVO CÁLCULO PARA O PRÓXIMO TURNO
            
            # 6. Adiciona o tabuleiro resultante à lista
            lances_tabuleiros.append(tabuleiro_simulado)
            
    return lances_tabuleiros