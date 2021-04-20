PATH = '\033[92m'
HEAT = '\033[91m'
WALL = '\033[95m'
MAGNET = '\033[94m'

END = '\033[0m'
BOLD = '\033[1m'

class MapOutputter:
    def __init__(self):
        self.x = []
        self.y = []

        for x in range(36):
            self.x.append(0)
        for y in range(36):
            self.y.append(0)

    def Wall(self):
        for x in range(10):
            print(BOLD + "X" + END)

    def Path(self):
        print(PATH + "|" + END)

    def Magnet(self):
        print(MAGNET + BOLD + "1" + END)

    def Heat(self):
        print(HEAT + BOLD + "2" + END)

    # printMap(self):

mapOutputter = MapOutputter()
mapOutputter.Wall()
mapOutputter.Path()
mapOutputter.Magnet()
mapOutputter.Heat()