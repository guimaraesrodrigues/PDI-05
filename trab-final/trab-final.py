import cv2 as cv2
import statistics
import numpy as np
from matplotlib import pyplot as plt

entrada = "GT2.BMP"
# entrada = "Wind Waker GC.bmp"

input = cv2.imread(entrada, 0)

#######################################
##  SEPARAR CAMADAS BASE E DETALHES  ##
#######################################
base = cv2.bilateralFilter(input,9,75,75)
detalhe = cv2.Laplacian(input,cv2.CV_64F)
base2 = input - detalhe

cv2.imshow("detalhe", detalhe)
cv2.imshow("base2", base2)
cv2.imshow("base", base)
cv2.imshow("input", input)
cv2.waitKey(0)

