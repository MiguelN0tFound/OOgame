import pygame
from funcoes import transformar

class Projetil(pygame.sprite.Sprite):
    def __init__(self, grupo, x, y, direcao, imagem_path):
        super().__init__(grupo)
        self.image = transformar(pygame.image.load(imagem_path)).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 500
        self.direcao = direcao  # pygame.Vector2

    def update(self, dt):
        movimento = self.direcao * self.velocidade * dt
        self.rect.x += movimento.x
        self.rect.y += movimento.y
        # Remove se sair da tela
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()