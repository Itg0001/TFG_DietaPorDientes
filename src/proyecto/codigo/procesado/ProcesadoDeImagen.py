from skimage import io  # Librerias para importar las imagenes
from skimage.color import rgb2grey  # Mostrar las 3 imagenes
from skimage.color import rgb2hsv  # Mostrar las 3 imagenes
from skimage.filters import threshold_otsu
from skimage.morphology import  skeletonize 
from skimage.transform import probabilistic_hough_line
import numpy as np
import tempfile
import os,shutil
from skimage.color import rgb2lab,gray2rgb
from PIL import Image, ImageDraw
from proyecto.diccionario import Diccionario
import warnings
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
        self.dic=Diccionario()     
        img = io.imread(path_img.replace('\\', '/'))
        
        return gray2rgb(img)
    
    @classmethod
    def guardar_y_pintar(self, path, temp, segmentos,cuadrado):
        """
        Metodo que se encargara de guardar y pintar los segmentos pasados 
        en la imagen para asi poder usarla para informes.
        
        @param path: Camino donde guardar la imagen con las lineas nuevas pintadas. 
        @param tem ruta al fichero temporal donde guardar la imagen.
        @param segmentos: Segmentos a pintar en la imagen.
        """
        im = Image.open(path).convert("RGB")
        draw = ImageDraw.Draw(im)
        for i in segmentos:             
            draw.line((i[0][0], i[0][1], i[1][0], i[1][1]), fill='red', width=2)         
        if cuadrado[0]!="-" and cuadrado[1]!="-" and cuadrado[2]!="-" and cuadrado[3]!="-":
            draw.line((cuadrado[1]-2, cuadrado[3], cuadrado[0]+2, cuadrado[3]), fill='#020202', width=6)    
            draw.line((cuadrado[1], cuadrado[3], cuadrado[1], cuadrado[2]), fill='#020202', width=6)    
            draw.line((cuadrado[1]-2, cuadrado[2], cuadrado[0]+2, cuadrado[2]), fill='#020202', width=6)    
            draw.line((cuadrado[0], cuadrado[2], cuadrado[0], cuadrado[3]), fill='#020202', width=6) 
                           
        im.save(temp + self.dic.pintada, self.dic.jpg, quality=100)

    @classmethod
    def distancia_al_rojo(self, img,pixel):
        """
        Metodo para:
        Pasamos la imagen al espacio de color RGB y nos quedamos con el canal rojo
        Pasamos la imagen al espacio de color HSV
        Normalizamos la imagen del espacio de color HSV para utilizar que distancia 
        al rojo tenemos y poder hacer el theshold.
        
        @param img: imagen original leida anteriormente.

        @return: distance_red: distancia de cada pixel al rojo apra luego hacer el threshold.
        
        """ 
        r,g,b = pixel        
        g,v,b=rgb2lab([[[r/255,g/255,b/255]]])[0][0]
        
        lab=rgb2lab(img)
        distance_red=abs(lab - [g,v,b]).mean(axis=2)
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
        img_bin = distance_red <= threshold_global_otsu
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
    
    @classmethod
    def binarizar_para_cuadrado(self,img):
        """
        Este metodo va a consistir en que a partir de la imagen que hemos abierto
        nos la va a binarizar resaltando unicamente los bordes del cuadrado donde
        detectar las lineas 
        @param img: imagen que hemos leido.
        
        @return: imagen binarizada resaltando bordes. 
        """
        img_hsv=rgb2hsv(img)
        grises = rgb2grey(img_hsv)
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
    
    @classmethod
    def obtener_max_y_min(self,lines):
        """
        En este metodo vamos a calcular las xmax, xmin ymax e ymin de neustro cuadrado
        es decir los 4 vertices que componen el cuadrado
        @param lines: lista de puntos que forman las lineas del cuadrado.
        @return: 4 vertices del cuadrado.
        """
        puntos_x,puntos_y=set(),set()
        for i in lines:
            puntos_x.add(i[0][0])
            puntos_x.add(i[1][0])    
            puntos_y.add(i[0][1])
            puntos_y.add(i[1][1])
        if len(lines)==0:
            return 0,0,0,0
        return max(puntos_x),min(puntos_x),max(puntos_y),min(puntos_y)
    
    @classmethod
    def pertenece_o_no(self,x,y,x_min,x_max,y_min,y_max):
        """
        En este metodo dado un punto y los 4 vertices del cuadrado comprobaremos
        si las coordenadas del punto pertenecen al area pintable.
        @param x: coordenada x del punto a comprobar.
        @param y: coordenada y del punto a comprobar.
        @param x_min: coordenada x minima del cuadrado
        @param x_max: coordenada x macima del cuadrado.
        @param y_min: coodenada y minima del cuadrado.
        @param y_max: coordenada y maxima del cuadrado.
        @return: true/false dependiendo si pertenece a esa region o no.     
        """
        if x == None and y==None:
            return False
        if (x_min< x < x_max) and  (y_min< y < y_max):
            return True
        else:
            return False

    
    def obtener_numeros(self,img):
        """
        Metodo que se va a encargar de obtener los numero que componen
        la referencia.
        @param img: imagen de la que obtener la referencia. 
        @return: devolvemos el valor leido de la imagen que sera la referencia.
        """
        img_crop = img[860:950,520:645]
        img_hsv=rgb2hsv(img_crop)
        distance_red = rgb2grey(1 - np.abs(img_hsv - (1, 1, 0)))

        #binarizar
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
        #guardar en temp
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            io.imsave(temp+self.dic.pro_img,distance_red)

        act=os.getcwd()
        tes=act+self.dic.pro_tessera
        dir_img=temp+self.dic.pro_img_tesse
        dir_salida=temp+self.dic.pro_sal
        opt=self.dic.pro_batch

        #ejecutar tesseract
        os.system(tes+dir_img+dir_salida+opt)
        #obtener resultado de la ejecucion.
        f = open(temp+self.dic.pro_sal_txt)
        g=f.read()
        f.close()
        #borrar temporal.
        shutil.rmtree(temp) 
        return g.replace('3','0').replace('\n','').replace('8','0')
    @classmethod
    def pixel_rgb_2_lab(self,pixel):
        """
        Esta funcion se encargara de pasar un pixel de rgb a lab.
        @param pixel: pixel que pasar a espacio de color lab.
        @return: pixel en espacio de color lab. 
        """
        r,g,b = pixel        
        return rgb2lab([[[r/255,g/255,b/255]]])[0][0]
    
    @classmethod
    def pixelrgb_2_hsv(self,pixel):
        """
        Esta funcion se encargara de pasar un pixel de rgb a hsv.
        @param pixel: pixel que pasar a espacio de color hsv.
        @return: pixel en espacio de color hsv. 
        """
        r,g,b = pixel
        return rgb2hsv([[[r/255,g/255,b/255]]])[0][0]