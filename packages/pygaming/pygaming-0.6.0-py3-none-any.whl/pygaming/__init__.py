"""
Pygaming is a python library used to create videogames in python, based on pygame.
Pygaming provide an exhaustive template to create your own offline and online games
by defining your own game phases and transitions between them. Pygaming also
provides settings, loggers, inputs, files, music and sounds, network, and database management,
as well as multi-language support, screen, widgets and frames.
"""
from .config import Config
from .game import Game
from .base import NO_NEXT, STAY
from .logger import Logger
from .phase import ServerPhase, GamePhase
from .server import Server
from .settings import Settings
from .color import Color

from .screen.screen import Screen
from .screen.frame import Frame
from .screen.element import (
    Element, TOP_LEFT, TOP_RIGHT, CENTER, BOTTOM_LEFT, BOTTOM_CENTER,
    BOTTOM_RIGHT, CENTER_LEFT, CENTER_RIGHT, TOP_CENTER
)
from .screen.widget.label import Label
from .screen.widget.widget import Widget
from .screen.widget.slider import Slider
from .screen.widget.button import Button, TextButton
from .file import get_file
from .screen.widget.entry import Entry
from .screen.actor import Actor
from .screen.art.art import Art
from .screen.art import transformation
from .screen.art import binary_transformation
from .screen.art.file import ImageFile, ImageFolder, GIFFile
from .screen.art.colored_surfaces import ColoredRectangle, ColoredCircle, ColoredPolygon

from .inputs import Inputs, Controls, Click, Keyboard, Mouse
from .connexion import Client, Server as Network, HEADER, ID, CONTENT, TIMESTAMP

from .database import Database, Texts, Speeches, TypeWriter, SoundBox
from . import commands
from .screen.art.colored_surfaces import ColoredRectangle, ColoredCircle, ColoredPolygon

__all__ = ['Config', 'Font', 'Game', 'NO_NEXT', 'STAY', 'Logger', 'ServerPhase', 'GamePhase',
           'Server', 'Settings', 'Screen', 'Frame', 'Actor', 'TextButton', 'CENTER_LEFT', 'CENTER_RIGHT', 'TOP_CENTER', 'BOTTOM_CENTER',
           'Element', 'AnimatedSurface', 'SurfaceLike', 'SurfacesLike', 'Inputs', 'Controls', 'Click', 'transformation',
           'get_file', 'Client', 'Keyboard', 'Mouse', 'ImageFile', 'ImageFolder', 'GIFFile', 'binary_transformation',
           'Network', 'HEADER', 'ID', 'CONTENT', 'TIMESTAMP', 'Database', 'Texts', 'Speeches', 'Button','Entry', 'Art',
           'commands', 'ColoredRectangle', 'TOP_LEFT', 'TOP_RIGHT', 'CENTER', 'BOTTOM_LEFT', 'BOTTOM_RIGHT',
           'Label', 'Widget', 'Slider', 'ColoredCircle', 'ColoredPolygon', 'TypeWriter', 'SoundBox', 'Color']
