# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()


# ----- Gera tela principal
WIDTH = 1000
HEIGHT = 650
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Passeio de Jetpack')
player_image = pygame.image.load('PYGAME-24.1-Grupo-MAT/assets/player.png').convert()
# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = True

class Player (pygame.sprite.Sprite):  ### classe personagem
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//4
        self.rect.centery = HEIGHT//2



class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
       
    def update(self):
        self.rect.x -= 5  


#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()


#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)

obstaculo = Obstaculos()
all_sprites.add(obstaculo)



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