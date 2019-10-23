import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

entrada = "img/0.bmp"
entrada2 = "img/5.bmp"
objeto = cv.imread(entrada, cv.IMREAD_COLOR)

# fundo = cv.imread(entrada2, cv.IMREAD_COLOR)



imgHSV = cv.cvtColor(objeto, cv.COLOR_BGR2HSV)

lower_green = np.array([45,50,50])
upper_green= np.array([75,255,255])

mask = cv.inRange(imgHSV, lower_green, upper_green)

print(mask.shape[0], mask.shape[1])

final_img = objeto
final_img[::] = 255

print(final_img.shape[0], final_img.shape[1])


for linha in range(mask.shape[0]):
    for coluna in range(mask.shape[1]):
        # print("altura ", linha)
        # print("largura ", coluna)
        if mask[linha][coluna] == 1.0:
            final_img[linha][coluna] = objeto[linha][coluna]


# res = cv.bitwise_and(objeto,fundo, mask= mask)


cv.imshow("mask", mask)
cv.imshow("entrada", objeto)
cv.imshow("final", final_img)
cv.waitKey(0)

