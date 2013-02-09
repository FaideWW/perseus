:mod:`map` --- Map and Tile operations
======================================

.. module:: map
   :synopsis: Handles reading and organizing level and tile data

.. sectionauthor:: cmcFaide <michael@faide.net>

The :mod:`map` module includes the :class:`Map` and :class:`Tile` classes, and is responsible for reading/parsing map files, and creating levels that the renderer and collider can use.

Map files are read top left to bottom right, and are oriented in the game in the same manner.

------

.. class:: Map(map_file, tilesheet, tile_data)

   Creates a :class:`Map` object based on the map data in ``map_file``.  The result is a 2-D array of :class:`Tile` objects, a set of tile dimensions (in worldspace) and a tilesheet. 

   ``tile_data`` is similar to ``region_data`` from :class:`Animation` in that it defines sections of ``tilesheet`` that correspond to particular tile types.

   .. method:: _readMapFile(map_file)

      Reads and parses the map file.  Returns a 2-D array of :class:`Tile` objects corresponding to the level geometry.

      .. note::

         Because the map file is read in backwards from worldspace coordinates, the array must be built from the top down.  At the end of each row of the map, ``array.insert(0, row)`` must be called instead of appending the row on the end of the array.
    
   .. method:: _readTileData(tilesheet, tile_data)

      Reads tile data and binds Sprites to each tile type.

   .. method:: getTile(position)
               getTile(tileID)

      Takes a worldspace position and returns the :class:`Tile` corresponding to that position, or ``None`` if the position is empty.

      Can also accept a tile ID.

   .. method:: getTileSize()

      Returns the worldpsace tile size of the level.

   .. method:: loadMap()

      Creates an array of Sprites that represents each tile on the map, and returns it for loading into the renderer.


.. class:: Tile(id, type[, boundingpoly=None])

   Creates a :class:`Tile` object with a unique ID and a type.  

   If the type is not zero, the Tile also has a bounding polygon assigned to it.

   .. method:: setTexture(type)

      Alters the texture for this individual tile.  This is used for creating secret areas or altering the look of particular maps.

   .. method:: getBoundingPoly()

      Returns the tile's bounding poly.