'''
Created on 6 nov. 2016

@author: Tobar
'''
from PyQt5 import QtWidgets,QtCore

class FachadaBotonesAndLayaout():
    def __init__(self,pestannas,dic):
        self.pestannas=pestannas
        self.dic=dic
    def inicia_ui1(self):
        self.pestannas.groupBox= QtWidgets.QGroupBox(self.dic.md_pe_lineas_pintadas)
        self.pestannas.groupBox_auto= QtWidgets.QGroupBox(self.dic.md_pe_automatico)
        self.pestannas.groupBox_dire= QtWidgets.QGroupBox("Orientacion del diente")
        
        self.pestannas.group = QtWidgets.QVBoxLayout()

        self.pestannas.addTab(self.pestannas.tab1, self.dic.md_pe_lin_pin) 
        self.pestannas.button = QtWidgets.QPushButton(self.dic.md_pe_calc)
        self.pestannas.button.clicked.connect(self.pestannas.ventana.calcular_lineas)
     
        self.pestannas.button33 = QtWidgets.QPushButton(self.dic.sel_col)
        self.pestannas.button33.clicked.connect(self.pestannas.ventana.obtener_color)

        self.pestannas.color = QtWidgets.QHBoxLayout()
        self.pestannas.color_eti = QtWidgets.QLabel(self.dic.md_pe_col)
        self.pestannas.color_sele = QtWidgets.QLabel(self.dic.md_pe_no_sel)
        self.pestannas.color.addWidget(self.pestannas.color_eti)
        self.pestannas.color.addWidget(self.pestannas.color_sele)
     
        self.pestannas.repetici = QtWidgets.QHBoxLayout()
        self.pestannas.repeticiones = QtWidgets.QLabel(self.dic.md_pe_repe)
        
        self.pestannas.combo_repeti = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pestannas.combo_repeti.setMinimum(1)
        self.pestannas.combo_repeti.setMaximum(7)
        self.pestannas.combo_repeti.setValue(2)
        self.pestannas.combo_repeti.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.pestannas.combo_repeti.setTickInterval(1)
        self.pestannas.combo_repeti.valueChanged.connect(self.pestannas.mediador_pestannas.valuechange_repeti)
        
        self.pestannas.repe_actual = QtWidgets.QLabel(str(self.pestannas.combo_repeti.value()))
        self.pestannas.repe_actual.setStyleSheet(self.dic.md_pe_color_red)

        self.pestannas.long_min_layout = QtWidgets.QHBoxLayout()
        self.pestannas.long_min = QtWidgets.QLabel(self.dic.md_pe_long_min)

        self.pestannas.combo_lon = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pestannas.combo_lon.setMinimum(1)
        self.pestannas.combo_lon.setMaximum(50)
        self.pestannas.combo_lon.setValue(20)
        self.pestannas.combo_lon.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.pestannas.combo_lon.setTickInterval(5)
        self.pestannas.combo_lon.valueChanged.connect(self.pestannas.mediador_pestannas.valuechange_lon)
        
        self.pestannas.lon_actual = QtWidgets.QLabel(str(self.pestannas.combo_lon.value()))
        self.pestannas.lon_actual.setStyleSheet(self.dic.md_pe_color_red)
  
        self.pestannas.direccion_layout = QtWidgets.QHBoxLayout()
        self.pestannas.direccion = QtWidgets.QLabel(self.dic.md_pe_direccion)
        
        self.pestannas.combo_dir = QtWidgets.QComboBox()
        self.pestannas.combo_dir.addItems(self.dic.md_pe_direc)
        self.pestannas.combo_dir.setCurrentIndex(1)
        
        self.pestannas.layout_segundo = QtWidgets.QVBoxLayout() 
       
        self.pestannas.direccion_layout.addWidget(self.pestannas.direccion)
        self.pestannas.direccion_layout.addWidget(self.pestannas.combo_dir)
        self.pestannas.groupBox_dire.setLayout(self.pestannas.direccion_layout)
        
        self.pestannas.layout_direccion = QtWidgets.QVBoxLayout()
        self.pestannas.layout_direccion.addWidget(self.pestannas.groupBox_dire)
        self.pestannas.layout_direccion.setAlignment(QtCore.Qt.AlignTop) 

        self.pestannas.repetici.addWidget(self.pestannas.repeticiones)
        self.pestannas.repetici.addWidget(self.pestannas.repe_actual)
        self.pestannas.layout_segundo.addLayout(self.pestannas.repetici)
        self.pestannas.layout_segundo.addWidget(self.pestannas.combo_repeti)

        self.pestannas.long_min_layout.addWidget(self.pestannas.long_min)
        self.pestannas.long_min_layout.addWidget(self.pestannas.lon_actual)
        self.pestannas.layout_segundo.addLayout(self.pestannas.long_min_layout)
        self.pestannas.layout_segundo.addWidget(self.pestannas.combo_lon)
        self.pestannas.layout_segundo.addLayout(self.pestannas.color)

        self.pestannas.layout_segundo.addWidget(self.pestannas.button33)
        self.pestannas.layout_segundo.addWidget(self.pestannas.button)
        self.pestannas.layout_segundo.setAlignment(QtCore.Qt.AlignTop) 
        self.pestannas.groupBox.setLayout(self.pestannas.layout_segundo)
        
        self.pestannas.slider_lon_auto = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pestannas.slider_lon_auto.setMinimum(20)
        self.pestannas.slider_lon_auto.setMaximum(60)
        self.pestannas.slider_lon_auto.setValue(25)
        self.pestannas.slider_lon_auto.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.pestannas.slider_lon_auto.setTickInterval(5)
        self.pestannas.slider_lon_auto.valueChanged.connect(self.pestannas.mediador_pestannas.cambio_valor_min)
      
        self.pestannas.layout_repeticiones_auto=QtWidgets.QHBoxLayout()
        self.pestannas.long_min_auto = QtWidgets.QLabel(self.dic.md_pe_long_min)
        self.pestannas.lon_auto_actual = QtWidgets.QLabel(str(self.pestannas.slider_lon_auto.value()))
        self.pestannas.lon_auto_actual.setStyleSheet(self.dic.md_pe_color_red)
        self.pestannas.layout_repeticiones_auto.addWidget(self.pestannas.long_min_auto)
        self.pestannas.layout_repeticiones_auto.addWidget(self.pestannas.lon_auto_actual)
        
        self.pestannas.button_auto = QtWidgets.QPushButton(self.dic.md_pe_automati)
        self.pestannas.button_auto.clicked.connect(self.pestannas.ventana.calcular_automatic)
             
        self.pestannas.button_fijar = QtWidgets.QPushButton(self.dic.md_pe_fijar)
        self.pestannas.button_fijar.clicked.connect(self.pestannas.ventana.fijar_cuadrado_auto)
                
        self.pestannas.layout_pestanna_3 = QtWidgets.QVBoxLayout()
        
        self.pestannas.layout_pestanna_3.addLayout(self.pestannas.layout_repeticiones_auto)
        self.pestannas.layout_pestanna_3.addWidget(self.pestannas.slider_lon_auto)
        
        self.pestannas.layout_pestanna_3.addWidget(self.pestannas.button_auto)
        self.pestannas.layout_pestanna_3.addWidget(self.pestannas.button_fijar)

        self.pestannas.layout_pestanna_3.setAlignment(QtCore.Qt.AlignTop)       
        self.pestannas.groupBox_auto.setLayout(self.pestannas.layout_pestanna_3)
        
        self.pestannas.group.addLayout(self.pestannas.layout_direccion)
        self.pestannas.group.addWidget(self.pestannas.groupBox)
        self.pestannas.group.addWidget(self.pestannas.groupBox_auto)
        self.pestannas.group.setAlignment(QtCore.Qt.AlignTop) 

        self.pestannas.tab1.setLayout(self.pestannas.group)
        
    def inicia_ui2(self):
        self.pestannas.layaut_corregir=QtWidgets.QVBoxLayout()
        self.pestannas.layaut_table=QtWidgets.QVBoxLayout()
        self.pestannas.layaut_general=QtWidgets.QVBoxLayout()
        self.pestannas.groupBox_correc= QtWidgets.QGroupBox(self.dic.md_pe_corregir)        
        self.pestannas.groupBox_table= QtWidgets.QGroupBox(self.dic.md_pe_tablas)

        self.pestannas.addTab(self.pestannas.tab2, self.dic.md_pe_corre)

        self.pestannas.button2 = QtWidgets.QPushButton(self.dic.md_pe_corre)
        self.pestannas.button2.clicked.connect(self.pestannas.corregir_lineas)
        
        self.pestannas.button3 = QtWidgets.QPushButton(self.dic.md_pe_anadir_p)
        self.pestannas.button3.clicked.connect(self.pestannas.anadir_lineas)
        self.pestannas.button3.setEnabled(False)

        self.pestannas.button4 = QtWidgets.QPushButton(self.dic.md_pe_anadir_seg)
        self.pestannas.button4.clicked.connect(self.pestannas.anadir_puntos)  
        self.pestannas.button4.setEnabled(False)

        self.pestannas.button5 = QtWidgets.QPushButton(self.dic.md_pe_borrar)
        self.pestannas.button5.clicked.connect(self.pestannas.borrar_selec)
        
        self.pestannas.button7 = QtWidgets.QPushButton(self.dic.md_pe_guardar)
        self.pestannas.button7.clicked.connect(self.pestannas.guardar_tabla)
        self.pestannas.button7.setEnabled(False)

        self.pestannas.button8 = QtWidgets.QPushButton(self.dic.md_pe_limpiar)
        self.pestannas.button8.clicked.connect(self.pestannas.limpiar_tabla)

        self.pestannas.P1 = QtWidgets.QLabel(self.dic.md_pe_p1)
        self.pestannas.p_2 = QtWidgets.QLabel(self.dic.md_pe_p2)
        
        self.pestannas.P1_x = QtWidgets.QLabel(self.dic.md_pe_cero)
        self.pestannas.P1_y = QtWidgets.QLabel(self.dic.md_pe_cero)
        
        self.pestannas.P2_x = QtWidgets.QLabel(self.dic.md_pe_cero)
        self.pestannas.P2_y = QtWidgets.QLabel(self.dic.md_pe_cero)
        
        self.pestannas.table = QtWidgets.QTableWidget(self.pestannas)
        self.pestannas.table.setRowCount(0)
        self.pestannas.table.setColumnCount(4)
        self.pestannas.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pestannas.table.itemSelectionChanged.connect(self.pestannas.selected_row)
        self.pestannas.header = self.pestannas.table.horizontalHeader()
        self.pestannas.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.pestannas.table.setHorizontalHeaderLabels(self.dic.md_pe_cabe_tab)
      
        self.pestannas.layout_tab_2 = QtWidgets.QHBoxLayout()
        
        self.pestannas.layout_pestanna_1 = QtWidgets.QVBoxLayout()
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
        
        self.pestannas.layaut_corregir.addLayout(self.pestannas.layaut_corregir_punto_1)
        self.pestannas.layaut_corregir.addWidget(self.pestannas.button2)
        self.pestannas.groupBox_correc.setLayout(self.pestannas.layaut_corregir)
        self.pestannas.layaut_general.addWidget(self.pestannas.groupBox_correc)
    
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button3)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button5)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button8)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.table)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button4)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button7)
        self.pestannas.layout_tab_2.addLayout(self.pestannas.layout_pestanna_1)
        
        self.pestannas.groupBox_table.setLayout(self.pestannas.layout_tab_2)
        self.pestannas.layaut_table.addWidget(self.pestannas.groupBox_table)
        self.pestannas.layaut_general.addLayout(self.pestannas.layaut_table)
        self.pestannas.tab2.setLayout(self.pestannas.layaut_general)    
        