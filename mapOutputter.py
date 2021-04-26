import curses
import threading
import numpy as np
import time

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
        self.length = int(length/10)
        self.width = int(width/10)
        self.pointList = np.empty((self.width,self.length), dtype=object)

        self.priorityList = [self.Origin(), self.Heat(), self.Magnet(), self.Path(), self.Wall()]

        self.printMapThread = threading.Thread(target=self.printMap, args=(), daemon=True)
        self.printMapThread.start()

    def checkPriority(self, str1, x, y):
        try:
            if self.priorityList.index(str1) > self.priorityList.index(self.pointList[int(x/10),int(y/10)]):
                return False
        except Exception:
            pass
        return True

    def addPoint(self, pointStr, x, y):
        if(self.checkPriority(pointStr, x, y)):
            self.pointList[int(x/10),int(y/10)] = pointStr

    def setWall(self, x, y):
        addPoint(self.Wall(), x, y)

    def Wall(self):
        return "0"##BOLD + "0" + END

    def setPath(self, x, y):
        addPoint(self.Path(), x, y)

    def Path(self):
        return "1"#PATH + "1" + END

    def setOrigin(self, x, y):
        addPoint(self.Origin(), x, y)

    def Origin(self):
        return "5"#PATH + "5" + END

    def setExit(self, x, y):
        addPoint(self.Exit(), x, y)

    def Exit(self):
        return "4"#PATH + "4" + END

    def setMagnet(self, x, y):
        addPoint(self.Magnet(), x, y)

    def Magnet(self):
        return "3" # MAGNET + BOLD + "3" + END

    def setHeat(self, x, y):
        addPoint(self.Heat(), x, y)

    def Heat(self):
        return "2" #HEAT + BOLD + "2" + END

    def getRanges(self):
        # ACTUAL MAP
        seq = [x['x'] for x in self.pointList]
        maxX = max(seq)
        minX = min(seq)
        rangeX = maxX - minX
        seq = [y['y'] for y in self.pointList]
        maxY = max(seq)
        minY = min(seq)
        rangeY = maxY - minY
        return minX, minY, rangeX, rangeY

    def display_matrix(self, screen, m, x, y, precision=2, title=None):
        rows, cols = m.shape
        if title:
            screen.addstr(x, y, title)
            x += 1
        #screen.addstr(x, y, "[")
        #screen.addstr(x, cols*(4+precision)+y+1, "]")
        #screen.addstr(rows+x-1, y, "[")
        #screen.addstr(rows+x-1, cols*(4+precision)+y+1, "]")
        for row in range(rows):
            for col in range(cols):
                if(m[row, col]):
                    screen.addstr(row+x, col, m[row, col])
                else:
                    screen.addstr(row+x, col, self.Wall())

                #screen.addstr(row+x, col*(4+precision)+y+1, m[row, col])

    def printMap(self):
        while True:
            try:
                self.screen.addstr(0,0,"Team: 68")
                self.screen.addstr(1,0,"Map: " + self.mapNumber)
                self.screen.addstr(2,0,"Unit Length: ")
                self.screen.addstr(3,0,"Unit: cm")
                self.screen.addstr(4,0,"Origin: ")
                self.screen.addstr(5,0,"Notes: ")

                self.display_matrix(self.screen, self.pointList, 7, 0, 'Map!')
                self.screen.refresh()
            except curses.error:
                pass
            except Exception as err:
                print(err)
