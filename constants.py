import pygame
from utils import resource_path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

PLAYER_SPEED = 225
SIGHT_RADIUS = 340


COLOR_BACKGROUND = (38, 35, 34)
COLOR_PAPYRUS = (18, 18, 20)
COLOR_INK_VEIN = (95, 88, 80)
COLOR_PLAYER = (160, 35, 45)

COLOR_INK_DARK = (28, 24, 22)       # Rich charcoal ink for outlines and text
COLOR_INK_FLUID = (45, 30, 75)      # Deep indigo/purple fluid for the filled inkwell
COLOR_INK_STAIN = (180, 165, 145)

PATH_PLAYER_SPRITE = "assets/images/player.png"

PATH_MAIN_FONT = "assets/fonts/creepy_font.ttf"
PATH_DEBT_MUSIC = "assets/audio/cave_ambience.mp3"


CAVE_AMBIENCE = resource_path("assets/audio/cave_ambience.mp3")
TEXTURE_WALLS = resource_path("assets/images/dark_cave_page_abyss.png")
TEXTURE_PATHS = resource_path("assets/images/path_texture.png")

SPRITE_PLAYER = None
FONT_MAIN = None
SOUND_BACKGROUND = None

# --- STANDALONE VECTOR UI SURFACES ---

# Create a clean, transparent canvas for the container shape
UI_INKWELL_SURFACE = pygame.Surface((64, 64), pygame.SRCALPHA)

# Draw a sketchy ink bottle structure using your rich charcoal ink color:
# 1. The bottle neck ring (Top)
pygame.draw.ellipse(UI_INKWELL_SURFACE, COLOR_INK_DARK, (20, 2, 24, 10), 2)
# 2. Vertical neck walls
pygame.draw.line(UI_INKWELL_SURFACE, COLOR_INK_DARK, (20, 7), (20, 16), 2)
pygame.draw.line(UI_INKWELL_SURFACE, COLOR_INK_DARK, (44, 7), (44, 16), 2)
# 3. The rounded main reservoir base (Bottom)
pygame.draw.rect(UI_INKWELL_SURFACE, COLOR_INK_DARK, (8, 16, 48, 44), 2, border_radius=8)


def load_game_assets():
    global SPRITE_PLAYER, FONT_MAIN, SOUND_BACKGROUND
    try:
        raw_player = pygame.image.load(resource_path(PATH_PLAYER_SPRITE))
        SPRITE_PLAYER = pygame.transform.scale(
            raw_player.convert_alpha(), (32, 32)
        )
        FONT_MAIN = pygame.font.Font(resource_path(PATH_MAIN_FONT), 24)
        SOUND_BACKGROUND = pygame.mixer.Sound(resource_path(PATH_DEBT_MUSIC))
    except pygame.error:
        pass