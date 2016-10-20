import math
import numpy as np
class ProcesadoDeLineas():
    
    @classmethod
    def combina(self, epsilon1, epsilon2, lines, g): 
        """
        Entrada:
               epsilon1: Distancia que si superan dos rectas no une
               epsilon2: Angulo que si superan dos rectas no une
               lines: Lineas producidas al aplicar la transformada
               G: Grafo donde anadir los nodos que tengamso que unir
        Funcion que combina las lineas cercanas producidas por la Transformada probabilistica
        de hough que cumplen ciertos parametros y las anade a un grafo. 
        RETURN: devolvemos el Grafo completo donde estan los nodos que hemso fusionado.
        """
        for i in range(len(lines)):
            g.add_node(i)

        for i in range(len(lines) - 1):
            for j in range(i + 1, len(lines)):
                self.comprueba(lines, i, j, epsilon1, epsilon2, g)
        return g
    
    @classmethod
    def comprueba(self, lines, i, j, epsilon1, epsilon2, g):
        distance = self.segments_distance(lines[i], lines[j])
        if distance <= epsilon1 :
                    angle = self.ang(lines[i], lines[j])
                    # print(distance)
                    if angle <= epsilon2:
                        # print("combina ",i,j)
                        g.add_edge(i, j) 
                        
    
    
    @classmethod 
    def segments_distance(self, x, y):
        """
        Entrada:
               x11: Segmento 1 Punto 1 coordedana x
               y11: Segmento 1 Punto 1 coordedana y
               x12: Segmento 1 Punto 2 coordedana x
               y12: Segmento 1 Punto 2 coordedana y 
               x21: Segmento 2 Punto 1 coordedana x
               y21: Segmento 2 Punto 1 coordedana y
               x22: Segmento 2 Punto 2 coordedana x
               y22: Segmento 2 Punto 2 coordedana y
        Funcion que calcula la distancia entre dos segmentos que no se cruzan 
        RETURN: min(distances) la distancia minima de todas las posibles distancias
        """
        x11 = x[0][0]
        y11 = x[0][1]
        x12 = x[1][0]
        y12 = x[1][1]
        
        x21 = y[0][0]
        y21 = y[0][1]       
        x22 = y[1][0]        
        y22 = y[1][1]
        

        if self.segments_intersect(x, y): 
                return 0
        # try each of the 4 vertices w/the other segment
        distances = []
        distances.append(self.point_segment_distance(x11, y11, x21, y21, x22, y22))
        distances.append(self.point_segment_distance(x12, y12, x21, y21, x22, y22))
        distances.append(self.point_segment_distance(x21, y21, x11, y11, x12, y12))
        distances.append(self.point_segment_distance(x22, y22, x11, y11, x12, y12))
        return min(distances)
    
    
    @classmethod
    def segments_intersect(self, x, y):
        """ 
        Entrada:
               x11: Segmento 1 Punto 1 coordedana x
               y11: Segmento 1 Punto 1 coordedana y
               x12: Segmento 1 Punto 2 coordedana x
               y12: Segmento 1 Punto 2 coordedana y 
               x21: Segmento 2 Punto 1 coordedana x
               y21: Segmento 2 Punto 1 coordedana y
               x22: Segmento 2 Punto 2 coordedana x
               y22: Segmento 2 Punto 2 coordedana y
        Funcion boleana que calcula si dos segmentos se cruzan o no
        RETURN: true/false si se cruzan o no 
        """
        x11 = x[0][0]
        y11 = x[0][1]
        x12 = x[1][0]
        y12 = x[1][1]
        
        x21 = y[0][0]
        y21 = y[0][1]       
        x22 = y[1][0]        
        y22 = y[1][1]
        
        dx1 = x12 - x11
        dy1 = y12 - y11
        dx2 = x22 - x21
        dy2 = y22 - y21
        delta = dx2 * dy1 - dy2 * dx1
        if delta == 0: 
            return False  # parallel segments
        s = (dx1 * (y21 - y11) + dy1 * (x11 - x21)) / delta
        t = (dx2 * (y11 - y21) + dy2 * (x21 - x11)) / (-delta)
        return (0 <= s <= 1) and (0 <= t <= 1)
    
     
    @classmethod
    def point_segment_distance(self, px, py, x1, y1, x2, y2):
        """
        Entrada:
               px: Punto coordenada x 
               py: Punto coordenada y
               x1: Punto 1 coordenada x 
               y1: Punto 1 coordenada y
               x2: Punto 2 coordenada x 
               y2: Punto 2 coordenada y
        Funcion que calcula la distancia desde un punto dado a un segmento.
        RETURN: DIstancia desde el punto al segmento
        """
        dx = x2 - x1
        dy = y2 - y1
        if dx == dy == 0:  # the segment's just a point
            return math.hypot(px - x1, py - y1)

        # Calculate the t that minimizes the distance.
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

        # See if this represents one of the segment's
        # end points or a point in the middle.
        if t < 0:
            dx = px - x1
            dy = py - y1
        elif t > 1:
            dx = px - x2
            dy = py - y2
        else:
            near_x = x1 + t * dx
            near_y = y1 + t * dy
            dx = px - near_x
            dy = py - near_y

        return math.hypot(dx, dy)
    
    @classmethod
    def ang(self, line_a, line_b):
        """
        Entrada:
               lineA:linea o segmento A
               lineB:linea o segmento A
        Funcion que dadas dos rectas calcula el angulo que forman entre ellas.
        Return ang_deg: Devuelve el angulo que forman dichas rectas en grados.
        """
        # Get nicer vector form
        v_a = [line_a[0][0] - line_a[1][0], line_a[0][1] - line_a[1][1]]
        v_b = [line_b[0][0] - line_b[1][0], line_b[0][1] - line_b[1][1]]
        # Get dot prod
        dot_prod = self.dot(v_a, v_b)
        # Get magnitudes
        mag_a = self.dot(v_a, v_a) ** 0.5
        mag_b = self.dot(v_b, v_b) ** 0.5
        # Get cosine value
        cos_ = dot_prod / mag_a / mag_b
        if cos_ > 1: 
            cos_ = 1
        # Get angle in radians and then convert to degrees
        angle = math.acos(cos_)
        # Basically doing angle <- angle mod 360
        ang_deg = math.degrees(angle) % 360

        if ang_deg - 180 >= 0:
            # As in if statement
            return 360 - ang_deg
        else: 
            return ang_deg
    
    
    @classmethod
    def dot(self, v_a, v_b):
        """
        Entrada:
               vA: Punto A
               vB: Punto B
        Funcion que devuelve la multiplicacion de las coordenadas x de los dos puntos 
        mas la multiplicacion de las coordenadas y de los dos puntos
        Return: la multiplicacion de las coordenadas x de los dos puntos 
               mas la multiplicacion de las coordenadas y de los dos puntos
        """
        return v_a[0] * v_b[0] + v_a[1] * v_b[1]
    
    
    
    @classmethod
    def combina_segmentos(self, segmentos_list):
        """
        Entrada: segmentosList lista con todos los segmentos a combinar
        Combinamos los segmentos
        Lista con los segmentos combinados que calculamos con la teoria de grafos.
        """
        # print("combina",segmentos_list)
        xs = list(map(lambda x:[x[0][0], x[1][0]], segmentos_list))
        ys = list(map(lambda x:[x[0][1], x[1][1]], segmentos_list))
        x_max = np.max(xs)
        y_max = np.max(ys)
        x_min = np.min(xs)
        y_min = np.min(ys)
        if (x_max, y_max) in set(map(lambda x:x[0], segmentos_list)):
            # print("devuelvo",((x_max,y_max),(x_min,y_min)))
            return (x_max, y_max), (x_min, y_min)
        else:
            # print("devuelvo",((x_max,y_min),(x_min,y_max)))
            return (x_max, y_min), (x_min, y_max)
        
   
    @classmethod
    def segmentos_verdad(self, k_components, lines):
        """
        Entrada.
               k_components K_componentes del grafo en el que decimos que rectas tenemos que unir
               lines lineas calculadas por la tranformada de hough
        Funcion que dadas las lineas calculadas y las que nos marca el grafo que tenemso que unir
        devuelve lso segmentos que de verdad ha detectado el algoritmo
        """
        segmentos_de_verdad = []
        for i in range(len(k_components[1])):
            segmentos = list(map(lambda x:lines[x], k_components[1][i]))
            segmentos_de_verdad.append(self.combina_segmentos(segmentos))
        return segmentos_de_verdad
   
