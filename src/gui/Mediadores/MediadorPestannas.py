import numpy as np
from PyQt5 import QtWidgets, QtCore
from codigo  import Informe
from codigo.estadisticas import Estadistica
from codigo.informes.DatosToCsv import DatosToCsv
# from codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas
class MediadorPestannas():
    
    def __init__(self, pestannas):
        self.pestannas = pestannas
#         self.procesado_de_lineas=ProcesadoDeLineas()
        self.estad = Estadistica()
        self.escribeCSV = DatosToCsv()
#         self.pestannas.addTab(self.pestannas.tab2,"Corregir lineas")
#         self.pestannas.addTab(self.pestannas.tab3,"Automatico")
   
    def inicia_paneles(self):
        self.pestannas.tab1 = QtWidgets.QWidget()
        self.pestannas.tab2 = QtWidgets.QWidget()
        self.pestannas.tab3 = QtWidgets.QWidget()
        
    def tab_1_ui(self):
        self.pestannas.addTab(self.pestannas.tab1, "Lineas pintadas")        
        self.pestannas.button = QtWidgets.QPushButton('Calcular Lineas')
        self.pestannas.button.clicked.connect(self.pestannas.ventana.calcular_lineas)
        self.pestannas.layout_segundo = QtWidgets.QVBoxLayout()      
        self.pestannas.layout_segundo.addWidget(self.pestannas.button)
        self.pestannas.layout_segundo.setAlignment(QtCore.Qt.AlignTop)       
     
    def tab_2_ui(self): 
        self.pestannas.addTab(self.pestannas.tab2, "Corregir lineas")
        self.pestannas.addTab(self.pestannas.tab3, "Automatico")

        self.pestannas.button2 = QtWidgets.QPushButton('Corregir Lineas')
        self.pestannas.button2.clicked.connect(self.pestannas.corregir_lineas)
        
        self.pestannas.button3 = QtWidgets.QPushButton('Anadir punto')
        self.pestannas.button3.clicked.connect(self.pestannas.anadir_lineas)
        self.pestannas.button3.setEnabled(False)

        self.pestannas.button4 = QtWidgets.QPushButton('Anadir segmentos')
        self.pestannas.button4.clicked.connect(self.pestannas.anadir_puntos)  
        self.pestannas.button4.setEnabled(False)

        self.pestannas.button5 = QtWidgets.QPushButton('Borrar seleccionado')
        self.pestannas.button5.clicked.connect(self.pestannas.borrar_selec)
        
        self.pestannas.button7 = QtWidgets.QPushButton('Guardar tabla')
        self.pestannas.button7.clicked.connect(self.pestannas.guardar_tabla)
        self.pestannas.button7.setEnabled(False)

        self.pestannas.button8 = QtWidgets.QPushButton('Limpiar tabla')
        self.pestannas.button8.clicked.connect(self.pestannas.limpiar_tabla)
        
        self.pestannas.P1 = QtWidgets.QLabel("P_1:")
        self.pestannas.p_2 = QtWidgets.QLabel("P_2:")
        
        self.pestannas.P1_x = QtWidgets.QLabel("0")
        self.pestannas.P1_y = QtWidgets.QLabel("0")
        
        self.pestannas.P2_x = QtWidgets.QLabel("0")
        self.pestannas.P2_y = QtWidgets.QLabel("0")
        
        self.pestannas.table = QtWidgets.QTableWidget(self.pestannas)
        self.pestannas.table.setRowCount(0)
        self.pestannas.table.setColumnCount(4)
        self.pestannas.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pestannas.table.itemSelectionChanged.connect(self.pestannas.selected_row)
        self.pestannas.header = self.pestannas.table.horizontalHeader()
        self.pestannas.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.pestannas.table.setHorizontalHeaderLabels(['P1X', 'P1Y', 'P2X', 'P2Y'])
      
        self.pestannas.layout_tab_2 = QtWidgets.QHBoxLayout()
        
        self.pestannas.layout_pestanna_1 = QtWidgets.QVBoxLayout()
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button2)
        self.pestannas.layaut_corregir_punto_1 = QtWidgets.QVBoxLayout()
        self.pestannas.layaut_corregir_punto_1.setAlignment(QtCore.Qt.AlignTop)
        self.pestannas.layaut_corregir_punto_1.addWidget(self.pestannas.P1)
        self.pestannas.layout_punto_1 = QtWidgets.QHBoxLayout()
        self.pestannas.layout_punto_1.addWidget(self.pestannas.P1_x)
        self.pestannas.layout_punto_1.addWidget(self.pestannas.P1_y)
        self.pestannas.layout_punto_2 = QtWidgets.QHBoxLayout()
        self.pestannas.layout_punto_2.addWidget(self.pestannas.P2_x)
        self.pestannas.layout_punto_2.addWidget(self.pestannas.P2_y)
        
        self.pestannas.layaut_corregir_punto_1.addLayout(self.pestannas.layout_punto_1)
        self.pestannas.layaut_corregir_punto_1.addWidget(self.pestannas.p_2)
        self.pestannas.layaut_corregir_punto_1.addLayout(self.pestannas.layout_punto_2)
        
        self.pestannas.layout_pestanna_1.addLayout(self.pestannas.layaut_corregir_punto_1)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button3)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button5)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button8)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.table)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button4)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button7)
        self.pestannas.layout_tab_2.addLayout(self.pestannas.layout_pestanna_1)
        
        self.pestannas.tab2.setLayout(self.pestannas.layout_tab_2)    
        self.pestannas.tab1.setLayout(self.pestannas.layout_segundo)
        
    def selected_row(self):
        self.pestannas.row_actual = self.pestannas.table.currentRow()
        row = self.pestannas.row_actual
        if row >= 0:
            p1x = self.pestannas.table.item(row, 0)
            p1x = p1x.text()
            p1y = self.pestannas.table.item(row, 1)
            p1y = p1y.text()
            p2x = self.pestannas.table.item(row, 2)
            p2x = p2x.text()
            p2y = self.pestannas.table.item(row, 3)
            p2y = p2y.text()
            self.pestannas.ventana.ax.hold(True) 
            self.pestannas.ventana.ax.set_title('Figura con lineas')
            sel, = self.pestannas.ventana.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)), 'yellow', linewidth=2.0)
            if self.pestannas.ventana.selec_ante != None:            
                self.pestannas.ventana.ax.lines.remove(self.pestannas.ventana.selec_ante)
            self.pestannas.ventana.selec_ante = sel
            self.pestannas.ventana.ax.hold(False)
            self.pestannas.ventana.canvas.draw()             
            
    def corregir_lineas(self):
        self.pestannas.button3.setEnabled(False)
        self.pestannas.p_2.setStyleSheet('color: black')
        self.pestannas.P1.setStyleSheet('color: black')
 
        self.pestannas.P1_x.setText("0")
        self.pestannas.P1_y.setText("0")
        self.pestannas.P2_x.setText("0")
        self.pestannas.P2_y.setText("0")        
        self.pestannas.button2.setEnabled(False)
        coords = []     
        def onclick(event):
            ix, iy = event.xdata, event.ydata
            if ix != None and iy != None:
                if len(coords) == 0:
                    self.pestannas.P1.setStyleSheet('color: Red')
                    self.pestannas.P1_x.setText(str(round(ix, 0)))
                    self.pestannas.P1_y.setText(str(round(iy, 0)))
                    # print ('x = %d, y = %d'%(ix, iy))
                    coords.append((ix, iy))
                    self.pestannas.ventana.c1 = (ix, iy)
 
                else:
                    self.pestannas.p_2.setStyleSheet('color: Red')
                    self.pestannas.P2_x.setText(str(round(ix, 0)))
                    self.pestannas.P2_y.setText(str(round(iy, 0)))
                    self.pestannas.ventana.c2 = (ix, iy)                    
                    # print (' = %d, y = %d'%(ix, iy))
                    coords.append((ix, iy))
                    self.pestannas.ventana.fig.canvas.mpl_disconnect(cid)
                    self.pestannas.button2.setEnabled(True)
                    self.pestannas.button3.setEnabled(True)
 
            return coords
        cid = self.pestannas.ventana.fig.canvas.mpl_connect('button_press_event', onclick)
        self.pestannas.ventana.canvas.draw()           
         
    def anadir_lineas(self):
        self.pestannas.p_2.setStyleSheet('color: black')
        self.pestannas.P1.setStyleSheet('color: black') 
        self.pestannas.P1_x.setText("0")
        self.pestannas.P1_y.setText("0")
        self.pestannas.P2_x.setText("0")
        self.pestannas.P2_y.setText("0")
        if self.pestannas.ventana.c1 != None and self.pestannas.ventana.c2 != None:        
            row = self.pestannas.table.rowCount()
            self.pestannas.table.insertRow(row)
            self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[0]))))
            self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[1]))))
            self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[0]))))
            self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[1]))))
            self.pestannas.ventana.tam_segmen_verdad = len(self.pestannas.ventana.lineas)
            self.pestannas.ventana.c1 = None
            self.pestannas.ventana.c2 = None
        self.mostrar_tabla()
        self.pestannas.button3.setEnabled(False)
        item = self.pestannas.table.item(row, 0)
        self.pestannas.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.pestannas.table.selectRow(row)
        self.pestannas.button7.setEnabled(True)
        self.pestannas.ventana.padre.save_file.setEnabled(True) 
         
    def mostrar_tabla(self):
        row = self.pestannas.table.rowCount()
        segmentos = []
        x1, x2, y1, y2 = 0, 0, 0, 0
        for i in range(row):            
            x1 = int(self.pestannas.table.item(i, 0).text())
            x2 = int(self.pestannas.table.item(i, 1).text())
            y1 = int(self.pestannas.table.item(i, 2).text())
            y2 = int(self.pestannas.table.item(i, 3).text())
            # print(x1,x2,y1,y2)
            segmentos.append(((x1, x2), (y1, y2)))
 
        self.pestannas.ventana.pintar_imagen_y_segmentos(segmentos)
        self.pestannas.ventana.selec_ante = None
        self.pestannas.ventana.canvas.draw()   
                  
    def limpiar_tabla(self):
        for i in reversed(range(self.pestannas.table.rowCount())):
            self.pestannas.table.removeRow(i)
        self.mostrar_tabla()
        self.pestannas.button7.setEnabled(False)
        self.pestannas.ventana.padre.save_file.setEnabled(False)   
                  
    def borrar_selec(self):
        if self.pestannas.row_actual != -1:
            self.pestannas.table.removeRow(self.pestannas.row_actual)            
            self.pestannas.row_actual = -1
            self.mostrar_tabla()
        if self.pestannas.table.rowCount() > 0:
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
 
        else:
            self.pestannas.button7.setEnabled(False)
            self.pestannas.ventana.padre.save_file.setEnabled(False)
             
    def anadir_puntos(self):
        self.limpiar_tabla()
        row = self.pestannas.table.rowCount()
        if len(self.pestannas.ventana.lineas) != 0:
            for i in self.pestannas.ventana.lineas:
                self.pestannas.table.insertRow(row)
                self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0][0]))))
                self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[0][1]))))
                self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[1][0]))))
                self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[1][1]))))
                row += 1
            self.pestannas.button4.setEnabled(False)
            self.mostrar_tabla()
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
             
    def guardar_tabla(self):
        # Clase PARA LAS estadisticas
        path = QtWidgets.QFileDialog.getExistingDirectory(self.pestannas, "openFolder")
        row = self.pestannas.table.rowCount()
        segmentos = []
        angulos = {}
        long_segmento = {}
        lista = []
        x1, x2, y1, y2 = 0, 0, 0, 0
        for i in range(row):            
            x1 = int(self.pestannas.table.item(i, 0).text())
            x2 = int(self.pestannas.table.item(i, 1).text())
            y1 = int(self.pestannas.table.item(i, 2).text())
            y2 = int(self.pestannas.table.item(i, 3).text())
            # print(x1,x2,y1,y2)
            segmentos.append(((x1, x2), (y1, y2)))
            angulos[((x1, x2), (y1, y2))] = self.estad.angu(((x1, x2), (y1, y2)))
            long_segmento[((x1, x2), (y1, y2))] = self.estad.longitud_segemento(((x1, x2), (y1, y2)))   
             
        v, h, md, dm, total = self.estad.clasificar(segmentos, angulos, long_segmento)
    
        st_v, st_h, st_md, st_dm, st_tot, variables_tabla = self.estad.calcular_estadisticas(v, h, md, dm, total)
   
        informe = Informe(variables_tabla, path)  # @UnusedVariable
 
        lista.extend([v, h, md, dm, st_v, st_h, st_md, st_dm, st_tot])
        self.escribeCSV.escribe_csv(path, lista)               
        self.pestannas.button7.setEnabled(False)
        self.pestannas.ventana.padre.save_file.setEnabled(False)
