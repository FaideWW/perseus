:mod:`animation` --- Sprite animation
=====================================

.. module:: animation
   :synopsis: Classes and functions that support timed multiple-image Spriting (animation).

.. sectionauthor:: cmcFaide <michael@faide.net>

The :mod:`animation` module includes the Animation class and handles animated sprites in Perseus.

-------

.. class:: Animation(spritesheet, region_data, fps[, repeats=True])
   :module: animation

   Creates an animation based on a spritesheet.  ``region_data`` specifies the sections of the spritesheet represent each frame.  ``fps`` indicates the speed at which the animation runs (frames per second).

   In order to cooperate with Pyglet's framework, Animation includes a ``Sprite`` object from the :mod:`pyglet.graphics` module.  When the :class:`Animation` is added to the batch, the Sprite object is linked to it instead.  When the Animation switches frames, it updates the image contained in ``Sprite``, which is then updated in the batch. 

   .. method:: _readAnimationData(region_data)

      Reads in the data for splitting up the sprite sheet into individual frames.  Returns a parsed array of coordinates relating to the corners of each frame, and any necessary offset in objectspace for that frame.

      .. note::

         Region data is formatted as such:

         .. code-block:: python

            tl.x,tl.y,br.x,br.y,o.x,o.y

         Where each pair of numbers corresponds to a corner of the region, and ``o`` is the offset for the frame.

         Repeated for the number of frames in the animation.

   .. method:: _buildFrames(spritesheet, frame_data)

      Slices the spritesheet into regions for each frame, and then loads each region and any necessary transformations (offset) into a frame array.  Returns that frame array.

      .. note::

         In this case 'slicing' does not change the original spritesheet.  It only means that for each frame, only a section of the entire sheet is rendered.  This saves on GPU memory and calls, and preserves the original sheet.

   .. method:: update(dt)

      If enough time has passed since the last frame-switch (according to fps), :meth:`nextFrame` is called.

   .. method:: nextFrame()

      Loads up the next frame in the sequence.  If the last frame is reached, either the first frame will be loaded or nothing will happen, depending on whether or not ``repeats`` is set to ``True`` or not.

   .. method:: getCurrentFrame()

      Returns the index of the current frame (starting at 1).