import pygame
from funcoes import transformar
from os.path import join

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, imagem_path, speed=100):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(imagem_path)).convert_alpha()
        self.rect = self.image.get_frect(center=(x, y))
        self.speed = speed

        # Posição real (float)
        self.pos = pygame.math.Vector2(self.rect.center)

        # Hitbox: metade de baixo do sprite (igual ao player)
        w = self.rect.width * 0.7
        h = self.rect.height * 0.5
        self.hitbox = pygame.Rect(0, 0, w, h)
        self.update_hitbox()

        self.hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height), fill=True)

        self.cooldown = 0  # ms
        self.last_collision_time = 0

    def update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.top = self.rect.centery

    def move_and_collide(self, move, paredes, invert_axis='y', cooldown_ms=1000):
        now = pygame.time.get_ticks()
        if self.cooldown > 0 and now - self.last_collision_time < self.cooldown:
            return

        self.pos += move
        self.rect.center = self.pos
        self.update_hitbox()

        # Checa colisão pixel-perfect com paredes
        colidiu = False
        for p in paredes:
            offset = (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top)
            if p.mask.overlap(self.hitbox_mask, offset):
                colidiu = True
                break

        if colidiu:
            # Volta para posição anterior
            self.pos -= move
            self.rect.center = self.pos
            self.update_hitbox()
            # Inverte direção no eixo especificado
            if invert_axis == 'y':
                self.direction.y *= -1
            elif invert_axis == 'x':
                self.direction.x *= -1
            self.last_collision_time = now
            self.cooldown = cooldown_ms
        else:
            self.cooldown = 0