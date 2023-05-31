import number

class Block_type:
    def __init__(self,name ="unknown",block_face_textures = {"all":"cobblestone"}):
        self.name = name

        self.vertex_position = number.vertex_positions
        self.indices = number.indices
