from PyQt5 import QtWidgets,QtCore

import numpy as np
from codigo.procesado import Procesado
from codigo.estadisticas import Estadistica
from codigo.informes import Informe
from codigo.informes.DatosToCs import DatosToCsv

class PanelDePestañas(QtWidgets.QTabWidget):
    def __init__(self, parent = None):
        #------Creamos los componentes -------------------------
        super(PanelDePestañas, self).__init__(parent)
        self.ventana=parent
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        
        self.addTab(self.tab1,"Lineas pintadas")
        self.addTab(self.tab2,"Corregir lineas")
        self.addTab(self.tab3,"Automatico")
        self.tab1UI()
        self.tab2UI()
        
        self.rowActual=-1
        self.procesado=Procesado()
        self.estad = Estadistica()
        self.escribeCSV=DatosToCsv()

       
    def tab1UI(self):
        button = QtWidgets.QPushButton('Calcular Lineas')
        button.clicked.connect(self.ventana.calcularLineas)
        layoutSegundo = QtWidgets.QVBoxLayout()      
        layoutSegundo.addWidget(button)
        layoutSegundo.setAlignment(QtCore.Qt.AlignTop)       
        
        self.tab1.setLayout(layoutSegundo)
        
    
    def tab2UI(self): 
        self.button2 = QtWidgets.QPushButton('Corregir Lineas')
        self.button2.clicked.connect(self.corregirLineas)
        
        self.button3 = QtWidgets.QPushButton('Anadir punto')
        self.button3.clicked.connect(self.anadirLineas)
        self.button3.setEnabled(False)

        self.button4 = QtWidgets.QPushButton('Anadir segmentos')
        self.button4.clicked.connect(self.anadirPuntos)  
        self.button4.setEnabled(False)

        self.button5 = QtWidgets.QPushButton('Borrar seleccionado')
        self.button5.clicked.connect(self.borrarSelec)
        
        self.button7 = QtWidgets.QPushButton('Guardar tabla')
        self.button7.clicked.connect(self.guardarTabla)
        self.button7.setEnabled(False)

        self.button8 = QtWidgets.QPushButton('Limpiar tabla')
        self.button8.clicked.connect(self.limpiarTabla)
        
        self.P1=QtWidgets.QLabel("P_1:")
        self.P2=QtWidgets.QLabel("P_2:")
        
        self.P1_x=QtWidgets.QLabel("0")
        self.P1_y=QtWidgets.QLabel("0")
        
        self.P2_x=QtWidgets.QLabel("0")
        self.P2_y=QtWidgets.QLabel("0")
        
        self.table = QtWidgets.QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.selected_row)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(['P1X', 'P1Y', 'P2X', 'P2Y'])
      
        layoutTab2=QtWidgets.QHBoxLayout()
        
        layoutPestaña1 = QtWidgets.QVBoxLayout()
        layoutPestaña1.addWidget(self.button2)
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
        
        layoutPestaña1.addLayout(layautCorregirPunto1)
        layoutPestaña1.addWidget(self.button3)
        layoutPestaña1.addWidget(self.button5)
        layoutPestaña1.addWidget(self.button8)
        layoutPestaña1.addWidget(self.table)
        layoutPestaña1.addWidget(self.button4)
        #layoutPestaña1.addWidget(self.button6)
        layoutPestaña1.addWidget(self.button7)
        layoutTab2.addLayout(layoutPestaña1)
        
        self.tab2.setLayout(layoutTab2)

     
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
            self.ventana.ax.hold(True) 
            self.ventana.ax.set_title('Figura con lineas')
            #self.ax.set_xlim([0,self.img.shape[1]])
            #self.ax.set_ylim([0,self.img.shape[0]])
            sel,=self.ventana.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)),'yellow',linewidth=2.0)
            if self.ventana.SelecAnte!=None:            
                self.ventana.ax.lines.remove(self.ventana.SelecAnte)
            self.ventana.SelecAnte=sel
            self.ventana.ax.hold(False)
            self.ventana.canvas.draw() 
            
            
    def corregirLineas(self):
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
                    self.ventana.c1=(ix,iy)

                else:
                    self.P2.setStyleSheet('color: Red')
                    self.P2_x.setText(str(round(ix,0)))
                    self.P2_y.setText(str(round(iy,0)))
                    self.ventana.c2=(ix,iy)                    
                    #print (' = %d, y = %d'%(ix, iy))
                    coords.append((ix, iy))
                    self.ventana.fig.canvas.mpl_disconnect(cid)
                    self.button2.setEnabled(True)
                    self.button3.setEnabled(True)

            return coords
        cid = self.ventana.fig.canvas.mpl_connect('button_press_event', onclick)
        self.ventana.canvas.draw()  
        
        
    def anadirLineas(self):
        self.P2.setStyleSheet('color: black')
        self.P1.setStyleSheet('color: black')

        self.P1_x.setText("0")
        self.P1_y.setText("0")
        self.P2_x.setText("0")
        self.P2_y.setText("0")
        if self.ventana.c1!=None and self.ventana.c2!=None:        
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(self.ventana.c1[0]))))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(self.ventana.c1[1]))))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(self.ventana.c2[0]))))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(self.ventana.c2[1]))))
            #print(self.c2)
            #self.pintados.append((self.c1,self.c2))
            self.ventana.tamSegmenVerdad=len(self.ventana.lineas)
            #print(self.lineas)
            self.ventana.c1=None
            self.ventana.c2=None
        self.mostrarTabla()
        self.button3.setEnabled(False)
        item = self.table.item(row,0)
        self.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.table.selectRow(row)
        self.button7.setEnabled(True)
        self.ventana.padre.saveFile.setEnabled(True)  
        
        
        
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

        self.ventana.pintarImagenYsegmentos(segmentos)
        self.ventana.SelecAnte=None
        self.ventana.canvas.draw()   
        
        
    def limpiarTabla(self):
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)
        self.mostrarTabla()
        self.button7.setEnabled(False)
        self.ventana.padre.saveFile.setEnabled(False)   
        
        
    def borrarSelec(self):
        if self.rowActual!=-1:
            self.table.removeRow(self.rowActual)            
            self.rowActual=-1
            self.mostrarTabla()
        if self.table.rowCount() > 0:
            self.button7.setEnabled(True)
            self.ventana.padre.saveFile.setEnabled(True)

        else:
            self.button7.setEnabled(False)
            self.ventana.padre.saveFile.setEnabled(False)
            
    def anadirPuntos(self):
        self.limpiarTabla()
        row = self.table.rowCount()
        if len(self.ventana.lineas)!=0:
            for i in self.ventana.lineas:
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0][0]))))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[0][1]))))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[1][0]))))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[1][1]))))
                row+=1
            self.button4.setEnabled(False)
            self.mostrarTabla()
            self.button7.setEnabled(True)
            self.ventana.padre.saveFile.setEnabled(True)
            
    def guardarTabla(self):
        #Clase PARA LAS estadisticas
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"openFolder")
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
            longSegmento[((x1,x2),(y1,y2))]=self.estad.longitudSegemento(((x1,x2),(y1,y2)))   
            
        v,h,md,dm,total=self.estad.clasificar(segmentos,angulos,longSegmento)
   
        stV,stH,stMD,stDM,stTot,variablesTabla=self.estad.calcularEstadisticas(v, h, md, dm, total)
  
        informe=Informe(variablesTabla,path)#@UnusedVariable
        self.escribeCSV.escribeCsv(path,v,h,md,dm,stV,stH,stMD,stDM,stTot)               
        self.button7.setEnabled(False)
        self.ventana.padre.saveFile.setEnabled(False)
