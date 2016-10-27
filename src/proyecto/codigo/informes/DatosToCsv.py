import csv
from proyecto.codigo.informes.InGuardarDatos import InGuardarDatos

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
        csvsalida_lin = open(path.replace('\\', '/') + '/' + 'Salida_Lineas.csv', 'w', newline='')
        salida = csv.writer(csvsalida_lin, escapechar=' ', quoting=csv.QUOTE_NONE, delimiter=';')
        salida.writerow(['linea', 'angulo', 'tamano', 'tipo'])  
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
            
        csvsalida_stat = open(path.replace('\\', '/') + '/' + 'Salida_Estadisticas.csv', 'w', newline='')
        salida = csv.writer(csvsalida_stat, escapechar=' ', quoting=csv.QUOTE_NONE, delimiter=';')
        salida.writerow(['tipo', 'numero', 'mediaLon', 'desviacionTip'])
        salida.writerow(lista[4])
        salida.writerow(lista[5])
        salida.writerow(lista[6])
        salida.writerow(lista[7])
        salida.writerow(lista[8])
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
    
    