import unittest,os
from proyecto.codigo.informes.Informe import Informe

class TestInforme(unittest.TestCase):
    
    def test_cargar_plantilla(self):
        variables=[0, 0, 0, 0, 0, 0, 2, '55.29', '14.06', 1, '64.9', '0.0', 3, '58.49', '12.34']
        actual = os.getcwd()
        infor=Informe(variables,actual+'/Test')
        template=infor.cargar_plantilla()
        print("ESTO ES LO QUE IMPORTA",str(template))
        self.assertEqual(str(template),'<Template \'proyecto/codigo/informes/jinja-test.tex\'>')

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
        os.remove(actual+'/Test/Tabla.tex')
        print("OK,test_sustituir")
