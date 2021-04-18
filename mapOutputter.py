PATH = '\033[92m'
HEAT = '\033[91m'
WALL = '\033[95m'
MAGNET = '\033[94m'

END = '\033[0m'
BOLD = '\033[1m'

class MapOutputter:
    def __init__(self, robot):
        self.x = []
        self.y = []

        for x in range(36):
            self.x.append(0)
        for y in range(36):
            self.y.append(0)

    def Wall(self):
        for x in range(10):
            print(MapOutputter.BOLD + "X" + MapOutputter.END)

    def Path(self):
        print(MapOutputter.PATH + "X" + MapOutputter.END)

    def Magnet(self):
        print(MapOutputter.MAGNET + MapOutputter.BOLD + "X" + MapOutputter.END)

    def Heat(self):
        print(MapOutputter.HEAT + MapOutputter.BOLD + "X" + MapOutputter.END)

    printMap(self):

mapOutputter = MapOutputter()
mapOutputter.Wall()
mapOutputter.Path()
mapOutputter.Magnet()
mapOutputter.Heat()