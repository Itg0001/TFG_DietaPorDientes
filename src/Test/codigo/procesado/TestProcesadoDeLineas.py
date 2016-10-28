import unittest
from proyecto.codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas
import networkx as nx
from networkx.algorithms import approximation as apxa

class TestProcesadoDeLineas(unittest.TestCase):

    def test_combina(self):
        procesado=ProcesadoDeLineas()
        g=nx.Graph()
        lines=[((128, 72), (164, 18)), ((24, 43), (12, 31)), ((55, 71), (31, 49)), ((136, 59), (163, 19)), ((11, 31), (4, 24)), ((34, 51), (25, 43)), ((109, 42), (90, 18)), ((51, 67), (30, 48)), ((116, 50), (92, 20))]        
        graf=procesado.combina(8, 4, lines, g)
        
        self.assertEqual(graf.nodes(),[0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(graf.edges(),[(0, 3), (1, 4), (1, 5), (1, 7), (2, 5), (2, 7), (5, 7), (6, 8)])
      
        self.assertNotEqual(graf.nodes(),[])
        self.assertNotEqual(graf.edges(),[])
    
        g=nx.Graph()
        graf=procesado.combina(8, 4, [], g)

        self.assertEqual(graf.nodes(),[])
        self.assertEqual(graf.edges(),[])

        print("OK,test_combina")
    def test_segments_distance(self):
        procesado=ProcesadoDeLineas()
        x=((128, 72), (164, 18))
        y=((24, 43), (12, 31)) 
        dist=procesado.segments_distance(x, y)       
        
        self.assertEqual(round(dist,2),107.97)
        
        
        y=((18, 164), (128, 72)) 
        dist=procesado.segments_distance(x, y) 
        
        self.assertEqual(dist,0)
        
        try:
            procesado.segments_distance(0,0)
        except TypeError as ex:
            self.assertEqual(ex.args[0],'\'int\' object is not subscriptable')
        print("OK,test_segments_distance")

    def test_segments_intersect(self):
        procesado=ProcesadoDeLineas()
        x=((128, 72), (164, 18))
        y=((24, 43), (12, 31)) 
        intersec=procesado.segments_intersect(x, y)  
        
        self.assertEqual(intersec,False)
        
        y=((18, 164), (128, 72)) 
        intersec=procesado.segments_intersect(x, y)
        self.assertEqual(intersec,True)

        try:
            intersec=procesado.segments_intersect(0,0)
        except TypeError as ex:
            self.assertEqual(ex.args[0],'\'int\' object is not subscriptable')
        print("OK,test_segments_intersect")
        
        
    def test_point_segment_distance(self):
        procesado=ProcesadoDeLineas()
        x=((128, 72), (164, 18))
        y=((24, 43), (12, 31)) 

        dist=procesado.point_segment_distance( x[0][0], x[0][1], y[0][0], y[1][0], y[0][0], y[1][0])
        self.assertEqual(round(dist,2),120.07)
        
        
        dist=procesado.point_segment_distance( x[0][0], x[0][1], y[0][0], y[1][0], y[0][1], y[1][1])
        self.assertEqual(round(dist,2),94.37)
        
        y=((24, 43), (1, 100)) 
        dist=procesado.point_segment_distance( x[0][0], x[0][1], y[0][0], y[1][0], y[0][1], y[1][1])
        self.assertEqual(round(dist,2),88.75)        
        
        
        y=((24, 43), (1, 1900)) 
        dist=procesado.point_segment_distance( x[0][0], x[0][1], y[0][0], y[1][0], y[0][1], y[1][1])
        self.assertEqual(round(dist,2),103.28)        

        print("OK,test_point_segment_distance")
        
    def test_ang(self):
        procesado=ProcesadoDeLineas()
        x=((128, 72), (164, 18))
        y=((24, 43), (12, 31)) 

        ang = procesado.ang(x, y)
        self.assertEqual(round(ang,2),78.69)  

        x=((820, 257), (826, 242))
        y=((820, 254), (822, 249))
        ang = procesado.ang(x, y)
        self.assertEqual(round(ang,2),0.0)  
        
        x=((871, 183), (892, 183))
        y=((910, 182), (893, 182))
        ang = procesado.ang(x, y)
        self.assertEqual(round(ang,2),180.0)  

        print("OK,test_ang")
        
        
    def test_dot(self):
        procesado=ProcesadoDeLineas()
        x=(871, 183)
        y=(892, 183)
        dot=procesado.dot(x, y)
        
        self.assertEqual(dot,810421)  

        try:
            dot=procesado.dot([], [])
        except IndexError as ast:
            self.assertEqual(ast.args[0],'list index out of range')
                        
        print("OK,test_segments_distance")
        
    def test_combina_segmentos(self):        
        procesado=ProcesadoDeLineas()
        segmentos=[((128, 72), (164, 18)), ((136, 59), (163, 19))]
        
        combinado=procesado.combina_segmentos(segmentos)
        self.assertEqual(combinado,((164, 18), (128, 72)))


        segmentos=[((670, 196), (661, 185)), ((680, 209), (674, 201)), ((685, 215), (681, 210)), ((677, 206), (659, 183))]
        combinado=procesado.combina_segmentos(segmentos)
        self.assertEqual(combinado,((685, 215), (659, 183)))
        
        try:
            combinado=procesado.combina_segmentos([])        
        except ValueError as ver:
            self.assertEqual(ver.args[0],'zero-size array to reduction operation maximum which has no identity')        
        print("OK,test_combina_segmentos")

    def test_segmentos_verdad(self):
        procesado=ProcesadoDeLineas()
        g=nx.Graph()
        lines=[((128, 72), (164, 18)), ((24, 43), (12, 31)), ((55, 71), (31, 49)), ((136, 59), (163, 19)), ((11, 31), (4, 24)), ((34, 51), (25, 43)), ((109, 42), (90, 18)), ((51, 67), (30, 48)), ((116, 50), (92, 20))]        
        g=procesado.combina(8, 4, lines, g)
        k_components = apxa.k_components(g)
        
        segmentos_de_verdad = procesado.segmentos_verdad(k_components, lines)
        self.assertEqual(segmentos_de_verdad,[((164, 18), (128, 72)), ((55, 71), (4, 24)), ((116, 50), (90, 18))])

        print("OK,test_segmentos_verdad")
        

    
