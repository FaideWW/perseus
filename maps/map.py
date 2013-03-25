import collision.collision as collision
import component.component as component
import component.unit as unit
import gameobject.gameobject as gameobject
import pyglet.image


class Map(object):
    def __init__(self, map_file, tilesheet, tile_data, tilesize):
        self.mapdata = self._readMapFile(map_file)
        self.tilesheet = tilesheet
        self.tiles = self._readTileData(tilesheet, tile_data)
        self.t_size = tilesize
        self.spawn = None
        self.num_tiles = 0
        self.map = self._genMap(self.mapdata, self.tiles)
        #self.weldTileVertices(self.map)

    def _readMapFile(self, map_file):
        map_array = []
        with open(map_file) as r:
            for line in r:
                map_array.append([x for x in list(line)])
        return map_array

    def _readTileData(self, tilesheet, tile_file):
        """
            Tile data:

            *:tl.x,tl.y,tr.x,tr.y,br.x,br.y,bl.x,bl.y
        """
        tile_array = {}
        data_array = []
        tile_types = []
        with open(tile_file) as r:
            for line in r:
                data = line.rstrip('\n').split(':')
                tiletype = data[0]
                data = data[1].rstrip('\n').split(',')
                if str(data[0]) == 'spawn':
                    self.spawn = str(data)
                    continue
                elif len(data) != 8:
                    raise TypeError('Tile data is invalid.')
                else:
                    data = [component.Position([int(i), int(j)]) for i, j in zip(data[::2], data[1::2])]
                data_array.append(data)
                tile_types.append(tiletype)
        tilesheet = pyglet.image.load(tilesheet)
        for tile in range(len(data_array)):
            x = data_array[tile][0]
            y = data_array[tile][1]
            w = data_array[tile][2]
            h = data_array[tile][3]
            #print data_array[tile]
            tile_array[tile_types[tile]] = tilesheet.get_region(x, y, w-x, h-y)

        return tile_array

    def _genMap(self, mapdata, tiledata):
        #offset to align tiles with the grid
        offset_x = float(self.t_size.x) / 2
        offset_y = float(self.t_size.y) / 2
        map_array = [None] * len(mapdata)
        ident = 0

        #boundingpoly sizes
        bp_tl = component.Position([-float(self.t_size.x)/2, -float(self.t_size.y)/2])
        bp_tr = component.Position([float(self.t_size.x)/2, -float(self.t_size.y)/2])
        bp_br = component.Position([float(self.t_size.x)/2, float(self.t_size.y)/2])
        bp_bl = component.Position([-float(self.t_size.x)/2, float(self.t_size.y)/2])
        map_height = len(mapdata) - 1

        for y in range(len(mapdata)):
            map_array[y] = [None] * len(mapdata[y])
            for x in range(len(mapdata[y])):
                tilesprite = None
                bp = None
                if mapdata[y][x] in tiledata:
                    tilesprite = tiledata[mapdata[y][x]]
                    bp = collision.BoundingPoly([bp_tl, bp_tr, bp_br, bp_bl])
                map_array[y][x] = Tile(ident, component.Vector([x + offset_x, (map_height - y) + offset_y]), mapdata[y][x], tilesprite, bp, size=self.t_size, collider=collision.StaticCollidable())
                ident += 1

        self.num_tiles = ident
        #loop through again and build edge data for each tile
        #for now we're treating all tiles as having four solid edges (no slopes or fancy bits)
        for y in range(len(mapdata)):
            for x in range(len(mapdata[y])):
                tile = map_array[y][x]
                #edges wind clockwise from north
                edges = []
                try:
                    if map_array[y+1][x] is not None:
                        edges.append(Tile.EDGE_SOLID)
                    else:
                        edges.append(Tile.EDGE_NONE)
                except IndexError:
                    #if we're on the outside of the map, give the tiles a solid edge
                    edges.append(Tile.EDGE_SOLID)

                try:
                    if map_array[y][x+1] is not None:
                        edges.append(Tile.EDGE_SOLID)
                    else:
                        edges.append(Tile.EDGE_NONE)
                except IndexError:
                    #if we're on the outside of the map, give the tiles a solid edge
                    edges.append(Tile.EDGE_SOLID)

                try:
                    if map_array[y-1][x] is not None:
                        edges.append(Tile.EDGE_SOLID)
                    else:
                        edges.append(Tile.EDGE_NONE)
                except IndexError:
                    #if we're on the outside of the map, give the tiles a solid edge
                    edges.append(Tile.EDGE_SOLID)

                try:
                    if map_array[y][x-1] is not None:
                        edges.append(Tile.EDGE_SOLID)
                    else:
                        edges.append(Tile.EDGE_NONE)
                except IndexError:
                    #if we're on the outside of the map, give the tiles a solid edge
                    edges.append(Tile.EDGE_SOLID)

                tile.setEdgeData(edges)

        return map_array

    def weldTileVertices(self, tilemap):
        """
            Finds tiles that share an edge and removes the edge from collision detection.

            This is incredibly broken atm, and I might take it out altogether
        """
        for row in range(len(tilemap)):
            for col in range(len(tilemap[row])):
                tile = tilemap[row][col]
                neighbors = self.getNeighbors(component.Vector([col, row]))

                for side in range(len(neighbors)):
                    neighbor = neighbors[side]
                    if neighbor is None:
                        continue
                    #set the neighboring side to opposite the tile's side
                    #NOTE: this only works for axis aligned quadrilaterals
                    #      (aka tiles) so don't try this for actual bounding polygons
                    neighbor_side = (side + 2) % 4
                    if tile.getEdgeData()[side] == Tile.EDGE_SOLID and neighbor.getEdgeData()[neighbor_side] == Tile.EDGE_SOLID:
                        #if the tile and its neighbor share a solid edge, dsiable them both
                        if tile.getBoundingPoly() is not None:
                            tile.getBoundingPoly().disableSide(side)
                        if neighbor.getBoundingPoly() is not None:
                            neighbor.getBoundingPoly().disableSide(neighbor_side)

                #this needs to be thought out

    def getNeighbors(self, tile_index):
        """
            returns a list of neighboring tiles given a Pair with the row and column
        """
        row = tile_index.x
        col = tile_index.y
        up, down, left, right = [True] * 4
        if row <= 0:
            up = False
        if row >= len(self.map) - 1:
            down = False
        if col == 0:
            left = False
        if up and down and col >= len(self.map[row]) - 1:
            right = False

        neighbor_list = []

        #up neighbor
        neighbor_list.append(None if not up else self.map[row-1][col])
        #right neighbor
        neighbor_list.append(None if not right else self.map[row][col+1])
        #down neighbor
        neighbor_list.append(None if not down else self.map[row+1][col])
        #left neighbor
        neighbor_list.append(None if not left else self.map[row][col-1])

        return neighbor_list

    def getTile(self, data):
        if isinstance(data, component.Position):
            #get a tile based on map coordinates
            row_index = int(data.y // self.t_size.y)
            col_index = int(data.x // self.t_size.x)

            return self.mapdata[row_index][col_index]

        elif isinstance(data, (int, long)):
            #get a tile based on index
            for x in self.map:
                if data >= len(x):
                    data = data - len(x)
                    continue
                else:
                    return x[data]
            #if we get here
            return None

    def getTileSize(self):
        return self.t_size

    def loadMap(self):
        return [tile.sprite for row in self.map for tile in row if tile.sprite]

    def mapAsSprite(self):
        p_size = unit.Unit.toPixels(self.t_size)
        #returns a large sprite of the map, textures and all
        map_w = max([len(row) for row in self.map]) * p_size.y
        map_h = len(self.map) * p_size.x
        tile_x = 0
        #tile_y starts at max and counts down because texture origin begins at the bottom
        tile_y = map_h - p_size.y
        #6048 = pyglet.gl.GL_RGBA
        map_image = pyglet.image.Texture.create(map_w, map_h, 6408, True)
        for row in range(len(self.map)):
            for tile_index in range(len(self.map[row])):
                tile = self.map[row][tile_index]
                if tile.sprite:
                    map_image.blit_into(pyglet.image.load(self.tilesheet), tile_x, tile_y, 0)
                tile_x += p_size.x
            tile_x = 0
            tile_y -= p_size.y

        return map_image

    def getTileList(self):
        return filter(None, [tile for row in self.map for tile in row])

    def getMapSize(self):
        return component.Vector([max([len(x) for x in self.map]), len(self.map)])

    def __str__(self):
        return str(self.map)


class Tile(gameobject.GameObject):

    #enumerate edge types
    EDGE_NONE = 0
    EDGE_SOLID = 1
    EDGE_INTERESTING = 2

    def __init__(self, tileid, position, tiletype, sprite=None, boundingpoly=None, **kwargs):
        self.id = tileid
        self.type = tiletype
        kwargs['position'] = position
        kwargs['id'] = 'map' + str(tileid)
        kwargs['sprite'] = sprite
        kwargs['boundingpoly'] = boundingpoly
        super(Tile, self).__init__(**kwargs)
        self.edge_data = []

    def setEdgeData(self, edge_data, edge_type=None):
        if edge_type is not None and len(edge_type) > edge_data:
            #set an individual edge
            self.edge_data[edge_data] = edge_type
        else:
            #set all edges
            self.edge_data = edge_data

    def getEdgeData(self):
        return self.edge_data

    def setTexture(self, texture_region):
        self.sprite = texture_region

    def getBoundingPoly(self):
        return self.boundingpoly

    def __str__(self):
        return 'Tile ' + str(self.id) + '[' + str(self.position.y) + ', ' + str(self.position.x) + ']'
