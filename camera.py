# camera.py
import constants


class Camera:

    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        """Centers the camera coordinates smoothly around a target object."""
        # Calculate ideal position to center the player on screen
        self.x = target.x - (constants.SCREEN_WIDTH // 2)
        self.y = target.y - (constants.SCREEN_HEIGHT // 2)

        # Optional: Clamp camera inside the absolute map dimensions
        self.x = max(0, min(self.x, self.width - constants.SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.height - constants.SCREEN_HEIGHT))

    def apply(self, entity_rect_or_pos):
        """Transforms world coordinates into screen drawing coordinates."""
        if hasattr(entity_rect_or_pos, "topleft"):
            # If a pygame.Rect is passed in, shift it
            return entity_rect_or_pos.move(-self.x, -self.y)
        else:
            # If a tuple/list (x, y) is passed in, shift it
            return (
                int(entity_rect_or_pos[0] - self.x),
                int(entity_rect_or_pos[1] - self.y),
            )