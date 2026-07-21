# ui.py
import pygame
import constants


class JournalUI:
    def __init__(self):
        self.current_debt = 50000

        # 🗺️ SPACED WITHIN THE INITIAL SPAWN ZONE (Around center x: 400-500, y: 300-400)
        self.notes = {
            "debt_log": {
                "text": f"BLACK MARKET DEBT: ${self.current_debt}",
                "world_x": 380,
                "world_y": 260,
                "rotation": -3.5
            }
        }

        self.font = pygame.font.Font(constants.PATH_MAIN_FONT, 32)

    def update_note_text(self, key, new_text):
        if key in self.notes:
            self.notes[key]["text"] = new_text

    def add_note(self, note_id, text, x, y, rotation=-3.5):
        """Helper to quickly drop new scrawls onto the page whenever you're ready."""
        self.notes[note_id] = {
            "text": text,
            "world_x": x,
            "world_y": y,
            "rotation": rotation
        }

    def draw(self, surface, camera):
        COLOR_SKETCH_INK = (15, 12, 10)
        COLOR_SHADOW_INK = (210, 195, 175)

        for note_id, data in self.notes.items():
            screen_pos = camera.apply((data["world_x"], data["world_y"]))

            shadow_surface = self.font.render(data["text"], True, COLOR_SHADOW_INK)
            rotated_shadow = pygame.transform.rotate(shadow_surface, data["rotation"])

            text_surface = self.font.render(data["text"], True, COLOR_SKETCH_INK)
            rotated_text = pygame.transform.rotate(text_surface, data["rotation"])

            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 2)]:
                surface.blit(
                    rotated_shadow,
                    (screen_pos[0] + dx, screen_pos[1] + dy)
                )

            surface.blit(rotated_text, screen_pos)