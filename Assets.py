import pygame

def load_assets():
    # Dicionário de assets
    assets = {}

    # Carregar imagens
    assets['player_image'] = pygame.image.load('assets/player.png').convert_alpha()
    assets['player_mask'] = pygame.mask.from_surface(assets['player_image'])
    assets['obstaculo_image'] = pygame.image.load('assets/bala.png').convert_alpha()
    assets['coin_image'] = pygame.image.load('assets/moedas.png').convert_alpha()
    assets['fumaca_image'] = pygame.image.load('assets/fumaca.png').convert_alpha()
    assets['background'] = pygame.image.load('assets/background.png')
    assets['background'] = pygame.transform.scale(assets['background'], (1000, 650))
    assets['background_inicio_final'] = pygame.image.load('assets/background2.png').convert_alpha()
    assets['background_inicio_final'] = pygame.transform.scale(assets['background_inicio_final'], (1000, 650))

    # Carregar músicas e sons
    pygame.mixer.music.load('assets/musica_de_fundo.ogg')
    pygame.mixer.music.set_volume(0.5)
    assets['moedas_sound'] = pygame.mixer.Sound('assets/moedas_sfx.ogg')
    assets['moedas_sound'].set_volume(0.5)
    assets['lapis_sound'] = pygame.mixer.Sound('assets/som_lapis.ogg')
    
    return assets
