import unittest,os
from proyecto.codigo.informes.Informe import Informe

class TestInforme(unittest.TestCase):
    
    def test_cargar_plantilla(self):
        variables=[0, 0, 0, 0, 0, 0, 2, '55.29', '14.06', 1, '64.9', '0.0', 3, '58.49', '12.34']
        actual = os.getcwd()
        infor=Informe(variables,actual+'/Test/codigo/informes/fichero_pruebas')
        template=infor.cargar_plantilla()
        self.assertEqual(str(template),'<Template \'jinja-test.tex\'>')

        print("OK,test_cargar_plantilla")
    
    def test_sustituir(self):
        variables=[0, 0, 0, 0, 0, 0, 2, '55.29', '14.06', 1, '64.9', '0.0', 3, '58.49', '12.34']
        actual = os.getcwd()
        infor=Informe(variables,actual+'/Test/codigo/informes/fichero_pruebas')
        template=infor.cargar_plantilla()
        cop=False #@UnusedVariable   
        infor.sustituir(variables, template)
        cop=True
        self.assertEqual(cop,True)

        print("OK,test_sustituir")
