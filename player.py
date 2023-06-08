import math
import entity
import matrix

WALKING_SPEED = 4.317
SPRINTING_SPEED = 7

class Player(entity.Entity):
    def __init__(self,world,shader,width,height):
        super().__init__(world)
        self.view_width = width
        self.view_height = height
        #matrices
        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()
        #shaders
        self.shader = shader
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        #camera bariables
        
        self.eyelevel = self.height -0.2
        self.input = [0,0,0]
        
        self.target_speed = WALKING_SPEED
        self.speed = self.target_speed
        
    def update(self,delta_time):
        self.speed += (self.target_speed - self.speed) * delta_time * 20
        
        if self.input[1]:
            self.velocity[1] += self.input[1] * self.speed
        
        if self.input[0] or self.input[2]:   
            angle = self.rotation[0] - math.atan2(self.input[2],self.input[0]) + math.tau /4
        
            self.velocity[0] = math.cos(angle) * self.speed
            self.velocity[2] = math.sin(angle) * self.speed
        
        super().update(delta_time)

    def update_matrices(self):
        #create projection matrix
        self.p_matrix.load_identity()
        self.p_matrix.perspective(90+20 * (self.speed - WALKING_SPEED) / (SPRINTING_SPEED - WALKING_SPEED),
                                  float(self.view_width)/self.view_height,0.1,500)
        #create modelview matrix
        self.mv_matrix.load_identity()
        self.mv_matrix.rotate_2d(self.rotation[0] + math.tau / 4,self.rotation[1])
        self.mv_matrix.translate(-self.position[0],-self.position[1],-self.position[2])
        #modelviewprojectionmatrix
        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location,mvp_matrix)