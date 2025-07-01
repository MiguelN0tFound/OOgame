import pygame
from funcoes import transformar
from os.path import join


class InimigoHorizontal(pygame.sprite.Sprite):
    def __init__(self, groups, x, y):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(join('images', 'inimigo.png'))).convert_alpha()
        self.rect = self.image.get_frect(center=(x, y))
        self.direction = pygame.math.Vector2(1, 0)  # Começa indo para a direita
        self.speed = 80

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

    def update(self, dt, paredes):
        now = pygame.time.get_ticks()
        if self.cooldown > 0 and now - self.last_collision_time < self.cooldown:
            return

        move = self.direction * self.speed * dt
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
            # Inverte direção X
            self.direction.x *= -1
            self.last_collision_time = now
            self.cooldown = 1500  # ms
        else:
            self.cooldown = 0