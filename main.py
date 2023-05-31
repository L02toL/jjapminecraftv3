#dictionaries
import math
import ctypes
import pyglet
import pyglet.gl as gl
#files
import shader
import matrix
import block_type

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

class Window(pyglet.window.Window):
    def __init__(self, **args):
        super().__init__(**args)
        #blocks
        
        self.cobblestone = block_type.Block_type("cobblestone",{"all":"cobblestone"})
        self.grass = block_type.Block_type("grass",{"top":"grass","bottom":"dirt","sides":"grass_side"})
        self.dirt = block_type.Block_type("dirt",{"all":"dirt"})
        self.stone = block_type.Block_type("stone",{"all":"stone"})
        self.sand = block_type.Block_type("sand",{"all":"sand"})
        self.planks = block_type.Block_type("planks",{"all":"planks"})
        self.log = block_type.Block_type("log",{"top":"log_top","bottom":"log_top","side":"log_side"})

        #vertex array
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1,ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)
        #vertex buffer
        self.vbo = gl.GLuint(0)
        gl.glGenBuffers(1,ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,self.vbo)

        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_position)),
                        (gl.GLfloat * len(self.grass.vertex_position)) (*self.grass.vertex_position),
                        gl.GL_STATIC_DRAW)
        
        gl.glVertexAttribPointer(0,3,gl.GL_FLOAT,gl.GL_FALSE,0,0)
        gl.glEnableVertexAttribArray(0)
        #indexbufferobject
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1,self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER,self.ibo)

        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLuint * len(self.grass.indices)),
                        (gl.GLuint * len(self.grass.indices)) (*self.grass.indices),
                        gl.GL_STATIC_DRAW)
        #shader
        self.shader = shader.Shader("vert.glsl","frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader.use()
        #matrices
        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()
        
        self.x = 0
        pyglet.clock.schedule_interval(self.update,1.0/60)
        
    def update(self,delta_time):
        self.x += delta_time

    def on_draw(self):
        #create projection matrix
        self.p_matrix.load_identity()
        self.p_matrix.perspective(90,float(self.width)/self.height,0.1,500)
        #create modelview matrix
        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0,0,-3)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)
        #modelviewprojectionmatrix
        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location,mvp_matrix)
        #draw
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.grass.indices),
            gl.GL_UNSIGNED_INT,
            None
        )
    
    def on_resize(self,width,height):
        print(f"resize {width} * {height}")
        gl.glViewport(0,0,width,height)

class Game:
    def __init__(self):
        self.config = gl.Config(double_buffer = True, major_version = 3, minor_version = 3, depth_size = 16)
        self.window = Window(config = self.config, width = 800, height = 600, caption = "jjapmincraft", resizable = True, vsync = False)
    def run(self):
        pyglet.app.run()
if __name__ == "__main__":
    game = Game()
    game.run()