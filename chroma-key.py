import cv2 as cv2
import numpy as np
import math
from matplotlib import pyplot as plt

# entrada = "img/0.bmp"
# entrada = "img/1.bmp"
# entrada = "img/2.bmp"
# entrada = "img/3.bmp"
# entrada = "img/4.bmp"
# entrada = "img/5.bmp"
# entrada = "img/6.bmp"
# entrada = "img/7.bmp"
# entrada = "img/8.bmp"
objeto = cv2.imread(entrada, cv2.IMREAD_COLOR)


imgHSV = cv2.cvtColor(objeto, cv2.COLOR_BGR2HSV)

lower_green = np.array([45,0,40])
upper_green = np.array([75,255,255])
upper_green2 = np.array([75,255,90])

mask = cv2.inRange(imgHSV, lower_green, upper_green)
mask = cv2.bitwise_not(mask)

mask2 = cv2.inRange(imgHSV, lower_green, upper_green2)
mask2 = cv2.bitwise_not(mask2)

cv2.imshow("mask", mask)
cv2.imshow("mask2", mask2)
# cv2.imshow("entrada", objeto)
cv2.waitKey(0)

