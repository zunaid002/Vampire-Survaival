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

        # Groups
        self.all_sprite = AllSprites()
        self.collision_sprite = pygame.sprite.Group()

        self.setup()

        #spritess
        self.player = Player(self.all_sprite, self.collision_sprite, (0, 0))

    def setup(self):
        map = load_pygame(join('data','maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite(self.all_sprite, (x * TILE_SIZE,y * TILE_SIZE), image)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((self.all_sprite, self.collision_sprite), (obj.x, obj.y), obj.image)

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite(self.collision_sprite, (obj.x, obj.y), pygame.Surface((obj.width, obj.height)))

    def run(self):
        while True:
            # Delta time
            dt = self.clock.tick(100) / 1000
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Update
            self.all_sprite.update(dt)

            # Draw
            self.display_surface.fill((0,0,30))
            self.all_sprite.draw()
            pygame.display.update()