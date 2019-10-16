/*https://www.ime.usp.br/~pf/algoritmos/aulas/pont.html*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "pdi.h"
#include <math.h>

/*
#include "imagem.h"
#include "base.h"
#include "cores.h"
#include "geometria.h"
#include "desenho.h"
*/
/*============================================================================*/

#define INPUT_IMAGE "4.bmp"
#define INPUT_IMAGE_2 "GT2.bmp"
//#define INPUT_IMAGE "GT2.bmp"

//Como calcular
// 1 Através de um fator aleatório
// 2 Através da distância Euclidean7
#define METHOD 4


//Faixa de cores normalizada para selecionar verde no HSL
#define D 0.199
#define EUCLIDEAN_DMIN 0.09

//#define R 0.33  //85
//#define G 0.75  //165
//#define B 0.26  //68

#define R 0.33  //85
#define G 0.65  //165
#define B 0.26  //68


#define FATOR 1.8



/*============================================================================*/

void encontraVerde(Imagem *in, float *red, float *green, float *blue);
void substituiPixels(Imagem* in, Imagem* destino, Imagem* out);
void substituiPixelsComMascara(Imagem* destino, Imagem* mascara, Imagem* out);

/*============================================================================*/

int main ()
{

    Imagem* img_chroma = abreImagem (INPUT_IMAGE, 3);
    if (!img_chroma)
    {
        printf ("Erro abrindo a imagem com o chroma hey.\n");
        exit (1);
    }

    Imagem* img_2 = abreImagem (INPUT_IMAGE_2, 3);
    if (!img_2)
    {
        printf ("Erro abrindo a imagem.\n");
        exit (1);
    }

    Imagem* buffer = criaImagem (img_chroma->largura, img_chroma->altura, img_chroma->n_canais);
    Imagem* binaria;

    copiaConteudo(img_chroma, buffer);

    int i, j;

    if(METHOD == 1){
        binaria = criaImagem (img_chroma->largura, img_chroma->altura, img_chroma->n_canais);

        for(i=0; i < ((buffer->altura)-2); i++)
            for(j=0; j < ((buffer->largura)-2); j++){
                float r, g, b;
                r = buffer->dados[0][i][j];
                g = buffer->dados[1][i][j];
                b = buffer->dados[2][i][j];

                if((g > (r+D)) && (g > (b+D))){
                    binaria->dados[0][i][j] = 255;
                    binaria->dados[1][i][j] = 255;
                    binaria->dados[2][i][j] = 255;
                }
                else{
                    binaria->dados[0][i][j] = buffer->dados[0][i][j];
                    binaria->dados[1][i][j] = buffer->dados[1][i][j];
                    binaria->dados[2][i][j] = buffer->dados[2][i][j];
                }
            }
    }
    else if(METHOD == 2){
        binaria = criaImagem (img_chroma->largura, img_chroma->altura, img_chroma->n_canais);

        for(i=0; i < ((buffer->altura)-2); i++)
            for(j=0; j < ((buffer->largura)-2); j++){
                float r, g, b;
                r = buffer->dados[0][i][j];
                g = buffer->dados[1][i][j];
                b = buffer->dados[2][i][j];

                if( (pow(r-g*r, 2) + pow(g-g*g, 2) + pow(b-g*b, 2)) < EUCLIDEAN_DMIN){
                    binaria->dados[0][i][j] = 255;
                    binaria->dados[1][i][j] = 255;
                    binaria->dados[2][i][j] = 255;

                }
                else{
                    binaria->dados[0][i][j] = buffer->dados[0][i][j];
                    binaria->dados[1][i][j] = buffer->dados[1][i][j];
                    binaria->dados[2][i][j] = buffer->dados[2][i][j];
                }
            }
    }
    else if(METHOD == 3){
        binaria = criaImagem (img_chroma->largura, img_chroma->altura, 1);

        float red = 0, green = 0, blue = 0;
        encontraVerde(buffer, &red, &green, &blue);

        for(i=0; i < ((buffer->altura)-2); i++)
            for(j=0; j < ((buffer->largura)-2); j++){
                float r, g, b;
                r = buffer->dados[0][i][j];
                g = buffer->dados[1][i][j];
                b = buffer->dados[2][i][j];

                // Distância euclideana
                //Quanto menor o valor, mais próximo de verde está
                float x = sqrt(pow(green - g, 2)  + pow(red - r, 2) + pow(blue - b, 2));

                //Aumenta a importânica do canal verde para subtrair os outros canais dele
                float x1 = ((g*FATOR) - r - b);

                x = x1 - x;

                //if(x < 0.45){x=0;}
                //else if(x > 0.8){x=1;}

                binaria->dados[0][i][j] = x;

            }
        normaliza(binaria, binaria, 0, 1);

        //Imagem* binaria2 = criaImagem (img_chroma->largura, img_chroma->altura, 1);
        //binariza(binaria, binaria2, thresholdOtsu(binaria));
        //salvaImagem(binaria, "001. Teste.bmp");
        //salvaImagem(binaria2, "001. Teste2.bmp");
        //destroiImagem(binaria2);
    }
    else if (METHOD == 4) {
        binaria = criaImagem (img_chroma->largura, img_chroma->altura, 1);
        float r, g, b, x;

        for(i=0; i < (buffer->altura); i++) {
            for(j=0; j < (buffer->largura); j++){
                r = buffer->dados[0][i][j];
                g = buffer->dados[1][i][j];
                b = buffer->dados[2][i][j];

                x = g - r - b;
                if (x>1) x=1;
                if (x<1) x=0;

                binaria->dados[0][i][j] = x;
            }
        }

        //normaliza(binaria, binaria, 0, 1);
        salvaImagem(binaria, "001. RemoveFundo.bmp");
        return 0;

        if((img_chroma->altura != img_2->altura) || (img_chroma->largura != img_2->largura)){
            redimensionaBilinear(img_2,buffer);
        }

        salvaImagem(buffer, "002. Reescale.bmp");

        Imagem* nova = criaImagem (img_chroma->largura, img_chroma->altura, img_chroma->n_canais);

        for(i=0; i < (buffer->altura); i++) {
            for(j=0; j < (buffer->largura); j++){
                nova->dados[0][i][j] = ((binaria->dados[0][i][j])*(buffer->dados[0][i][j])) + ((1-(binaria->dados[0][i][j]))*(img_chroma->dados[0][i][j]));
                nova->dados[1][i][j] = ((binaria->dados[0][i][j])*(buffer->dados[1][i][j])) + ((1-(binaria->dados[0][i][j]))*(img_chroma->dados[1][i][j]));
                nova->dados[2][i][j] = ((binaria->dados[0][i][j])*(buffer->dados[2][i][j])) + ((1-(binaria->dados[0][i][j]))*(img_chroma->dados[2][i][j]));
            }
        }

        salvaImagem(nova, "003.NewBackgroud.bmp");

        destroiImagem (buffer);
        destroiImagem (binaria);
        destroiImagem (img_chroma);
        destroiImagem (img_2);

        return 0;

    }
    else{
        printf("Nao foi possivel remover o fundo");
    }

    //salvaImagem(binaria, "001. RemoveFundo.bmp");

    //Redimensiona imagem
    if((img_chroma->altura != img_2->altura) || (img_chroma->largura != img_2->largura)){
        redimensionaBilinear(img_2,buffer);
    }

    salvaImagem(buffer, "002. Reescale.bmp");



    Imagem* nova = criaImagem (img_chroma->largura, img_chroma->altura, img_chroma->n_canais);
    if(binaria->n_canais == 1){
        substituiPixelsComMascara(buffer, binaria, nova);
    }
    else{
        substituiPixels(binaria, buffer, nova);
    }


    //Substitui pixels brancos
/*
    for(i=0; i < ((binaria->altura)-2); i++)
        for(j=0; j < ((binaria->largura)-2); j++)
        {
            float r, g, b;
            r = binaria->dados[0][i][j];
            g = binaria->dados[1][i][j];
            b = binaria->dados[2][i][j];

            if(r == 255 && g == 255 && b == 255)
            {
                nova->dados[0][i][j] = buffer->dados[0][i][j];
                nova->dados[1][i][j] = buffer->dados[1][i][j];
                nova->dados[2][i][j] = buffer->dados[2][i][j];
            }
            else
            {
                nova->dados[0][i][j] = binaria->dados[0][i][j];
                nova->dados[1][i][j] = binaria->dados[1][i][j];
                nova->dados[2][i][j] = binaria->dados[2][i][j];
            }
        }
*/
    salvaImagem(nova, "003. NewBackgroud.bmp");



    destroiImagem (buffer);
    destroiImagem (binaria);
    destroiImagem (nova);

    destroiImagem (img_chroma);
    destroiImagem (img_2);

    return (0);
}


