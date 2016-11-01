from skimage import io  # Librerias para importar las imagenes
from skimage.color import rgb2grey  # Mostrar las 3 imagenes
from skimage.color import rgb2hsv  # Mostrar las 3 imagenes
from skimage.filters import threshold_otsu
from skimage.morphology import  skeletonize 
from skimage.transform import probabilistic_hough_line
import numpy as np
import tempfile
import os,shutil

from PIL import Image, ImageDraw

class ProcesadoDeImagen():
    """
    Clase que contendra los metodos necesarios para poder realizar el procesado de las 
    imagenes para obtener a partir de una simple imagen las lienas que hay en ella pintadas
    en rojo.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
   
    @classmethod
    def leer_imagen(self, path_img):
        """
        Metodo Para leer una imagen a traves de scikit-Image (skimage)
        dandole el path de la imagen.
        @param path_img: camino hasta la imagen.
        @retrun Img: imagen leida.
        """     
        img = io.imread(path_img.replace('\\', '/'))
        return img
    
    @classmethod
    def guardar_y_pintar(self, path, temp, segmentos):
        """
        Metodo que se encargara de guardar y pintar los segmentos pasados 
        en la imagen para asi poder usarla para informes.
        
        @param path: Camino donde guardar la imagen con las lineas nuevas pintadas. 
        @param tem ruta al fichero temporal donde guardar la imagen.
        @param segmentos: Segmentos a pintar en la imagen.
        """
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        for i in segmentos:             
            draw.line((i[0][0], i[0][1], i[1][0], i[1][1]), fill='red', width=2)        
        im.save(temp + "/Pintada.jpg", "JPEG", quality=100)
    
    @classmethod
    def distancia_al_rojo(self, img):
        """
        Metodo para:
        Pasamos la imagen al espacio de color RGB y nos quedamos con el canal rojo
        Pasamos la imagen al espacio de color HSV
        Normalizamos la imagen del espacio de color HSV para utilizar que distancia 
        al rojo tenemos y poder hacer el theshold.
        
        @param img: imagen original leida anteriormente.

        @return: distance_red: distancia de cada pixel al rojo apra luego hacer el threshold.
        
        """        
        img_hsv = rgb2hsv(img)
        distance_red = rgb2grey(1 - np.abs(img_hsv - (0, 1, 0)))
        return distance_red


    @classmethod
    def binarizar(self, distance_red):
        """
        Metodo para binarizar la imagen para obtener una clara diferenciacion entre 
        el fondo y las lineas que queremos detectar.
        
        @param distance_red: distancia de cada pixel al rojo apra luego hacer el threshold.

        @return: imgBin: imagen binarizada.
        """
        threshold_global_otsu = threshold_otsu(distance_red)
        img_bin = distance_red >= threshold_global_otsu
        return img_bin

    
    @classmethod
    def crop_img(self, img_bin, img):
        """
        Metodo para la imagen no hay qeu procesarla completa porque solo tiene una region
        marcada con lineas tenemos qque recortarla
        
        @param img_bin: imagen binarizada.
        @param img: imagen normal.
        
        @return: imgBinCrop: Es la imagen binarizada recortada a la region que queremos.
        @return: imgCrop: Es la imagen original recortada a la region que queremos.
        """
        img_bin_crop = img_bin[0:750, 500:1500]
        img_crop = img[0:750, 500:1500]
        return img_bin_crop, img_crop


    @classmethod
    def reducir_grosor(self, img_bin_crop):
        """
        Metodo para:
        Esta funcion en lo que consiste es qeu entrando la imagen binarizada 
        reduzcamos el tamano de las lineas para que la deteccion tenga menos
        incertidumbre y sea mas rapida la deteccion de lineas.
        
        @param img_bin_crop: Es la imagen binarizada recortada a la region que queremos.

        @return: sinRuido: Es la imagen una vez corregida la binarizacion apra que las 
                lineas sean mas delgadas.
        """
        sin_ruido = skeletonize(img_bin_crop)
        return sin_ruido

    
    @classmethod
    def pro_hough(self, threshold, line_length, line_gap, sin_ruido):
        """
        Este metodo lo que va a hacer es calcular los segmentos(ORIGEN"Ox,Oy" Y FIN "FX,FY") 
        de cada una de las lineas que se han detectado en la imagen binarizada atraves de la 
        funcion probabilistica de la transformada de hough.
        Entrada:
        
        @param threshold: Densidad de lineas. 
        @param line_length: Distancia minima de las lineas que calcula.
        @param line_gap: Distancia a la que si estan los extremos de las rectas las una.
        @param sin_ruido: Es la imagen una vez corregida la binarizacion apra que las 
            lineas sean mas delgadas.
            
        @return: lines: Lista de todos los segmentos que ha detectado.
        """
        lines = probabilistic_hough_line(sin_ruido, threshold, line_length, line_gap)
        return lines
    
    def binarizar_para_cuadrado(self,img):
        imgHSV=rgb2hsv(img)
        grises = rgb2grey(imgHSV)
        ii=0
        jj=0
        for i in grises:
            for j in i:
                if j>0 and j<0.0025:
                    grises[ii][jj]=1
                else:
                    grises[ii][jj]=0
                jj=jj+1
            jj=0
            ii=ii+1
        return grises

    def obtener_max_y_min(self,lines):
        puntos_x,puntos_y=set(),set()
        for i in lines:
            puntos_x.add(i[0][0])
            puntos_x.add(i[1][0])    
            puntos_y.add(i[0][1])
            puntos_y.add(i[1][1])
        return max(puntos_x),min(puntos_x),max(puntos_y),min(puntos_y)
 
    def pertenece_o_no(self,x,y,xMin,xMax,yMin,yMax):
        if x == None and y==None:
            return False
        if (xMin< x < xMax) and  (yMin< y < yMax):
            return True
        else:
            return False
    def binarizar_referencia(self,imagen):
        ii=0
        jj=0
        for i in imagen:
            for j in i:
                if round(j,2)>0 and round(j,2)<0.09:
                    imagen[ii][jj]=0
                else:
                    imagen[ii][jj]=1
                jj=jj+1
            jj=0
            ii=ii+1
        return imagen
    def obtener_referencia(self,img):
        imgCrop = img[840:860,555:750]
        imgHSV=rgb2hsv(imgCrop)
        distance_white = rgb2grey(1 - np.abs(imgHSV - (1, 1, 0)))
        img_binarizada=self.binarizar_referencia(distance_white)
        sin_ruido = skeletonize(img_binarizada)
        lines = probabilistic_hough_line(sin_ruido, threshold=50, line_length=50,line_gap=50)
        return lines
    
    def obtener_numeros(self,img):
        imgCrop = img[860:950,520:645]
        imgHSV=rgb2hsv(imgCrop)
        distance_red = rgb2grey(1 - np.abs(imgHSV - (1, 1, 0)))
    
    
        ii=0
        jj=0
        for i in distance_red:
            for j in i:
                if round(j,2)>0 and round(j,2)<0.09:
                    distance_red[ii][jj]=1
                else:
                    distance_red[ii][jj]=0
                jj=jj+1
            jj=0
            ii=ii+1
        temp = tempfile.mkdtemp()
        io.imsave(temp+"/imagen.png",distance_red,)
        
        act=os.getcwd()
        tes=act+"/tesseract/tesseract.exe "
        dir_img=temp+"/imagen.png "
        dir_salida=temp+"/salida "
        opt="nobatch digits "
        os.system(tes+dir_img+dir_salida+opt)
        f = open(temp+'/salida.txt')
        g=f.read()
        f.close()
        shutil.rmtree(temp) 
        return g.replace('3','0').replace('\n','').replace('8','0')