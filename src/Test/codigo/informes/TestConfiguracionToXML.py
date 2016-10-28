import unittest,os
from proyecto.codigo.informes.ConfiguracionToXML import ConfiguracionToXML

class TestConfiguracionToXML(unittest.TestCase):
    
    def test_guardar(self):
        configuracionxml=ConfiguracionToXML()
        actual = os.getcwd()

        configuracionxml.guardar(actual+'/Test/codigo/informes/fichero_pruebas')
        
        self.assertEqual(os.path.exists(actual+'/Test/codigo/informes/fichero_pruebas/Proyecto.xml'),True)
        if os.path.exists(actual+'/fichero_pruebas/Proyecto.xml'):
            os.remove(actual+'/fichero_pruebas/Proyecto.xml')
        
        print("OK,test_guardar")
        
        
