
import pygame
from inimigos.inimigo import Inimigo
from os.path import join

class InimigoHorizontal(Inimigo):
    def __init__(self, groups, x, y):
        super().__init__(groups, x, y, join('images', 'inimigo2.png'), speed=100)
        self.direction = pygame.math.Vector2(1, 0)  # Começa indo para a direita

    def update(self, dt, paredes):
        move = self.direction * self.speed * dt
        self.move_and_collide(move, paredes, invert_axis='x', cooldown_ms=1500)
