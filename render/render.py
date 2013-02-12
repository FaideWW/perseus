import pyglet.gl
import pyglet.graphics
import pyglet.sprite

"""
    module render
    written by cmcFaide

    Project Perseus
"""

# Set up textured batch groups

class TextureEnableGroup(pyglet.graphics.OrderedGroup):
    def __init__(self, order):
        super(TextureEnableGroup, self).__init__(order=order)

    def set_state(self):
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)

texture_enable_group = TextureEnableGroup()

class TexturedGroup(pyglet.graphics.OrderedGroup):
    def __init__(self,order,texture):
        super(TexturedGroup, self).__init__(order=order, parent=texture_enable_group)
        if texture.target != GL_TEXTURE_2D:
            raise TypeError('Invalid texure target')
        self.texture = texture

    def set_state(self):
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and self.texture == other.__class__)



class Render(Object):
    def __init__(self):

        #init the batch
        self.batch = pyglet.graphics.Batch()

        #set up the group dict
        self.groups = {}

        self.cam = None

    def addToBatch(self, obj, group=None):
        if group is not None and group not in self.groups:
            raise Exception('No group named ' + group + '.')

        if isinstance(obj, GLObject):
            self.batch.add(
                obj.count,
                obj.draw_mode,
                group,
                obj.vertex_list
            )
        elif isinstance(obj, pyglet.sprite.Sprite):
            obj.batch = self.batch
            obj.group = group
        else:
            raise TypeError('Not a valid renderable.')


    def setCamera(self, cam):
        self.cam = cam

    def draw(self, dt):
        to_clipspace = self.cam.toClipSpace()

        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(to_clipspace.x, to_clipspace.y, 0)

        #draw the batch
        self.batch.draw()

        pyglet.gl.glPopMatrix()




class GLObject(Object):
    def __init__(self, draw_mode=None, vertex_data=[], transform_matrix=[], color_data=None, tex_data=None):
        #Create an empty object
        self.draw_mode = draw_mode
        self.transform_matrix = transform_matrix
        self.count = len(vertex_data)

        #formatted as a tuple for compatibility with pyglet sprites
        self.position = (0,0)

        """
            vertex_data is formatted as:
                [
                    [x1,y1]
                    [x2,y2]
                        .
                        .
                    [xn,yn]
                ]
        """

        vertices = tuple([tuple(pair) for pair in vertex_data])
        colors = tuple(Color.white().rgba) * self.count

        self.vertex_list = (
            self.count,
            ('v2f', vertices),
            ('c4f', colors),
            None if tex_data is None else ('t2f', tuple([tuple(pair) for pair in tex_data]))
        )

        


    def __init__(self, globj):
        #Clone globj
        self.draw_mode = globj.draw_mode
        self.transform_matrix = globj.transform_matrix
        self.vertex_list = globj.vertex_list

class Color(Object):
    def __init__(num_list):
        if len(num_list) != 4 or any(not isinstance(x, float) for x in num_list)
            raise Exception('Color accepts four floating point numbers')

        self.rgba = [min(0.0,max(x, 1.0)) for x in num_list]

    @staticmethod
    def white():
        return Color([1.0,1.0,1.0,1.0])
