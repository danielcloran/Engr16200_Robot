import curses
import threading
import numpy as np
import time


def add_to_front(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


pointList = np.full((10, 3), "1")

def save_to_csv():
    np.savetxt("test.csv", pointList, fmt='%d', delimiter=",")
    add_to_front('test.csv', 'Map #5')
