PATH = '\033[92m'
HEAT = '\033[91m'
WALL = '\033[95m'
MAGNET = '\033[94m'

END = '\033[0m'
BOLD = '\033[1m'

class MapOutputter:
    def __init__(self, robot, length, width):
        self.robot = robot
        self.length = length
        self.width = width
        pointList = {}

    def setWall(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':0})

    def Wall(self):
        print(BOLD + "0" + END)

    def setPath(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':1})

    def Path(self):
        print(PATH + "1" + END)

    def setOrigin(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':5})

    def Origin(self):
        print(PATH + "5" + END)

    def setExit(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':4})

    def Exit(self):
        print(PATH + "4" + END)

    def setMagnet(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':3})

    def Magnet(self):
        print(MAGNET + BOLD + "3" + END)

    def setHeat(self, x, y):
        pointList.append({'x':x, 'y':y, 'value':2})

    def Heat(self):
        print(HEAT + BOLD + "2" + END)