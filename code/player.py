from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def input(self):
        key_pressed = pygame.key.get_pressed()

        self.direction.x = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        self.direction.y = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]

        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)
