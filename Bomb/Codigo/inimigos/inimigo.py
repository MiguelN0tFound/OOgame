import pygame
from funcoes import transformar
from os.path import join

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, imagem_path, speed=100):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(imagem_path)).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.__speed = speed
        self.__pos = pygame.math.Vector2(self.rect.center)

        # Hitbox visível (pública)
        w = self.rect.width * 0.7
        h = self.rect.height * 0.5
        self.hitbox = pygame.Rect(0, 0, w, h)
        self.__update_hitbox()

        self.__hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height), fill=True)

        self.__cooldown = 0  # ms
        self.__last_collision_time = 0

    # ---------- PROPERTIES ----------
    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, valor):
        if valor > 0:
            self.__speed = valor

    @property
    def pos(self):
        return self.__pos

    @property
    def cooldown(self):
        return self.__cooldown

    # ---------- MÉTODOS INTERNOS ----------
    def __update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.top = self.rect.centery

    # ---------- MÉTODOS PÚBLICOS ----------
    def move_and_collide(self, move, paredes, invert_axis='y', cooldown_ms=1000):
        now = pygame.time.get_ticks()
        if self.__cooldown > 0 and now - self.__last_collision_time < self.__cooldown:
            return

        self.__pos += move
        self.rect.center = self.__pos
        self.__update_hitbox()

        # Checa colisão pixel-perfect com paredes
        colidiu = False
        for p in paredes:
            offset = (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top)
            if p.mask.overlap(self.__hitbox_mask, offset):
                colidiu = True
                break

        if colidiu:
            # Volta para posição anterior
            self.__pos -= move
            self.rect.center = self.__pos
            self.__update_hitbox()

            # Inverte direção no eixo especificado
            if hasattr(self, 'direction'):
                if invert_axis == 'y':
                    self.direction.y *= -1
                elif invert_axis == 'x':
                    self.direction.x *= -1

            self.__last_collision_time = now
            self.__cooldown = cooldown_ms
        else:
            self.__cooldown = 0
