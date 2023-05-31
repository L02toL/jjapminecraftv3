import number

class Block_type:
    def __init__(self,texture_manager,name ="unknown",block_face_textures = {"all":"cobblestone"}):
        self.name = name

        self.vertex_positions = number.vertex_positions
        self.indices = number.indices

        for face in block_face_textures:
            texture = block_face_textures[face]
            texture_manager.add_texture(texture)