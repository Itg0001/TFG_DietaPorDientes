from PyQt5 import QtWidgets
from PyQt5 import QtCore
#from PyQt5.QtCore import *
#from PyQt5.QtGui  import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import csv
import networkx as nx
from networkx.algorithms import approximation as apxa
from codigo.procesado import Procesado
#from Procesado import Procesado
from codigo.informes import Informe
##Clase Ventana 
#Esta clase contendra la ventana principal de la aplcacion en la que colgaran los diferentes 
#componentes.
class Window(QtWidgets.QWidget):
    def __init__(self,path, parent=None ):
        super(Window, self).__init__(parent)
        self.resize(900, 700)
        #Figura sobre la que trabajaremos
        self.fig = Figure((6.5, 5.0), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        #---------Guardar Coordenadas--------------
        self.c1=0
        self.c2=0
        self.tamSegmenVerdad=-1
        self.lineas=[]
        self.pintados=[]
        self.rowActual=-1
        self.SelecAnte=None
        self.procesado=Procesado()
        self.padre=parent
        #---------------------------------------------------------------
        
        #parent.saveFile.setEnabled(True)

        
        #---------MENU cargar imagen------------------------------------
        self.path=path
       
        #---------------------------------------------------------------
        
        #------Para mostrar la Imagen del inicio--------------------------
        self.img=self.procesado.leerImagen(path)
        self.distance_red=self.procesado.distanciaAlRojo(self.img)
        self.imgBin=self.procesado.binarizar(self.distance_red)
        #self.imgBinCrop,self.imgCrop=cropImg(self.imgBin,self.img)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Figura sin lineas')
        self.ax.set_xlim([0,self.img.shape[1]])
        self.ax.set_ylim([0,self.img.shape[0]])
        self.ax.imshow(self.img ,origin='lower',vmax=1, interpolation='nearest')
    #-------------------------------------------------------
        
        #------Creamos los componentes -------------------------
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtWidgets.QPushButton('Calcular Lineas')
        self.button.clicked.connect(self.plot1)
        
        self.button2 = QtWidgets.QPushButton('Corregir Lineas')
        self.button2.clicked.connect(self.plot2)
        
        self.button3 = QtWidgets.QPushButton('Anadir punto')
        self.button3.clicked.connect(self.plot3)
        self.button3.setEnabled(False)

        self.button4 = QtWidgets.QPushButton('Anadir segmentos')
        self.button4.clicked.connect(self.anadirPuntos)  
        self.button4.setEnabled(False)

        self.button5 = QtWidgets.QPushButton('Borrar seleccionado')
        self.button5.clicked.connect(self.borrarSelec)
        
        #self.button6 = QtGui.QPushButton('Mostrar Tabla')
        #self.button6.clicked.connect(self.mostrarTabla)
        
        self.button7 = QtWidgets.QPushButton('Guardar tabla')
        self.button7.clicked.connect(self.guardarTabla)
        self.button7.setEnabled(False)
        self.padre.saveFile.setEnabled(False)

        self.button8 = QtWidgets.QPushButton('Limpiar tabla')
        self.button8.clicked.connect(self.limpiarTabla)
        
        self.P1=QtWidgets.QLabel("P_1:")
        self.P2=QtWidgets.QLabel("P_2:")
        
        self.P1_x=QtWidgets.QLabel("0")
        self.P1_y=QtWidgets.QLabel("0")
        
        self.P2_x=QtWidgets.QLabel("0")
        self.P2_y=QtWidgets.QLabel("0")
        
        tabs= QtWidgets.QTabWidget()
        
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab3 = QtWidgets.QWidget()
        
        tabs.addTab(tab1,"Lineas pintadas")
        tabs.addTab(tab2,"Corregir lineas")
        tabs.addTab(tab3,"Automatico")
        
        self.table = QtWidgets.QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.selected_row)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(['P1X', 'P1Y', 'P2X', 'P2Y'])

        
        #-------------------------------------------------------

        #------Asignamos los componentes a un layout----------
        layoutTabs=QtWidgets.QHBoxLayout()
        layoutTab1=QtWidgets.QHBoxLayout()
        layoutTab2=QtWidgets.QHBoxLayout()
        layoutTab3=QtWidgets.QHBoxLayout()
        
        #layout principal - - 
        
        laoutPrincipal = QtWidgets.QHBoxLayout()
        # Layout (-) - /n 1
        layoutPrimero = QtWidgets.QVBoxLayout() 
        layoutPrimero.addWidget(self.toolbar)
        layoutPrimero.addWidget(self.canvas)
        # Layout - (-) /n 1 y 2
        layoutSegundo = QtWidgets.QVBoxLayout()      
        layoutSegundo.addWidget(self.button)
        layoutSegundo.setAlignment(QtCore.Qt.AlignTop)
        layoutPestana1 = QtWidgets.QVBoxLayout()
        layoutPestana1.addWidget(self.button2)


        
        #layout - (-) /n 3 y 4
        layautCorregirPunto1 = QtWidgets.QVBoxLayout()
        layautCorregirPunto1.setAlignment(QtCore.Qt.AlignTop)
        layautCorregirPunto1.addWidget(self.P1)
        layoutPunto1 = QtWidgets.QHBoxLayout()
        layoutPunto1.addWidget(self.P1_x)
        layoutPunto1.addWidget(self.P1_y)
        layoutPunto2 = QtWidgets.QHBoxLayout()
        layoutPunto2.addWidget(self.P2_x)
        layoutPunto2.addWidget(self.P2_y)
        layautCorregirPunto1.addLayout(layoutPunto1)
        layautCorregirPunto1.addWidget(self.P2)
        layautCorregirPunto1.addLayout(layoutPunto2)
        #Anadimos al layout - (-)
        layoutPestana1.addLayout(layautCorregirPunto1)
        layoutPestana1.addWidget(self.button3)
        layoutPestana1.addWidget(self.button5)
        layoutPestana1.addWidget(self.button8)
        layoutPestana1.addWidget(self.table)
        layoutPestana1.addWidget(self.button4)
        #layoutPestana1.addWidget(self.button6)
        layoutPestana1.addWidget(self.button7)
        
        #Anadimos las dos col al layaut principal
        
        layoutTab1.addLayout(layoutSegundo)
        
        layoutTab2.addLayout(layoutPestana1)
        
        layoutTab3.addLayout(layoutSegundo)
        
        tab1.setLayout(layoutTab1)
        tab2.setLayout(layoutTab2)
        tab3.setLayout(layoutTab3)
        
        layoutTabs.addWidget(tabs)
        layoutTabs.setAlignment(QtCore.Qt.AlignRight)

        laoutPrincipal.addLayout(layoutPrimero)
        laoutPrincipal.setStretch(0,2)
        laoutPrincipal.addLayout(layoutTabs)
        laoutPrincipal.setStretch(2,3)

        #laoutPrincipal.addWidget(tabs)
        #laoutPrincipal.addLayout(layoutSegundo)
        
        self.setLayout(laoutPrincipal)#Asignamos como principal el principal
        #-------------------------------------------------------------------
                     
    def selected_row(self):
        self.rowActual=self.table.currentRow()
        row=self.rowActual
        if row>=0:
            p1x = self.table.item(row,0)
            p1x=p1x.text()
            p1y = self.table.item(row,1)
            p1y=p1y.text()
            p2x = self.table.item(row,2)
            p2x=p2x.text()
            p2y = self.table.item(row,3)
            p2y=p2y.text()

            #self.ax.lines[0].remove()
            self.ax.hold(True) 
            self.ax.set_title('Figura con lineas')
            #self.ax.set_xlim([0,self.img.shape[1]])
            #self.ax.set_ylim([0,self.img.shape[0]])
            sel,=self.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)),'yellow',linewidth=2.0)
            if self.SelecAnte!=None:            
                self.ax.lines.remove(self.SelecAnte)
            self.SelecAnte=sel
            self.ax.hold(False)
            self.canvas.draw()
        #print(self.tamSegmenVerdad)
        #if self.tamSegmenVerdad!=-1:
        #    self.ax.lines[self.tamSegmenVerdad].remove()
        
        #print(self.table.currentRow())
    
    def plot1(self):        
        sinRuido=self.procesado.reducirGrosor(self.imgBin)
        lines=self.procesado.proHough(10,5,11,sinRuido)        
        G=nx.Graph()
        G=self.procesado.combina(8,4,lines,G)
        k_components = apxa.k_components(G)
        segmentosDeVerdad=self.procesado.segmentosVerdad(k_components,lines)
        #print(sys.version_info)
        self.pintarImagenYsegmentos(segmentosDeVerdad)
        self.canvas.draw()
        self.lineas=segmentosDeVerdad
        self.tamSegmenVerdad=len(self.lineas)
        self.button4.setEnabled(True)

        
    def pintarImagenYsegmentos(self,segmentos):
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Figura con lineas')
        self.ax.set_xlim([0,self.img.shape[1]])
        self.ax.set_ylim([0,self.img.shape[0]])
        self.ax.imshow(self.img ,origin='lower',vmax=1, interpolation='nearest')
        self.ax.hold(True)
        for line in segmentos:
            p0, p1 = line
            #print(ang((p0,p1),((10, 0), (500, 0))))
            self.ax.set_title('Figura con lineas')
            self.ax.set_xlim([0,self.img.shape[1]])
            self.ax.set_ylim([0,self.img.shape[0]])            
            self.ax.plot((p0[0], p1[0]), (p0[1], p1[1]),'b',linewidth=2.0)
            #-print(type(p0[0]))
        self.ax.hold(False)
        self.canvas.draw()

        
    def plot2(self):
        self.button3.setEnabled(False)
        self.P2.setStyleSheet('color: black')
        self.P1.setStyleSheet('color: black')

        self.P1_x.setText("0")
        self.P1_y.setText("0")
        self.P2_x.setText("0")
        self.P2_y.setText("0")        
        self.button2.setEnabled(False)
        coords = []     
        def onclick(event):
            ix, iy = event.xdata, event.ydata
            if ix != None and iy != None:
                if len(coords) == 0:
                    self.P1.setStyleSheet('color: Red')
                    self.P1_x.setText(str(round(ix,0)))
                    self.P1_y.setText(str(round(iy,0)))
                    #print ('x = %d, y = %d'%(ix, iy))
                    coords.append((ix, iy))
                    self.c1=(ix,iy)

                else:
                    self.P2.setStyleSheet('color: Red')
                    self.P2_x.setText(str(round(ix,0)))
                    self.P2_y.setText(str(round(iy,0)))
                    self.c2=(ix,iy)                    
                    #print (' = %d, y = %d'%(ix, iy))
                    coords.append((ix, iy))
                    self.fig.canvas.mpl_disconnect(cid)
                    self.button2.setEnabled(True)
                    self.button3.setEnabled(True)


            return coords
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw()

    def plot3(self):
        self.P2.setStyleSheet('color: black')
        self.P1.setStyleSheet('color: black')

        self.P1_x.setText("0")
        self.P1_y.setText("0")
        self.P2_x.setText("0")
        self.P2_y.setText("0")
        if self.c1!=None and self.c2!=None:        
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(self.c1[0]))))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(self.c1[1]))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(self.c2[0]))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(self.c2[1]))))
            #print(self.c2)
            self.pintados.append((self.c1,self.c2))
            self.tamSegmenVerdad=len(self.lineas)
            #print(self.lineas)
            self.c1=None
            self.c2=None
        self.mostrarTabla()
        self.button3.setEnabled(False)
        item = self.table.item(row,0)
        self.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.table.selectRow(row)
        self.button7.setEnabled(True)
        self.padre.saveFile.setEnabled(True)

    def anadirPuntos(self):
        self.limpiarTabla()
        row = self.table.rowCount()
        if len(self.lineas)!=0:
            for i in self.lineas:
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0][0]))))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[0][1]))))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[1][0]))))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[1][1]))))
                row+=1
            self.button4.setEnabled(False)
            self.mostrarTabla()
            self.button7.setEnabled(True)
            self.padre.saveFile.setEnabled(True)


                
    def borrarSelec(self):
        if self.rowActual!=-1:
            self.table.removeRow(self.rowActual)            
            self.rowActual=-1
            self.mostrarTabla()
        if self.table.rowCount() > 0:
            self.button7.setEnabled(True)
            self.padre.saveFile.setEnabled(True)

        else:
            self.button7.setEnabled(False)
            self.padre.saveFile.setEnabled(False)



    def mostrarTabla(self):
        row = self.table.rowCount()
        segmentos=[]
        x1,x2,y1,y2=0,0,0,0
        for i in range(row):            
            x1=int(self.table.item(i,0).text())
            x2=int(self.table.item(i,1).text())
            y1=int(self.table.item(i,2).text())
            y2=int(self.table.item(i,3).text())
            #print(x1,x2,y1,y2)
            segmentos.append(((x1,x2),(y1,y2)))

        self.pintarImagenYsegmentos(segmentos)
        self.SelecAnte=None
        self.canvas.draw()
    
        #pintarImagenYsegmentos(,1)
    def guardarTabla(self):
        #Leer tabla para guardar sementos.
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"openFolder")
        #print(path)
        
        row = self.table.rowCount()
        segmentos=[]
        angulos={}
        longSegmento={}
        x1,x2,y1,y2=0,0,0,0
        for i in range(row):            
            x1=int(self.table.item(i,0).text())
            x2=int(self.table.item(i,1).text())
            y1=int(self.table.item(i,2).text())
            y2=int(self.table.item(i,3).text())
            #print(x1,x2,y1,y2)
            segmentos.append(((x1,x2),(y1,y2)))
            angulos[((x1,x2),(y1,y2))]=self.procesado.angu(((x1,x2),(y1,y2)))
            longSegmento[((x1,x2),(y1,y2))]=self.longitudSegemento(((x1,x2),(y1,y2)))   
            
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
        
   
        #print("NUMERO de h:",len(h))
        #print("media h",self.mediaLongSegmentos(h))
        #print("Desviacion Tipica h",self.desviacionTipica(h))
        #print()
        
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
        #print("ESTE ES EL PATH",path)
     
        informe=Informe(variablesTabla,path)#@UnusedVariable
        #print(informe.variables)

        #print(path)
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
        self.button7.setEnabled(False)
        self.padre.saveFile.setEnabled(False)


    #def totales(self,h,v,md,dm): 
    #    tot=[]
    #    for i in h:
    #        tot.append(i)
    #    for i in v:
    #        tot.append(i)
    #    for i in md:
    #        tot.append(i)
    #    for i in dm:
    #        tot.append(i)
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
        
    def limpiarTabla(self):
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)
        self.mostrarTabla()
        self.button7.setEnabled(False)
        self.padre.saveFile.setEnabled(False)