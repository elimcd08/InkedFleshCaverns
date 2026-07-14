import constants


class Camera:

    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        self.x = target.x - (constants.SCREEN_WIDTH // 2)
        self.y = target.y - (constants.SCREEN_HEIGHT // 2)

        self.x = max(0, min(self.x, self.width - constants.SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.height - constants.SCREEN_HEIGHT))

    def apply(self, entity_rect_or_pos):
        if hasattr(entity_rect_or_pos, "topleft"):
            return entity_rect_or_pos.move(-self.x, -self.y)
        else:
            return (
                int(entity_rect_or_pos[0] - self.x),
                int(entity_rect_or_pos[1] - self.y),
            )