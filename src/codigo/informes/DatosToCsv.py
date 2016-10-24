import csv
from codigo.informes.InGuardarDatos import InGuardarDatos
class DatosToCsv(InGuardarDatos):

    
    @classmethod    
    def guardar(self, path, lista):
        
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
    
    