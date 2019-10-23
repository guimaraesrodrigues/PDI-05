import cv2 as cv2
import numpy as np
import math
from matplotlib import pyplot as plt

TAM_JANELA = 36

#####
# soma_max = TAM_JANELA * 255
# peso = soma_janela /￿ soma_max
#####


def is_out_of_bound(img, i, j):
    return (i > img.shape[1] or i < 0) or (j > img.shape[0] or j < 0)


def define_peso(img, img_fundo, img_objeto):

    img_final = img_objeto
    peso = 0

    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):

            if img[linha][coluna] == 255:
                peso = 1

            if img[linha][coluna] == 128:
                soma_janela = 0

                for linha_janela in range(linha - TAM_JANELA, linha + TAM_JANELA):
                    for coluna_janela in range(coluna - TAM_JANELA, coluna + TAM_JANELA):

                        if not is_out_of_bound(img, linha_janela, coluna_janela):
                            soma_janela = soma_janela + img[linha_janela][coluna_janela]

                soma_max = math.pow(TAM_JANELA * 2 + 1, 2) * 255
                peso = soma_janela / soma_max


            for canal in range(3):
                img_final[linha][coluna][canal] = math.floor(img_objeto[linha][coluna][canal] * peso + img_fundo[linha][coluna][canal] * (1 - peso))

    cv2.imshow("entrada", img_final)
    cv2.waitKey(0)



                # print("pixel ", img[linha][coluna])

entrada = "img/0.bmp"
# entrada = "img/1.bmp"
# entrada = "img/2.bmp"
# entrada = "img/3.bmp"
# entrada = "img/4.bmp"
# entrada = "img/5.bmp"
# entrada = "img/6.bmp"
# entrada = "img/7.bmp"
# entrada = "img/8.bmp"

objeto = cv2.imread(entrada, cv2.IMREAD_COLOR)
novo_fundo = cv2.imread('img/GT2.BMP', cv2.IMREAD_COLOR)
novo_fundo = cv2.resize(novo_fundo, (objeto.shape[1], objeto.shape[0]), interpolation=cv2.INTER_AREA)

imgHSV = cv2.cvtColor(objeto, cv2.COLOR_BGR2HSV)

lower_green = np.array([45,0,40])
upper_green = np.array([75,255,255])
upper_green2 = np.array([75,255,90])

mask = cv2.inRange(imgHSV, lower_green, upper_green)
mask = cv2.bitwise_not(mask)

mask2 = cv2.inRange(imgHSV, lower_green, upper_green2)
mask2 = cv2.bitwise_not(mask2)

final_mask = cv2.addWeighted(mask, 1, mask2, 0.5, 0)

define_peso(final_mask, novo_fundo, objeto)

cv2.imshow("final_mask", final_mask)
# cv2.imshow("mask2", mask2)
cv2.imshow("entrada", objeto)
cv2.waitKey(0)



