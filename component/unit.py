class Unit(object):

    ppu = 1

    @classmethod
    def toPixels(cls, units):
        return units * cls.ppu

    @classmethod
    def toUnits(cls, pixels):
        return pixels / cls.ppu
