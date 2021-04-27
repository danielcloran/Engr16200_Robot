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

        self.negativeBoundX = 0
        self.negativeBoundY = 0

        self.origin = [0,0]

        self.robot = robot
        self.length = int(length/10)
        self.width = int(width/10)
        self.pointList = np.full((self.width, self.length), self.Wall())
        self.wallArr = np.full((self.length), self.Wall())

        self.priorityList = [self.Origin(), self.Heat(), self.Magnet(), self.Path(), self.Wall()]

        self.printMapThread = threading.Thread(target=self.printMap, args=(), daemon=True)
        self.printMapThread.start()

    def checkPriority(self, str1, x, y):
        try:
            if self.priorityList.index(str1) > self.priorityList.index(self.pointList[int(x/10) - self.negativeBoundX,int(y/10) - self.negativeBoundY]):
                return False
        except Exception:
            pass
        return True

    def checkNegativeOffsets(self, x, y):
        x = int(x/10)
        if (x < self.negativeBoundX):
            offsetX = x - self.negativeBoundX
            for newPoint in range(abs(offsetX)):
                self.pointList = np.insert(self.pointList, 0, self.wallArr, axis = 0)
                self.pointList = np.delete(self.pointList, self.width-1, axis = 0)
                #self.pointList.insert(0, self.wallArr)
            self.negativeBoundX = x

        y = int(y/10)
        if (y < self.negativeBoundY):
            offsetY = y - self.negativeBoundY
            for newPoint in range(abs(offsetY)):
                self.pointList = np.insert(self.pointList, 0, self.Wall(), axis=1)
                self.pointList = np.delete(self.pointList, self.length-1, axis=1)
                    #point.insert(0, self.Wall())
            self.negativeBoundY = y

    def addPoint(self, pointStr, x, y):
        y = -y
        if(self.checkPriority(pointStr, x, y)):
            self.checkNegativeOffsets(x, y)
            self.pointList[int(x/10) - self.negativeBoundX, int(y/10) - self.negativeBoundY] = pointStr

    def setWall(self, x, y):
        self.addPoint(self.Wall(), x, y)

    def Wall(self):
        return "0"

    def setPath(self, x, y):
        self.addPoint(self.Path(), x, y)

    def Path(self):
        return "1"

    def setOrigin(self, x, y):
        self.origin = [x, y]
        self.addPoint(self.Origin(), x, y)

    def Origin(self):
        return "5"

    def setExit(self, x, y):
        self.addPoint(self.Exit(), x, y)

    def Exit(self):
        return "4"

    def setMagnet(self, x, y):
        self.addPoint(self.Magnet(), x, y)

    def Magnet(self):
        return "3"

    def setHeat(self, x, y):
        self.addPoint(self.Heat(), x, y)

    def Heat(self):
        return "2"

    def display_matrix(self, screen, matrix, x, y,):
        rows, cols = matrix.shape
        
        for row in reversed(range(rows)):
            for col in range(cols):
                if(matrix[(self.width - 1) - row, col]):
                    screen.addstr(row+x, col, matrix[(self.width - 1) - row, col])

    def printMap(self):
        while True:
            try:
                self.screen.addstr(0,0,"Team: 68")
                self.screen.addstr(1,0,"Map: " + self.mapNumber)
                self.screen.addstr(2,0,"Unit Length: 10cm")
                self.screen.addstr(3,0,"Unit: cm")
                self.screen.addstr(4,0,"Origin: (" + str(self.origin[1]-self.negativeBoundY) + ',' + str(self.origin[0]-self.negativeBoundX) + ')')
                self.screen.addstr(5,0,"Notes: ")

                self.display_matrix(self.screen, self.pointList, 7, 0)
                self.screen.refresh()
            except curses.error:
                pass
            except Exception as err:
                pass
                #print(err)
