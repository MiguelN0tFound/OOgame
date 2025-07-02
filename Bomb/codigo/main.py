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
from coletavel import Coletavel
from projetil import Projetil

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

    # Limpa e recria coletáveis
    coletaveis.empty()
    Coletavel(coletaveis, 494, 276, join('images', 'projetil.png'))

    # Limpa e recria inimigos
    inimigos.empty()
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
vitoria_surf  = pygame.transform.scale_by(pygame.image.load(join('images', 'vitoria.png')), 5).convert_alpha()
chao_rect = chao_surf.get_frect(center = (WW/2,WH/2))

#sprites
all_sprites = pygame.sprite.Group()
construcoes = pygame.sprite.Group()
coletaveis = pygame.sprite.Group()
projeteis = pygame.sprite.Group()

Coletavel(coletaveis, 494, 276, join('images', 'projetil.png'))
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
pode_atirar = False
explosao_som =pygame.mixer.Sound(join('sounds', 'explosao.wav')) 
ultima_direcao = pygame.Vector2(1, 0)  # Começa para a direita
vitoria_sound= False


while running:
    dt = clock.tick(60) / 1000
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False

    # MENU
    if menu.visivel:
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
    for coletavel in coletaveis:
        coletavel.desenhar(tela)
    
    projeteis.update(dt)
    projeteis.draw(tela)
    coletados = pygame.sprite.spritecollide(player, coletaveis, dokill=True)



    #coletar e atirar
    for coletavel in coletados:
        coletavel.coletado(player)
        pode_atirar = True
    keys = pygame.key.get_pressed()
    if pode_atirar and keys[pygame.K_SPACE]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ultima_direcao = pygame.Vector2(1, 0)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ultima_direcao = pygame.Vector2(-1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            ultima_direcao = pygame.Vector2(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ultima_direcao = pygame.Vector2(0, 1)
        Projetil(projeteis, player.rect.centerx, player.rect.centery, ultima_direcao, join('images', 'projetil.png'))
        pode_atirar = False 
    
    #colisao do tiro com inimigos
    for projetil in projeteis:
        inimigos_atingidos = pygame.sprite.spritecollide(projetil, inimigos, dokill=True)
        if inimigos_atingidos:
            projetil.kill()
            explosao_som.play()


    
    # CHECA VITÓRIA
    if player.hitbox.colliderect(nave.rect):
        print("Vitória! Você chegou na nave!")
        pygame.mixer.music.stop()
        tela.blit(vitoria_surf, vitoria_surf.get_rect(center = (WW/2, WH/2)))
        musica_fase= False
        vitoria = True
        
        
        
    if vitoria and not vitoria_sound:
        
        explosao_som.play()
        vitoria_sound = True

    if desenhar_menu(eventos):
        running = False

    
    menu.update(dt)
    pygame.display.flip()

pygame.quit()