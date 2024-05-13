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
player_mask = pygame.mask.from_surface(player_image)
obstaculo_image = pygame.image.load('assets/bala.png').convert_alpha()
coin_image = pygame.image.load('assets/moedas.png').convert_alpha()
fumaca_image=pygame.image.load('assets/fumaca.png').convert_alpha()
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = False

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
        self.image = pygame.transform.scale(coin_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,HEIGHT - self.rect.height)
        self.speed_x = -3

    def update(self):
        self.rect.x += self.speed_x

pontos = 0
coins = pygame.sprite.Group()

def mais_coins():
    if random.randrange(100)< 2:
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
    fonte = pygame.font.Font(None, 50)
    texto = fonte.render(str(pontos), True,(255,255,255))
    window.blit(texto,(WIDTH/2,20))

class Fumaca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fumaca_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH//4)-60
        self.rect.y = player.rect.centery
        self.speed_y = 8

    def update(self):
        self.rect.y += self.speed_y

class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(obstaculo_image, (100, 60))
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
fumaca = pygame.sprite.Group()

#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)


clock = pygame.time.Clock()
FPS = 60 
bg_x = 0  # Posição inicial do background
space_pressed = False
def tela_inicio():
    window.fill((0,0,0))
    fonte = pygame.font.Font(None, 50)
    texto = fonte.render("pressione espaço para jogar", True, (255,255,255))
    window.blit(texto, (WIDTH// 4, HEIGHT// 2))
    pygame.display.flip()

tela_inicio()
while not game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game =  True
# ===== Loop principal =====
game = True
obstaculo_mask = pygame.mask.from_surface(obstaculo_image)

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
        player.speed_y = -10
        nova_fumaca = Fumaca()
        all_sprites.add(nova_fumaca)
        fumaca.add(nova_fumaca)

    for f in fumaca:
        f.update()
        if f.rect.right < 0:
            f.kill()
    
    
    if random.randrange(100)< 2:
        obstaculo = Obstaculos()
        all_sprites.add(obstaculo)
        obstaculos.add(obstaculo)

        if len(obstaculos) > 1 and (pygame.sprite.collide_rect(obstaculo, obstaculos.sprites()[-2]) or distancia(obstaculo, obstaculos.sprites()[-2]) < 200):
            obstaculo.kill()

    mais_coins()
    atualiza_coins()
    all_sprites.update()

    for obstaculo in obstaculos:
        obstaculo.update()

        obstaculo_mask = pygame.mask.from_surface(obstaculo_image)

        if pygame.sprite.spritecollide(player,obstaculos,False,pygame.sprite.collide_mask):
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
