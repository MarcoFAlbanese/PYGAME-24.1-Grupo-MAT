# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from Sprites import Player, Obstaculos

pygame.init()

# ----- Gera tela principal
WIDTH = 1024
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Passeio de Jetpack')

# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = True


#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)


# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    #window.fill((255, 255, 255))  # Preenche com a cor branca
    window.fill((255, 255, 255))
    all_sprites.draw(window)


    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados