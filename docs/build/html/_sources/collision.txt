:mod:`collision` --- Collision Operations
=========================================

.. module:: collision
   :synopsis: Mechanics and behaviors of GameObjects during and after collisions

.. sectionauthor:: cmcFaide <michael@faide.net>

The :mod:`collision` module handles collision detection and behavior for GameObjects.


.. _collision_sequence:

The Collision Sequence
----------------------

The collision sequence contains two phases that occur on either side of the physics update.

The first phase is **collision detection**.  During this phase, GameObjects are polled for position and velocity, and those properties are compared to determine if any paths collide with each other.  If they do collide, the collision is added to the collision queue to be processed after the physics update.

The second phase is **collision resolution**.  During this phase, each collision in the collision queue goes through the following steps:

#. Determine the direction of collision.
#. Set each object back to a position where they are no longer considered colliding. (Maintain velocity)
#. Each object involved has the collision flag triggered in its internal state (used for falling platforms, damage, etc).
#. Fetch the collision behavior for each object. 
#. Perform the collision behavior transformations on the objects. (Knockback, bounce, static)
#. Remove the collision from the queue and repeat.

------

.. class:: Collider()
   :module: collision

   Creates a collider class which performs collision detection and resolution during the collision sequence.

   .. method:: detectCollisions(objects)

      Takes a list of game objects and performs broad-phase collision (via quadtrees) to find possible matches.  The list of possible matches then each undergoes narrow-phase collision (via the separating axis theorem) to find confirmed collisions.  Any confirmed collisions are then added to the collision queue.

      .. note::

         The collision queue is a unique set.  All collisions should only occur once per game tick.  The broad-phase sorting technique used solves any possible duplication errors by only comparing objects of a higher index in the list (see :ref:`broad_phase`)


   .. method:: _broadPhase(objects)
      
      Performs broad-phase cllision detection on a list of objects.  Returns a list of possible collisions for narrow-phase detection.

      See :ref:`broad_phase` for a detailed description of how broad-phase collision detection is performed.

   .. method:: _narrowPhase(possible_collisions)

      Performs narrow-phase collision detection on a list of possible collisions.

      See :ref:`narrow_phase` for a detailed description of how narrow-phase collision detection is performed.

   .. method:: resolveCollisions(collisions)

      Takes a list of colliding objects, and based on their collision behavior, performs a transformation on their game state. 

------

.. class:: ObjectCollision(GameObject, GameObject)
   :module: collision

   Holds two objects that are currently colliding, to be resolved.

   .. method:: compare(ObjectCollision)

      Determines if two :class:`ObjectCollision` objects are the same.  If an :class:`ObjectCollision` has the same :class:`GameObject` items regardless of their order, it is considered equivalent.


.. class:: BoundingPoly(vertices)
   :module: collision

   Creates a bounding polygon for use in collision detection.  The bounding box constructor takes a list of vertices (Positions in object space), and produces a polygon that represents that object's physical borders in the game.

   .. method:: getVertices()

      Returns the vertex list.

   .. method:: getAxes()

      Returns a list of axes normal to the faces of the polygon for use in the collision detection algorithm.

   .. method:: project(axis)

      Projects the polygon onto ``axis`` using vector projection.  Returns a pair of numbers that represent the endpoints of the projection.

Checking for Collisions - the Separating Axis Theorem
-----------------------------------------------------

When two objects are selected for narrow-phase detection, their bounding boxes undergo an algorithm to check if they are intersecting.  The algorithm uses the Separating Axis Theorem to determine if there is any overlap between the two boxes.  If there is, they are considered colliding.

The separating axis theorem states that if there exists an axis for which the projections of two objects *do not overlap*, then they do not intersect.  

The theorem operates on the assumption that non-collisions are much more likely than collisions, and therefore it is much faster to determine that there is no collision than it is to determine that there is one, especially for polygons with complex shapes.

There are a few drawbacks of this algorithm.  First, collision between simple shapes (axis aligned bounding boxes or bounding circles for example) can be resolved in a simpler and faster manner.  This algorithm works best on geometry and polygons with many sides.  Second, the SAT does not work on polygons with concave facets.  Crescent shapes will give false positives on collisions if an object is inside the crescent.  This is a limitation of the method, and so in future iterations we will have to either update the method or make it a design limitation to not include concave polygons.
   

