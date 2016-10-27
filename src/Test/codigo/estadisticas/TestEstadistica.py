from proyecto.codigo.estadisticas.Estadistica import Estadistica
import unittest

class TestEstadistica(unittest.TestCase):
       
    def test_clasificar(self):
        estadistica = Estadistica()

        segmentos = [((538, 5), (523, 951)), ((3, 478), (1272, 500)), ((1267, 5), (7, 947)), ((5, 5), (1267, 947))]
        angulos = {((3, 478), (1272, 500)): 0.9932079501041022, ((5, 5), (1267, 947)): 36.73891946007598, ((538, 5), (523, 951)): 90.90841932025899, ((1267, 5), (7, 947)): 143.2175100354142}
        long_segmento = {((3, 478), (1272, 500)): 1269.190687012791, ((5, 5), (1267, 947)): 1574.8041148028537, ((538, 5), (523, 951)): 946.1189143020025, ((1267, 5), (7, 947)): 1573.2018306625505}
        
 
        v, h, md, dm, total = estadistica.clasificar(segmentos, angulos, long_segmento)
        self.assertEqual(v, [(((538, 5), (523, 951)), '90,91', '946,12', 'v')])
        self.assertEqual(h, [(((3, 478), (1272, 500)), '0,99', '1269,19', 'h')])
        self.assertEqual(md, [(((5, 5), (1267, 947)), '36,74', '1574,8', 'md')])
        self.assertEqual(dm, [(((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')])
        self.assertEqual(total, [(((538, 5), (523, 951)), '90,91', '946,12', 'v'), (((3, 478), (1272, 500)), '0,99', '1269,19', 'h'), (((5, 5), (1267, 947)), '36,74', '1574,8', 'md'), (((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')])

        v, h, md, dm, total = estadistica.clasificar([], [], [])
        
        self.assertEqual(v, [])
        self.assertEqual(h, [])
        self.assertEqual(md, [])
        self.assertEqual(dm, [])
        self.assertEqual(total, [])

        print("OK,test_clasificar")
        
    def test_stadisticas(self):
        estadistica = Estadistica()
        tipo, numero, media_lon, desviacion_tip = 'v', 1, 946.12, 0.0
        
        lista = estadistica.stadisticas(tipo, numero, media_lon, desviacion_tip)
        self.assertEqual(lista, [tipo, numero, str(media_lon), str(desviacion_tip)])
        
        lista = estadistica.stadisticas(0, 0, 0, 0)
        self.assertEqual(lista, [0, 0, str(0), str(0)])
        
        print("OK,test_stadisticas")

    def test_desviacion_tipica(self):
        estadistica = Estadistica()
        lista_distancias=[(((538, 5), (523, 951)), '90,91', '946,12', 'v'), (((3, 478), (1272, 500)), '0,99', '1269,19', 'h'), (((5, 5), (1267, 947)), '36,74', '1574,8', 'md'), (((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')]
        
        val=estadistica.desviacion_tipica(lista_distancias)
        self.assertEqual(round(val,2), round(259.6469003642254,2))

        val=estadistica.desviacion_tipica([])
        self.assertEqual(val, None)

        print("OK,test_desviacion_tipica")
        
    def test_media_long_segmentos(self):
        estadistica = Estadistica()
        lista_distancias=[(((538, 5), (523, 951)), '90,91', '946,12', 'v'), (((3, 478), (1272, 500)), '0,99', '1269,19', 'h'), (((5, 5), (1267, 947)), '36,74', '1574,8', 'md'), (((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')]
        
        val=estadistica.media_long_segmentos(lista_distancias)
        self.assertEqual(round(val,2), round(1340.8274999999999,2))
        
        val=estadistica.media_long_segmentos([])
        self.assertEqual(val, None)

        print("OK,test_media_long_segmentos")
    
    def test_longitud_segemento(self):
        estadistica = Estadistica()
        segmento=((538, 5), (523, 951))
        
        lon=estadistica.longitud_segemento(segmento)
        self.assertEqual(round(lon,2), 946.12)
        
        try:
            lon=estadistica.longitud_segemento([])
        except IndexError as ex:
            self.assertEqual(ex.args[0], "list index out of range")
            
        print("OK,test_longitud_segemento")
        
    def test_angu(self):
        estadistica = Estadistica()
        segmento=((538, 5), (523, 951))
        
        ang=estadistica.angu(segmento)
        self.assertEqual(round(ang,2), 90.91)
        
        try:
            ang=estadistica.longitud_segemento([])
        except IndexError as ex:
            self.assertEqual(ex.args[0], "list index out of range")
            
        print("OK,test_angu")
    def test_calcular_estadisticas(self):
        estadistica = Estadistica()
        
        v=[(((538, 5), (523, 951)), '90,91', '946,12', 'v')]
        h=[(((3, 478), (1272, 500)), '0,99', '1269,19', 'h')] 
        md=[(((5, 5), (1267, 947)), '36,74', '1574,8', 'md')] 
        dm=[(((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')]
        total=[(((538, 5), (523, 951)), '90,91', '946,12', 'v'), (((3, 478), (1272, 500)), '0,99', '1269,19', 'h'), (((5, 5), (1267, 947)), '36,74', '1574,8', 'md'), (((1267, 5), (7, 947)), '143,22', '1573,2', 'dm')]
        
        st_v, st_h, st_md, st_dm, st_tot, variables_tabla=estadistica.calcular_estadisticas(v, h, md, dm, total)
        
        self.assertEqual(st_v, ['v', 1, '946.12', '0.0'])
        self.assertEqual(st_h, ['h', 1, '1269.19', '0.0'])
        self.assertEqual(st_md, ['md', 1, '1574.8', '0.0'])
        self.assertEqual(st_dm, ['dm', 1, '1573.2', '0.0'])
        self.assertEqual(st_tot, ['totales', 4, '1340.83', '259.65'])
        self.assertEqual(variables_tabla, [1, '946.12', '0.0', 1, '1269.19', '0.0', 1, '1574.8', '0.0', 1, '1573.2', '0.0', 4, '1340.83', '259.65'])
        
        try:
            st_v, st_h, st_md, st_dm, st_tot, variables_tabla=estadistica.calcular_estadisticas([], [], [], [], [])
        except IndexError as ie:
            self.assertEqual(ie.args[0], "list index out of range")
        except TypeError as te:
            self.assertEqual(te.args[0], "type NoneType doesn't define __round__ method")

        print("OK,test_calcular_estadisticas")
        
