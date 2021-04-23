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
        self.mapNumber = input("Which map number? : ")

        self.screen = curses.initscr()
        self.screen.nodelay(True)
        self.screen.keypad(True)

        self.robot = robot
        self.length = length
        self.width = width
        self.pointList = []

        self.printMapThread = threading.Thread(target=self.printMap, args=(), daemon=True)
        self.printMapThread.start()

    def setWall(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Wall()})

    def Wall(self):
        return BOLD + "0" + END

    def setPath(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Path()})

    def Path(self):
        return PATH + "1" + END

    def setOrigin(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Origin()})

    def Origin(self):
        return PATH + "5" + END

    def setExit(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Exit()})

    def Exit(self):
        return PATH + "4" + END

    def setMagnet(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Magnet()})

    def Magnet(self):
        return MAGNET + BOLD + "3" + END

    def setHeat(self, x, y):
        self.pointList.append({'x':x, 'y':y, 'paintStr':self.Heat()})

    def Heat(self):
        return HEAT + BOLD + "2" + END

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
                seq = [x['x'] for x in self.pointList]
                maxX = max(seq)
                seq = [y['y'] for y in self.pointList]
                maxY = max(seq)
                if maxX != 0 and maxY != 0:
                    for point in self.pointList:
                        self.screen.addstr(6,0,str(int((point['x']/maxX)*self.length)))
                        #self.screen.addstr(int((point['x']/maxX)*self.length),int((point['y']/maxY)*self.width), 'hello')

                self.screen.clrtoeol()
                self.screen.refresh()
            except Exception as err:
                print(err)
