import os
from animation import Animation

class AnimationFactory(object):
    """
        Factory class that produces Animation objects given a set of parameters
    """

    def __init__(self, asset_path, spritesheets):
        #test the asset path (some inconsistency over directory structure)
        if not os.path.exists(asset_path):
            if asset_path[0] == '/':
                #strip the leading slash
                asset_path = asset_path[1:]
                if not os.path.exists(asset_path):
                    raise IOError("Asset path does not exist")
            else:
                #insert leading slash
                asset_path = '/'.join(asset_path)
                if not os.path.exists(asset_path):
                    raise IOError("Asset path does not exist")
        self.asset_path = asset_path

        print 'asset_path', self.asset_path

        #if the spritesheet is not a list, make it one
        if type(spritesheets) is not 'list':
            self.spritesheets = []
            self.spritesheets.append(spritesheets)
        else:
            self.spritesheets = spritesheets

    def makeAnimation(self, spritesheet, infosheet):
        """
            Generate and return an Animation
            ATM this leaves all the heavy lifting to Animation,
            but in the future the factory should handle all the calculation and
            make Animation just a data vessel
        """
        sprite = ''.join([self.asset_path, self.spritesheets[spritesheet]])
        info = ''.join([self.asset_path, infosheet])

        a = Animation(sprite, info)
        return a
