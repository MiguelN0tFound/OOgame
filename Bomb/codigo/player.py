import pygame
from funcoes import transformar
from os.path  import join


#setup + imports
escala = 3
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
        self.speed = 130
        

        # Posição real (float)
        self.pos = pygame.math.Vector2(self.rect.center)

        # Hitbox: metade de baixo do sprite
        w = self.rect.width * 0.7
        h = self.rect.height * 0.5  # metade da altura
        self.hitbox = pygame.Rect(0, 0, w, h)
        self.update_hitbox()

        self.hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height), fill=True)

        self.pos = pygame.math.Vector2(self.rect.center)


    def update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.top = self.rect.centery

    def update(self, dt, paredes):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    
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
            self.direction.x = self.last_direction.x
            self.direction.y = self.last_direction.y
    
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            move = self.direction * self.speed * dt
    
            # Testa colisão pixel-perfect no eixo X
            old_pos = self.pos.copy()
            self.pos.x += move.x
            self.rect.centerx = self.pos.x
            self.update_hitbox()
            colidiu = False
            for p in paredes:
                offset = (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top)
                if p.mask.overlap(self.hitbox_mask, offset):
                    colidiu = True
                    break
            if colidiu:
                self.pos.x = old_pos.x
                self.rect.centerx = self.pos.x
                self.update_hitbox()
    
            # Testa colisão pixel-perfect no eixo Y
            old_pos = self.pos.copy()
            self.pos.y += move.y
            self.rect.centery = self.pos.y
            self.update_hitbox()
            colidiu = False
            for p in paredes:
                offset = (self.hitbox.left - p.rect.left, self.hitbox.top - p.rect.top)
                if p.mask.overlap(self.hitbox_mask, offset):
                    colidiu = True
                    break
            if colidiu:
                self.pos.y = old_pos.y
                self.rect.centery = self.pos.y
                self.update_hitbox()
        else:
            self.rect.center = self.pos
            self.update_hitbox()


    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.hitbox, 2)

    
