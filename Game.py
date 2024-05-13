# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import math

pygame.init()


# ----- Gera tela principal
WIDTH = 1000
HEIGHT = 650
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Passeio de Jetpack')
player_image = pygame.image.load('assets/player.png').convert_alpha()
obstaculo_image = pygame.image.load('assets/bala.png').convert_alpha()
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
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

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill((255,215,0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,HEIGHT - self.rect.height)
    def update(self):
        self.rect.x += self.speed_x
pontos = 0
coins = pygame.sprite.Group()
def mais_coins():
    if random.randrange(100)< 3:
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)
def atualiza_coins():
    for coin in coins:
        coin.update()
        if pygame.sprite.collide_rect(player,coin):
            coin.kill()
            aumenta_pontos()
def aumenta_pontos():
    global pontos
    pontos +=1
def show_pontos():
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(pontos, True,(0,0,0))
    window.blit(texto,(10,10))






class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(obstaculo_image, (70, 50))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,(HEIGHT-self.rect.height))
        self.speed_x = -5
       
    def update(self):
        self.rect.x += self.speed_x 
        
def distancia (sprite1,sprite2):
    centro1 = sprite1.rect.center
    centro2 = sprite2.rect.center
    return (math.sqrt((centro1[0] - centro2[0]) ** 2 + (centro1[1] - centro2[1]) ** 2))

#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()


#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)


clock = pygame.time.Clock()
FPS = 60 
bg_x = 0  # Posição inicial do background
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
    
    
    if random.randrange(100)< 3:
        obstaculo = Obstaculos()
        all_sprites.add(obstaculo)
        obstaculos.add(obstaculo)

        if len(obstaculos) > 1 and (pygame.sprite.collide_rect(obstaculo, obstaculos.sprites()[-2]) or distancia(obstaculo, obstaculos.sprites()[-2]) < 200):
            obstaculo.kill()
    mais_coins()
    atualiza_coins()
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, obstaculos, False)
    if hits:
        game = False
    
    # Atualiza a posição do background
    bg_x -= 3  # Velocidade de rolagem do background
    if bg_x <= -WIDTH:
        bg_x = 0

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(background, (bg_x, 0))
    window.blit(background, (bg_x + WIDTH, 0))
    all_sprites.draw(window)
    show_pontos()



    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
