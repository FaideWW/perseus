import pyglet.gl
import pyglet.graphics
import pyglet.sprite

import component.component as component
import animation.animation as animation
import renderable

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
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)

    def unset_state(self):
        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)

texture_enable_group = TextureEnableGroup(0)


class TexturedGroup(pyglet.graphics.OrderedGroup):
    def __init__(self, order, texture):
        super(TexturedGroup, self).__init__(order=order, parent=texture_enable_group)
        if texture.target != pyglet.gl.GL_TEXTURE_2D:
            raise TypeError('Invalid texure target')
        self.texture = texture

    def set_state(self):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self.texture.id)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and self.texture == other.__class__)


class Render(object):
    def __init__(self):

        #init the batch
        self.batch = pyglet.graphics.Batch()

        self.batch_list = []
        self.batch_vertexes = []
        self.blit_positions = []
        self.blit_list = []

        #set up the group dict
        self.groups = {}

        self.cam = None

    """
        Adds a Renderable or group of Renderables to the batch,
        and allocates a chunk of space in the vertex list for vertices

        Returns a Pair representing the index of the allocated block and
        the size of the block

        if the object is a list:
            save the current length (starting index for the block),
            and start with 0 size
            call addToBatch on each element
            sum the sizes of all the Pairs (in case one element is another list)
            return the allocation as the starting index and the total size
    """
    def addToBatch(self, obj, group=None):

        if group is not None and group not in self.groups:
            raise Exception('No group named ' + group + '.')
        if type(obj) == list:
            obj_ret = []
            for o in obj:
                obj_ret.append(self.addToBatch(o, group))
            return obj_ret
        elif isinstance(obj, GLObject):
            self.batch_vertexes.append(self.batch.add(
                obj.count,
                obj.draw_mode,
                group,
                obj.vertices,
                obj.colors
            ))
        elif isinstance(obj, pyglet.sprite.Sprite):
            self.batch_vertexes.append(obj)
            self.batch_list.append(obj)
            obj.batch = self.batch
            obj.group = group
        elif isinstance(obj, animation.Animation):
            spr = pyglet.sprite.Sprite(obj.asPygletAnimation())
            self.batch_vertexes.append(spr)
            self.batch_list.append(spr)
            spr.batch = self.batch
            #obj.sprite.group = group
        else:
            raise TypeError('Not a valid renderable.  Type ', type(obj), 'cannot be rendered')
        return len(self.batch_vertexes) - 1

    def addToBlit(self, obj, position=component.Vector.zero()):
        if isinstance(obj, pyglet.image.Texture):
            self.blit_positions.append(position)
            self.blit_list.append(obj)
        return len(self.blit_list) - 1

    def changeBatchPosition(self, index, position):
        if index < 0 or index >= len(self.batch_vertexes):
            return

        position = position
        batch_obj = self.batch_vertexes[index]
        if isinstance(batch_obj, pyglet.sprite.Sprite):
            batch_obj.set_position(batch_obj.x + position.x, batch_obj.y + position.y)
        else:
            #batch_obj is a vertex list
            #add x position
            batch_obj.vertices[::2] = [x + position.x for x in batch_obj.vertices[::2]]
            #add y position
            batch_obj.vertices[1::2] = [y + position.y for y in batch_obj.vertices[1::2]]

    def getVertexList(self, index=None):
        if index is None:
            return self.batch_vertexes
        else:
            return self.batch_vertexes[index]

    def setBlitPosition(self, index, position):
        pass

    def setCamera(self, cam):
        self.cam = cam

    def draw(self, dt):
        to_clipspace = self.cam.toClipSpace()

        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(to_clipspace.x, to_clipspace.y, 0)

        for obj in self.blit_list:
            obj.blit(0, 0)
        #draw the batch
        self.batch.draw()

        pyglet.gl.glPopMatrix()

    def generateRenderables(self, obj_list, group=None):
        """
            returns a list of batched renderables
            (blitted renderables not compatible)
        """
        return [renderable.Renderable(obj, self, self.addToBatch(obj, group)) for obj in obj_list]


class GLObject(object):
    def __init__(self, draw_mode=None, vertex_data=[], transform_matrix=[], color_data=None, tex_data=None):
        #Create an empty object
        self.draw_mode = draw_mode
        self.transform_matrix = transform_matrix
        self.count = len(vertex_data)

        #formatted as a tuple for compatibility with pyglet sprites
        self.position = (0, 0)

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

        self.vertices = ('v2f', tuple([coord for pair in vertex_data for coord in pair]))
        self.colors = ('c4f', tuple(Color.white().rgba if color_data is None else color_data) * self.count)

        if tex_data is not None:
            self.vertex_list = self.vertex_list + ('t2f', tuple([tuple(pair) for pair in tex_data]))

    @staticmethod
    def rectFromPoints(topleft, bottomright, mask, color=None):
        vertex_list = []
        if mask[0]:
            vertex_list.append([topleft.x, topleft.y])
            vertex_list.append([bottomright.x, topleft.y])
        if mask[1]:
            vertex_list.append([bottomright.x, topleft.y])
            vertex_list.append([bottomright.x, bottomright.y])
        if mask[2]:
            vertex_list.append([bottomright.x, bottomright.y])
            vertex_list.append([topleft.x, bottomright.y])
        if mask[3]:
            vertex_list.append([topleft.x, bottomright.y])
            vertex_list.append([topleft.x, topleft.y])
        return GLObject(
            pyglet.gl.GL_LINES,
            vertex_list,
            [],
            color,
        )


class Color(object):
    def __init__(self, num_list):
        if len(num_list) != 4 or any(not isinstance(x, float) for x in num_list):
            raise Exception('Color accepts four floating point numbers')

        self.rgba = [min(0.0, max(i, 1.0)) for i in num_list]

    @staticmethod
    def white():
        return Color([1.0, 1.0, 1.0, 1.0])
