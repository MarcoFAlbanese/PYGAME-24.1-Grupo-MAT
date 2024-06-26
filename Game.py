# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import math
from pygame.sprite import Group
from Assets import load_assets
from Sprites import Player,Coin,Fumaca,Obstaculos,Powerup,Intangivel,ReduzVelo
from Funcoes import *

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 1000
HEIGHT = 650
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Passeio de Jetpack')


# ----- Inicia estruturas de dados
BLACK = (0,0,0)
game = False
powerup_timer = 0
powerup_intervalo = 600
assets = load_assets()

pontos = 0
coins = pygame.sprite.Group()





#lista com todos sprites
all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
fumaca = pygame.sprite.Group()
powerups = pygame.sprite.Group()


#adiciona o player na lista de sprites
player = Player(assets)
all_sprites.add(player)


clock = pygame.time.Clock()
FPS = 60
bg_x = 0  # Posição inicial do background
space_pressed = False

#### Função da tela de inicio
def tela_inicio():
    background_inicio_final = assets["background_inicio_final"]
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
    background_inicio_final = assets["background_inicio_final"]
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(background_inicio_final,(0,0))
    fonte = pygame.font.SysFont("Menlo", 30)
    texto = fonte.render("Fim de jogo. Você deseja jogar novamente? (Y/N)", True, (200,255,70))
    texto_pontuacao = fonte.render("Pontuação: " + str(pontuacao_alcançada), True, (200,255,70))
    texto_pontuacao_rect = texto_pontuacao.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    texto_rect = texto.get_rect(center=(WIDTH//2,HEIGHT//2))
    window.blit(texto_pontuacao, texto_pontuacao_rect)
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
obstaculo_mask = pygame.mask.from_surface(assets['obstaculo_image'])
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
                    assets['lapis_sound'].play()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    assets['lapis_sound'].stop()
            
        if space_pressed == True:
            player.speed_y = -10
            nova_fumaca = Fumaca(assets,player)
            all_sprites.add(nova_fumaca)
            fumaca.add(nova_fumaca)



        for f in fumaca:
            f.update()
            if f.rect.right < 0:
                f.kill()
        
        
        if random.randrange(100)< 2:
            obstaculo = Obstaculos(assets,pontos)
            all_sprites.add(obstaculo)
            obstaculos.add(obstaculo)

            if len(obstaculos) > 1 and (pygame.sprite.collide_rect(obstaculo, obstaculos.sprites()[-2]) or distancia(obstaculo, obstaculos.sprites()[-2]) < 200):
                obstaculo.kill()

        mais_coins(all_sprites, coins, assets)
        pontos = atualiza_coins(player, coins, assets, pontos)
        mais_poder(all_sprites, powerups, pontos, powerup_timer, powerup_intervalo)
        atualiza_poder(player, powerups, all_sprites, obstaculos, powerup_timer)
        all_sprites.update()

        for obstaculo in obstaculos: ## gera obstaculos
            obstaculo.update()

            obstaculo_mask = pygame.mask.from_surface(assets['obstaculo_image'])

            if pygame.sprite.spritecollide(player,obstaculos,False,pygame.sprite.collide_mask): ## forma de perder
                pontuacao_alcançada = pontos
                game = False 

            if obstaculo.rect.right < 0:
                obstaculo.kill()

        # Atualiza a posição do background
        bg_x -= 3  # Velocidade de rolagem do background
        if bg_x <= -WIDTH:
            bg_x = 0

        # ----- Gera saídas
        window.fill((255, 255, 255))  # Preenche com a cor branca
        window.blit(assets['background'], (bg_x, 0))
        window.blit(assets['background'], (bg_x + WIDTH, 0))
        all_sprites.draw(window)
        show_pontos(window, pontos)

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



