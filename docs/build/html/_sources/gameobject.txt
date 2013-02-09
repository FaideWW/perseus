:mod:`gameobject` --- GameObjects
=================================

.. module:: gameobject
   :synopsis: Models every object that has a presence or position in worldspace

.. sectionauthor:: cmcFaide <michael@faide.net>

The :mod:`gameobject` module contains the unifying GameObject class that every element in the game is based on.  If an object has a position in worldspace, or is drawn to the screen based on its position in worldspace, it extends this class.  :class:`GameObject` provides the base functionality for an object to exist in Perseus.

In future iterations, :class:`GameObject` will include functionality for health.

------

.. class:: GameObject(id, position[, sprite=None])
           GameObject(id, position, boundingpoly, collider[, sprite=None])
           GameObject(id, position, boundingpoly, type[, sprite=None])
   :module: gameobject

   Creates an empty GameObject shell that has a presence in worldspace.

   GameObjects are identified to most systems by their ``id``

   GameObjects that participate in collision detection must declare a type (by default this behavior is disabled), or include a custom collider.

   If a sprite is declared, 

   .. method:: addGLObject(GLObject)

      Ties a :class:`GLObject` to this GameObject, which will be drawn at the position of the GameObject.

   .. method:: getRenderables()

      If the GameObject has either a Sprite or a :class:`GLObject` or both, this returns a list of all the renderable objects tied to it.

   .. method:: accelerate(acc)

      Adds acceleration to the acceleration vector.

   .. method:: stopAcceleration()

      Sets the acceleration vector to zero.

   .. method:: setVelocity(vel)

      Erases the existing velocity vector and replaces it with ``vel``.

   .. method:: getWorldSpacePosition()

      Returns the worldspace position of the GameObject.

   .. method:: getVelocity()

      Returns the velocity of the GameObject.

   .. method:: getBoundingPoly()

      Returns the bounding polygon for this GameObject.

   .. method:: addVelocity(rel_vel)

      Adds ``rel_vel`` to the velocity vector.

      .. note::

         This is distinct from :meth:`accelerate` in that :meth:`accelerate` is bound by game time.  :meth:`addVelocity` will instantaneously change the velocity of the GameObject. :meth:`accelerate` will change the velocity over a period of 1 second.  Not sure if both of these will be needed, but it's nice to have both.

   .. method:: setFlags(flag_data)

      Sets instance-specific flags for a particular GameObject.  This will be expanded upon in later iterations.

   .. method:: update(dt)

      ``acceleration * dt`` is added to ``velocity``.

      ``velocity * dt`` is added to ``position``.

      General purpose update method.  Subclasses will extend this if they need to.
