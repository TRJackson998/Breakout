"""
Sound
=======
Handles sound files and sound effects for the game.
This module initializes the pygame mixer and provides a SoundManager class
that loads and plays sound effects and background music from the game's sounds folder.

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

import time

import pygame

from breakout import base_path

# Initialize the mixer (if not already initialized elsewhere)
pygame.mixer.init()
# pylint: disable=no-member


class SoundManager:
    """
    Manages sound effects and background music for the game.

    Sound files are loaded from the "sounds" directory located at base_path.
    If a sound file fails to load, its attribute is set to None.
    """

    sound_on = True
    sound_path = base_path.joinpath("sounds")

    try:
        powerup_sound = pygame.mixer.Sound(
            str(sound_path.joinpath("powerup_catch.wav"))
        )
        brick_sound = pygame.mixer.Sound(str(sound_path.joinpath("brick_hit.wav")))
        paddle_sound = pygame.mixer.Sound(str(sound_path.joinpath("wall_sound.wav")))
        wall_sound = pygame.mixer.Sound(str(sound_path.joinpath("wall_sound.wav")))
        life_lost_sound = pygame.mixer.Sound(str(sound_path.joinpath("life_lost.wav")))
        game_over_sound = pygame.mixer.Sound(str(sound_path.joinpath("game_over.wav")))
        background_music = [
            pygame.mixer.Sound(str(sound_path.joinpath("background_music1.mp3"))),
            pygame.mixer.Sound(str(sound_path.joinpath("background_music2.mp3"))),
            pygame.mixer.Sound(str(sound_path.joinpath("background_music3.mp3"))),
        ]
    except (FileNotFoundError, pygame.error) as e:
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
    if background_music:
        music_channel = pygame.mixer.Channel(1)
        current_music = 0
        music_channel.set_endevent(pygame.USEREVENT + 1)
        music_channel.play(background_music[current_music])

    @staticmethod
    def play_powerup():
        """Plays powerup sound"""
        if SoundManager.powerup_sound and SoundManager.sound_on:
            SoundManager.powerup_sound.play()

    @staticmethod
    def play_brick():
        """Plays brick hit sound"""
        if SoundManager.brick_sound and SoundManager.sound_on:
            SoundManager.brick_sound.play()

    @staticmethod
    def play_paddle():
        """Plays paddle hit sound"""
        if SoundManager.paddle_sound and SoundManager.sound_on:
            SoundManager.paddle_sound.play()

    @staticmethod
    def play_wall():
        """Plays wall hit sound"""
        if SoundManager.wall_sound and SoundManager.sound_on:
            SoundManager.wall_sound.play()

    @staticmethod
    def play_life_lost():
        """Plays life lost sound"""
        if SoundManager.life_lost_sound and SoundManager.sound_on:
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
    def play_background_music():
        """Play the background music on loop."""
        if SoundManager.background_music and SoundManager.sound_on:
            SoundManager.music_channel.unpause()
            if not SoundManager.music_channel.get_busy():
                SoundManager.music_channel.play(
                    SoundManager.background_music[SoundManager.current_music]
                )

    @staticmethod
    def stop_background_music():
        """Stops the background screen music."""
        if SoundManager.background_music:
            SoundManager.music_channel.pause()

    @staticmethod
    def stop_other_sounds():
        """Stops all sounds except background music."""
        for sound in SoundManager.sound_effects:
            if sound:
                sound = None
