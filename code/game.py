from settings import *
from player import Player
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # Set Up
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survavial")
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprite = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.bullet_sprite = pygame.sprite.Group()
        self.enemy_sprite = pygame.sprite.Group()

        # Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.spawn_position = []

        #setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        
        for folder in folders:
            for folder_paths, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join( folder_paths, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
                    
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
            else:
                self.spawn_position.append((obj.x, obj.y))

    def run(self):
        while True:
            # Delta time
            dt = self.clock.tick(100) / 1000
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == self.enemy_event:
                    Enemy((self.all_sprite, self.enemy_sprite), choice(list(self.enemy_frames.values())), self.player, choice(self.spawn_position), self.collision_sprite)
                    
            # Input
            self.input()

            # Update
            self.all_sprite.update(dt)

            # Draw
            self.display_surface.fill((0,0,30))
            self.all_sprite.draw(self.player.rect.center)
            pygame.display.update()