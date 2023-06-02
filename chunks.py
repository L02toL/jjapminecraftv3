import ctypes

import pyglet.gl as gl
import block_type

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
CHUNK_LENGHT =16

class Chunk:
    def __init__ (self, chunk_position):
        self.chunk_position = chunk_position

        self.position = (
            self.chunk_position[0] * CHUNK_WIDTH,
            self.chunk_position[1] * CHUNK_HEIGHT,
            self.chunk_position[2] * CHUNK_LENGHT
        )

        self.has_mesh = False

        self.mesh_vertex_positions = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []

        self.mesh_index_counter=0
        self.mesh_indices=[]

        #array

        self.vao = gl.GLuint(0)
        gl.glGenBuffers(1,self.vao)
        gl.glBindVertexArray(self.vao)

        #positionvbo

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1,self.vertex_position_vbo)

        #rexcoord

        self.tex_coord_vbo = gl.GLuint(0)
        gl.glGenBuffers(1,self.tex_coord_vbo)

        #shading values

        self.shading_values_vbo = gl.GLuint(0)
        gl.glGenBuffers(1,self.shading_values_vbo)

        #inder buffer

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1,self.ibo)
    def update_mesh(self,block_type):
        self.has_mesh = True
        
        self.mesh_vertex_position = []
        self.mesh_tex_coords = []
        self.mesh_shading_values = []

        self.mesh_index_counter = 0
        self.mesh_indices = []

        for local_x in range(CHUNK_WIDTH):
            for local_y in range(CHUNK_HEIGHT):
                for local_z in range(CHUNK_LENGHT):
                    x,y,z = (
                        self.position[0] + local_x,
                        self.position[1] + local_y,
                        self.posiiton[2] + local_z
                    )

                    vertex_positions = block_type.vertex_positions.copy()

                    for i in range(24):
                        vertex_positions[i * 3 + 0] += x
                        vertex_positions[i * 3 + 1] += y
                        vertex_positions[i * 3 + 2] += z
                    
                    self.mesh_vertex_positions
                        