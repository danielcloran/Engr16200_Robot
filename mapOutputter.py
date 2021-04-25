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

        self.priorityList = [self.Origin(), self.Heat(), self.Magnet(), self.Path(), self.Wall()]

        self.printMapThread = threading.Thread(target=self.printMap, args=(), daemon=True)
        self.printMapThread.start()

    def checkPriority(self, str1, x, y):
        if self.priorityList.index(str1) < self.pointList[int(x)][int(y)]:
            return True
        else: return False

    def setWall(self, x, y):
        if(self.checkPriority(self.Wall, x, y)):
            self.pointList[int(x)][int(y)] = self.Wall()

    def Wall(self):
        return BOLD + "0" + END

    def setPath(self, x, y):
        if(self.checkPriority(self.Path(), x, y)):
            self.pointList[int(x)][int(y)] = self.Path()()

    def Path(self):
        return PATH + "1" + END

    def setOrigin(self, x, y):
        if(self.checkPriority(self.Origin(), x, y)):
            self.pointList[int(x)][int(y)] = self.Origin()()

    def Origin(self):
        return PATH + "5" + END

    def setExit(self, x, y):
        if(self.checkPriority(self.Exit(), x, y)):
            self.pointList[int(x)][int(y)] = self.Exit()()

    def Exit(self):
        return PATH + "4" + END

    def setMagnet(self, x, y):
        if(self.checkPriority(self.Magnet(), x, y)):
            self.pointList[int(x)][int(y)] = self.Magnet()()

    def Magnet(self):
        return MAGNET + BOLD + "3" + END

    def setHeat(self, x, y):
        if(self.checkPriority(self.Heat(), x, y)):
            self.pointList[int(x)][int(y)] = self.Heat()()

    def Heat(self):
        return HEAT + BOLD + "2" + END

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

    def display_matrix(screen, m, x, y, precision=2, title=None):
        rows, cols = m.shape
        if title:
            screen.addstr(x, y, title)
            x += 1
        screen.addstr(x, y, "[")
        screen.addstr(x, cols*(4+precision)+y+1, "]")
        screen.addstr(rows+x-1, y, "[")
        screen.addstr(rows+x-1, cols*(4+precision)+y+1, "]")
        for row in range(rows):
            for col in range(cols):
                screen.addstr(row+x, col*(4+precision)+y+1, "%+.*f," % (precision, m[row, col]))

    def printMap(self):
        while True:
            try:
                self.screen.addstr(0,0,"Team: 68")
                self.screen.addstr(1,0,"Map: " + self.mapNumber)
                self.screen.addstr(2,0,"Unit Length: ")
                self.screen.addstr(3,0,"Unit: cm")
                self.screen.addstr(4,0,"Origin: ")
                self.screen.addstr(5,0,"Notes: ")

                display_matrix(self.screen, self.pointList, 6, 0)

                #minX, minY, rangeX, rangeY = self.getRanges()
                #yOffset = 10

                #self.screen.addstr(7,0,"rangeX: " + str(rangeX))
                #self.screen.addstr(8,0,"rangeY: " + str(rangeY))
                #if rangeX != 0 and rangeY != 0:
                #    for point in self.pointList:
                #        shiftedX = int((point['x'] + abs(minX))/ rangeX) * 50
                #        shiftedY = yOffset + int((point['y'] + abs(minY))/ rangeY) * 50
                #        #self.screen.addstr(shiftedY,shiftedX, 'X')
                #        self.screen.addstr(10,0, 'shiftedY:' + str(shiftedY) + ', shiftedX:' + str(shiftedX) )
                        #self.screen.addstr(int((point['x']/maxX)*self.length),int((point['y']/maxY)*self.width), 'hello')
                #self.screen.addstr(12,0, str(len(self.pointList)))

                self.screen.refresh()
            except curses.error:
                pass
            except Exception as err:
                print(err)
