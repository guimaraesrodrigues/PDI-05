import cv2 as cv2
import statistics
import math
import numpy as np
from matplotlib import pyplot as plt


def interpolar(img):
    altura = 2 * img.shape[0]
    largura = 2 * img.shape[1]
    img_saida = np.float32(np.zeros((altura, largura)))
    for linha in range(3, altura - 3):
        for coluna in range(3, largura - 3):
            linha_entrada = math.trunc(linha / 2)
            coluna_entrada = math.trunc(coluna / 2)

            if (linha % 2 == 0) and (coluna % 2 == 0):
                img_saida[linha][coluna] = img[linha_entrada][coluna_entrada]

            elif (linha % 2 == 1) and (coluna % 2 == 1):
                diagonal1 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal2 = abs(img[linha_entrada][coluna_entrada + 1] - img[linha_entrada + 1][coluna_entrada])
                if diagonal1 == min(diagonal1, diagonal2):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada][coluna_entrada] + img[linha_entrada + 1][coluna_entrada + 1]) / 2
                elif diagonal2 == min(diagonal1, diagonal2):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada][coluna_entrada + 1] + img[linha_entrada + 1][coluna_entrada]) / 2

            elif (linha % 2 == 1) and (coluna % 2 == 0):
                diagonal1 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada + 1][coluna_entrada])
                diagonal2 = abs(img[linha_entrada][coluna_entrada - 1] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal3 = abs(img[linha_entrada + 1][coluna_entrada - 1] - img[linha_entrada][coluna_entrada + 1])

                if diagonal1 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada][coluna_entrada] + img[linha_entrada + 1][coluna_entrada]) / 2

                elif diagonal2 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada][coluna_entrada - 1] + img[linha_entrada + 1][coluna_entrada + 1]) / 2

                elif diagonal3 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada + 1][coluna_entrada - 1] + img[linha_entrada][coluna_entrada + 1]) / 2

            else:
                diagonal1 = abs(img[linha_entrada - 1][coluna_entrada] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal2 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada][coluna_entrada + 1])
                diagonal3 = abs(img[linha_entrada - 1][coluna_entrada + 1] - img[linha_entrada + 1][coluna_entrada])

                if diagonal1 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada - 1][coluna_entrada] + img[linha_entrada + 1][coluna_entrada + 1]) / 2

                elif diagonal2 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada][coluna_entrada] + img[linha_entrada][coluna_entrada + 1]) / 2

                elif diagonal3 == min(diagonal1, diagonal2, diagonal3):
                    img_saida[linha][coluna] = abs(
                        img[linha_entrada - 1][coluna_entrada + 1] + img[linha_entrada + 1][coluna_entrada]) / 2

    return img_saida


entrada = "GT2.BMP"
#entrada = "Wind Waker GC.bmp"

img_original = np.float32(cv2.imread(entrada, 0))
height, width = img_original.shape[:2]
input = cv2.resize(img_original, (math.floor(width/2), math.floor(height/2)), interpolation=cv2.INTER_CUBIC)

#######################################
##  SEPARAR CAMADAS BASE E DETALHES  ##
#######################################
base = cv2.bilateralFilter(input, 5, 15, 15)
detalhe = cv2.subtract(input, base)

#######################################
##          AMPLIAR IMAGENS          ##
#######################################

base_ampliada = interpolar(base)
detalhe_ampliado = interpolar(detalhe)

imagem_ampliada = cv2.add(base_ampliada, detalhe_ampliado)

imagem_ampliada = np.uint8(imagem_ampliada)
detalhe_ampliado = np.uint8(detalhe_ampliado)
base_ampliada = np.uint8(base_ampliada)
detalhe = np.uint8(detalhe)
base = np.uint8(base)
input = np.uint8(input)
img_original = np.uint8(img_original)

nn = cv2.resize(input, (width,height), interpolation=cv2.INTER_NEAREST)
linear = cv2.resize(input, (width,height), interpolation=cv2.INTER_LINEAR)
bicubic = cv2.resize(input, (width,height), interpolation=cv2.INTER_CUBIC)

cv2.imwrite("imagem_ampliada.bmp", imagem_ampliada)
cv2.imwrite("detalhe_ampliado.bmp", detalhe_ampliado)
cv2.imwrite("base_ampliada.bmp", base_ampliada)
cv2.imwrite("detalhe.bmp", detalhe)
cv2.imwrite("base.bmp", base)
cv2.imwrite("input.bmp", input)

cv2.imshow("imagem_ampliada", imagem_ampliada)
cv2.imshow("NN", nn)
cv2.imshow("linear", linear)
cv2.imshow("bicubic", bicubic)

#cv2.imshow("detalhe_ampliado", detalhe_ampliado)
#cv2.imshow("base_ampliada", base_ampliada)
#cv2.imshow("detalhe", detalhe)
#cv2.imshow("base", base)
#cv2.imshow("input", input)
cv2.imshow("img_original", img_original)
cv2.waitKey(0)

