import pygame
import random
from Assets import load_assets



WIDTH = 1000
HEIGHT = 650

class Player (pygame.sprite.Sprite):  ### classe personagem
    def __init__(self,assets):
        pygame.sprite.Sprite.__init__(self) 
        player_image = assets['player_image']
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

    def __init__(self,assets):
        pygame.sprite.Sprite.__init__(self)
        coin_image = assets['coin_image']
        self.image = pygame.transform.scale(coin_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,HEIGHT - self.rect.height)
        self.speed_x = -3

    def update(self):
        self.rect.x += self.speed_x
    
class Fumaca(pygame.sprite.Sprite): ### classe para fumaça da jetpack
    def __init__(self,assets,player):
        pygame.sprite.Sprite.__init__(self)
        fumaca_image = assets['fumaca_image']
        self.image = pygame.transform.scale(fumaca_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH//4)-60
        self.rect.y = player.rect.centery
        self.speed_y = 8

    def update(self):
        self.rect.y += self.speed_y

class Obstaculos(pygame.sprite.Sprite): ### classe dos obstaculos
    def __init__(self,assets,pontos):
        pygame.sprite.Sprite.__init__(self)
        obstaculo_image = assets['obstaculo_image']
        self.image = pygame.transform.scale(obstaculo_image, (120,80))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(30,(HEIGHT-self.rect.height))
        self.speed_x = -5* (1+(0.01*pontos))
       
    def update(self):
        self.rect.x += self.speed_x 