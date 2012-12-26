import sys

class Tile(object):
	def __init__(self, tiletype, char):
		self.tiletype = tiletype
		self.char = char

	def defineCollisionType(collider):
		self.collision = collider

	def __str__(self):
		return self.char

class TileRenderer(object):
	def __init__(self):
		pass

class Map(object):
	def __init__(self, mapFile):
		""" Takes the name of the map without extension, to read both .map and .td files """
		#read the data into map format
		self.mapData = []
		dotMap = mapFile + '.map'
		dotTD = mapFile + '.td'
		self.tileDict = self.__bindTileDictionary_(dotTD)
		self.mapData = self.__createMapArray_(dotMap, self.tileDict)

		self.height = len(self.mapData)
		self.width = len(max(self.mapData, key=len))

	def getMap(self):
		pass

	def __createMapArray_(self, mapF, tileMap):
		mapData = []
		cur_line = 0
		with open(mapF) as fileData:
			for line in fileData.readlines():
				mapData.append([])
				for char in line:
					if char == '\n':
						continue
					t = Tile(tileMap[char], char)
					mapData[cur_line].append(t)
				cur_line += 1

		return mapData

	def __bindTileDictionary_(self, tileF):
		""" Binds tile types to map characters for engine comprehension """
		tileDict = {}
		with open(tileF) as tileData:
			for line in tileData.readlines():
				char = line[:1]
				tiletype = line[2:]
				tileDict[char] = tiletype
		return tileDict

	def __str__(self):
		s = ''
		for line in self.mapData:
			for tile in line:
				s += str(tile)
			s += '\n'

		return s

path = '/'.join(sys.argv[0].rsplit('/')[:-1])
m = Map(path + '/map1')
print m.width, m.height
print m
