import ctypes
import pyglet

import pyglet.gl as gl

class Texture_manager:
    def __init__(self, texture_width, texture_height, max_texture):
        self.texture_width = texture_width
        self.texture_height = texture_height

        self.max_texture = max_texture

        self.textures =[]