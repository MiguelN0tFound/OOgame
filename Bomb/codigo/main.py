import pygame
from os.path  import join
from menu import Menu
from player import Player


def desenhar_menu(eventos):
    return menu.botoes(eventos)
    

def fade_out(tela,clock, cor=(0,0,0), velocidade=2):
    fade = pygame.Surface((WW, WH))
    fade.fill(cor)
    # Fade out para preto
    for alpha in range(0, 255, velocidade):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        fade.set_alpha(alpha)
        tela.blit(fade, (0,0))
        pygame.display.update()
        clock.tick(60)
    # Fade in para roxo


#displaysetup + imports
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))
title_font = pygame.font.Font(None,font_size)
subtitle_font = pygame.font.Font(None, font_size - 10)

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
player = Player(all_sprites)
running =True
menu = Menu()
fade_out_aplicado = False


while running:
    dt = clock.tick(60) / 1000
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False
    

    

    
    if hasattr(menu,"visivel") and not menu.visivel and not fade_out_aplicado:
        fade_out(tela, clock)
        fade_out_aplicado = True
    
    if not fade_out_aplicado:
        tela.fill('purple')  # Fill the screen with black
    else:
        all_sprites.draw(tela)
        all_sprites.update(dt)

    if desenhar_menu(eventos):
        running = False
    
    menu.update(dt)
    

    
        

    pygame.display.flip()


pygame.quit()