import csv
class DatosToCsv():
    @classmethod    
    def escribe_csv(self,path,lista):
        
        csvsalida = open(path+'/'+'salidat.csv', 'w', newline='')
        salida = csv.writer(csvsalida,escapechar=' ',quoting=csv.QUOTE_NONE,delimiter=';')
        salida.writerow(['linea','angulo','tamano','tipo'])  
        if len(lista[0])>0:
            salida.writerows(lista[0])       
        if len(lista[1])>0:
            salida.writerows(lista[1])        
        if len(lista[2])>0:
            salida.writerows(lista[2])
        if len(lista[3])>0:
            salida.writerows(lista[3])        
        salida.writerow(['tipo','numero','mediaLon','desviacionTip'])
        salida.writerow(lista[4])
        salida.writerow(lista[5])
        salida.writerow(lista[6])
        salida.writerow(lista[7])
        salida.writerow(lista[8])
        del salida
        csvsalida.close()