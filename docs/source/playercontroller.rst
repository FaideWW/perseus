:mod:`playercontroller` --- PlayerController
============================================

.. module:: playercontroller
   :synopsis: Handles input that directly controls the player character in game.

.. sectionauthor:: cmcFaide <michael@faide.net>

The :class:`PlayerController` is the interface between Pyglet's input events and the player character's actions in game.  :class:`PlayerController` provides an abstraction for the controls that allows keys to be rebound without having adverse or unintended effects on the game.

:class:`PlayerControllers` have a one-to-one relationship with :class:`Player` objects.  

------

.. class:: PlayerController(player)
   
   Creates an instance of the controller that is bound to a :class:`Player` object. 



   .. method:: bindKeys(key_config)

      Takes a key configuration file and maps each action to a particular key.

   .. method:: keyDown(key)

      Accepts a key press.  If the key is mapped to an action and isn't already on the list of pressed keys, then perform that action.

      Adds the key to the list of pressed keys.

   .. method:: keyUp(key)

      If the key release is mapped to an action, perform that action.

      Removes the key from the list of pressed keys.


   .. method:: leftPress()
   
      Calls ``Player.left()``

   .. method:: rightPress()

      Calls ``Player.right()``

   .. method:: upPress()

      Calls ``Player.up()``

   .. method:: downPress()

      Calls ``Player.down()``

   .. method:: leftRelease()

      If both left and right keys are unpressed, calls ``Player.stop()``

   .. method:: rightRelease()

      If both left and right keys are unpressed, calls ``Player.stop()``


------

.. note:: 

   The following is not included in the current version.  It was originally planned for this release but was cut to save time.  It will be included in the future.

.. class:: KeyCombination(key_combination, mapping[, ordered=True[, exclusive=True]])

   Creates a set of keys that when pressed in combination, performs a particular action as defined by mapping.


   .. method:: isEqual(key_list)

      Tests a key press combination (formatted as a list) for equivalency.  

      A combination is equivalent if:

      * If ``ordered`` is ``True``, the lists in the same order.
      * If ``ordered`` is ``False``, every element in ``key_list`` is found in the :class:`KeyCombination`

      AND

      * If ``exclusive`` is ``True``, ``key_list`` contains only the elements found in the combination


      Returns ``True`` if the sequence is equivalent, or ``False`` if not.


.. class:: KeySequence(key_sequence, mapping)

   Creates a set of keys that when typed in sequence, performs a particular action.

   .. method:: isEqual(key_list)

      Tests a key sequence for equivalency.

      A sequence is equivalent if and only if the two lists are exactly equal.



.. For next release - 
   Look into trees to store lots of key sequences.