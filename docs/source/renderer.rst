:mod:`render` --- Renderer and associated functions
===================================================

.. module:: render
   :synopsis: Functions involving the drawing of objects to the screen.

.. sectionauthor:: cmcFaide <michael@faide.net>

The renderer handles drawing objects to the screen during the draw phase of the game loop.  

.. _draw_sequence:

Operation of the Draw Sequence
------------------------------

When the renderer's :meth:`draw` is invoked, the batch draws each batch group in order of lowest to highest priority.

The groups from lowest to highest priority are as follows:

#. skybox
#. bg_terrain
#. bg_scene
#. fg_terrain
#. fg_scene
#. level
#. entities
#. effects
#. hud

Groups are distinguished by their prominence in the game scene.  If two areas of a group overlap, the group with higher priority will be drawn over the other.  Groups may or may not share textures, but one group must use one texture for all objects in that group, or no texture at all (in the case of entities).

For each object in the batch, its position in the world will be interpolated based on the time between game cycle updates and its position/velocity from the last cycle.

.. note:: 
    
   In order to accomodate multiple renderers, we have to assume the screen has already been cleared before the renderer's :meth:`draw` is invoked.  This way one renderer will not overwrite another's :meth:`draw`.

------

..  class:: Render()
    :module: render
   
    Creates a :class:`Render` object with an empty rendering queue and a batch.

    A :class:`Render` object has the following methods.

    .. method:: addToBatch(GLObject[, group='effects'])
                addToBatch(Sprite[, group='effects'])

       Adds a GLObject or Sprite to the batch.  The object will be drawn on the next iteration of the loop.  If a group is specified, that object will be added to and drawn with that group.  If no group is specified, the object will be added to the effects group by default.

       .. note::

          The GameObject is tied to the object that created it, not the batch.  If the object is destroyed outside of the batch, it is automatically removed from the batch.

    .. method:: setCamera(Camera)

       Centers clipspace to the worldspace position of ``Camera``.  See :ref:`draw_spaces` for more information.

    .. method:: draw(dt)

       Invokes the draw sequence.  See :ref:`draw_sequence` for information.

------

.. class:: GLObject([draw_mode[, vertex_data[, transform_matrix[, color[, tex_data=None]]]]]])
           GLObject(GLObject)
   :module: render

   Creates an OpenGL object that contains the necssary data to completely render a GL shape or sprite to the screen.
   The :class:`GLObject` is mostly a container class, used only for communicating render data in a common format between GameObjects and the renderer.

   A :class:`GLObject` can be cloned from another :class:`GLObject` by instantiating it with the source as the only parameter.

   A GLObject has the following properties:

   *draw_mode*
      The GL draw mode for the particular object.  The available draw modes are:

      * GL_POINTS
      * GL_LINES
      * GL_TRIANGLES
      * GL_TRIANGLE_STRIP
      * GL_TRIANGE_FAN

      See `opengl modes`_ for more details on these draw modes.

      .. _opengl modes: http://en.wikibooks.org/wiki/OpenGL_Programming/GLStart/Tut3

   *vertex_array*
      A set of vertex data that consists of a list of vertices, and a second list that determines the order in which these vertices should be drawn to correctly draw the object.

   *transform_matrix*
      A transformation matrix to be performed on the object when being drawn.  See `understanding transformation matrices`_ for more details on transformation matrices.

      .. _understanding transformation matrices: http://en.wikibooks.org/wiki/OpenGL_Programming/3D/Matrices

   *color*
      A :class:`Color` object representing the RGBA value of the object to be drawn. 

   *tex_data*
      If the GLObject has a texture associated with it, tex_data will consist of the coordinates of the region of the texture to draw for the object.

      If the GLObject does not have a texture, this will default to None.

   .. note::

      Using colorization on a sprite will *add* the color into the sprite's pixels, meaning if the red and blue values of the color are 0.0, only the green component of the sprite will be drawn and the result will be a very nauseous looking sprite.

.. class:: Color(num_list)

   Takes a list of length ``4`` that represents the RGBA value of a color in OpenGL.

   The list should consist of four floating-point values between 0.0 and 1.0.


Textured Batch Groups
---------------------

The following outlines internal class structure used for enabling and drawing GL textures with batch groups.  

The :class:`TextureEnableGroup` class handles setting and unsetting the GL_TEXTURE state.  Each :class:`TextureBindGroup` inherits this state setting, and then loads its group's texture into memory.  When the group's :meth:`unset_state` is called, the inhertied :class:`TextureEnableGroup` method disables GL_TEXTURE again.

Because the logic of these classes are handled by pyglet, they will not be documented here.

The following example outlines the proper usage of these groups for two batched texture groups::

   batch.add(4, GL_QUADS, TextureBindGroup(texture1), 'v2f', 't2f')
   batch.add(4, GL_QUADS, TextureBindGroup(texture2), 'v2f', 't2f')
