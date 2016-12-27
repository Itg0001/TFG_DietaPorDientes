import csv
from proyecto.analisis.informes.InGuardarDatos import InGuardarDatos
from proyecto.analisis.diccionario import Diccionario

class DatosToCsv(InGuardarDatos):
    """
    Clase que va a encargarse de dados unos datos pasarlos a dos ficheros csv: un fichero csv, en el 
    que se encontraran las lineas,su longitud ,su angulo y su direccion, otro en el que se encontraran almacenadas 
    las estadisticas de las lineas en conjunto y en cada grupo.
    
    @author: Ismael Tobar Garcia
    @version: 1.0    
    """
    
    @classmethod    
    def guardar(self, path, lista):
        """
        Metodo que permitira generar los scv de datos de las lineas uno con sus estadisticos 
        y otro con la longitud y el angulo de cada recta o segmento.
        
        @param path: Camino donde guardar los ficheros generados.
        
        @param lista:
                    v: lista de lineas en vertical.
                    h: lista de lineas en horizontal.
                    md: lista de lineas en diagonal md.
                    dm: lista de lineas en diagonal dm.
                    st_v: estadisticas de lineas en vertical.
                    st_h: estadisticas de lineas en horizontal.
                    st_md: estadisticas de lineas en diagonal md.
                    st_dm: estadisticas de lineas en diagonal dm.
                    st_tot: estadisticas totales de lineas.
        """
        
        self.dic=Diccionario()

        csvsalida_lin = open(path.replace('\\', '/') + self.dic.sal_lin, 'w', newline='')
        salida = csv.writer(csvsalida_lin, escapechar=' ', quoting=csv.QUOTE_NONE, delimiter=';')
        salida.writerow(self.dic.cabecera_csv_lineas)  
        if len(lista[0]) > 0:
            salida.writerows(lista[0])
        if len(lista[1]) > 0:
            salida.writerows(lista[1])        
        if len(lista[2]) > 0:
            salida.writerows(lista[2])
        if len(lista[3]) > 0:
            salida.writerows(lista[3])
        del salida
        csvsalida_lin.close()

        desv_v=float(lista[4][3])
        num_h=float(lista[5][1])
        med_h=float(lista[5][2])
        desv_h=float(lista[5][3])
        num_md=float(lista[6][1])
        desv_dm=float(lista[7][3])
        num_tot=float(lista[8][1])
        med_tot=float(lista[8][2])
        desv_tot=float(lista[8][3])

        f1=round((0.11364*num_h)-(0.03017*num_md)-(0.00169*desv_dm)-(0.01485*med_tot)+(0.00958*desv_tot)-(-0.00468*desv_v)+(0.00454*med_h)+(0.00203*num_tot)+0.06819,3)
        f2=round((-0.05361*num_h)+(0.09573*num_md)+(0.00730*desv_h)-(0.01340*med_tot)-(0.00922*desv_tot)+(0.01098*desv_v)+(0.00061*med_h)+(0.03253*num_tot)-0.42014,3)
        pt1="punto_x"
        pt2="punto_y"
        punto=[]
        punto.extend([pt1,f1,pt2,f2])
        
        csvsalida_stat = open(path.replace('\\', '/') + self.dic.sal_estad, 'w', newline='')
        salida = csv.writer(csvsalida_stat, escapechar=' ', quoting=csv.QUOTE_NONE, delimiter=';')
        salida.writerow(self.dic.cabecera_csv_estad)
        salida.writerow(lista[4])
        salida.writerow(lista[5])
        salida.writerow(lista[6])
        salida.writerow(lista[7])
        salida.writerow(lista[8])
        salida.writerow(punto)

 
        del salida
        csvsalida_stat.close()
        
    @classmethod    
    def leer(self,path):
        """
        Metodo que a partir de la ruta de un fichero csv leera la configuracion y lo guardara en una
        lista.
        
        @param path: Camino donde leer el fichero csv.

        @return segmentos: Lista con las lineas o segmentos.
        """
        segmentos=[]
        with open(path, 'rt') as csvfile:
            reader = csv.reader(csvfile, escapechar=' ', quoting=csv.QUOTE_NONE, delimiter=';')
            flag=0
            for row in reader:
                if flag==0:
                    flag=1
                else:
                    segmentos.append(row[0])
        return segmentos
    
    