:mod:`component` --- List and Vector Components
===============================================

.. module:: component
   :synopsis: Includes various classes that are core to the game but do not fit in any other modules.

.. sectionauthor:: cmcFaide <michael@faide.net>

Components include the Vector class, Position class, and various other compatibility classes to work with OpenGL.

Vector operations
-----------------

.. class:: Vector(num_list)

   Creates a collection of ``n`` numbers that represent a position in ``n``-space.

   .. method:: dot(other)

      Returns the dot product of two vectors.

      If the two vectors are not in the same space, raises an ``InvalidComparisonException``.

   .. method:: cross(other)

      Returns the cross product of two vectors.

      If the two vectors are not in the same space, raises an ``InvalidComparisonException``.

   .. method:: rot(angle)

      Rotates the current :class:`Vector` about the z-axis.

   .. method:: mag()

      Retuns the magnitude of the :class:`Vector`.

   .. method:: normalize()

      Returns a :class:`Vector` of magnitude 1 with the same direction.

   .. method:: project(axis)

      Returns a 1D projection of the :class:`Vector` onto ``axis``.

   .. method:: isParallel(vector)

      Returns ``True`` if the two vectors have the same direction.

   .. py:staticmethod:: zero()

      Returns the zero vector in 3-space.

.. class:: Pair(Vector)

   Creates a Vector in 2-space.  Pair extends all the methods from :class:`Vector`, but will only operate against other Pairs.  Any other comparison will throw a ``TypeError`` exception.

.. class:: Position(Pair)

   Creates a Pair that represents an object's position in a space.  

   :class:`Position` will operate against other :class:`Position` objects as well as :class:`Velocity` objects.

.. class:: Velocity(Pair)

   Creates a Pair that represents the rate of movement in a space with respect to time.

   To prevent redundancy, :class:`Velocity` objects also represent acceleration.

   :class:`Velocity` will operate on objects of the same type.  Comparing against other types will throw a ``TypeError`` exception.

