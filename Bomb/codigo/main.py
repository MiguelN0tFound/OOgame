import pygame
from os.path import join
from menu import Menu
from funcoes import transformar
from player import Player
from parede import Parede
from inimigos.inimigoVertical import InimigoVertical
from inimigos.inimigoHorizontal import InimigoHorizontal
from construcoes.base import Base
from construcoes.nave import Nave


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

def iniciarlvl1(parede):
    Parede(parede, parede_lvl1_img)

def update():
    player.checar_colisao(parede)



#displaysetup
pygame.init() 
WW, WH = 800, 600
tela = pygame.display.set_mode((WW, WH))



#imports
parede_lvl1_img = transformar(pygame.image.load(join('images', 'lvl1', 'parede.png'))).convert_alpha()
chao_surf = transformar(pygame.image.load(join('images', 'chao.png'))).convert_alpha()
chao_rect = chao_surf.get_frect(center = (WW/2,WH/2))


#sprites
all_sprites = pygame.sprite.Group()



construcoes = pygame.sprite.Group()
nave = Nave(construcoes, 567, 180, join('images', 'nave.png'))
base = Base(construcoes, 136, 180, join('images', 'base.png'))
spawn_x, spawn_y = base.get_spawn_pos()
player = Player(all_sprites, spawn_x, spawn_y)


parede = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
posicoes = [
    (257, 87),
    (303, 489),
    (400, 489),
    (450, 87),
    (640, 87),
    (685, 87)
]

for x, y in posicoes:
    InimigoVertical(inimigos, x, y)

InimigoHorizontal(inimigos, 252, 250)



#variaveis
clock = pygame.time.Clock()
running =True
menu = Menu()
fade_out_aplicado = False
parede_criada = False
vitoria = False




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
        tela.fill('#124e89')  # Fill the screen with black
    else:
        if not parede_criada:
            iniciarlvl1(parede)
            parede_criada=True
        
        player.update(dt, parede)
        inimigos.update(dt,parede)
        print("Rect center do player:", player.rect.midbottom)
        
        tela.fill('#124e89')
        tela.blit(chao_surf, chao_rect)
        parede.draw(tela)
        for construcao in construcoes:
            construcao.desenhar(tela)
        all_sprites.draw(tela)
        player.draw_hitbox(tela) 
        inimigos.draw(tela)

        if player.hitbox.colliderect(nave.rect):
            vitoria = True
            print("Vitória! Você chegou na nave!")


        
            
                    
        
    if desenhar_menu(eventos):
        running = False
    
    menu.update(dt)

    pygame.display.flip()


pygame.quit()