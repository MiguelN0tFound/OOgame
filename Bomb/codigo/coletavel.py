import pygame
from funcoes import transformar

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, grupo, x, y, imagem_path):
        super().__init__(grupo)
        self.image = transformar(pygame.image.load(imagem_path)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))

    def coletado(self, player):
        # Ação ao coletar (pode ser sobrescrita)
        print("Coletável coletado!")

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)