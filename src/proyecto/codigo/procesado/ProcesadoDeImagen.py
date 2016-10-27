from skimage import io  # Librerias para importar las imagenes
from skimage.color import rgb2grey  # Mostrar las 3 imagenes
from skimage.color import rgb2hsv  # Mostrar las 3 imagenes
from skimage.filters import threshold_otsu
from skimage.morphology import  skeletonize 
from skimage.transform import probabilistic_hough_line
import numpy as np
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
