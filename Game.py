# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 1024
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Passeio de Jetpack')

# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = True

class Player (pygame.sprite.Sprite):  ### classe personagem
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//4
        self.rect.centery = HEIGHT//2

class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self):
        self.image = pygame.surface((30,50))
        self.image.fill(255,0,0)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT
        self.rect.y = random.randint (0, HEIGHT - self.rect.height)


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