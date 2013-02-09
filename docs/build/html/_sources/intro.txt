Introduction to Perseus
=======================

Project Perseus is a 2D platforming action-adventure game developed by Alien Swordfish Game Laboratories.  

The game is written in Python using the Pyglet OpenGL framework.  Planned platforms for the moment are Windows, Mac and Linux.  Future platform support is tentative.

The current version of the game is |release|.


Technical Elements
------------------

Perseus is designed around the Pyglet framework which includes a simple window manager, input listeners and bindings for OpenGL.  As such, most of the game elements are written from scratch.  The game loop features two main asynchronous cycles: the game cycle where game logic is handled, and the draw cycle where rendering is managed.  

The game cycle is configured to run at a fixed rate of 60 cycles per second for two reasons.  First, t was necessary for the physics and collision detection to synchronize and mesh correctly.  And second, the game logic is fairly calculation heavy and fixing it guarantees consistent behavior for complicated scenes and future updates.

The draw cycle is not bound by a fixed rate.  It is configured to run as fast as possible.  The main reason for this is because the game is developed for PC, it must be able to run on a variety of systems.  Separating the draw loop from game logic allows the game to behave consistently on all configurations, while letting the game take advantage of high-end computers to provide a high framerate and still giving players with low-end computers the same experience at a lower framerate.

Synchronising the draw and game cycles
--------------------------------------

Because the two cycles are decoupled, the draw cycle is only updated on every game loop update at a potentially very high framerate.  To solve this, we interpolate between cycle updates based on an object's current position and velocity.  This is an accurate enough estimate to insert frames between updates.


Phases of the game cycle
------------------------

During the running game state, the game cycle runs through several phases.

#. *Player Input*

   Checks for player input and applies the corresponding events to the game (moving the player, pausing the game, performing an action)

#. *Collision detection*
        
   See :ref:`collision_sequence` for information.

#. *Physics*

   All GameObject movement occurs here.  Any necessary physics updates, including gravity and other in-game forces, are applied here.


#. *Collision resolution*

   See :ref:`collision_sequence` for information.