Resolving Collisions
--------------------

Collisions are resolved in two parts.  The first is a game state update to both objects as a function of the other object's type.  A gameobject may have a specific reaction to a particular object type (for example, entities take damage from projectiles).  This is best handled by a collision component specific to the object.  If the first part returns a collision type, the collision continues.  The second is mechanical transformation; this consists entirely of all velocity changes (speed and direction).  This can be handled by the general collider. 

The following is a list of the object types that currently exist in Perseus:

+---------------+-----------------------------------------------------------------------+
|GameObject type| Description                                                           |
+===============+=======================================================================+
| Entity        | Any living being in the game world.                                   |
+---------------+-----------------------------------------------------------------------+
| Hostile       | Enemy entity.                                                         |
+---------------+-----------------------------------------------------------------------+
| Player        | Extends from the Entity class but with special constructs for handling|
|               | player input and game state links.                                    |
+---------------+-----------------------------------------------------------------------+
| Static        | An immutable piece of the world.  A common example is level geometry. |
+---------------+-----------------------------------------------------------------------+
| Trigger       | An object that when activated has some effect on the gameworld.       |
+---------------+-----------------------------------------------------------------------+
| Attack        | Temporary collision block that appears when an attack is being        |
|               | performed that outlines the hit detection of the move.                |
+---------------+-----------------------------------------------------------------------+
| Projectile    | Similar to an attack but moves through the world independent of its   |
|               | origin.  Is almost always destroyed after collision.                  |
+---------------+-----------------------------------------------------------------------+

The following is the corresponding list of physical transformation types in Perseus:

+---------------+----------------------------------------------------------------------------------------------+
|Collision type | Description                                                                                  |
+===============+==============================================================================================+
|Bounce         | Reflects the object along the axis of collision.                                             |
+---------------+----------------------------------------------------------------------------------------------+
|Stop           | Stops movement along collision normal axis.                                                  |
+---------------+----------------------------------------------------------------------------------------------+
|StopAll        | Stops all movement in all directions.                                                        |
+---------------+----------------------------------------------------------------------------------------------+
|Knockback      | Pushes the colliding entity in the direction opposite of the collision and slightly upwards. |
+---------------+----------------------------------------------------------------------------------------------+
|Slow           | Slows the offending object to a fraction of its current speed, but maintains direction.      |
+---------------+----------------------------------------------------------------------------------------------+


Collidable Objects
------------------

All gameobjects that interact with collision detection have a Collidable component that inherits from the :class:`Collidable` interface.

------

.. class:: Collidable()
   :module: collision

   This is an interface class for extending the behavior of a particular gameobject type during a collision beyond a physical transformation.  

   .. method:: getType()

      Returns the GameObject type from one of the choices in the table above.

   .. method:: collideWith(type)

      Updates game state based on the type of object with which the collision occurred.

      :meth:`collideWith` will return a collision type if it exists, or ``None`` if the collision should stop.



Collidable has the following subclasses:

.. class:: EntityCollidable()
   :module: collision

   Handles collisions involving Entities.

   .. method:: getType()

      Returns ``Entity``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors the Entity will inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``,   | None.  Entities may pass through without consequence.                                      |``None``     |
      | ``Trigger``   |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Hostile``,  | Entities will take damage and trigger either a fight or flight response.                   |``Knockback``|
      | ``Attack``,   |                                                                                            |             |
      | ``Projectile``|                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | Entities have no special interaction with static geometry.                                 |``Stop``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+

.. class:: HostileCollidable()
   :module: collision

   Handles collisions involving Hostiles.

   .. method:: getType()

      Returns ``Hostile``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors the Hostile will inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``,   | None.  Hostiles may pass through without consequence.                                      |``None``     |
      | ``Hostile``,  |                                                                                            |             |
      | ``Player``,   |                                                                                            |             |
      | ``Trigger``   |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Attack``,   | Hostiles will take damage.                                                                 |``None``     |
      | ``Projectile``|                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | Entities have no special interaction with static geometry.                                 |``Stop``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+

