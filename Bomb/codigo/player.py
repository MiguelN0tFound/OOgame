import pygame
from funcoes import transformar
from os.path  import join

#setup + imports
escala = 5
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(join('images', 'player.png'))).convert_alpha()
        self.rect = self.image.get_frect(center = (WW/2, WH/2))
        self.direction = pygame.math.Vector2(0,0)
        self.last_direction = pygame.math.Vector2(0,0)
        self.speed = 100

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        # Só aceita movimento em uma direção por vez
        if dx != 0 and dy == 0:
            self.direction.x = dx
            self.direction.y = 0
            self.last_direction.x = dx
            self.last_direction.y = 0
        elif dy != 0 and dx == 0:
            self.direction.x = 0
            self.direction.y = dy
            self.last_direction.x = 0
            self.last_direction.y = dy
        elif dx == 0 and dy == 0:
            self.direction.x = 0
            self.direction.y = 0
        else:
            # Se diagonal, mantém a última direção válida
            self.direction.x = self.last_direction.x
            self.direction.y = self.last_direction.y

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            self.rect.centerx += self.direction.x * self.speed * dt
            self.rect.centery += self.direction.y * self.speed * dt

        self.rect.center += self.direction * self.speed * dt
        pygame.draw.rect(pygame.display.get_surface(), "red", self.rect, 2) 

