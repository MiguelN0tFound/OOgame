import pygame
from funcoes import transformar
from os.path  import join

#setup + imports
escala = 5
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))

class Menu():
    def __init__(self):
        super().__init__()
        botao =load_buttons()
        self.title_surf = transformar(pygame.image.load(botao['titulo']).convert_alpha())
        self.title_rect = self.title_surf.get_frect(center=(WW/2, WH/3-50))


        self.jogar_surf_lit = transformar(pygame.image.load(botao['jogar1']).convert_alpha())
        self.jogar_surf_unlit = transformar(pygame.image.load(botao['jogar2']).convert_alpha())
        self.jogar_rect = self.jogar_surf_unlit.get_frect(center=(WW/2, WH/2+60))
        
        
        self.tutorial_surf_lit = transformar(pygame.image.load(botao['tutorial1']).convert_alpha())
        self.tutorial_surf_unlit = transformar(pygame.image.load(botao['tutorial2']).convert_alpha())
        self.tutorial_rect = self.tutorial_surf_unlit.get_frect(center=(WW/2, WH/2+125))
        

        self.sair_surf_lit = transformar(pygame.image.load(botao['sair1']).convert_alpha())
        self.sair_surf_unlit = transformar(pygame.image.load(botao['sair2']).convert_alpha())
        self.sair_rect = self.sair_surf_unlit.get_frect(center=(WW/2, WH/2+190))

        self.visivel = True
        self.animando = False
        self.title_anim_y = self.title_rect.y
        self.jogar_anim_y = self.jogar_rect.y
        self.tutorial_anim_y = self.tutorial_rect.y
        self.sair_anim_y = self.sair_rect.y
        self.menu_vel = 0
        self.menu_acc = -500

        
    
    def botoes(self, eventos):
        
        if not self.visivel:
            return False
        
        tela.blit(self.title_surf, self.title_rect)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        sair_clicado = False
        jogar_clicado = False
        # Jogar
        if self.jogar_rect.collidepoint(mouse_pos):
            tela.blit(self.jogar_surf_lit, self.jogar_rect)
            if mouse_click:
                tela.blit(self.jogar_surf_unlit, self.jogar_rect)
        else:
            tela.blit(self.jogar_surf_unlit, self.jogar_rect)
        
        # Tutorial
        if self.tutorial_rect.collidepoint(mouse_pos):
            tela.blit(self.tutorial_surf_lit, self.tutorial_rect)
            if mouse_click:
                tela.blit(self.tutorial_surf_unlit, self.tutorial_rect)
        else:
            tela.blit(self.tutorial_surf_unlit, self.tutorial_rect)
        
        # Sair
        if self.sair_rect.collidepoint(mouse_pos):
            tela.blit(self.sair_surf_lit, self.sair_rect)
            if mouse_click:
                tela.blit(self.sair_surf_unlit, self.sair_rect)
        else:
            tela.blit(self.sair_surf_unlit, self.sair_rect)
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.sair_rect.collidepoint(event.pos):
                    sair_clicado = True
                if self.jogar_rect.collidepoint(event.pos):
                    self.animando = True
        return sair_clicado

    def update(self, dt):
        if self.animando:
            self.menu_vel += self.menu_acc * dt  # pixels por segundo
            self.title_rect.y += self.menu_vel * dt
            self.jogar_rect.y += self.menu_vel * dt
            self.tutorial_rect.y += self.menu_vel * dt
            self.sair_rect.y += self.menu_vel * dt
            if self.sair_rect.y + self.sair_rect.height < 0:
                self.animando = False
                self.visivel = False


        

def load_buttons():
    return{
        'titulo' : join("images", 'menu', "titulo.png"),
        'jogar1' : join("images", 'menu', "menu-buttons-lit", "jogar.png"),
        'tutorial1' : join("images", 'menu', "menu-buttons-lit", "tutorial.png"),
        'sair1' : join("images", 'menu', "menu-buttons-lit", "sair.png"),
        'jogar2' : join("images", 'menu', "menu-buttons-unlit", "jogar.png"),
        'tutorial2' : join("images", 'menu', "menu-buttons-unlit", "tutorial.png"),
        'sair2' : join("images", 'menu', "menu-buttons-unlit", "sair.png"),
    }
    

    