from settings import *
from player import Player
class Game:
    def __init__(self):
        # Set Up
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survavial")
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprite = pygame.sprite.Group()

        #spritess
        self.player = Player(self.all_sprite, (400, 400))

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
            self.all_sprite.draw(self.display_surface)
            pygame.display.update()