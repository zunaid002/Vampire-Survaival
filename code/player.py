from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-70, -90)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.collision_sprite = collision_sprites

    def load_images(self):
        self.frames = {'left' : [], 'right' : [], 'up' : [], 'down' : []}

        for state in self.frames.keys():
            for folder_path, sub_folder, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        key_pressed = pygame.key.get_pressed()

        self.direction.x = key_pressed[pygame.K_RIGHT] - key_pressed[pygame.K_LEFT]
        self.direction.y = key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP]

        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.left += self.direction.x * self.speed * dt
        self.collision('Horizontal')
        self.hitbox_rect.top += self.direction.y * self.speed * dt
        self.collision('Vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'Horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left  
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top  

    def animate(self, dt):
        # get state
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'

        # animation
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
