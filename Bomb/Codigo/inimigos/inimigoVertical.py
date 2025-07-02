
import pygame
from inimigos.inimigo import Inimigo
from os.path import join

class InimigoVertical(Inimigo):
    def __init__(self, groups, x, y):
        super().__init__(groups, x, y, join('images', 'inimigo.png'), speed=100)
        self.direction = pygame.math.Vector2(0, 1)  # Começa indo para baixo

    def update(self, dt, paredes):
        move = self.direction * self.speed * dt
        self.move_and_collide(move, paredes, invert_axis='y', cooldown_ms=1000)
