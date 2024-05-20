# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import math

from pygame.sprite import Group

pygame.init()
pygame.mixer.init()

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
background_inicio_final = pygame.image.load('assets/background2.png').convert_alpha()
background_inicio_final = pygame.transform.scale(background_inicio_final, (WIDTH, HEIGHT))
music = pygame.mixer.music.load('assets/musica_de_fundo.ogg')
pygame.mixer.music.set_volume(0.5)
moedas = pygame.mixer.Sound('assets/moedas_sfx.ogg')
moedas.set_volume(0.5)
lapis = pygame.mixer.Sound('assets/som_lapis.ogg')

# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = False
powerup_timer = 0
powerup_intervalo = 600

class Player (pygame.sprite.Sprite):  ### classe personagem
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (85, 85))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//4
        self.rect.centery = HEIGHT//2
        self.speed_y = 0
        self.intangivel = False
        self.intangivel_timer = 0
    
    def update(self):
        self.speed_y +=1
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0

        #atualiza tempo de intangivel
        if self.intangivel:
            self.intangivel_timer -= 1
            if self.intangivel_timer <=0:
                self.intangivel = False



class Coin(pygame.sprite.Sprite): ### classe sistema de pontuação

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

def mais_coins(): ## aparece mais coins
    if random.randrange(100)< 2:
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

def atualiza_coins(): ## atualiza pontuação
    for coin in coins:
        coin.update()
        if pygame.sprite.collide_rect(player,coin):
            coin.kill()
            aumenta_pontos()

def aumenta_pontos(): ## aumenta a pontuação
    global pontos
    pontos +=1
    pygame.mixer.Sound.play(moedas)

def show_pontos(): ## mostra pontuação
    fonte = pygame.font.Font(None, 50)
    texto = fonte.render(str(pontos), True,(255,255,255))
    window.blit(texto,(WIDTH/2,20))

class Fumaca(pygame.sprite.Sprite): ### classe para fumaça da jetpack
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
        self.image = pygame.transform.scale(obstaculo_image, (120,80))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,(HEIGHT-self.rect.height))
        self.speed_x = -5* (1+(0.01*pontos))
       
    def update(self):
        self.rect.x += self.speed_x 
        
def distancia (sprite1,sprite2):
    centro1 = sprite1.rect.center
    centro2 = sprite2.rect.center
    return (math.sqrt((centro1[0] - centro2[0]) ** 2 + (centro1[1] - centro2[1]) ** 2))

class Powerup (pygame.sprite.Sprite): ## classe dos poderes do jogo
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image,(60,60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30, HEIGHT - self.rect.height)
        self.speed_x = -3

    def update(self):
        self.rect.x += self.speed_x

class Intangivel(Powerup): ## poder de ficar imortal
    def __init__(self):
        super().__init__(pygame.image.load('assets/intangibilidade.png').convert_alpha())
    def aplica_poder(self,player):
        player.intangivel = True
        player.intangivel_timer = 300 #5 segundos

class ReduzVelo (Powerup): ## poder de diminuir a velocidade do jogo
    def __init__(self):
        super().__init__(pygame.image.load('assets/reduzvelo.png').convert_alpha())
    def aplica_poder (self,obstaculos):
        for obstaculo in obstaculos:
            obstaculo.speed_x *= 0.5

def mais_poder(): ## Adiciona powerups
    global powerup_timer
    if len(powerups) == 0 and powerup_timer<=0:
        if pontos % 30 == 0 and pontos != 0:
            powerup = Intangivel()
        elif pontos % 15 == 0 and pontos!= 0:
            powerup = ReduzVelo()
        else:
            return
        all_sprites.add(powerup)
        powerups.add(powerup)
        powerup_timer = powerup_intervalo


def atualiza_poder():
    global powerup_timer
    for powerup in powerups:
        powerup.update()
        if pygame.sprite.collide_rect(player, powerup):
            if isinstance(powerup, Intangivel):
                powerup.aplica_poder(player)
            elif isinstance(powerup, ReduzVelo):
                powerup.aplica_poder(obstaculos)
            powerup.kill()
    if powerup_timer>0:
        powerup_timer-=1


#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
fumaca = pygame.sprite.Group()
powerups = pygame.sprite.Group()


#adiciona o player na lista de sprites
player = Player()
all_sprites.add(player)


clock = pygame.time.Clock()
FPS = 60
bg_x = 0  # Posição inicial do background
space_pressed = False

#### Função da tela de inicio
def tela_inicio():
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(background_inicio_final,(0,0))
    fonte = pygame.font.SysFont("Menlo", 30)
    texto = fonte.render("pressione espaço para jogar", True, (200,255,70))
    texto_rect = texto.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(texto, texto_rect)
    fonte = pygame.font.SysFont("Menlo", 40)
    texto2 = fonte.render("bem-vindo(a) a um passeio de jetpack!", True, (200,255,70))
    texto2_rect = texto.get_rect(center=(WIDTH//2-190, HEIGHT//4))
    window.blit(texto2, texto2_rect)
    pygame.display.flip()

#### Função tela final
def tela_final():
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(background_inicio_final,(0,0))
    fonte = pygame.font.SysFont("Menlo", 30)
    texto = fonte.render("Fim de jogo. Você deseja jogar novamente? (Y/N)", True, (200,255,70))
    texto_rect = texto.get_rect(center=(WIDTH//2,HEIGHT//2))
    window.blit(texto,texto_rect)
    pygame.display.flip()

tela_inicio() #inicia tela de inicio

# ==== Loop tela inicial =====
while not game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game =  True
# ===== Loop principal =====
game = True
game_over = False
obstaculo_mask = pygame.mask.from_surface(obstaculo_image)
# ==== Loop do jogo =====
while not game_over:

    pygame.mixer.music.play(-1)

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
                    lapis.play()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    lapis.stop()
            
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
        mais_poder()
        atualiza_poder()
        all_sprites.update()

        for obstaculo in obstaculos: ## gera obstaculos
            obstaculo.update()

            obstaculo_mask = pygame.mask.from_surface(obstaculo_image)

            if pygame.sprite.spritecollide(player,obstaculos,False,pygame.sprite.collide_mask): ## forma de perder
                game = False 

            if obstaculo.rect.right < 0:
                obstaculo.kill()

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

    tela_final() ## inicia tela final
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y: ## reinicia o jogo
                game =  True
                pontos = 0
                player.rect.centerx = WIDTH//4
                player.rect.centery = HEIGHT//2
                for sprite in all_sprites.copy():
                    if sprite != player:
                        sprite.kill()
            elif event.key == pygame.K_n: ## fecha o jogo
                pygame.quit()
        
        elif event.type == pygame.QUIT:
            pygame.quit



