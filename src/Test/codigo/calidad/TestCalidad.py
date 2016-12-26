'''
Created on 18 dic. 2016

@author: Tobar
'''
from proyecto.analisis.procesado.ProcesadoDeImagen import ProcesadoDeImagen
from proyecto.analisis.procesado.ProcesadoDeLineas import ProcesadoDeLineas
import os
from skimage.color import rgb2lab
from skimage.filters import threshold_otsu
import networkx as nx
from networkx.algorithms import approximation as apxa
from PIL import Image, ImageDraw
import unittest
class TestCalidad(unittest.TestCase):

        
    
    def iniciar_test(self):
        actual = os.getcwd()
        
        procesado_de_imagen=ProcesadoDeImagen()
        procesado_de_lineas=ProcesadoDeLineas
        img=procesado_de_imagen.leer_imagen(actual+"/Test/codigo/calidad/imagenesPrueba/1-350-7547 1.jpg")
        l,a,b=self.pixel_rgb_2lab([255, 8, 0])        
        lab=rgb2lab(img)
        distance=abs(lab - [l,a,b]).mean(axis=2)
        im=self.binarizar(distance) 
#         tru_positive_inicial,tru_negative_inicial,false_positive_inicial,false_negative_inicial = self.inicial_test(im,img)
#         print(tru_positive_inicial,tru_negative_inicial)
#         print(false_positive_inicial,false_negative_inicial)         
        sin_ruido=procesado_de_imagen.reducir_grosor(im)
        lines=procesado_de_imagen.pro_hough(10,5,11,sin_ruido) 
        G=nx.Graph()
        G=procesado_de_lineas.combina2(4,8,4,1,lines,G)
        k_components = apxa.k_components(G)
        segmentos_de_verdad=procesado_de_lineas.segmentos_verdad(k_components,lines)
        
        
        pathh=actual+"/Test/codigo/calidad/imagenesPrueba/1-350-7547 1SinPintar.jpg"
        temp=actual+"/Test/codigo/calidad/imagenesPrueba/"
    
        self.guardar_y_pintar( pathh, temp, segmentos_de_verdad)
    
        img_pintada=procesado_de_imagen.leer_imagen(actual+"/Test/codigo/calidad/imagenesPrueba/calculada.jpg")

        tru_positive_compara,false_negative_compara,false_positive_compara,tru_negative_compara=self.calcula_medidas(img_pintada,im)
        TP=tru_positive_compara
        TN=tru_negative_compara
        FP=false_positive_compara
        FN=false_negative_compara
        P=TP+FN
        N=FP+TN
        TPR=TP/(TP+FN)
        self.assertGreater(TPR, 0.6)
        
        TNR=TN/(FP+TN)
        self.assertGreater(TNR, 0.6)
        
        PPV=TP/(TP+FP)          
        self.assertGreater(PPV, 0.6)
        
        NPV=TN/(TN+FN)
        self.assertGreater(NPV, 0.6)
        
        FPR=1-TNR        
        self.assertGreater(0.4,FPR)
        
        FDR=1-PPV
        self.assertGreater(0.4,FDR)
        
        FNR=1-TPR
        self.assertGreater(0.4,FNR)
        
        ACC=(TP+TN)/(P+N)
        self.assertGreater(ACC, 0.6)

        F1=(2*TP)/((2*TP)+FP+FN)
        self.assertGreater(F1, 0.6)
        
        MCC=(TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**(1/2)
        self.assertGreater(MCC, 0.6)
        
        BM=TPR+TNR-1
        self.assertGreater(BM, 0.6)
        
        MK=PPV+NPV-1
        self.assertGreater(MK, 0.6)  
        
     
        print("TP",TP,"TN",TN,"FP",FP,"FN",FN)
        print("TPR", TPR, "TNR" ,TNR ,"PPV ",PPV )
        print("NPV ",NPV,"FPR ",FPR, "FDR ",FDR )
        print("FNR ",FNR, "ACC ",ACC ,"F1 ",F1)
        print("N",N,"P",P,"MCC",MCC,"MK",MK,"BM",BM)
        
        
        
        
        
        
        
        print()
    @classmethod      
    def pixel_rgb_2lab(self,pixel):
        r,g,b = pixel
        return rgb2lab([[[r/255,g/255,b/255]]])[0][0]

    @classmethod      
    def binarizar(self,distance_red):
        threshold_global_otsu = threshold_otsu(distance_red)
        img_bin = distance_red <= threshold_global_otsu
        return img_bin    
    

    @classmethod      
    def es_rojo(self,l):
        r,g,b=l
        if r > 130 and g <90 and b < 85:
            return True
        else:
            return False
        
    def inicial_test(self,im,img):
        tru_positive_inicial=0
        tru_negative_inicial=0
        false_positive_inicial=0
        false_negative_inicial=0
        for i,ii in zip(im,img):
            for j,jj in zip(i,ii):
                if j == True and self.es_rojo(jj):
                    tru_positive_inicial=tru_positive_inicial+1
                elif self.es_rojo(jj) and j == False:
                    false_negative_inicial=false_negative_inicial+1
                elif not self.es_rojo(jj) and j == True:
                    false_positive_inicial=false_positive_inicial+1
                elif j == False and  not self.es_rojo(jj):
                    tru_negative_inicial=tru_negative_inicial+1
        return tru_positive_inicial,tru_negative_inicial,false_positive_inicial,false_negative_inicial          
    
    
 
    
    @classmethod      
    def guardar_y_pintar(self, path, temp, segmentos):
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
            draw.line((i[0][0], i[0][1], i[1][0], i[1][1]), fill='red', width=5)         
                                   
        im.save(temp + "/calculada.jpg", "JPEG", quality=100)
    
    def calcula_medidas(self,img_pintada,im):
        tru_positive_compara=0
        tru_negative_compara=0
        false_positive_compara=0
        false_negative_compara=0
        for i,ii in zip(img_pintada,im):
            for j,jj in zip(i,ii):
                if self.es_rojo(j) and jj == True:
                    tru_positive_compara=tru_positive_compara+1
                elif jj == True and not self.es_rojo(j):
                    false_negative_compara=false_negative_compara+1
                elif jj == False and self.es_rojo(j):
                    false_positive_compara=false_positive_compara+1
                elif not self.es_rojo(j) and  jj == False:
                    tru_negative_compara=tru_negative_compara+1
        return tru_positive_compara,false_negative_compara,false_positive_compara,tru_negative_compara

       
        
                
                
                
                
    
