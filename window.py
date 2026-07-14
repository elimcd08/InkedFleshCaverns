# window.py
import sys
import pygame
import constants
from camera import Camera
from player import Player

from map import CaveMap


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

        # Define the absolute massive size of your scroll map
        self.MAP_WIDTH = 2000
        self.MAP_HEIGHT = 2000

        # Instantiate player and global camera system
        self.player = Player(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2)

        # --- FIXED LINE HERE: Added 'self.' prefix ---
        self.camera = Camera(self.MAP_WIDTH, self.MAP_HEIGHT)

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
            # clock.tick returns milliseconds. Divide by 1000.0 to get fractions of a second (Delta Time)
            dt = self.clock.tick(constants.FPS) / 1000.0

            # Cap delta time so if the window freezes or moves, the player doesn't
            # wildly teleport through a wall mask on the next frame update.
            dt = min(dt, 0.1)

            self._handle_events()
            self._update(dt)  # Pass dt here
            self._draw()

        pygame.quit()
        sys.exit()

    def _update(self, dt):
        # Pass delta time directly into the player update system
        self.player.update(self.cave_map, dt)
        self.camera.update(self.player)

    def _draw(self):
        self.screen.fill(constants.COLOR_BACKGROUND)

        # 1. Parchment base layer
        world_scroll_rect = pygame.Rect(0, 0, self.MAP_WIDTH, self.MAP_HEIGHT)
        screen_scroll_rect = self.camera.apply(world_scroll_rect)
        pygame.draw.rect(self.screen, constants.COLOR_PAPYRUS, screen_scroll_rect)

        # 2. Draw custom mask cave channels
        self.cave_map.draw(self.screen, self.camera)

        # 3. Draw Player safely inside the channels
        self.player.draw(self.screen, self.camera)

        pygame.display.flip()