
class Estadistica():
    
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
