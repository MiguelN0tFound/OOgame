
import pygame
from os.path import join
from construcoes.construcao import Construcao


class Nave(Construcao):
    def __init__(self, groups, x, y, imagem_path):
        super().__init__(groups, x, y, imagem_path)
    
    def get_spawn_pos(self):
        spawn_x = self.rect.centerx
        spawn_y = self.rect.bottom + 10  # 10 pixels abaixo da base
        return (spawn_x, spawn_y)
