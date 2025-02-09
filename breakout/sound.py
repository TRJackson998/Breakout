# sound.py
import pygame

# Initialize the mixer (if not already initialized elsewhere)
pygame.mixer.init()


class SoundManager:
    try:
        POWERUP_SOUND = pygame.mixer.Sound("breakout/sounds/powerup_catch.wav")
        BRICK_SOUND = pygame.mixer.Sound("breakout/sounds/brick_hit.wav")
        PADDLE_SOUND = pygame.mixer.Sound("breakout/sounds/wall_sound.wav")
        WALL_SOUND = pygame.mixer.Sound("breakout/sounds/wall_sound.wav")
        LIFE_LOST_SOUND = pygame.mixer.Sound("breakout/sounds/life_lost.wav")
        GAME_OVER_SOUND = pygame.mixer.Sound("breakout/sounds/game_over.wav")
        BACKGROUND_MUSIC = pygame.mixer.Sound("breakout/sounds/background_music.mp3")
    except Exception as e:
        print("Error loading sound effects:", e)
        POWERUP_SOUND = None
        BRICK_SOUND = None
        PADDLE_SOUND = None
        WALL_SOUND = None
        LIFE_LOST_SOUND = None
        GAME_OVER_SOUND = None
        BACKGROUND_MUSIC = None

    @staticmethod
    def play_powerup():
        """Plays powerup sound"""
        if SoundManager.POWERUP_SOUND:
            SoundManager.POWERUP_SOUND.play()

    @staticmethod
    def play_brick():
        """Plays brick hit sound"""
        if SoundManager.BRICK_SOUND:
            SoundManager.BRICK_SOUND.play()

    @staticmethod
    def play_paddle():
        """Plays paddle hit sound"""
        if SoundManager.PADDLE_SOUND:
            SoundManager.PADDLE_SOUND.play()

    @staticmethod
    def play_wall():
        """Plays wall hit sound"""
        if SoundManager.WALL_SOUND:
            SoundManager.WALL_SOUND.play()

    @staticmethod
    def play_life_lost():
        """Plays life lost sound"""
        if SoundManager.LIFE_LOST_SOUND:
            SoundManager.LIFE_LOST_SOUND.play()

    @staticmethod
    def play_game_over():
        """Plays game over sound"""
        if SoundManager.GAME_OVER_SOUND:
            SoundManager.GAME_OVER_SOUND.play()

    @staticmethod
    def play_background_music(loops=-1):
        """Play the background music on loop."""
        if SoundManager.BACKGROUND_MUSIC:
            SoundManager.BACKGROUND_MUSIC.play(loops=loops)

    @staticmethod
    def stop_background_music():
        """Stops the background screen music."""
        if SoundManager.BACKGROUND_MUSIC:
            SoundManager.BACKGROUND_MUSIC.stop()
