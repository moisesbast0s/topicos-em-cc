import pygame
import sys
from settings import *
from src.player import Player

# --- CLASSE DA CÂMERA (Estilo Mario - Travada na Vertical) ---
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        # Carrega o background
        try:
            self.bg_surf = pygame.image.load('assets/images/background.png').convert()
            self.bg_surf = pygame.transform.scale(self.bg_surf, (LARGURA_TELA, ALTURA_TELA))
        except:
            self.bg_surf = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.bg_surf.fill((135, 206, 235)) 

    def custom_draw(self, player):
        # 1. Câmera segue o jogador APENAS na Horizontal
        self.offset.x = player.rect.centerx - LARGURA_TELA // 2
        self.offset.y = 0 # Travado no zero para o chão não sair do lugar

        # 2. Desenha o Background em Loop
        bg_offset = self.offset.x 
        largura_bg = self.bg_surf.get_width()
        tiles_necessarios = (LARGURA_TELA // largura_bg) + 2
        inicio_x = -(bg_offset % largura_bg)
        
        for i in range(tiles_necessarios):
            self.display_surface.blit(self.bg_surf, (inicio_x + (i * largura_bg), 0))

        # 3. Desenha os Sprites (Player)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

# --- JOGO PRINCIPAL ---
class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        self.clock = pygame.time.Clock()

        # Grupos
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Tamanho do Mapa
        self.largura_mapa = 4000 

        # Criação do Mundo
        self.criar_chao_invisivel()
        self.criar_plataformas() # Chama a função, mas ela está vazia agora
        self.player = Player(self.all_sprites)

    def criar_chao_invisivel(self):
        """Cria o chão físico na base da tela (invisível)"""
        chao = pygame.sprite.Sprite(self.collision_sprites)
        chao.image = pygame.Surface((self.largura_mapa, 50)) 
        # O chão fica alinhado com o fundo da tela (720px)
        # Se quiser o personagem mais para cima, diminua o valor 720 para 700, etc.
        chao.rect = chao.image.get_rect(bottomleft=(0, ALTURA_TELA))

    def criar_plataformas(self):
        """
        Aqui criaremos os obstáculos no futuro.
        Por enquanto está vazio (pass) para limpar a tela.
        """
        pass 

    def checar_colisoes_verticais(self):
        self.player.on_ground = False
        sprites_atingidos = pygame.sprite.spritecollide(self.player, self.collision_sprites, False)
        
        if sprites_atingidos:
            obstaculo = sprites_atingidos[0]
            # Lógica simples de colisão com o chão
            if self.player.direction.y > 0:
                self.player.rect.bottom = obstaculo.rect.top
                self.player.direction.y = 0
                self.player.on_ground = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.tela.fill(COR_PRETA)
            
            self.all_sprites.update()
            self.checar_colisoes_verticais()
            
            # Desenha a cena
            self.all_sprites.custom_draw(self.player)
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    jogo = Jogo()
    jogo.run()