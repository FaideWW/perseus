:mod:`player` --- Player Character
==================================

.. module:: player
   :synopsis: The player character

.. sectionauthor:: cmcFaide <michael@faide.net>

The :mod:`player` module contains the :class:`Player` class.

:class:`Player` extends the :class:`GameObject` class.  It adds functionality for the moveset available to the player character, as well as a state manager for handling input from the user.

In future iterations, :class:`Player` will include game state handles for pausing and game over screens. 

Managing State
--------------

The movement set of the player character is quite complex.  In order to keep everything straight, :class:`Player` tracks the current movement being performed in a state called the movement state.  There are 10 available movement states:

+----------+--------------------------------------------------------------------+
|State name|Description                                                         |
+==========+====================================================================+
|*IDLE*    |Active whenever there is no movement.                               |
+----------+--------------------------------------------------------------------+
|*RUN*     |Active whenever x-movement is not zero and y-movement is zero and   |
|          |no modifiers are active.                                            |
+----------+--------------------------------------------------------------------+
|*SPRINT*  |Active when the sprint modifier is active during the *RUN* state.   |
+----------+--------------------------------------------------------------------+
|*CROUCH*  |Active when the down modifier is active during either *IDLE*        |
|          |or *RUN*.                                                           |
+----------+--------------------------------------------------------------------+
|*SLIDE*   |Active when the down modifier is activated AFTER the sprint modifier|
|          |is activated.                                                       |
+----------+--------------------------------------------------------------------+
|*AIRONE*  |Active when y-movement is not zero.                                 |
+----------+--------------------------------------------------------------------+
|*AIRTWO*  |Active when the jump key is pressed from the *AIRONE* state.        |
+----------+--------------------------------------------------------------------+
|*LAND*    |Active immediately after *AIRONE* or *AIRTWO* becomes *RUN*.        |
+----------+--------------------------------------------------------------------+
|*ROLL*    |Active when the down modifier is active during the *LAND* state.    |
+----------+--------------------------------------------------------------------+
|*HIDDEN*  |Active when the stealth modifier is active from a hiding spot.      |
|          |(stealth is not covered in this version of the game)                |
+----------+--------------------------------------------------------------------+

------


.. class:: Player(GameObject)
   :module: player

   Creates a player character instance.

   Default movement state is *IDLE*

   .. method:: getMovementState()

      Returns the current movement state.

   .. method:: checkState()

      Checks the player's surroundings to see if a state change is necessary.

      The following is a list of automatic state changes to check for:

      * When the player has stopped moving in both the x and y directions, set the state to *IDLE*.
      * If the player has no ground beneath them and is NOT in *AIRONE* or *AIRTWO*, set the state to *AIRONE*.
      * If the player is in *AIRONE* or *AIRTWO* but has ground beneath them and no y-movement, set the state to *LAND*.
      * If the player is in *LAND* and enough time has passed that the player cannot roll anymore, set the state appropriately.
      * If the player is in *ROLL* and enough time has passed that the roll has been completed, set the state appropriately.

   .. method:: left()

      Moves in the negative x-direction at a pre-determined speed.

      Sets the movement state to *RUN*.

      .. note::

         For the sake of clarity, *moving* refers to setting the velocity to a particular value.  

   .. method:: right()

      Moves in the positive x-direction at a pre-determined speed.

      Sets the movement state to *RUN*.

   .. method:: sprint )

      If the current state is *RUN*, increases the speed of movement in the direction of motion by a factor.

      Sets the movement state to *SPRINT*.

   .. method:: down()

      If the current state is *RUN* or *IDLE*, crouches the player and sets the state to *CROUCH*.

      If the current state is *SPRINT*, puts the player into a slide animation and sets the state to *SLIDE*.

      If the current state is *LAND*, puts the player into a roll and sets the state to *ROLL*.

   .. method:: up()

      If the current state is *IDLE*, *RUN* or *SPRINT*, the player will jump and set the state to *AIRONE*.

      If the current state is *ROLL*, the player will jump (higher than normal) and set the state to *AIRONE*.

      If the current state is *AIRONE*, the player will jump for a second time and set the state to *AIRTWO*.

   .. method:: stop()

      Stops horizontal movement.