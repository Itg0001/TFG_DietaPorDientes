import unittest
import os
import numpy as np
from proyecto.codigo.procesado.ProcesadoDeImagen import ProcesadoDeImagen
from skimage import io
class TestProcesadoDeImagen(unittest.TestCase):

    def test_leer_imagen(self):
        proc_imagen = ProcesadoDeImagen()

        actual = os.getcwd()
        
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        img_ori = io.imread(actual.replace('\\', '/') + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        
        self.assertEqual(img.shape, img_ori.shape)
        self.assertEqual(np.all(img == img_ori), True)
        
        print("OK,test_leer_imagen")
    def test_distancia_al_rojo(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
               
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img,[250,50,50])
        self.assertEqual(np.all(img == dist_red), False)
        print("OK,test_distancia_al_rojo")

    def test_binarizar(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img,[250,50,50])
        binari = proc_imagen.binarizar(dist_red)
        
        self.assertEqual(np.all(binari == dist_red), False)
        print("OK,test_binarizar")

    def test_reducir_grosor(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img,[250,50,50])
        binari = proc_imagen.binarizar(dist_red)
        skeleto = proc_imagen.reducir_grosor(binari)
        
        self.assertEqual(np.all(skeleto == binari), False)

        print("OK,test_reducir_grosor")        

    def test_pro_hough(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img,[250,50,50])
        binari = proc_imagen.binarizar(dist_red)
        skeleto = proc_imagen.reducir_grosor(binari)        
        lines = proc_imagen.pro_hough(10, 5, 11, skeleto)
        linias=[((129, 70), (163, 19)), ((48, 65), (4, 24)), ((55, 71), (11, 30)), ((128, 72), (138, 57)), ((116, 50), (90, 18)), ((96, 26), (92, 21))]
        
        self.assertEqual(lines, linias)

        print("OK,test_pro_hough")        


    
