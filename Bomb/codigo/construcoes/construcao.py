import pygame
from os.path import join
from funcoes import transformar

class Construcao(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, imagem_path):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(imagem_path)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))

    def desenhar(self, surface):
        surface.blit(self.image, self.rect)