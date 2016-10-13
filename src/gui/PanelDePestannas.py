from PyQt5 import QtWidgets,QtCore

import numpy as np
from codigo.estadisticas import Estadistica
from codigo.informes import Informe
from codigo.informes.DatosToCsv import DatosToCsv
from codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas

class PanelDePestannas(QtWidgets.QTabWidget):
    def __init__(self, parent = None):
        #------Creamos los componentes -------------------------
        super(PanelDePestannas, self).__init__(parent)
        self.ventana=parent
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        
        self.addTab(self.tab1,"Lineas pintadas")
        self.addTab(self.tab2,"Corregir lineas")
        self.addTab(self.tab3,"Automatico")
        self.tab_1_ui()
        self.tab_2_ui()
        
        self.row_actual=-1
        self.procesado_de_lineas=ProcesadoDeLineas()
        self.estad = Estadistica()
        self.escribeCSV=DatosToCsv()

       
    def tab_1_ui(self):
        button = QtWidgets.QPushButton('Calcular Lineas')
        button.clicked.connect(self.ventana.calcular_lineas)
        layout_segundo = QtWidgets.QVBoxLayout()      
        layout_segundo.addWidget(button)
        layout_segundo.setAlignment(QtCore.Qt.AlignTop)       
        
        self.tab1.setLayout(layout_segundo)
        
    
    def tab_2_ui(self): 
        self.button2 = QtWidgets.QPushButton('Corregir Lineas')
        self.button2.clicked.connect(self.corregir_lineas)
        
        self.button3 = QtWidgets.QPushButton('Anadir punto')
        self.button3.clicked.connect(self.anadir_lineas)
        self.button3.setEnabled(False)

        self.button4 = QtWidgets.QPushButton('Anadir segmentos')
        self.button4.clicked.connect(self.anadir_puntos)  
        self.button4.setEnabled(False)

        self.button5 = QtWidgets.QPushButton('Borrar seleccionado')
        self.button5.clicked.connect(self.borrar_selec)
        
        self.button7 = QtWidgets.QPushButton('Guardar tabla')
        self.button7.clicked.connect(self.guardar_tabla)
        self.button7.setEnabled(False)

        self.button8 = QtWidgets.QPushButton('Limpiar tabla')
        self.button8.clicked.connect(self.limpiar_tabla)
        
        self.P1=QtWidgets.QLabel("P_1:")
        self.p_2=QtWidgets.QLabel("P_2:")
        
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
      
        layout_tab_2=QtWidgets.QHBoxLayout()
        
        layout_pestanna_1 = QtWidgets.QVBoxLayout()
        layout_pestanna_1.addWidget(self.button2)
        layaut_corregir_punto_1 = QtWidgets.QVBoxLayout()
        layaut_corregir_punto_1.setAlignment(QtCore.Qt.AlignTop)
        layaut_corregir_punto_1.addWidget(self.P1)
        layout_punto_1 = QtWidgets.QHBoxLayout()
        layout_punto_1.addWidget(self.P1_x)
        layout_punto_1.addWidget(self.P1_y)
        layout_punto_2 = QtWidgets.QHBoxLayout()
        layout_punto_2.addWidget(self.P2_x)
        layout_punto_2.addWidget(self.P2_y)
        
        layaut_corregir_punto_1.addLayout(layout_punto_1)
        layaut_corregir_punto_1.addWidget(self.p_2)
        layaut_corregir_punto_1.addLayout(layout_punto_2)
        
        layout_pestanna_1.addLayout(layaut_corregir_punto_1)
        layout_pestanna_1.addWidget(self.button3)
        layout_pestanna_1.addWidget(self.button5)
        layout_pestanna_1.addWidget(self.button8)
        layout_pestanna_1.addWidget(self.table)
        layout_pestanna_1.addWidget(self.button4)
        #layout_pestanna_1.addWidget(self.button6)
        layout_pestanna_1.addWidget(self.button7)
        layout_tab_2.addLayout(layout_pestanna_1)
        
        self.tab2.setLayout(layout_tab_2)

     
    def selected_row(self):
        self.row_actual=self.table.currentRow()
        row=self.row_actual
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
            sel,=self.ventana.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)),'yellow',linewidth=2.0)
            if self.ventana.selec_ante!=None:            
                self.ventana.ax.lines.remove(self.ventana.selec_ante)
            self.ventana.selec_ante=sel
            self.ventana.ax.hold(False)
            self.ventana.canvas.draw() 
            
            
    def corregir_lineas(self):
        self.button3.setEnabled(False)
        self.p_2.setStyleSheet('color: black')
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
                    self.p_2.setStyleSheet('color: Red')
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
        
        
    def anadir_lineas(self):
        self.p_2.setStyleSheet('color: black')
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
            self.ventana.tam_segmen_verdad=len(self.ventana.lineas)
            self.ventana.c1=None
            self.ventana.c2=None
        self.mostrar_tabla()
        self.button3.setEnabled(False)
        item = self.table.item(row,0)
        self.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.table.selectRow(row)
        self.button7.setEnabled(True)
        self.ventana.padre.save_file.setEnabled(True)  
        
        
        
    def mostrar_tabla(self):
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

        self.ventana.pintar_imagen_y_segmentos(segmentos)
        self.ventana.selec_ante=None
        self.ventana.canvas.draw()   
        
        
    def limpiar_tabla(self):
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)
        self.mostrar_tabla()
        self.button7.setEnabled(False)
        self.ventana.padre.save_file.setEnabled(False)   
        
        
    def borrar_selec(self):
        if self.row_actual!=-1:
            self.table.removeRow(self.row_actual)            
            self.row_actual=-1
            self.mostrar_tabla()
        if self.table.rowCount() > 0:
            self.button7.setEnabled(True)
            self.ventana.padre.save_file.setEnabled(True)

        else:
            self.button7.setEnabled(False)
            self.ventana.padre.save_file.setEnabled(False)
            
    def anadir_puntos(self):
        self.limpiar_tabla()
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
            self.mostrar_tabla()
            self.button7.setEnabled(True)
            self.ventana.padre.save_file.setEnabled(True)
            
    def guardar_tabla(self):
        #Clase PARA LAS estadisticas
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"openFolder")
        row = self.table.rowCount()
        segmentos=[]
        angulos={}
        long_segmento={}
        lista=[]
        x1,x2,y1,y2=0,0,0,0
        for i in range(row):            
            x1=int(self.table.item(i,0).text())
            x2=int(self.table.item(i,1).text())
            y1=int(self.table.item(i,2).text())
            y2=int(self.table.item(i,3).text())
            #print(x1,x2,y1,y2)
            segmentos.append(((x1,x2),(y1,y2)))
            angulos[((x1,x2),(y1,y2))]=self.procesado_de_lineas.angu(((x1,x2),(y1,y2)))
            long_segmento[((x1,x2),(y1,y2))]=self.estad.longitud_segemento(((x1,x2),(y1,y2)))   
            
        v,h,md,dm,total=self.estad.clasificar(segmentos,angulos,long_segmento)
   
        st_v,st_h,st_md,st_dm,st_tot,variables_tabla=self.estad.calcular_estadisticas(v, h, md, dm, total)
  
        informe=Informe(variables_tabla,path)#@UnusedVariable

        lista.extend([v,h,md,dm,st_v,st_h,st_md,st_dm,st_tot])
        self.escribeCSV.escribe_csv(path,lista)               
        self.button7.setEnabled(False)
        self.ventana.padre.save_file.setEnabled(False)
