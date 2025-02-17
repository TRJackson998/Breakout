"""
Sound
=======
Handle the sound files and add sound effects to the game.

Class
-----
Capstone in Computer Science
UMGC CMSC 495
Professor Munoz

Team Charlie
------------
Daniel Coreas
Aimi Hanson
Terrence Jackson
Thomas Nugent
"""

import sys
import time
from pathlib import Path

import pygame

# Initialize the mixer (if not already initialized elsewhere)
pygame.mixer.init()
# pylint: disable=no-member


class SoundManager:
    sound_on = True
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent

    sound_path = base_path.joinpath("sounds")

    try:
        powerup_sound = pygame.mixer.Sound(sound_path.joinpath("powerup_catch.wav"))
        brick_sound = pygame.mixer.Sound(sound_path.joinpath("brick_hit.wav"))
        paddle_sound = pygame.mixer.Sound(sound_path.joinpath("wall_sound.wav"))
        wall_sound = pygame.mixer.Sound(sound_path.joinpath("wall_sound.wav"))
        life_lost_sound = pygame.mixer.Sound(sound_path.joinpath("life_lost.wav"))
        game_over_sound = pygame.mixer.Sound(sound_path.joinpath("game_over.wav"))
        background_music = pygame.mixer.Sound(
            sound_path.joinpath("background_music.mp3")
        )
    except Exception as e:
        print("Error loading sound effects:", e)
        powerup_sound = None
        brick_sound = None
        paddle_sound = None
        wall_sound = None
        life_lost_sound = None
        game_over_sound = None
        background_music = None

    sound_effects = [
        powerup_sound,
        brick_sound,
        paddle_sound,
        wall_sound,
        life_lost_sound,
        game_over_sound,
    ]

    @staticmethod
    def play_powerup():
        """Plays powerup sound"""
        if SoundManager.powerup_sound:
            SoundManager.powerup_sound.play()

    @staticmethod
    def play_brick():
        """Plays brick hit sound"""
        if SoundManager.brick_sound:
            SoundManager.brick_sound.play()

    @staticmethod
    def play_paddle():
        """Plays paddle hit sound"""
        if SoundManager.paddle_sound:
            SoundManager.paddle_sound.play()

    @staticmethod
    def play_wall():
        """Plays wall hit sound"""
        if SoundManager.wall_sound:
            SoundManager.wall_sound.play()

    @staticmethod
    def play_life_lost():
        """Plays life lost sound"""
        if SoundManager.life_lost_sound:
            SoundManager.life_lost_sound.play()

    @staticmethod
    def play_game_over():
        """Plays game over sound"""
        SoundManager.stop_background_music()
        if SoundManager.game_over_sound and SoundManager.sound_on:
            SoundManager.game_over_sound.play()
            time.sleep(1)
            SoundManager.play_background_music()

    @staticmethod
    def play_background_music(loops=-1):
        """Play the background music on loop."""
        if SoundManager.background_music and SoundManager.sound_on:
            SoundManager.background_music.play(loops=loops)

    @staticmethod
    def stop_background_music():
        """Stops the background screen music."""
        if SoundManager.background_music:
            SoundManager.background_music.stop()

    @staticmethod
    def stop_other_sounds():
        """Stops all sounds except background music."""
        for sound in SoundManager.sound_effects:
            if sound:
                sound = None
