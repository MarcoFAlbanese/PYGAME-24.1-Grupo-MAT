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
player_image = pygame.image.load('assets/player.png').convert_alpha()
# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = True

class Player (pygame.sprite.Sprite):  ### classe personagem
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (85, 85))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//4
        self.rect.centery = HEIGHT//2
        self.speed_y = 0
    
    def update(self):
        self.speed_y +=1
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0





class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0,(HEIGHT-self.rect.height))
        self.speed_x = -5
       
    def update(self):
        self.rect.x += self.speed_x 
        

#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()


#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)


clock = pygame.time.Clock()
FPS = 50

space_pressed = False

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False
        
    if space_pressed == True:
        player.speed_y = -8
    
    if random.randrange(100)< 5:
        obstaculo = Obstaculos()
        all_sprites.add(obstaculo)
        obstaculos.add(obstaculo)
        if len(obstaculos) > 1 and pygame.sprite.collide_rect(obstaculo, obstaculos.sprites()[-2]):
            obstaculo.kill()

    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, obstaculos, False)
    if hits:
        game = False


    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca
    all_sprites.draw(window)



    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados