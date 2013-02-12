:mod:`camera` --- Camera operations
===================================

.. module:: camera
   :synopsis: Represents the perspective of the player in the gameworld.

.. sectionauthor:: cmcFaide <michael@faide.net>

The camera is the in-game representation of the user's perspective.  :class:`Camera` consists of a world-space position, and a viewport size.  :class:`Camera` is responsible for the world-space to clip-space transformation as well.

Camera extends :class:`GameObject` but does not have a physical presence in the game.  This makes it easy to move the Camera around the map while following another :class:`GameObject`

------

.. class:: Camera(viewport[, target=None])

   Creates a Camera object with a worldspace viewport size.   If no target is specified, the Camera is positioned at (map.width / 2, map.height / 2), in the middle of the map.

   There are two transition variables to track: ``target_transition`` and ``viewport_transition``.  These determine the delay with which the camera performs its translate and scale operations. 

   .. method:: setTarget(target[, transition=0])

      Changes targets.  If ``transition`` is not 0, the camera smoothly scrolls to the new target in ``transition`` milliseconds.

   .. method:: zoom(new_viewport[, transition=0])

      Changes the viewport size.  If ``transition`` is not 0, the zoom effect takes ``transition`` milliseconds.

   .. method:: toClipSpace()

      Returns the translation of the worldspace origin to this camera's clipspace. See :ref:`draw_space_translation` for more information.

   .. method:: update(dt)

      Sets position relative to the target, or if ``target_transition`` is greater than 0, interpolates the position along the separating vector based on dt, then subtracts dt from ``target_transition``.

      If ``viewport_transition`` is greater than 0, interpolates the scale between the source and destination sizes based on dt, then subtracts dt from ``viewport_transition``.

    