void encontraVerde(Imagem *in, float *red, float *green, float *blue){

    float media_r = 0, media_g = 0, media_b = 0;
    int i, j, contagem = 0;

    for(i=0; i < ((in->altura)/2); i++)
        for(j=0; j < ((in->largura)); j++)
        {
            float r, g, b;
            r = in->dados[0][i][j];
            g = in->dados[1][i][j];
            b = in->dados[2][i][j];

            // identifica quanto o verde é maior que as outras cores
            float g_em_b = g/b;
            float g_em_r = g/r;

            // Quando o verde for 95% maior que as outras cores, soma os valores do pixel para identificar a média deles
            if(g_em_b > 0.95 && g_em_r > 0.95)
            {
                media_r += r;
                media_g += g;
                media_b += b;
                contagem += 1;
            }
        }

    *red = media_r/contagem;
    *green = media_g/contagem;
    *blue = media_b/contagem;

}

void substituiPixels(Imagem* in, Imagem* destino, Imagem* out){
    int i, j;

    for(i=0; i < ((in->altura)-2); i++)
        for(j=0; j < ((in->largura)-2); j++)
        {
            float r, g, b;
            r = in->dados[0][i][j];
            g = in->dados[1][i][j];
            b = in->dados[2][i][j];

            if(r == 255 && g == 255 && b == 255)
            {
                out->dados[0][i][j] = destino->dados[0][i][j];
                out->dados[1][i][j] = destino->dados[1][i][j];
                out->dados[2][i][j] = destino->dados[2][i][j];
            }
            else
            {
                out->dados[0][i][j] = in->dados[0][i][j];
                out->dados[1][i][j] = in->dados[1][i][j];
                out->dados[2][i][j] = in->dados[2][i][j];
            }
        }
    salvaImagem(out, "003. NewBackgroud.bmp");
}


void substituiPixelsComMascara(Imagem* destino, Imagem* mascara, Imagem* out){
    int i, j;
    for(i=0; i < ((destino->altura)-2); i++)
        for(j=0; j < ((destino->largura)-2); j++)
        {
            //float r, g, b;
            //r = binaria->dados[0][i][j];
            //g = binaria->dados[1][i][j];
            //b = binaria->dados[2][i][j];

            out->dados[0][i][j] = destino->dados[0][i][j] * mascara->dados[0][i][j];
            out->dados[1][i][j] = destino->dados[1][i][j] * mascara->dados[0][i][j];
            out->dados[2][i][j] = destino->dados[2][i][j] * mascara->dados[0][i][j];


        }

    salvaImagem(out, "003. NewBackgroud.bmp");
}

