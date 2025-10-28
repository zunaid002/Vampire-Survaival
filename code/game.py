from settings import *
from player import *
class Game:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survavial")
        self.clock = pygame.time.Clock()

        self.all_sprite = pygame.sprite.Group()
        player = Player(self.all_sprite)


    def run(self):
        while True:
            dt = self.clock.tick(100) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            

            self.all_sprite.update(dt)

            self.display_surface.fill((0,0,30))
            self.all_sprite.draw(self.display_surface)
            pygame.display.update()