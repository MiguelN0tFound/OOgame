import pygame
from funcoes import transformar
from os.path import join

escala = 3
pygame.init()
WW, WH = 800, 600
font_size = 36
tela = pygame.display.set_mode((WW, WH))


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, x, y):
        super().__init__(groups)
        self.image = transformar(pygame.image.load(join('images', 'player.png'))).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Encapsulados
        self.__speed = 130
        self.__direction = pygame.math.Vector2(0, 0)
        self.__last_direction = pygame.math.Vector2(0, 0)
        self.__pos = pygame.math.Vector2(self.rect.center)

        # hitbox pública
        w = self.rect.width * 0.7
        h = self.rect.height * 0.5
        self.hitbox = pygame.Rect(0, 0, w, h)
        self.__hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height), fill=True)

        self.update_hitbox()

    # ----------- PROPERTIES ------------
    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, valor):
        if valor > 0:
            self.__speed = valor

    @property
    def direction(self):
        return self.__direction

    @property
    def pos(self):
        return self.__pos
    
    @pos.setter
    def pos(self, valor):
        if isinstance(valor, pygame.math.Vector2):
            self.__pos = valor



    # ----------- MÉTODOS INTERNOS ------------
    def update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.top = self.rect.centery

    # ----------- MÉTODOS PÚBLICOS ------------
    def update(self, dt, paredes):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        if dx != 0 and dy == 0:
            self.__direction.x = dx
            self.__direction.y = 0
            self.__last_direction.x = dx
            self.__last_direction.y = 0
        elif dy != 0 and dx == 0:
            self.__direction.x = 0
            self.__direction.y = dy
            self.__last_direction.x = 0
            self.__last_direction.y = dy
        elif dx == 0 and dy == 0:
            self.__direction.x = 0
            self.__direction.y = 0
        else:
            self.__direction.x = self.__last_direction.x
            self.__direction.y = self.__last_direction.y

        if self.__direction.length_squared() > 0:
            move = self.__direction * self.__speed * dt

            # Eixo X
            old_pos = self.__pos.copy()
            self.__pos.x += move.x
            self.rect.centerx = self.__pos.x
            self.update_hitbox()
            colidiu = any(
                p.mask.overlap(self.__hitbox_mask, (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top))
                for p in paredes
            )
            if colidiu:
                self.__pos.x = old_pos.x
                self.rect.centerx = self.__pos.x
                self.update_hitbox()

            # Eixo Y
            old_pos = self.__pos.copy()
            self.__pos.y += move.y
            self.rect.centery = self.__pos.y
            self.update_hitbox()
            colidiu = any(
                p.mask.overlap(self.__hitbox_mask, (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top))
                for p in paredes
            )
            if colidiu:
                self.__pos.y = old_pos.y
                self.rect.centery = self.__pos.y
                self.update_hitbox()

        else:
            self.rect.center = self.__pos
            self.update_hitbox()

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)
