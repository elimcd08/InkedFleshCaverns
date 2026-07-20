# player.py
import math

import pygame
import constants


class Player:

    def __init__(self, start_x, start_y):
        self.x = float(start_x)
        self.y = float(start_y)
        self.radius = 10
        self.facing_right = True
        self.facing_up = True
        self.facing_angle = 0.0
        self.width = 32
        self.height = 32
        self.hitbox_size = 16
        self.img = pygame.transform.scale(constants.SPRITE_PLAYER, (self.width, self.height))

    def get_collision_rect(self, x, y):
        rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        rect.center = (int(x), int(y))
        return rect

    def _is_position_walkable(self, check_x, check_y, cave_map):
        """Internal check to test the 4 corners of the shrunken hit-box."""
        rect = self.get_collision_rect(check_x, check_y)
        corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
        return all(cave_map.is_walkable(cx, cy) for cx, cy in corners)

    def _check_footprint(self, center_x, center_y, cave_map):
        """Helper to check if a 32x32 footprint centered at (center_x, center_y) is clear."""
        hx = self.width // 2
        hy = self.height // 2

        # Calculate the 4 exact outer corner pixels for this hypothetical position
        corners = [
            (center_x - hx, center_y - hy),  # Top-Left
            (center_x + hx, center_y - hy),  # Top-Right
            (center_x - hx, center_y + hy),  # Bottom-Left
            (center_x + hx, center_y + hy),  # Bottom-Right
        ]

        # Returns True only if every single corner pixel evaluates as walkable ground
        return all(cave_map.is_walkable(cx, cy) for cx, cy in corners)

    def update(self, cave_map, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # 1. Gather RAW direction inputs (-1, 0, or 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Track old legacy facing booleans if needed elsewhere
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
        if dy > 0:
            self.facing_up = True
        elif dy < 0:
            self.facing_up = False

        # 2. Process orientation and vector normalization BEFORE applying speed
        if dx != 0 or dy != 0:
            # Calculate angle based on raw direction vectors
            radians = math.atan2(-dy, dx)
            self.facing_angle = math.degrees(radians)

            # Properly normalize the diagonal vector to a maximum length of 1.0
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

            # 3. Apply your time-scaled movement distance directly to the normalized vector
            move_distance = constants.PLAYER_SPEED * dt
            dx *= move_distance
            dy *= move_distance

        # 4. Process sliding collisions on the map grid using the final scaled distance
            # --- HORIZONTAL AXIS (X) ---
            if dx != 0:
                next_x = self.x + dx
                if self._is_position_walkable(next_x, self.y, cave_map):
                    self.x += dx
                else:
                    nudge_amount = max(1.0, 120.0 * dt)
                    for nudge in [-nudge_amount, nudge_amount]:
                        if self._is_position_walkable(next_x, self.y + nudge, cave_map):
                            self.y += nudge
                            self.x += dx
                            break

            # --- VERTICAL AXIS (Y) ---
            if dy != 0:
                next_y = self.y + dy
                if self._is_position_walkable(self.x, next_y, cave_map):
                    self.y += dy
                else:
                    nudge_amount = max(1.0, 120.0 * dt)
                    for nudge in [-nudge_amount, nudge_amount]:
                        if self._is_position_walkable(self.x + nudge, next_y, cave_map):
                            self.x += nudge
                            self.y += dy
                            break

    def draw(self, surface, camera):
        screen_pos = camera.apply((self.x, self.y))

        blit_img = pygame.transform.rotate(self.img, self.facing_angle)

        sprite_rect = blit_img.get_rect(center=screen_pos)
        surface.blit(blit_img, sprite_rect)