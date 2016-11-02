import math
from proyecto.diccionario import Diccionario

class Estadistica():
    """
    Clase que se encargara de calcular las estadisticas de una conjunto de rectas dadas
    dependiendo de esto las agrupara y calculara sus atributos como distancia , numero de cada
    tipo o angulo de cada recta para tener una informacion mas especifica de lo detectado.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """

        
    @classmethod    
    def clasificar(self, segmentos, angulos, long_segmento):
        
        """
        Guardado como matriz de adyacencia.
        En esta funcion lo que vamso a hacer es a partir de los datos de las lineas dados
        clasificar en las direcciones apropiadas.
        
        @param segmentos: Lista con las lineas que hemso encontrado.
        @param angulos: diccionario clave(linea) valor(angulo) de todas las lineasGuardado como matriz de adyacencia.
        @param long_segmento: diccionario clave(linea) valor(longitud) de todas las lineas.
                
        @Return v: Lineas en vertical.
        @Return h: Lineas en horizontal.
        @Return md: Lineas en diagonal md.
        @Return dm:Lineas en diagonal dm.
        @Return total: todas las lioneas con sus valores.        
        """
        self.dic=Diccionario()

        v, h, md, dm, total = [], [], [], [], []  
        # CLASIFICAR LAS RECTAS POR SUS ANGULOS
        for i in segmentos:
            if 67.5 < angulos[i] < 112.5: 
                v.append((i, str(round(angulos[i], 2)).replace('.', ','), str(round(long_segmento[i], 2)).replace('.', ','), self.dic.v))
            elif 22.5 < angulos[i] < 67.5:
                md.append((i, str(round(angulos[i], 2)).replace('.', ','), str(round(long_segmento[i], 2)).replace('.', ','), self.dic.md))
                
            elif 112.5 < angulos[i] < 157.5:
                dm.append((i, str(round(angulos[i], 2)).replace('.', ','), str(round(long_segmento[i], 2)).replace('.', ','), self.dic.dm))
                
            elif (0 < angulos[i] < 22.5) or (157.5 < angulos[i] < 180):                
                h.append((i, str(round(angulos[i], 2)).replace('.', ','), str(round(long_segmento[i], 2)).replace('.', ','), self.dic.h))
        total.extend(v)
        total.extend(h)
        total.extend(md)
        total.extend(dm)
        return v, h, md, dm, total
    
    @classmethod       
    def stadisticas(self, tipo, numero, media_lon, desviacion_tip):
        """
        Metodo que va a llamar a las funcines de calculo de las estadisticas para
        poder mostrarlas mas adelante en el csv y poder guardarlas para el informe.
        
        @param tipo: tipo de recta entre los 4 posibles +total.
        @param numero: numero de ellas que hay.
        @param media_lon: media de la longitud.
        @param desviacion_tip: desviacion tipica de la longitud.
        
        @Return lista: Con toda la informacion.
        """
        lista = []
        lista.append(tipo)
        lista.append(numero)
        if media_lon != None and desviacion_tip!=None:
            lista.append(str(round(media_lon, 2)).replace(',', '.'))
            lista.append(str(round(desviacion_tip, 2)).replace(',', '.'))
        return lista
    
    @classmethod        
    def desviacion_tipica(self, lista_distancias):
        """
        Funcion que calcula la desviacion tipica de ladistacia.
        
        @param lista_distancias: lista con las distancias de cada recta.

        @Return Desviacion tipica.
        """
        if len(lista_distancias)!=0:
            media = self.media_long_segmentos(lista_distancias)
            acumulador = 0
            for i in lista_distancias:
                acumulador += (float(str(i[2]).replace(',', '.')) - media) ** 2
            return (acumulador / len(lista_distancias)) ** (1 / 2)
        else:
            return None
    @classmethod        
    def media_long_segmentos(self, lista_distancias):
        """
        Funcion que calcula la media de la longitud de los segmentos.
        
        @param lista_distancias: lsita de rectas con sus distancias.

        @Return meida de la longitud de la lista que entra.
        """
        if len(lista_distancias)!=0:
            media = 0
            for i in lista_distancias:
                media += float(str(i[2]).replace(',', '.'))
            return media / len(lista_distancias)
        else:
            return None
    @classmethod            
    def longitud_segemento(self, p,r,valor=100):
        """
        Funcion que calcula la longitud de un segmento.
        
        @param p: segmento del que calcular su distancia.
        
        @Return distancia del segmento
        """
        
        valor=int(valor)
        long_ref=int(valor)
        long_seg=(((p[1][0] - p[0][0]) ** 2) + ((p[1][1] - p[0][1]) ** 2)) ** (1 / 2)
        
        return (long_seg*valor)/long_ref
    
    @classmethod
    def angu(self, line_a):
        """
        Funcion que calcula el angulo de una recta con respecto el eje x
        
        @param line_a: Una linea (2puntos)
        
        @Return Angulo en grados.
        """
        # Get nicer vector form
        if line_a[1][0] - line_a[0][0] != 0:
            m = (line_a[1][1] - line_a[0][1]) / (line_a[1][0] - line_a[0][0])
        else:
            return 90
        angle = math.atan(m)
        # Basically doing angle <- angle mod 360
        ang_deg = math.degrees(angle)

        ang_deg = ang_deg % 360

        if ang_deg > 180:
            return ang_deg - 180
        else:
            return ang_deg

    @classmethod    
    def calcular_estadisticas(self, v, h, md, dm, total):
        """
        
        Metodo que llamara a los anteriorres y calculara
        los datos estadisticos de todas las rectas en su clasificacion.
        
        @param v: Rectas o segmentos en vertical.
        @param h: Rectas o segmentos en horizontal.
        @param md: Rectas o segmentos en diagonal md.
        @param dm: Rectas o segmentos en diagonal dm.
        @param total: todas las Rectas o segmentos.
        
        @Return st_v: estadisticas de segmentos en vertical.
        @Return st_h: estadisticas de segmentos en horizontal.
        @Return st_md: estadisticas de segmentos en diagonal md.
        @Return st_dm: estadisticas de segmentos en diagonal dm.
        @Return st_tot: estadisticas de segmentos totales.
        @Return variables_tabla: estadisticas de segmentos totales sin el tipo.
            
        """
        st_v, st_h, st_md, st_dm = [], [], [], [] 
        variables_tabla = []
        if len(v) > 0:
            st_v = self.stadisticas(self.dic.v, len(v), self.media_long_segmentos(v), self.desviacion_tipica(v))
            variables_tabla.extend(st_v[1:4])
        else:
            variables_tabla.extend([0, 0, 0])       
        if len(h) > 0:
            st_h = self.stadisticas(self.dic.h, len(h), self.media_long_segmentos(h), self.desviacion_tipica(h))
            variables_tabla.extend(st_h[1:4])
        else:
            variables_tabla.extend([0, 0, 0])
        if len(md) > 0:
            st_md = self.stadisticas(self.dic.md, len(md), self.media_long_segmentos(md), self.desviacion_tipica(md))
            variables_tabla.extend(st_md[1:4])
        else:
            variables_tabla.extend([0, 0, 0])        
        if len(dm) > 0:
            st_dm = self.stadisticas(self.dic.dm, len(dm), self.media_long_segmentos(dm), self.desviacion_tipica(dm))
            variables_tabla.extend(st_dm[1:4])
        else:
            variables_tabla.extend([0, 0, 0])
        st_tot = self.stadisticas(self.dic.totales, len(total), self.media_long_segmentos(total), self.desviacion_tipica(total))        
        variables_tabla.extend(st_tot[1:4])
        return st_v, st_h, st_md, st_dm, st_tot, variables_tabla
