import unittest,os
from proyecto.analisis.informes.DatosToCsv import DatosToCsv

class TestDatosToCsv(unittest.TestCase):
    
    def test_guardar(self):
        datos_csv=DatosToCsv()
        actual = os.getcwd()

        lista=[[], [], [(((55, 71), (4, 24)), '42,66', '69,35', 'md'), (((116, 50), (90, 18)), '50,91', '41,23', 'md')], [(((164, 18), (128, 72)), '123,69', '64,9', 'dm')], [], [], ['md', 2, '55.29', '14.06'], ['dm', 1, '64.9', '0.0'], ['totales', 3, '58.49', '12.34']]
        datos_csv.guardar(actual+'/Test/codigo/informes/fichero_pruebas', lista)
        
        uno=os.path.exists(actual+'/Test/codigo/informes/fichero_pruebas/Salida_Lineas.csv')
        dos=os.path.exists(actual+'/Test/codigo/informes/fichero_pruebas/Salida_Estadisticas.csv')
        self.assertEqual(uno and dos,True)

        if uno and dos:
            os.remove(actual+'/Test/codigo/informes/fichero_pruebas/Salida_Lineas.csv')
            os.remove(actual+'/Test/codigo/informes/fichero_pruebas/Salida_Estadisticas.csv')
            
        print("OK,test_guardar")
        
    def test_leer(self):
        datos_csv=DatosToCsv()
        actual = os.getcwd()
        
        lista=datos_csv.leer(actual+'/Test/codigo/informes/fichero_pruebas/Salida_Lineas_for_test.csv')
        self.assertEqual(lista,['((55, 71), (4, 24))', '((116, 50), (90, 18))', '((164, 18), (128, 72))'])
        
        print("OK,test_leer")

        

