import cv2 as cv2
import statistics
import math
import numpy as np
from matplotlib import pyplot as plt


def ampliar(img):
    altura = 2 * img.shape[0]
    largura = 2 * img.shape[1]
    linha_entrada = 0
    coluna_entrada = 0
    img_saida = np.zeros((altura, largura))
    for linha in range(3, altura - 3):
        for coluna in range(3, largura - 3):
            linha_entrada = math.trunc(linha / 2)
            coluna_entrada = math.trunc(coluna / 2)

            if (linha % 2 == 0) and (coluna % 2 == 0):
                img_saida[linha][coluna] = img[linha_entrada][coluna_entrada]
            elif (linha % 2 == 1) and (coluna % 2 == 1):
                diagonal1 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal2 = abs(img[linha_entrada][coluna_entrada + 1] - img[linha_entrada + 1][coluna_entrada])
                m = (diagonal1, diagonal2)
                menor_diagonal = min(m)
                img_saida[linha][coluna] = menor_diagonal / 2
            elif (linha % 2 == 1) and (coluna % 2 == 0):
                diagonal1 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada + 1][coluna_entrada])
                diagonal2 = abs(img[linha_entrada][coluna_entrada - 1] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal3 = abs(img[linha_entrada + 1][coluna_entrada - 1] - img[linha_entrada][coluna_entrada + 1])
                m = (diagonal1, diagonal2, diagonal3)
                menor_diagonal = min(m)
                img_saida[linha][coluna] = menor_diagonal / 2
            else:
                diagonal1 = abs(img[linha_entrada - 1][coluna_entrada] - img[linha_entrada + 1][coluna_entrada + 1])
                diagonal2 = abs(img[linha_entrada][coluna_entrada] - img[linha_entrada][coluna_entrada + 1])
                diagonal3 = abs(img[linha_entrada - 1][coluna_entrada + 1] - img[linha_entrada + 1][coluna_entrada])
                m = (diagonal1, diagonal2, diagonal3)
                menor_diagonal = min(m)
                img_saida[linha][coluna] = menor_diagonal / 2
    return img_saida


entrada = "GT2.BMP"
# entrada = "Wind Waker GC.bmp"

input = cv2.imread(entrada, 0)

#######################################
##  SEPARAR CAMADAS BASE E DETALHES  ##
#######################################
base = cv2.bilateralFilter(input, 9, 75, 75)
detalhe = cv2.subtract(input, base)

#######################################
##          AMPLIAR IMAGENS          ##
#######################################

base_ampliada = ampliar(base)
detalhe_ampliado = ampliar(detalhe)

imagem_ampliada = cv2.add(base_ampliada, detalhe_ampliado)

cv2.imshow("imagem_ampliada", imagem_ampliada)
cv2.imshow("detalhe_ampliado", detalhe_ampliado)
cv2.imshow("base_ampliada", base_ampliada)
cv2.imshow("detalhe", detalhe)
cv2.imshow("base", base)
cv2.imshow("input", input)
cv2.waitKey(0)

