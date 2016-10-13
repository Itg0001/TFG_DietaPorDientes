# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import networkx as nx
from networkx.algorithms import approximation as apxa

from codigo.procesado import Procesado
from gui.PanelDePestannas import PanelDePestannas
from codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas
##Clase Ventana 
#Esta clase contendra la ventana principal de la aplcacion en la que colgaran los diferentes 
#componentes.
class Window(QtWidgets.QWidget):

    def __init__(self,path, parent=None ):
        super(Window, self).__init__(parent)
        self.resize(900, 700)
        self.path=path
        #----------------Inicializaciones de variables----------------------
        #Figura sobre la que trabajaremos
        self.fig = Figure((6.5, 5.0), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        #Guardar Coordenadas
        self.c1=0
        self.c2=0
        #Guardar Tamano
        self.tam_segmen_verdad=-1
        
        self.pestannas=PanelDePestannas(self)
        self.procesado=Procesado()
        self.procesado_de_lineas=ProcesadoDeLineas()

        #Guardamso las lineas pintadas para poder acceder desde otros metodos
        self.lineas=[]
        #self.pintados=[]
        #Guardamso la columna actual de la tabla al clicar sobre ella
        self.row_actual=-1
        #Guardamos la linea seleccionada para poder borrarla mas adelante
        self.selec_ante=None
        #Creamso una instancia d la clase procesado para llamar a sus funciones.
        self.padre=parent        
        #parent.save_file.setEnabled(True)        
        #Estadisticas para las lineas.
        #Clase que contiene el metodo de clasificacion
        #vamos invocando al procesado de la imagen.
        self.img=self.procesado.leer_imagen(path)
        self.distance_red=self.procesado.distancia_al_rojo(self.img)
        self.img_bin=self.procesado.binarizar(self.distance_red)
        #---------------------------------------------------------------
        self.padre.save_file.setEnabled(False)

    
        
        #------Para mostrar la Imagen del inicio--------------------------
        #self.imgBinCrop,self.imgCrop=cropImg(self.img_bin,self.img)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Figura sin lineas')
        self.ax.set_xlim([0,self.img.shape[1]])
        self.ax.set_ylim([self.img.shape[0],0])
        self.ax.imshow(self.img ,origin='upper',vmax=1,interpolation='nearest')
    #-------------------------------------------------------
        
        #------Creamos los componentes -------------------------
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
      
        

        
        #-------------------------------------------------------

        #------Asignamos los componentes a un layout----------
        layout_tabs=QtWidgets.QHBoxLayout()
        #layout principal - - 
        
        laout_principal = QtWidgets.QHBoxLayout()
        # Layout (-) - /n 1
        layout_primero = QtWidgets.QVBoxLayout() 
        layout_primero.addWidget(self.toolbar)
        layout_primero.addWidget(self.canvas)
        # Layout - (-) /n 1 y 2
            
        layout_tabs.addWidget(self.pestannas)
        layout_tabs.setAlignment(QtCore.Qt.AlignRight)

        laout_principal.addLayout(layout_primero)
        laout_principal.setStretch(0,2)
        laout_principal.addLayout(layout_tabs)
        laout_principal.setStretch(2,3)

        
        self.setLayout(laout_principal)#Asignamos como principal el principal
        #-------------------------------------------------------------------
                     

    
    def calcular_lineas(self):        
        sin_ruido=self.procesado.reducir_grosor(self.img_bin)
        lines=self.procesado.pro_hough(10,5,11,sin_ruido)        
        G=nx.Graph()
        G=self.procesado_de_lineas.combina(8,4,lines,G)
        k_components = apxa.k_components(G)
        segmentos_de_verdad=self.procesado_de_lineas.segmentos_verdad(k_components,lines)
        #print(sys.version_info)
        self.pintar_imagen_y_segmentos(segmentos_de_verdad)
        self.canvas.draw()
        self.lineas=segmentos_de_verdad
        self.tam_segmen_verdad=len(self.lineas)
        self.pestannas.button4.setEnabled(True)
        self.selec_ante=None

        
    def pintar_imagen_y_segmentos(self,segmentos):
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Figura con lineas')
        self.ax.set_xlim([0,self.img.shape[1]])
        self.ax.set_ylim([self.img.shape[0],0])
        self.ax.imshow(self.img ,origin='upper',vmax=1, interpolation='nearest')
        self.ax.hold(True)
        for line in segmentos:
            p0, p1 = line
            #print(ang((p0,p1),((10, 0), (500, 0))))
            self.ax.set_title('Figura con lineas')
            self.ax.set_xlim([0,self.img.shape[1]])
            self.ax.set_ylim([self.img.shape[0],0])
            self.ax.plot((p0[0], p1[0]), (p0[1], p1[1]),'b',linewidth=2.0)
            #print(type(p0[0]))
        self.ax.hold(False)
        self.canvas.draw()

    