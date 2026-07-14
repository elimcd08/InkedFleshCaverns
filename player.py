# player.py
import pygame
import constants


class Player:

    def __init__(self, start_x, start_y):
        self.x = float(start_x)
        self.y = float(start_y)
        self.radius = 10

    def update(self, cave_map, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0


        move_distance = constants.PLAYER_SPEED * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= move_distance
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += move_distance
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= move_distance
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += move_distance


        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071


        if cave_map.is_walkable(self.x + dx, self.y):
            self.x += dx
        elif dx != 0:
            nudge_amount = max(1.0, 120.0 * dt)
            for nudge in [-nudge_amount, nudge_amount]:
                if cave_map.is_walkable(self.x + dx, self.y + nudge):
                    self.y += nudge
                    self.x += dx
                    break


        if cave_map.is_walkable(self.x, self.y + dy):
            self.y += dy
        elif dy != 0:
            nudge_amount = max(1.0, 120.0 * dt)
            for nudge in [-nudge_amount, nudge_amount]:
                if cave_map.is_walkable(self.x + nudge, self.y + dy):
                    self.x += nudge
                    self.y += dy
                    break

    def draw(self, surface, camera):
        screen_pos = camera.apply((self.x, self.y))
        if constants.SPRITE_PLAYER:
            sprite_rect = constants.SPRITE_PLAYER.get_rect(center=screen_pos)
            surface.blit(constants.SPRITE_PLAYER, sprite_rect)
        else:
            pygame.draw.circle(
                surface, constants.COLOR_PLAYER, screen_pos, self.radius
            )