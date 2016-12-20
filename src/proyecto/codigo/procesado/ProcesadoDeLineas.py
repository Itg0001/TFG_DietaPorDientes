import math
import numpy as np
class ProcesadoDeLineas():
    """
    Clase que va a contener las funciones necesarias para poder hacer
    el procesado de las lineas.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    
    @classmethod
    def combina(self, epsilon1, epsilon2, lines, g): 
        """
        Funcion que combina las lineas cercanas producidas por la Transformada probabilistica
        de hough que cumplen ciertos parametros y las anade a un grafo.

        @param epsilon1: Distancia que si superan dos rectas no une
        @param epsilon2: Angulo que si superan dos rectas no une
        @param lines: Lineas producidas al aplicar la transformada
        @param G: Grafo donde anadir los nodos que tengamso que unir
 
        @return: devolvemos el Grafo completo donde estan los nodos que hemso fusionado.
        """
        for i in range(len(lines)):
            g.add_node(i)

        for i in range(len(lines) - 1):
            for j in range(i + 1, len(lines)):
                self.comprueba(lines, i, j, epsilon1, epsilon2, g)
        return g
    
    
    def modulo(self,linea):
        p1,p2=linea 
        x1,y1 = p1
        x2,y2 = p2
        
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def combina2(self,distancia1,distancia2,diffOrientacion,longcorto,lines,G): 
        for i in range(len(lines)):
            G.add_node(i)

        for i in range(len(lines)-1):
            for j in range(i+1,len(lines)):
                d1 = self.segments_distance(lines[i],lines[j])
                d2 = self.segment_points_distance(lines[i],lines[j])
                         
                #paralelas y d1 menor que distancia1
                #consecutivas y d2 menor que distancia2
                if (d1<d2 and d1<distancia1) or (d1>=d2 and d2<distancia2): 
                    angle = self.ang(lines[i],lines[j])
                    
                    if angle <= diffOrientacion or self.modulo(lines[i])<longcorto or self.modulo(lines[j])<longcorto:
                        #print("combina ",i,j)
                        G.add_edge(i,j) 
        return G
    def segment_points_distance(self,seg1, seg2):
        """distance between two segments in the plane:
        one segment is (x11, y11) to (x12, y12)
        the other is   (x21, y21) to (x22, y22)
        """
        
        
        x11, y11 = seg1[0]
        x12, y12 = seg1[1]
        x21, y21 = seg2[0]
        x22, y22 = seg2[1]
        
        # try each of the 4 vertices w/the other segment
        distances = []
        distances.append(self.point_distance((x11, y11), (x21, y21)))
        distances.append(self.point_distance((x11, y11), (x22, y22)))
        distances.append(self.point_distance((x12, y12), (x21, y21)))
        distances.append(self.point_distance((x12, y12), (x22, y22)))
        return min(distances)
    
    def point_distance(self,p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return (dx*dx + dy*dy)**0.5
    @classmethod
    def comprueba(self, lines, i, j, epsilon1, epsilon2, g):
        """
        Metodo que comprueba si hay que añadirlo al grafo o no.
        
        @param lines: Lineas producidas al aplicar la transformada.
        @param i: variable i del bucle.
        @param j: variable j del bucle.
        @param epsilon1: Distancia que si superan dos rectas no une.
        @param epsilon2: Angulo que si superan dos rectas no une.
        @param g: grafo donde estan las lineas.
        """
        distance = self.segments_distance(lines[i], lines[j])
        if distance <= epsilon1 :
                    angle = self.ang(lines[i], lines[j])
                    if angle <= epsilon2:
                        g.add_edge(i, j) 
                        
    
    
    @classmethod 
    def segments_distance(self, x, y):
        """
        Funcion que calcula la distancia entre dos segmentos que no se cruzan.        
        
        @param x: puntos x e y del punto 1
        @param y: puntos x e y del punto 2
 
        @return: min(distances): la distancia minima de todas las posibles distancias
        """
        x1, y1 = x
        x11, y11 = x1
        x12, y12 = y1
        
        x2, y2, = y
        x21, y21 = x2
        x22, y22 = y2

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
        Funcion boleana que calcula si dos segmentos se cruzan o no.
        
        @param x: puntos x e y del punto 1.
        @param y: puntos x e y del punto 2.
        
        @return: true/false si se cruzan o no 
        """
        x1, y1 = x
        x11, y11 = x1
        x12, y12 = y1
                
        x2, y2, = y
        x21, y21 = x2
        x22, y22 = y2
        
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
        Funcion que calcula la distancia desde un punto dado a un segmento.
        @param px: Punto coordenada x 
        @param py: Punto coordenada y
        @param x1: Punto 1 coordenada x 
        @param y1: Punto 1 coordenada y
        @param x2: Punto 2 coordenada x 
        @param y2: Punto 2 coordenada y

        @return: Distancia desde el punto al segmento.
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
        Funcion que dadas dos rectas calcula el angulo que forman entre ellas.
        
        @return: ang_deg: Devuelve el angulo que forman dichas rectas en grados.
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
        Funcion que devuelve la multiplicacion de las coordenadas x de los dos puntos 
        mas la multiplicacion de las coordenadas y de los dos puntos.

        @param vA: Punto A.
        @param vB: Punto B.

        @return: la multiplicacion de las coordenadas x de los dos puntos 
               mas la multiplicacion de las coordenadas y de los dos puntos.
        """
        return v_a[0] * v_b[0] + v_a[1] * v_b[1]
    

    @classmethod
    def combina_segmentos(self, segmentos_list):
        """
        Lista con los segmentos combinados que calculamos con la teoria de grafos.
        
        @param segmentosList: lista con todos los segmentos a combinar
        Combinamos los segmentos.
        """
        xs = list(map(lambda x:[x[0][0], x[1][0]], segmentos_list))
        ys = list(map(lambda x:[x[0][1], x[1][1]], segmentos_list))
        x_max = np.max(xs)
        y_max = np.max(ys)
        x_min = np.min(xs)
        y_min = np.min(ys)
        if (x_max, y_max) in set(map(lambda x:x[0], segmentos_list)):
            return (x_max, y_max), (x_min, y_min)
        else:
            return (x_max, y_min), (x_min, y_max)
    @classmethod
    def filtra_contenidas(self,lineas,x_min,x_max,y_min,y_max,lon_min):
        lines_pintar=[]
        for i in lineas:
            existe_punto1=self.pertenece_o_no(i[0][0], i[0][1],x_min,x_max,y_min,y_max)
            existe_punto2=self.pertenece_o_no(i[1][0], i[1][1],x_min,x_max,y_min,y_max)
            if existe_punto1 and existe_punto2 and self.longitud_linea(i) > lon_min:
                lines_pintar.append(i)
        return lines_pintar
    @classmethod
    def filtra_intersec(self,lineas,cuadr,variables,lon_min):
        nuevas=[]
        x_min,x_max,y_min,y_max=variables
        for i in lineas:
            add=0
            p1,p2=i
            x1,y1=p1
            x2,y2=p2
            fl=0
            for j in cuadr:
                marc=0
                un=self.segments_intersect( i, j)
                existe_punto1=self.pertenece_o_no(i[0][0], i[0][1],x_min,x_max,y_min,y_max)
                existe_punto2=self.pertenece_o_no(i[1][0], i[1][1],x_min,x_max,y_min,y_max)
                if not existe_punto1 and fl!=1 and un:
                    tem_p1x,tem_p1y=self.seg_intersect(i,j)
                    x1=tem_p1x
                    y1=tem_p1y
                    add=1
                    marc=1
                    fl=1
                x2,y2,add=self.prueba_point2(existe_punto2, marc, un, i, j,[x2,y2,add])
                marc=0
            if add==1 and self.longitud_linea([(x1,y1),(x2,y2)]) > lon_min:
                nuevas.append([(x1,y1),(x2,y2)])
                add=0   
        return nuevas
    @classmethod
    def prueba_point2(self,existe_punto2,marc,un,i,j,dos):
        x2,y2,add=dos
        if not existe_punto2 and marc!=1 and un:
            tem_p2x,tem_p2y=self.seg_intersect(i,j)
            x2=tem_p2x
            y2=tem_p2y
            add=1
        return x2,y2,add
    @classmethod
    def pertenece_o_no(self,x,y,x_min,x_max,y_min,y_max):
        """
        En este metodo dado un punto y los 4 vertices del cuadrado comprobaremos
        si las coordenadas del punto pertenecen al area pintable.
        @param x: coordenada x del punto a comprobar.
        @param y: coordenada y del punto a comprobar.
        @param x_min: coordenada x minima del cuadrado
        @param x_max: coordenada x macima del cuadrado.
        @param y_min: coodenada y minima del cuadrado.
        @param y_max: coordenada y maxima del cuadrado.
        @return: true/false dependiendo si pertenece a esa region o no.     
        """
        if x == None and y==None:
            return False
        if (x_min< x < x_max) and  (y_min< y < y_max):
            return True
        else:
            return False
    @classmethod
    def perp( self,a ) :
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] =  a[0]
        return b
    @classmethod
    def seg_intersect(self,segment1, segment2) :
        a1, a2 = np.array(segment1)
        b1, b2 = np.array(segment2)    
        
        da = a2-a1
        db = b2-b1
        dp = a1-b1
        dap = self.perp(da)
        denom = np.dot( dap, db)
        num = np.dot( dap, dp )
        return list((num / denom.astype(float))*db + b1)
        
    @classmethod
    def longitud_linea(self, p, valor=100):
        """
        Funcion que calcula la longitud de un segmento.
        
        @param p: segmento del que calcular su distancia.
        
        @Return distancia del segmento
        """
        
        valor = int(valor)
        long_ref = int(valor)
        long_seg = (((p[1][0] - p[0][0]) ** 2) + ((p[1][1] - p[0][1]) ** 2)) ** (1 / 2)
        
        return (long_seg * valor) / long_ref
    
    @classmethod
    def segmentos_verdad(self, k_components, lines):
        """
        Funcion que dadas las lineas calculadas y las que nos marca el grafo que tenemso que unir
        devuelve lso segmentos que de verdad ha detectado el algoritmo.
        
        @param k_components: K_componentes del grafo en el que decimos que rectas tenemos que unir
        @param lines: lineas calculadas por la tranformada de hough
        
        @return: segmentos_de_verdad: lista de los segmentos que tienen.
        """
        segmentos_de_verdad = []
        for i in range(len(k_components[1])):
            segmentos = list(map(lambda x:lines[x], k_components[1][i]))           
            segmentos_de_verdad.append(self.combina_segmentos(segmentos))
        return segmentos_de_verdad
   
