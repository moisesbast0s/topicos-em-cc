import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # --- CONFIGURAÇÃO DAS ANIMAÇÕES ---
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True
        
        # Dicionário para guardar as listas de quadros
        self.animations = {'idle': [], 'run': [], 'attack': []}
        
        # Carrega e recorta as imagens
        self.import_character_assets()
        
        # Define a imagem inicial
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        self.rect.inflate_ip(-50, -10) # Ajuste fino da colisão

        # --- FÍSICA ---
        self.direction = pygame.math.Vector2()
        self.speed = VELOCIDADE_JOGADOR
        self.gravity = GRAVIDADE
        self.jump_speed = PULO_FORCA
        self.on_ground = False
        self.is_attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

    def import_character_assets(self):
        """
        Carrega as Sprite Sheets e as fatia em quadros individuais.
        Assume que a IA gerou os quadros alinhados horizontalmente.
        """
        # Configuração: Quantos quadros tem em cada imagem gerada pela IA?
        # Ajuste estes números se sua imagem tiver mais ou menos poses
        qtd_frames = {
            'idle': 4,   # A IA gerou 4 poses paradas?
            'run': 8,    # A IA gerou 8 poses correndo?
            'attack': 4  # A IA gerou 4 poses atacando?
        }

        for animation in self.animations.keys():
            full_path = f'assets/images/player/{animation}.png'
            try:
                sheet = pygame.image.load(full_path).convert_alpha()
                
                # Descobre a largura de UM quadro (dividir largura total por qtd frames)
                sheet_width = sheet.get_width()
                sheet_height = sheet.get_height()
                frame_width = sheet_width // qtd_frames[animation]
                
                # Recorta cada quadro
                for x in range(qtd_frames[animation]):
                    # Cria uma superfície transparente para o quadro
                    frame_surface = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
                    
                    # Recorta o pedaço da folha (blit com area)
                    rect_recorte = pygame.Rect(x * frame_width, 0, frame_width, sheet_height)
                    frame_surface.blit(sheet, (0, 0), rect_recorte)
                    
                    # Escala o quadro para o tamanho do jogo (ex: 128x128)
                    frame_surface = pygame.transform.scale(frame_surface, TAMANHO_PLAYER)
                    
                    self.animations[animation].append(frame_surface)
            except:
                print(f"ERRO: Não encontrei a imagem {full_path}. Usando quadrado vermelho.")
                # Fallback de segurança
                surf = pygame.Surface(TAMANHO_PLAYER)
                surf.fill(COR_VERMELHA)
                self.animations[animation].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()

        # Só move se não estiver atacando (opcional, trava o player no ataque)
        if not self.is_attacking:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()

        # Ataque (Tecla Z ou J)
        if (keys[pygame.K_z] or keys[pygame.K_j]) and not self.is_attacking:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.frame_index = 0 # Reinicia animação para começar do frame 0 do ataque

    def get_status(self):
        """Define qual animação deve tocar"""
        if self.is_attacking:
            self.status = 'attack'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        # Loop da animação
        self.frame_index += self.animation_speed
        
        # Se a animação acabou
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.is_attacking = False # Fim do ataque
            self.frame_index = 0

        # Pega a imagem certa e vira se necessário
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
            
        # Atualiza o rect (mantendo a posição do pé alinhada)
        # Isso evita que o personagem "vibre" se os sprites tiverem tamanhos diferentes
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)
            
        # Re-aplica o ajuste da hitbox
        self.rect.inflate_ip(-50, -10) 

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False

    def update(self):
        self.input()
        self.get_status() # Descobre o estado (correndo, parado...)
        self.animate()    # Troca a imagem
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()