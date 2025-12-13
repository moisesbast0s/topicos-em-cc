# main.py
import pygame
import sys
from settings import * # Importa tudo do arquivo settings

class Jogo:
    def __init__(self):
        # 1. Inicializa o Pygame
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        self.clock = pygame.time.Clock()
        
        # Aqui vamos carregar os sprites depois...
        # self.jogador = Jogador() 

    def run(self):
        """O Loop Principal do Jogo"""
        while True:
            # 1. Checar Eventos (Teclado/Mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Aqui podemos colocar o 'if event.key == K_SPACE: pular'

            # 2. Atualizar a Lógica (Movimento, Colisão)
            # self.jogador.update()
            
            # 3. Desenhar na Tela (Renderizar)
            self.tela.fill(COR_PRETA) # Limpa a tela com preto a cada frame
            
            # self.jogador.draw(self.tela) # Desenha o jogador
            
            pygame.display.update() # Atualiza o display
            self.clock.tick(FPS) # Garante que rode a 60 FPS

# Só roda se for o arquivo principal
if __name__ == '__main__':
    jogo = Jogo()
    jogo.run()