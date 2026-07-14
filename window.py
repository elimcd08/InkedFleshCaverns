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

        # 1. Create a screen-sized overlay to handle the shadow casting
        self.shadow_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.light_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)

        # 2. 🌟 PRE-BAKE A PURE SHADOW MASK
        # We build a static mask matching your sight dimensions.
        # This mask will be pure black, fading from completely opaque at the outer edge
        # to completely transparent in the middle.
        vision_diameter = constants.SIGHT_RADIUS * 2
        self.vision_vignette = pygame.Surface(
            (vision_diameter, vision_diameter), pygame.SRCALPHA
        )

        # Draw soft, layered shadow rings from the outside moving in
        for r in range(constants.SIGHT_RADIUS, 0, -1):
            ratio = r / constants.SIGHT_RADIUS
            # Opaque black (240-255) at the far edges, completely transparent (0) in the dead center
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
        # Step A: Draw the full, uninhibited textured game world
        self.screen.fill((0, 0, 0))
        self.cave_map.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        # Step B: 🌫️ SUBTRACTIVE SCREEN-SPACE SHADOWS
        # 1. Reset our shadow overlay to your solid dark paper shadow tone (alpha 245)
        self.shadow_surface.fill((0, 0, 0, 245))

        # 2. Reset our light overlay to complete transparency (alpha 0)
        self.light_surface.fill((0, 0, 0, 0))

        # 3. Get player coordinates relative to the screen window viewport
        player_screen_x = int(self.player.x - self.camera.x)
        player_screen_y = int(self.player.y - self.camera.y)

        # 4. Draw the light source directly onto our screen-sized light surface.
        # We draw solid white circles with decreasing alpha from the center outward.
        for r in range(constants.SIGHT_RADIUS, 0, -2):
            ratio = r / constants.SIGHT_RADIUS
            # Invert the ratio so it's strongest (245) in the center, and weakest (0) at the edge
            subtract_alpha = int((1.0 - (ratio ** 2)) * 245)

            # We draw white circles. The white color doesn't matter; only the alpha channel does!
            pygame.draw.circle(
                self.light_surface,
                (255, 255, 255, subtract_alpha),
                (player_screen_x, player_screen_y),
                r
            )

        # 5. Subtract the light surface's alpha from our solid dark shadow surface.
        # BLEND_RGBA_SUB physically subtracts the alpha channels, leaving a perfect,
        # seamless circular hole with zero square boundaries!
        self.shadow_surface.blit(
            self.light_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB
        )

        # 6. Layer the completed screen-space shadow layer right over the view
        self.screen.blit(self.shadow_surface, (0, 0))

        pygame.display.flip()