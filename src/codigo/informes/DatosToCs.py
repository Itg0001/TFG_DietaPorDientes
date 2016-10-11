

import csv
class DatosToCsv():    
    def escribeCsv(self,path,v,h,md,dm,stV,stH,stMD,stDM,stTot):
        csvsalida = open(path+'/'+'salidat.csv', 'w', newline='')
        salida = csv.writer(csvsalida,escapechar=' ',quoting=csv.QUOTE_NONE,delimiter=';')
        salida.writerow(['linea','angulo','tamano','tipo'])  
        if len(v)>0:
            salida.writerows(v)       
        if len(h)>0:
            salida.writerows(h)        
        if len(md)>0:
            salida.writerows(md)
        if len(dm)>0:
            salida.writerows(dm)        
        salida.writerow(['tipo','numero','mediaLon','desviacionTip'])
        salida.writerow(stV)
        salida.writerow(stH)
        salida.writerow(stMD)
        salida.writerow(stDM)
        salida.writerow(stTot)
        del salida
        csvsalida.close()