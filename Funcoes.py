import pygame
import random
import math
from Assets import load_assets
from Sprites import Coin, Powerup,Intangivel,ReduzVelo


WIDTH = 1000
HEIGHT = 650

def mais_coins(all_sprites, coins, assets):  ## aparece mais coins
    if random.randrange(100) < 2:
        coin = Coin(assets)
        all_sprites.add(coin)
        coins.add(coin)

def atualiza_coins(player, coins, assets, pontos):  ## atualiza pontuação
    for coin in coins:
        coin.update()
        if pygame.sprite.collide_rect(player, coin):
            coin.kill()
            pontos = aumenta_pontos(assets, pontos)
    return pontos

def aumenta_pontos(assets, pontos):  ## aumenta a pontuação
    pontos += 1
    pygame.mixer.Sound.play(assets['moedas_sound'])
    return pontos

def show_pontos(window, pontos):  ## mostra pontuação
    fonte = pygame.font.Font(None, 50)
    texto = fonte.render(str(pontos), True, (255, 255, 255))
    window.blit(texto, (WIDTH / 2, 20))

def distancia(sprite1, sprite2):
    centro1 = sprite1.rect.center
    centro2 = sprite2.rect.center
    return math.sqrt((centro1[0] - centro2[0]) ** 2 + (centro1[1] - centro2[1]) ** 2)


def mais_poder(all_sprites, powerups, pontos, powerup_timer, powerup_intervalo):
    if len(powerups) == 0 and powerup_timer <= 0:
        if pontos % 25 == 0 and pontos != 0:
            powerup = Intangivel()
        elif pontos % 10 == 0 and pontos != 0:
            powerup = ReduzVelo()
        else:
            return
        all_sprites.add(powerup)
        powerups.add(powerup)
        powerup_timer = powerup_intervalo

def atualiza_poder(player, powerups, all_sprites, obstaculos, powerup_timer):
    for powerup in powerups:
        powerup.update()
        if pygame.sprite.collide_rect(player, powerup):
            if isinstance(powerup, Intangivel):
                powerup.aplica_poder(player)
            elif isinstance(powerup, ReduzVelo):
                powerup.aplica_poder(obstaculos)
            powerup.kill()
    if powerup_timer > 0:
        powerup_timer -= 1