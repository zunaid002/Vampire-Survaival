from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # Set Up
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survavial")
        self.clock = pygame.time.Clock()
        self.load_images()

        # Groups
        self.all_sprite = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.bullet_sprite = pygame.sprite.Group()

        self.setup()

        # Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 1

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

    def gun_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() > self.shoot_time + self.gun_cooldown:
                self.can_shoot = True

    def input(self):
        self.gun_timer()
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet((self.all_sprite, self.bullet_sprite), self.bullet_surf, pos, self.gun.player_direction)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()


    def setup(self):
        map = load_pygame(join('data','maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite(self.all_sprite, (x * TILE_SIZE,y * TILE_SIZE), image)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((self.all_sprite, self.collision_sprite), (obj.x, obj.y), obj.image)

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite(self.collision_sprite, (obj.x, obj.y), pygame.Surface((obj.width, obj.height)))
        
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == 'Player':
                self.player = Player(self.all_sprite, self.collision_sprite, (obj.x, obj.y))
                self.gun = Gun(self.all_sprite, self.player)

    def run(self):
        while True:
            # Delta time
            dt = self.clock.tick(100) / 1000
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Input
            self.input()

            # Update
            self.all_sprite.update(dt)

            # Draw
            self.display_surface.fill((0,0,30))
            self.all_sprite.draw(self.player.rect.center)
            pygame.display.update()