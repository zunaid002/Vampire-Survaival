from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.collision_sprite = collision_sprites

    def input(self):
        key_pressed = pygame.key.get_pressed()

        self.direction.x = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        self.direction.y = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]

        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        self.rect.left += self.direction.x * self.speed * dt
        self.collision('Horizontal')
        self.rect.top += self.direction.y * self.speed * dt
        self.collision('Vertical')

    def collision(self, direction):
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.rect):
                if direction == 'Horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left  
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top  


    def update(self, dt):
        self.input()
        self.move(dt)
