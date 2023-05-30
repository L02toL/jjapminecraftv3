import ctypes
import pyglet.gl as gl

class Shader_error(Exception):
    def __init__(self, message):
        self.message = message
def create_shader(target,source_path):
    