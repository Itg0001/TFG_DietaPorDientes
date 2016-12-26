import unittest,os
from proyecto.analisis.informes.ConfiguracionToXML import ConfiguracionToXML

class TestConfiguracionToXML(unittest.TestCase):
    
    def test_guardar(self):
        configuracionxml=ConfiguracionToXML()
        actual = os.getcwd()
        nombres={'docu2': '/Salida_Estadisticas.csv', 'docu3': '/Salida_Lineas.csv', 'docu4': '/Original.jpg', 'docu1': '/Tabla.tex', 'docu5': '/Pintada.jpg'}
        
        configuracionxml.guardar(actual+'/Test/codigo/informes/fichero_pruebas',nombres,0,1,0,[0,50,20,30])
        
        self.assertEqual(os.path.exists(actual+'/Test/codigo/informes/fichero_pruebas/Proyecto.xml'),True)
        if os.path.exists(actual+'/Test/codigo/informes/fichero_pruebas/Proyecto.xml'):
            os.remove(actual+'/Test/codigo/informes/fichero_pruebas/Proyecto.xml')
        
        print("OK,test_guardar")
        
        
