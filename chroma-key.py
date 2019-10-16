import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

entrada = "img/0.bmp"
input = cv.imread(entrada, cv.IMREAD_COLOR)

imgHSV = cv.cvtColor(input, cv.COLOR_BGR2HSV)




cv.imshow("input", imgHSV)
cv.waitKey(0)

