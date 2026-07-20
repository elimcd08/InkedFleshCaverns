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

PATH_PLAYER_SPRITE = "assets/images/player.png"

PATH_MAIN_FONT = "assets/fonts/creepy_font.ttf"
PATH_DEBT_MUSIC = "assets/audio/cave_ambience.mp3"


CAVE_AMBIENCE = resource_path("assets/audio/cave_ambience.mp3")
TEXTURE_WALLS = resource_path("assets/images/dark_cave_page_abyss.png")
TEXTURE_PATHS = resource_path("assets/images/path_texture.png")

SPRITE_PLAYER = None
FONT_MAIN = None
SOUND_BACKGROUND = None


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