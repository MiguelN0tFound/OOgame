import pygame
from funcoes import transformar
from os.path  import join

#setup + imports
escala = 5
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))

class Parede(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WW/2,WH/2))
        self.mask = pygame.mask.from_surface(self.image)