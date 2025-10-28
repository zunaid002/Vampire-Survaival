from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, dt):
        key_pressed = pygame.key.get_pressed()

        self.direction.x = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        self.direction.y = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]

        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center += self.direction * self.speed * dt
