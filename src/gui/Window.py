# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5 import QtCore
#from PyQt5.QtCore import *
#from PyQt5.QtGui  import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import networkx as nx
from networkx.algorithms import approximation as apxa
from codigo.procesado import Procesado

from gui.PanelDePestañas import PanelDePestañas
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
        self.tamSegmenVerdad=-1
        
        self.pestañas=PanelDePestañas(self)
        self.procesado=Procesado()

        #Guardamso las lineas pintadas para poder acceder desde otros metodos
        self.lineas=[]
        #self.pintados=[]
        #Guardamso la columna actual de la tabla al clicar sobre ella
        self.rowActual=-1
        #Guardamos la linea seleccionada para poder borrarla mas adelante
        self.SelecAnte=None
        #Creamso una instancia d la clase procesado para llamar a sus funciones.
        self.padre=parent        
        #parent.saveFile.setEnabled(True)        
        #Estadisticas para las lineas.
        #Clase que contiene el metodo de clasificacion
        #vamos invocando al procesado de la imagen.
        self.img=self.procesado.leerImagen(path)
        self.distance_red=self.procesado.distanciaAlRojo(self.img)
        self.imgBin=self.procesado.binarizar(self.distance_red)
        #---------------------------------------------------------------
        self.padre.saveFile.setEnabled(False)

    
        
        #------Para mostrar la Imagen del inicio--------------------------
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
      
        

        
        #-------------------------------------------------------

        #------Asignamos los componentes a un layout----------
        layoutTabs=QtWidgets.QHBoxLayout()
        #layout principal - - 
        
        laoutPrincipal = QtWidgets.QHBoxLayout()
        # Layout (-) - /n 1
        layoutPrimero = QtWidgets.QVBoxLayout() 
        layoutPrimero.addWidget(self.toolbar)
        layoutPrimero.addWidget(self.canvas)
        # Layout - (-) /n 1 y 2
            
        layoutTabs.addWidget(self.pestañas)
        layoutTabs.setAlignment(QtCore.Qt.AlignRight)

        laoutPrincipal.addLayout(layoutPrimero)
        laoutPrincipal.setStretch(0,2)
        laoutPrincipal.addLayout(layoutTabs)
        laoutPrincipal.setStretch(2,3)

        #laoutPrincipal.addWidget(tabs)
        #laoutPrincipal.addLayout(layoutSegundo)
        
        self.setLayout(laoutPrincipal)#Asignamos como principal el principal
        #-------------------------------------------------------------------
                     

    
    def calcularLineas(self):        
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
        self.pestañas.button4.setEnabled(True)
        self.SelecAnte=None

        
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
            #print(type(p0[0]))
        self.ax.hold(False)
        self.canvas.draw()

    