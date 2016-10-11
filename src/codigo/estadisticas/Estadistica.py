
class Estadistica():
    
    def clasificar(self,segmentos,angulos,longSegmento):
        v,h,md,dm,total=[],[],[],[],[]  
        #CLASIFICAR LAS RECTAS POR SUS ANGULOS
        for i in segmentos:
            if 67.5< angulos[i] <112.5: 
                v.append((i,str(round(angulos[i],2)).replace('.',','),str(round(longSegmento[i],2)).replace('.',','),'v'))
                #print("linea",i,"angulo",self.angulos[i],"= vertical" )
            elif 22.5< angulos[i] <67.5:
                md.append((i,str(round(angulos[i],2)).replace('.',','),str(round(longSegmento[i],2)).replace('.',','),'md'))
                
            elif 112.5< angulos[i] <157.5:
                dm.append((i,str(round(angulos[i],2)).replace('.',','),str(round(longSegmento[i],2)).replace('.',','),'dm'))
                
            elif (0< angulos[i] <22.5) or (157.5< angulos[i] <180):                
                h.append((i,str(round(angulos[i],2)).replace('.',','),str(round(longSegmento[i],2)).replace('.',','),'h'))
        total.extend(v)
        total.extend(h)
        total.extend(md)
        total.extend(dm)
        return v,h,md,dm,total
    
    def stadisticas(self,tipo,numero,mediaLon,desviacionTip):
        lista=[]
        lista.append(tipo)
        lista.append(numero)
        lista.append(str(round(mediaLon,2)).replace(',','.'))
        lista.append(str(round(desviacionTip,2)).replace(',','.'))
        return lista
    
    def desviacionTipica(self,listaDistancias):
        media=self.mediaLongSegmentos(listaDistancias)
        acumulador=0
        for i in listaDistancias:
            acumulador+=((float(str(i[2]).replace(',','.'))-media)**2)
        return ((acumulador/len(listaDistancias))**(1/2))
    
    def mediaLongSegmentos(self,listaDistancias):
        media=0
        for i in listaDistancias:
            media+=float(str(i[2]).replace(',','.'))
        return media/len(listaDistancias)
        
    def longitudSegemento(self,p):
        return (((p[1][0]-p[0][0])**2)+((p[1][1]-p[0][1])**2))**(1/2)

    def calcularEstadisticas(self,v,h,md,dm,total):
        stV,stH,stMD,stDM=[],[],[],[] 
        variablesTabla=[]
        if len(v)>0:
            stV=self.stadisticas('v',len(v),self.mediaLongSegmentos(v),self.desviacionTipica(v))
            variablesTabla.extend(stV[1:4])
        else:
            variablesTabla.extend([0,0,0])       
        if len(h)>0:
            stH=self.stadisticas('h',len(h),self.mediaLongSegmentos(h),self.desviacionTipica(h))
            variablesTabla.extend(stH[1:4])
        else:
            variablesTabla.extend([0,0,0])
        if len(md)>0:
            stMD=self.stadisticas('md',len(md),self.mediaLongSegmentos(md),self.desviacionTipica(md))
            variablesTabla.extend(stMD[1:4])
        else:
            variablesTabla.extend([0,0,0])        
        if len(dm)>0:
            stDM=self.stadisticas('dm',len(dm),self.mediaLongSegmentos(dm),self.desviacionTipica(dm))
            variablesTabla.extend(stDM[1:4])
        else:
            variablesTabla.extend([0,0,0])
        stTot=self.stadisticas('totales',len(total),self.mediaLongSegmentos(total),self.desviacionTipica(total))        
        variablesTabla.extend(stTot[1:4])
        return stV,stH,stMD,stDM,stTot,variablesTabla