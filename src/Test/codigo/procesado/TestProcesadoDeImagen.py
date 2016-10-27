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
        imgOri = io.imread(actual.replace('\\', '/') + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        
        self.assertEqual(img.shape, imgOri.shape)
        self.assertEqual(np.all(img == imgOri), True)
        
        print("OK,test_leer_imagen")
    def test_distancia_al_rojo(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
               
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img)
        self.assertEqual(np.all(img == dist_red), False)
        print("OK,test_distancia_al_rojo")

    def test_binarizar(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img)
        binari = proc_imagen.binarizar(dist_red)
        
        self.assertEqual(np.all(binari == dist_red), False)
        print("OK,test_binarizar")

    def test_reducir_grosor(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img)
        binari = proc_imagen.binarizar(dist_red)
        skeleto = proc_imagen.reducir_grosor(binari)
        
        self.assertEqual(np.all(skeleto == binari), False)

        print("OK,test_reducir_grosor")        

    def test_pro_hough(self):
        proc_imagen = ProcesadoDeImagen()
        actual = os.getcwd()
        img = proc_imagen.leer_imagen(actual + '/Test/codigo/procesado/imgProc/ATP02 UE4 46_1.jpg')
        dist_red = proc_imagen.distancia_al_rojo(img)
        binari = proc_imagen.binarizar(dist_red)
        skeleto = proc_imagen.reducir_grosor(binari)        
        lines = proc_imagen.pro_hough(10, 5, 11, skeleto)
        linias=[((128, 72), (164, 18)), ((24, 43), (12, 31)), ((55, 71), (31, 49)), ((136, 59), (163, 19)), ((11, 31), (4, 24)), ((34, 51), (25, 43)), ((109, 42), (90, 18)), ((51, 67), (30, 48)), ((116, 50), (92, 20))]        

        self.assertEqual(lines, linias)

        print("OK,test_pro_hough")        


    
