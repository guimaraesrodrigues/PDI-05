import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

entrada = "img/0.bmp"
entrada2 = "img/5.bmp"
objeto = cv.imread(entrada, cv.IMREAD_COLOR)
fundo = cv.imread(entrada2, cv.IMREAD_COLOR)



imgHSV = cv.cvtColor(objeto, cv.COLOR_BGR2HSV)

lower_green = np.array([45,50,50])
upper_green= np.array([75,255,255])

mask = cv.inRange(imgHSV, lower_green, upper_green)

res = cv.bitwise_and(objeto,fundo, mask= mask)


cv.imshow("mask", mask)
cv.imshow("entrada", objeto)
cv.waitKey(0)

