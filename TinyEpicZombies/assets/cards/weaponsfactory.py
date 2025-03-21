from .weapons import Crowbar, golfClub

class WeaponsFactory:
    def __init__(self):

        self._fMap = { # for use with deserialisation
            "crowbar": self.__returnCrowbar(),
            "golfClub": self.__returnGolfClub()
        }

    def __returnCrowbar(self):
        return Crowbar()
    
    def __returnGolfClub(self):
        return golfClub()
    
    def returnWeapon(self, weapon):
        return self._fMap[weapon]