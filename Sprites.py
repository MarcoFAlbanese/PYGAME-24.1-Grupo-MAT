#Funções que usaremos no nosso jogo:
import pygame
import random
from Game import WIDTH, HEIGHT,BLACK
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

        
