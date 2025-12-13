# settings.py

# --- Configurações da Janela ---
LARGURA_TELA = 1280
ALTURA_TELA = 720
FPS = 60
TITULO_JOGO = "Ecos da Fortaleza: A Fuga de São José"

# --- Cores ---
COR_PRETA = (0, 0, 0)
COR_BRANCA = (255, 255, 255)
COR_VERMELHA = (255, 0, 0)
COR_CINZA = (100, 100, 100)

# --- Configurações Visuais ---
TAMANHO_PLAYER = (128, 128) # Aumentei para ficar mais proporcional (antes era 64x64)
TAMANHO_TILE_CHAO = 64      # Tamanho de cada quadradinho do chão

# --- Física do Jogador ---
VELOCIDADE_JOGADOR = 6      # Um pouco mais rápido já que o mapa é grande
GRAVIDADE = 0.8
PULO_FORCA = -18            # Pulo mais forte para compensar o tamanho