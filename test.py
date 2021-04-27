import curses
import threading
import numpy as np
import time

pointList = np.full((10, 3), '1')
wallArr = np.full((3), '0')


print('Old', pointList)

newList = np.delete(pointList, 3-1, axis=1)

print('New', newList)
