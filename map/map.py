from collision.collision import BoundingPoly

class Map(Object):
    def __init__(self, map_file, tilesheet, tile_data, tilesize):
        self.mapdata = self._readMapFile(map_file)
        self.tilesheet = tilesheet
        self.tiles = self._readTileData(tilesheet, tile_data, map_array)
        self.t_size = tilesize
        self.map = self._genMap(self.mapdata, self.tiles)

    def _readMapFile(self, map_file):
        map_array = []
        with open(map_file) as r:
            for line in r.readLines():
                map_array.append([x for x in list(line)])
        return map_array

    def _readTileData(self, tilesheet, tile_file):
        """
            Tile data:

            *:tl.x,tl.y,tr.x,tr.y,br.x,br.y,bl.x,bl.y
        """
        tile_array = {}
        with open(tile_file) as r:
            for line in r.readLines():
                data = line.rstrip('\n').split(':')
                tiletype = data[0]
                data = data[1].rstrip('\n').split(',')
                if len(data) != 8:
                    raise TypeError('Tile data is invalid.')
                data = [Position([int(i), int(j)]) for i,j in zip(data[::2], data[1::2])]
                data_array.append(data)

        tilesheet = pyglet.image.load(tilesheet)
        for tile_data in data_array:
            x = tile[0]
            y = tile[1]
            w = tile[2]
            h = tile[3] 

            tile_array[tiletype] = tilesheet.get_region(x,y,w-x,h-y)

        return tile_array

    def _genMap(self, mapdata, tiledata):
        map_array = []
        ident = 0

        #boundingpoly sizes
        bp_tl = Position(-self.t_size.x/2, -self.t_size.y/2)
        bp_tr = Position(self.t_size.x/2, -self.t_size.y/2)
        bp_br = Position(self.t_size.x/2, self.t_size.y/2)
        bp_bl = Position(-self.t_size.x/2, self.t_size.y/2)

        for y in range(len(mapdata)):
            for x in range(len(y)):
                if mapdata[y][x] in tiledata:
                    bp = BoundingPoly([bp_tl, bp_tr, bp_br, bp_bl])
                    map_array[y][x] = Tile(ident, mapdata[y][x], tiledata[mapdata[y][x]], bp)

                ident = ident + 1

        return map_array

    def getTile(data):
        if isinstance(data, Position):
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
        return [[tile.sprite for tile in self.map[row]] for row in self.map]

class Tile(Object):
    def __init__(self, tileid, tiletype, sprite=None, boundingpoly=None):
        self.id = tileid
        self.type = tiletype
        self.sprite = sprite
        self.boundingpoly = boundingpoly

    def setTexture(self, texture_region):
        self.sprite = texture_region

    def getBoundingPoly(self):
        return self.boundingpoly