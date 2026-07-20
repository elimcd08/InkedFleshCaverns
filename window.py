import sys
import pygame
import constants
from camera import Camera
from player import Player

from map import CaveMap
from ui import JournalUI


class GameWindow:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Inked Flesh Caverns")
        self.clock = pygame.time.Clock()

        constants.load_game_assets()

        self.MAP_WIDTH = 2000
        self.MAP_HEIGHT = 2000

        self.player = Player(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2)
        self.game_ui = JournalUI()
        self.camera = Camera(self.MAP_WIDTH, self.MAP_HEIGHT)

        self.shadow_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.light_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)

        vision_diameter = constants.SIGHT_RADIUS * 2
        self.vision_vignette = pygame.Surface(
            (vision_diameter, vision_diameter), pygame.SRCALPHA
        )


        for r in range(constants.SIGHT_RADIUS, 0, -1):
            ratio = r / constants.SIGHT_RADIUS
            shadow_alpha = int((ratio ** 2) * 245)

            pygame.draw.circle(
                self.vision_vignette,
                (0, 0, 0, shadow_alpha),
                (constants.SIGHT_RADIUS, constants.SIGHT_RADIUS),
                r
            )

        self.cave_map = CaveMap(self.MAP_WIDTH, self.MAP_HEIGHT)
        self.running = True

        pygame.mixer.music.load(constants.CAVE_AMBIENCE)
        pygame.mixer.music.set_volume(0.125)
        pygame.mixer.music.play(-1)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(constants.FPS) / 1000.0


            dt = min(dt, 0.1)

            self._handle_events()
            self._update(dt)
            self._draw()
            print(self.clock.get_fps())

        pygame.quit()
        sys.exit()

    def _update(self, dt):
        self.player.update(self.cave_map, dt)
        self.camera.update(self.player)

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.cave_map.draw(self.screen, self.camera)
        self.game_ui.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)


        self.shadow_surface.fill((0, 0, 0, 245))


        self.light_surface.fill((0, 0, 0, 0))


        player_screen_x = int(self.player.x - self.camera.x)
        player_screen_y = int(self.player.y - self.camera.y)


        for r in range(constants.SIGHT_RADIUS, 0, -2):
            ratio = r / constants.SIGHT_RADIUS
            subtract_alpha = int((1.0 - (ratio ** 2)) * 245)


            pygame.draw.circle(
                self.light_surface,
                (255, 255, 255, subtract_alpha),
                (player_screen_x, player_screen_y),
                r
            )


        self.shadow_surface.blit(
            self.light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB
        )


        self.screen.blit(self.shadow_surface, (0, 0))

        pygame.display.flip()