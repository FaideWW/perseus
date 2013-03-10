from collision.collision import BoundingPoly
from component.component import Position
import pyglet.image

class Map(object):
    def __init__(self, map_file, tilesheet, tile_data, tilesize):
        self.mapdata = self._readMapFile(map_file)
        self.tilesheet = tilesheet
        self.tiles = self._readTileData(tilesheet, tile_data)
        self.t_size = tilesize
        self.spawn = None
        self.map = self._genMap(self.mapdata, self.tiles)

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
                    data = [Position([int(i), int(j)]) for i,j in zip(data[::2], data[1::2])]
                data_array.append(data)
                tile_types.append(tiletype)
        tilesheet = pyglet.image.load(tilesheet)
        for tile in range(len(data_array)):
            x = data_array[tile][0]
            y = data_array[tile][1]
            w = data_array[tile][2]
            h = data_array[tile][3] 
            #print data_array[tile]
            tile_array[tile_types[tile]] = tilesheet.get_region(x,y,w-x,h-y)

        return tile_array

    def _genMap(self, mapdata, tiledata):
        map_array = [None] * len(mapdata)
        ident = 0

        #boundingpoly sizes
        bp_tl = Position([-self.t_size.x/2, -self.t_size.y/2])
        bp_tr = Position([self.t_size.x/2, -self.t_size.y/2])
        bp_br = Position([self.t_size.x/2, self.t_size.y/2])
        bp_bl = Position([-self.t_size.x/2, self.t_size.y/2])

        for y in range(len(mapdata)):
            map_array[y] = [None] * len(mapdata[y])
            for x in range(len(mapdata[y])):
                tilesprite = None
                bp = None
                if mapdata[y][x] in tiledata:
                    tilesprite = tiledata[mapdata[y][x]]
                    bp = BoundingPoly([bp_tl, bp_tr, bp_br, bp_bl])

                map_array[y][x] = Tile(ident, mapdata[y][x], tilesprite, bp)
                ident += 1
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
        return [tile.sprite for row in self.map for tile in row if tile.sprite]

    def mapAsSprite(self):
        #returns a large sprite of the map, textures and all
        map_w = max([len(row) for row in self.map]) * self.t_size.y
        map_h = len(self.map) * self.t_size.x
        tile_x = 0
        #tile_y starts at max and counts down because texture origin begins at the bottom
        tile_y = map_h - self.t_size.y
        #6048 = pyglet.gl.GL_RGBA
        map_image = pyglet.image.Texture.create(map_w, map_h, 6408, True)
        for row in range(len(self.map)):
            for tile_index in range(len(self.map[row])):
                tile = self.map[row][tile_index]
                if tile.sprite:
                    map_image.blit_into(pyglet.image.load(self.tilesheet), tile_x, tile_y, 0)
                tile_x += self.t_size.x
            tile_x = 0
            tile_y -= self.t_size.y

        return map_image

    def __str__(self):
        return str(self.map)

class Tile(object):
    def __init__(self, tileid, tiletype, sprite=None, boundingpoly=None):
        self.id = tileid
        self.type = tiletype
        self.sprite = sprite
        self.boundingpoly = boundingpoly

    def setTexture(self, texture_region):
        self.sprite = texture_region

    def getBoundingPoly(self):
        return self.boundingpoly