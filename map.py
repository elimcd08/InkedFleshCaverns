# map.py
import math
import random
import pygame
import constants


class CaveMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        map_size = (self.width, self.height)

        # --- Procedural Tuning Panel ---
        self.TUNNEL_MIN_RADIUS = 15.0
        self.TUNNEL_MAX_RADIUS = 28.0
        self.TUNNEL_SWELL_SPEED = 0.1

        self.CAVERN_MIN_SIZE = 65.0
        self.CAVERN_MAX_SIZE = 105.0

        self.HUB_MIN_SIZE = 85.0
        self.HUB_MAX_SIZE = 120.0

        self.WALKER_STEPS = 800
        self.NUM_WALKERS = 5

        # 1. Load raw textures and dynamically scale them to your gameplay area size
        try:
            raw_bg = pygame.image.load(constants.TEXTURE_WALLS).convert()
            raw_path = pygame.image.load(constants.TEXTURE_PATHS).convert()

            bg_texture = pygame.transform.scale(raw_bg, map_size)
            path_texture = pygame.transform.scale(raw_path, map_size)
        except pygame.error as e:
            print(
                f"Asset Load Error: Make sure {constants.TEXTURE_WALLS} and {constants.TEXTURE_PATHS} are in your project folder!"
            )
            raise e

        # 2. Create the blank generation canvas (White paths, Black walls)
        self.cave_surface = pygame.Surface(map_size)
        self.cave_surface.fill((0, 0, 0))

        # 3. Run the generator to trace out the layout paths
        self._generate_caves()

        # 4. Compile the mask for player collision tracking
        ink_white = (255, 255, 255)
        self.mask = pygame.mask.from_threshold(
            self.cave_surface, ink_white, (1, 1, 1, 255)
        )

        # 5. 🛠️ THE TEXTURE MASKING SETUP
        # Start our final world canvas with the dark background/wall texture
        self.baked_surface = bg_texture.copy()

        # Step A: Make a copy of the path texture that we will cut out
        isolated_paths = path_texture.copy()

        # Step B: Prepare the stencil layer.
        # Mark WHITE as the transparent colorkey on our wireframe map.
        stencil_layer = self.cave_surface.copy()
        stencil_layer.set_colorkey((255, 255, 255))

        # Step C: Blit the stencil onto the path texture using MULTIPLY.
        # This erases the light paper everywhere EXCEPT where the paths are drawn.
        isolated_paths.blit(
            stencil_layer, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )

        # Step D: Mark the leftover black area of the path layer as completely see-through
        isolated_paths.set_colorkey((0, 0, 0))

        # Step E: Drop the cleanly cut out light parchment paths right over the dark wall texture!
        self.baked_surface.blit(isolated_paths, (0, 0))

    def _generate_caves(self):
        """Generates the underlying cave wireframe."""
        ink_white = (255, 255, 255)
        center_x = self.width // 2
        center_y = self.height // 2

        def grow_organic_chamber(surface, cx, cy, base_size):
            pygame.draw.circle(surface, ink_white, (cx, cy), base_size)
            num_bumps = random.randint(4, 7)
            for b in range(num_bumps):
                bump_angle = (b / num_bumps) * (
                    2 * math.pi
                ) + random.uniform(-0.2, 0.2)
                distance = base_size * random.uniform(0.65, 0.85)
                bx = cx + int(math.cos(bump_angle) * distance)
                by = cy + int(math.sin(bump_angle) * distance)

                bump_radius = int(base_size * random.uniform(0.45, 0.7))
                pygame.draw.circle(surface, ink_white, (bx, by), bump_radius)

        for _ in range(4):
            ox = random.randint(-35, 35)
            oy = random.randint(-35, 35)
            hub_size = random.randint(
                int(self.HUB_MIN_SIZE), int(self.HUB_MAX_SIZE)
            )
            grow_organic_chamber(
                self.cave_surface, center_x + ox, center_y + oy, hub_size
            )

        for i in range(self.NUM_WALKERS):
            wx, wy = float(center_x), float(center_y)
            angle = (i / self.NUM_WALKERS) * (2 * math.pi)

            current_state = "tunnel"
            current_radius = (self.TUNNEL_MIN_RADIUS + self.TUNNEL_MAX_RADIUS) / 2
            state_timer = random.randint(60, 120)

            for _ in range(self.WALKER_STEPS):
                state_timer -= 1
                if state_timer <= 0:
                    if current_state == "tunnel":
                        if random.random() < 0.25:
                            current_state = "cavern"
                            state_timer = random.randint(6, 12)
                        else:
                            state_timer = random.randint(50, 100)
                    else:
                        current_state = "tunnel"
                        state_timer = random.randint(70, 140)

                if current_state == "tunnel":
                    target_radius = random.uniform(
                        self.TUNNEL_MIN_RADIUS, self.TUNNEL_MAX_RADIUS
                    )
                    current_radius += (
                        target_radius - current_radius
                    ) * self.TUNNEL_SWELL_SPEED

                    angle += random.uniform(-0.15, 0.15)
                    wx += math.cos(angle) * 4.2
                    wy += math.sin(angle) * 4.2

                    pygame.draw.circle(
                        self.cave_surface,
                        ink_white,
                        (int(wx), int(wy)),
                        int(current_radius),
                    )

                elif current_state == "cavern":
                    angle += random.uniform(-0.12, 0.12)
                    wx += math.cos(angle) * 2.5
                    wy += math.sin(angle) * 2.5

                    room_size = random.randint(
                        int(self.CAVERN_MIN_SIZE), int(self.CAVERN_MAX_SIZE)
                    )
                    grow_organic_chamber(self.cave_surface, int(wx), int(wy), room_size)

                margin = 160
                if (
                    wx < margin
                    or wx > self.width - margin
                    or wy < margin
                    or wy > self.height - margin
                ):
                    target_angle = math.atan2(center_y - wy, center_x - wx)
                    angle += (target_angle - angle) * 0.2

                wx = max(margin, min(wx, self.width - margin))
                wy = max(margin, min(wy, self.height - margin))

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.mask.get_at((int(x), int(y))) == 1
        return False

    def draw(self, surface, camera):
        screen_pos = camera.apply(pygame.Rect(0, 0, self.width, self.height))
        surface.blit(self.baked_surface, screen_pos.topleft)