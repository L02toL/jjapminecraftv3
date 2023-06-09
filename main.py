#dictionaries
import math
import random
import ctypes
import pyglet
pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl
#files
import matrix
import shader
import player

import world

import hit

class Window(pyglet.window.Window):
    def __init__(self, **args):
        super().__init__(**args)
        #blocks
        
        self.world = world.World()
        
        #shader
        self.shader = shader.Shader("vert.glsl","frag.glsl")
        #gone to cam
        self.shader_sampler_location = self.shader.find_uniform(b"texture_array_sampler")
        self.shader.use()
        #matrices
        #gone to cam
        #pygletstuff

        pyglet.clock.schedule_interval(self.update,1.0 / 10000)
        self.mouse_captured = False
        #camera
        self.player = player.Player(self.world,self.shader,self.width,self.height)
        
        self.holding = 7
        
    def update(self,delta_time):
        if not self.mouse_captured:
            self.player.input = [0,0,0]
        
        self.player.update(delta_time)
        
    def on_draw(self):
        self.player.update_matrices()
        #gone to cam
        #bind textures
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY,self.world.texture_manager.texture_array)
        gl.glUniform1i(self.shader_sampler_location,0)
        #draw
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()
        self.world.draw()
        
        gl.glFinish()
        
    
    def on_resize(self,width,height):
        print(f"resize {width} * {height}")
        gl.glViewport(0,0,width,height)
        self.player.width = width
        self.player.height = height
    
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.mouse_captured:
            self.mouse_captured = True
            self.set_exclusive_mouse(True)
            return
        
        def hit_callback(current_block,next_block):
            if button == pyglet.window.mouse.RIGHT: self.world.set_block(current_block,self.holding)
            elif button == pyglet.window.mouse.LEFT: self.world.set_block(next_block,0)
            elif button == pyglet.window.mouse.MIDDLE: self.holding = self.world.get_block_number(next_block)
        
        x, y, z = self.player.position
        y+= self.player.eyelevel

        hit_ray = hit.Hit_ray(self.world,self.player.rotation,(x,y,z))
        
        while hit_ray.distance < hit.HIT_RANGE:
            if hit_ray.step(hit_callback):
                break
        
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        if self.mouse_captured:
            sensitivity = 0.004
            
            self.player.rotation[0] += delta_x * sensitivity
            self.player.rotation[1] += delta_y * sensitivity
            
            self.player.rotation[1] = max(-math.tau / 4, min(math.tau / 4, self.player.rotation[1]))
    
    def on_mouse_drag(self,x,y,delta_x,delta_y,buttons,modifiers):
        self.on_mouse_motion(x,y,delta_x,delta_y)
    
    def on_key_press(self, key, modifiers):
        if not self.mouse_captured:
            return
        
        if key == pyglet.window.key.W: self.player.input[2] += 1
        elif key == pyglet.window.key.S: self.player.input[2] -= 1
        elif key == pyglet.window.key.A: self.player.input[0] -= 1
        elif key == pyglet.window.key.D: self.player.input[0] += 1
        
        elif key == pyglet.window.key.SPACE: self.player.input[1] += 1
        elif key == pyglet.window.key.LSHIFT: self.player.input[1] -= 1
        elif key == pyglet.window.key.LCTRL : self.player.target_speed = player.SPRINTING_SPEED

        elif key == pyglet.window.key.G:
            self.holding = random.randint(1,len(self.world.block_types) - 1)
        elif key == pyglet.window.key.O:
            self.world.save.save()
        
        elif key == pyglet.window.key.ESCAPE:
            self.mouse_captured = False
            self.set_exclusive_mouse(False)
            
    def on_key_release(self, key, modifiers):
        if not self.mouse_captured:
            return
        
        if key == pyglet.window.key.W: self.player.input[2] -= 1
        elif key == pyglet.window.key.S: self.player.input[2] += 1
        elif key == pyglet.window.key.A: self.player.input[0] += 1
        elif key == pyglet.window.key.D: self.player.input[0] -= 1
        
        elif key == pyglet.window.key.SPACE: self.player.input[1] -= 1
        elif key == pyglet.window.key.LSHIFT: self.player.input[1] += 1
        elif key == pyglet.window.key.LCTRL : self.player.target_speed = player.WALKING_SPEED
    

class Game:
    def __init__(self):
        self.config = gl.Config(double_buffer = True, major_version = 3, minor_version = 3, depth_size = 16)
        self.window = Window(config = self.config, width = 800, height = 600, caption = "jjapmincraft", resizable = True, vsync = False)
    def run(self):
        pyglet.app.run()
if __name__ == "__main__":
    game = Game()
    game.run()