import curses
import threading

PATH = '\033[92m'
HEAT = '\033[91m'
WALL = '\033[95m'
MAGNET = '\033[94m'

END = '\033[0m'
BOLD = '\033[1m'

class MapOutputter:
    def __init__(self, robot, length, width):
        self.screen = curses.initscr()
        self.screen.nodelay(True)
        self.screen.keypad(True)

        self.robot = robot
        self.length = length
        self.width = width
        self.pointList = {}
        self.pointId = 0

        self.mapNumber = input("Which map number? : ")

        self.printMapThread = threading.Thread(target=self.printMap, args=(), daemon=True)
        self.printMapThread.start()

    def setWall(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':0})
        self.pointId += 1

    def Wall(self):
        print(BOLD + "0" + END)

    def setPath(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':1})
        self.pointId += 1

    def Path(self):
        print(PATH + "1" + END)

    def setOrigin(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':5})
        self.pointId += 1

    def Origin(self):
        print(PATH + "5" + END)

    def setExit(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':4})
        self.pointId += 1

    def Exit(self):
        print(PATH + "4" + END)

    def setMagnet(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':3})
        self.pointId += 1

    def Magnet(self):
        print(MAGNET + BOLD + "3" + END)

    def setHeat(self, x, y):
        self.pointList[self.pointId] = ({'x':x, 'y':y, 'value':2})
        self.pointId += 1

    def Heat(self):
        print(HEAT + BOLD + "2" + END)

    def printMap(self):
        # Team #
        # Map #
        # Unit Length
        # Unit
        # Origin
        # Notes
        #Map
        while True:
            try:
                self.screen.addstr(0,0,"Team: 68")
                self.screen.addstr(1,0,"Map: " + self.mapNumber)
                self.screen.addstr(2,0,"Unit Length: ")
                self.screen.addstr(3,0,"Unit: cm")
                self.screen.addstr(4,0,"Origin: ")
                self.screen.addstr(5,0,"Notes: ")

                # ACTUAL MAP
                self.screen.addstr(7,0, self.pointList)

                self.textScreen.clrtoeol()
                self.textScreen.refresh()
            except Exception as err:
                print(err)
