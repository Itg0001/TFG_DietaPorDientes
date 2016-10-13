class Estadistica():
    @classmethod    
    def clasificar(self,segmentos,angulos,long_segmento):
        v,h,md,dm,total=[],[],[],[],[]  
        #CLASIFICAR LAS RECTAS POR SUS ANGULOS
        for i in segmentos:
            if 67.5< angulos[i] <112.5: 
                v.append((i,str(round(angulos[i],2)).replace('.',','),str(round(long_segmento[i],2)).replace('.',','),'v'))
                #print("linea",i,"angulo",self.angulos[i],"= vertical" )
            elif 22.5< angulos[i] <67.5:
                md.append((i,str(round(angulos[i],2)).replace('.',','),str(round(long_segmento[i],2)).replace('.',','),'md'))
                
            elif 112.5< angulos[i] <157.5:
                dm.append((i,str(round(angulos[i],2)).replace('.',','),str(round(long_segmento[i],2)).replace('.',','),'dm'))
                
            elif (0< angulos[i] <22.5) or (157.5< angulos[i] <180):                
                h.append((i,str(round(angulos[i],2)).replace('.',','),str(round(long_segmento[i],2)).replace('.',','),'h'))
        total.extend(v)
        total.extend(h)
        total.extend(md)
        total.extend(dm)
        return v,h,md,dm,total
    @classmethod       
    def stadisticas(self,tipo,numero,media_lon,desviacion_tip):
        lista=[]
        lista.append(tipo)
        lista.append(numero)
        lista.append(str(round(media_lon,2)).replace(',','.'))
        lista.append(str(round(desviacion_tip,2)).replace(',','.'))
        return lista
    @classmethod        
    def desviacion_tipica(self,lista_distancias):
        media=self.media_long_segmentos(lista_distancias)
        acumulador=0
        for i in lista_distancias:
            acumulador+=(float(str(i[2]).replace(',','.'))-media)**2
        return (acumulador/len(lista_distancias))**(1/2)
    @classmethod        
    def media_long_segmentos(self,lista_distancias):
        media=0
        for i in lista_distancias:
            media+=float(str(i[2]).replace(',','.'))
        return media/len(lista_distancias)
    @classmethod            
    def longitud_segemento(self,p):
        return (((p[1][0]-p[0][0])**2)+((p[1][1]-p[0][1])**2))**(1/2)
    @classmethod    
    def calcular_estadisticas(self,v,h,md,dm,total):
        st_v,st_h,st_md,st_dm=[],[],[],[] 
        variables_tabla=[]
        if len(v)>0:
            st_v=self.stadisticas('v',len(v),self.media_long_segmentos(v),self.desviacion_tipica(v))
            variables_tabla.extend(st_v[1:4])
        else:
            variables_tabla.extend([0,0,0])       
        if len(h)>0:
            st_h=self.stadisticas('h',len(h),self.media_long_segmentos(h),self.desviacion_tipica(h))
            variables_tabla.extend(st_h[1:4])
        else:
            variables_tabla.extend([0,0,0])
        if len(md)>0:
            st_md=self.stadisticas('md',len(md),self.media_long_segmentos(md),self.desviacion_tipica(md))
            variables_tabla.extend(st_md[1:4])
        else:
            variables_tabla.extend([0,0,0])        
        if len(dm)>0:
            st_dm=self.stadisticas('dm',len(dm),self.media_long_segmentos(dm),self.desviacion_tipica(dm))
            variables_tabla.extend(st_dm[1:4])
        else:
            variables_tabla.extend([0,0,0])
        st_tot=self.stadisticas('totales',len(total),self.media_long_segmentos(total),self.desviacion_tipica(total))        
        variables_tabla.extend(st_tot[1:4])
        return st_v,st_h,st_md,st_dm,st_tot,variables_tabla