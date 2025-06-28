import pygame
from os.path  import join
from menu import Menu


def desenhar_menu(eventos):
    menu.titulo()
    return menu.botoes(eventos)
    
    # menu.subtitle()
    





#displaysetup + imports
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))
title_font = pygame.font.Font(None,font_size)
subtitle_font = pygame.font.Font(None, font_size - 10)


running =True
menu = Menu([])


while running:
    dt = pygame.time.Clock().tick() / 1000
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False
    


    tela.fill(('purple'))  # Fill the screen with black
    if desenhar_menu(eventos):
        running = False
    
    pygame.display.flip()


pygame.quit()