.. class:: PlayerCollidable()
   :module: collision

   Handles collisions involving the player character.

   .. method:: getType()

      Returns ``Player``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors the Player will inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``    | None.  Players may pass through without consequence.                                       |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Hostile``   | Players take damage from colliding with hostiles.                                          |``Knockback``|
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Trigger``   | None.  Players may pass through triggers without consequence.                              |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Attack``,   | Players take damage from attacks and projectiles.                                          |``Knockback``|
      | ``Projectile``|                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | Players have no special interaction with static geometry.                                  |``Stop``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+

      .. note::

         There can only be one Player in the gameworld at a specific time.  This is due to the way Player state is tied to game state (when a Player's health reaches 0, the game state changes).
   
.. class:: TriggerCollidable()
   :module: collision

   Handles collisions involving game triggers.  These include levers, pressure plates, invisible 'cutscene' triggers, etc.
   Triggers will almost always be the collidee in the case of a collision.

   .. method:: getType()

      Returns ``Trigger``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors a trigger inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``    | None.  Entities may pass through triggers without consequence.                             |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Hostile``   | None.  Hostiles may pass through triggers without consequence.                             |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Player``    | Colliding with a player will cause the trigger to activate and then be destroyed.          |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Trigger``   | None.  Triggers can pass through each other without consequence.                           |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Attack``,   | Depending on the trigger, some projectiles and attacks will cause the                      |``None``     |
      | ``Projectile``| trigger to actiavte and then be destroyed.                                                 |             |
      |               |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | None.  Triggers can pass through static geometry without consequence.                      |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
   
.. class:: AttackCollidable()
   :module: collision

   Handles collisions involving attacks.  Attack objects are invisible hitboxes around weapons during an attack state.  They do not physically collide with any objects, but entities will take damage from an attack.

   .. method:: getType()

      Returns ``Entity``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors the attack will inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``,   | Depending on the attack, the damage modifier may decrease by a factor when                 |``None``     |
      | ``Hostile``   | colliding with an Entity.                                                                  |             |
      | ``Player``    |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Trigger``   | None.  Attacks will pass through triggers without consequence.                             |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Attack``    | Depending on the attack (and the attacker), some attacks will be parried/cancelled out     |``None``     |
      |               | by each other.                                                                             |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Projectile``| None.  Attacks will knock projectiles away but will not be affected.                       |``None``     |
      |               |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | None.  Attacks can pass through static geometry without consequence.                       |``None``     |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
   
   
.. class:: ProjectileCollidable()
   :module: collision

   Handles collisions involving projectiles.  Projectile collisions are the most complex of the available gameobjects, because they have the most interactions with other objects.

   .. method:: getType()

      Returns ``Projectile``.

   .. method:: collideWith(type)

      Handles collisions with each of the other GameObject types.

      The following is a list of collision behaviors the projectile will inherit when it collides with a particular GameObject:

      +---------------+--------------------------------------------------------------------------------------------+-------------+
      |GameObject type|Description                                                                                 | Returns     |   
      +===============+============================================================================================+=============+
      | ``Entity``,   | Upon colliding with an Entity, the projectile will be destroyed.                           |``StopAll``  |
      | ``Hostile``   |                                                                                            |             |
      | ``Player``    |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Trigger``   | Upon colliding with a trigger, the projectile will be destroyed.                           |``StopAll``  |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Attack``    | Depending on the attack (and the attacker), some projectiles will be knocked away by an    |``Knockback``|
      |               | attack that is timed correctly.                                                            |             |  
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Projectile``| Two projectiles will reflect off of each other.                                            |``Bounce``   |
      |               |                                                                                            |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
      | ``Static``    | Depending on the projectile, colliding with static geometry will cause the projectile      |``StopAll``  |
      |               | to stop and lodge itself in the level, or be destroyed.                                    |             |
      +---------------+--------------------------------------------------------------------------------------------+-------------+
   

.. class:: StaticCollider()
   :module: collision

   Handles collisions involving static geometry.  Static objects do not have any special behaviors in this iteration of the game, but this is here for the future when falling blocks/other special case level elements are added.

   .. method:: getType()

      Returns ``Static``.

   .. method:: collideWith(type)

      Handles collisions.  

      Static objects will always return ``None``.




