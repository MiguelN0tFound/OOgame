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

def iniciarlvl1(parede):
    Parede(parede, parede_lvl1_img)

def update():
    player.checar_colisao(parede)

def desenhar_tela():
    tela.blit(chao_surf, chao_rect)
    parede.draw(tela)
    for construcao in construcoes:
        construcao.desenhar(tela)
    all_sprites.draw(tela)
    inimigos.draw(tela)

def desenhar_explosao():
    desenhar_tela()
    tela.blit(explosao, explosao.get_rect(center=player.rect.center))
    

def checar_morte():
    for inimigo in inimigos:
        if player.hitbox.colliderect(inimigo.rect):
            return True
    return False

def resetar_player():
    spawn_x, spawn_y = base.get_spawn_pos()
    player.pos = pygame.math.Vector2(spawn_x, spawn_y)
    player.rect.center = (spawn_x, spawn_y)
    player.update_hitbox()

def checar_vitoria():
    if player.hitbox.colliderect(nave.rect):
        print("Vitória! Você chegou na nave!")
        return True
    return False

#displaysetup
pygame.init() 
WW, WH = 800, 600
tela = pygame.display.set_mode((WW, WH))

#imports
parede_lvl1_img = transformar(pygame.image.load(join('images', 'lvl1', 'parede.png'))).convert_alpha()
chao_surf = transformar(pygame.image.load(join('images', 'chao.png'))).convert_alpha()
explosao = transformar(pygame.image.load(join('images', 'explosao.png'))).convert_alpha()

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
running = True
menu = Menu()
parede_criada = False
vitoria = False
morto = False
musica_fase = False
explosao_som =pygame.mixer.Sound(join('sounds', 'explosao.wav')) 



while running:
    dt = clock.tick(60) / 1000
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False

    # MENU
    if hasattr(menu, "visivel") and menu.visivel:
        tela.fill('#124e89')
        if desenhar_menu(eventos):
            running = False
        menu.update(dt)
        pygame.display.flip()
        continue

    # BLOCO DE MORTE
    if morto:
        desenhar_explosao()
        if pygame.time.get_ticks() - tempo_morte > 1000:
            resetar_player()
            morto = False
            print("Level resetado!")
        pygame.display.flip()
        continue

    # ATUALIZAÇÃO NORMAL
    if not parede_criada:
        iniciarlvl1(parede)
        parede_criada = True

    if not musica_fase:
        pygame.mixer.music.load(join('sounds', 'fase.mp3'))
        pygame.mixer.music.play(-1)
        musica_fase = True
    
    player.update(dt, parede)
    inimigos.update(dt, parede)

    # CHECA MORTE
    if checar_morte():
        explosao_som.play()
        morto = True
        pygame.mixer.music.stop()
        musica_fase= False
        tempo_morte = pygame.time.get_ticks()
        
        print("Você morreu!")
        continue

    # DESENHO NORMAL
    desenhar_tela()

    # CHECA VITÓRIA
    if checar_vitoria():
        vitoria = True

    if desenhar_menu(eventos):
        running = False

    menu.update(dt)
    pygame.display.flip()

pygame.quit()