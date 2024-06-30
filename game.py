import pygame
import sys
import random
import math

from scripts.utils import Animation, load_image, load_images
from scripts.entities import Player
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particle import Particle


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Ninja Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("entities/player/idle"), img_dur=6),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/run": Animation(load_images("entities/player/run"), img_dur=4),
            "player/slide": Animation(load_images("entities/player/slide")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
            "particles/leaf": Animation(
                load_images("particles/leaf"), img_dur=20, loop=False
            ),
            "particles/particle": Animation(
                load_images("particles/particle"), img_dur=6, loop=False
            ),
        }
        self.clouds = Clouds(self.assets["clouds"], count=16)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = TileMap(self, tile_size=16)
        self.tilemap.load("map.json")
        self.scroll = [0, 0]
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(tree["pos"][0] + 4, tree["pos"][1] + 4, 23, 13)
            )
        self.particles = []

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            # centering the map onto the character, the formulas below will remain in equilibrium
            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # particles
            for rect in self.leaf_spawners:
                if 30000 * random.random() < rect.width * rect.height:
                    pos = (
                        rect.x + rect.width * random.random(),
                        rect.y + rect.height * random.random(),
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            velocity=[0.1, 0.3],
                            frame=random.randint(0, 20),
                        )
                    )

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.p_type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
                        # self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)  # sleep for a length that will result in 60fps


Game().run()
