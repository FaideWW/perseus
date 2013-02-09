Appendix
========



.. _draw_spaces:

Distinction between different draw-spaces
-----------------------------------------

In this documentation I'm using terminology native to graphics programmers to describe game-logic elements.  Here I will explain what I mean by the different -spaces that I talk about.

-space describes a coordinate system that is relative to some reference point.  Typically in 3D games, this involves linear transformations as well as perspective projection, but in 2D games we only deal with the transformations.

.. note::

   Often I will contract -spaces into one word.  This is a bad habit of mine, there is no difference between world space and worldspace and you will see me use these interchangeably throughout the docs.

*Object Space*
    
    Object space or model space is space centered at an object's position.  Any points in object space are relative to that object's position.

    Object space is used by bounding polygons to stay attached to their object if it is moving through the game.

*World Space*
    
    Worldspace is the space as seen from the perspective of the game.  This is what most people think of when position is discussed.  Most of the game logic occurs in worldspace - collision detection, physics, and level geometry are all relative to worldspace.

    Worldspace is centered at the bottom left corner of of the world, unlike object space which is centered at the center of an object.

*Camera Space*

    Camera space or clipspace is what the user sees in the game window.  Before an object is drawn to the screen, it is transformed to the position and orientation of the Camera object, giving the camera space coordinates of that object.  This is how the world is able to move 'around' the player character; because the Camera is tied to the Player's worldspace position, and then everything is rendered to camera space.

    Camera space is centered at the worldspace position of the Camera object.

    Some interface elements, such as the pause menu and health bar are placed directly into camera space, because they do not move with the level.

.. _draw_space_translation:

Translating between draw-spaces
-------------------------------

*Object space to world space*

Simply add the object's object space coordinates to the worldspace coordinates of the object that owns the object space.

.. code-block:: python

   object_in_objectspace.worldspace_position = object_in_objectspace.objectspace_position + object_in_worldspace.worldspace_position

*World space to camera space*

This one is less intuitive.  Because camera space is centered in the middle of the window, and because drawing in OpenGL is centered at the bottom left like worldspace, we have to account for the window size in our translation.  So the calculation becomes:

.. code-block:: python
    
   #assume all objects are in worldspace
   object.cameraspace_position = object.worldspace_position - camera.worldspace_position + Position(WINDOW.width / 2, WINDOW.height / 2)



.. _broad_phase:

Broad-phase Collision Detection
-------------------------------

The methodology for broad-phase collision detection is as follows:

.. code-block:: python
   
   for object in object_list:
      for other_object in object_list not object and other_object.index > object.index:
         if distance(object, other_object) < object.speed + other_object.speed:
            #they're close enough to possibly collide
               possible_matches.add(collision(object, other_object))


.. _narrow_phase:

Narrow-phase Colision Detection using the Separating Axis Theorem
-----------------------------------------------------------------

The methodology for narrow-phase collision detection is as follows:

.. code-block:: python

   for match in possible_matches:
      collider = match.faster_object
      collidee = match.slower_object

      for axis in collidee:
         if axis.projection(collider) and axis.projection(collidee) do not overlap:
            #there is no collision here, since there is a separating axis
            return false

      #if this section of the code is reached, there is a collision because all axes overlap
      return true

