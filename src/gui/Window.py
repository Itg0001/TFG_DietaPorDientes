# coding: utf-8

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from gui.PanelDePestannas import PanelDePestannas
from gui.Mediadores import MediadorVentana

# #Clase Ventana 
# Esta clase contendra la ventana principal de la aplcacion en la que colgaran los diferentes 
# componentes.
class Window(QtWidgets.QWidget):
    def __init__(self, path, parent=None):
        super(Window, self).__init__(parent)
        self.resize(900, 700)
        self.path = path
        self.padre = parent    
        self.inicializa_figura_y_widgets()
        
        self.pestannas = PanelDePestannas(self)                
        self.mediador_ventana = MediadorVentana(self)
        
        #----------------Inicializaciones de variables----------------------
        self.c1 = 0
        self.c2 = 0
        # Guardar Tamano
        self.tam_segmen_verdad = -1
        # Guardamso las lineas pintadas para poder acceder desde otros metodos
        self.lineas = []
        # self.pintados=[]
        # Guardamso la columna actual de la tabla al clicar sobre ella
        self.row_actual = -1
        # Guardamos la linea seleccionada para poder borrarla mas adelante
        self.selec_ante = None
        self.inicializa_pestaña_1()
          
     
    def inicializa_figura_y_widgets(self):        
        # Figura sobre la que trabajaremos
        self.fig = Figure((6.5, 5.0), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        # Guardar Coordenadas
        # Widgets
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
           
    def inicializa_pestaña_1(self):
        self.mediador_ventana.inicializa_pestaña_1()

    def calcular_lineas(self):        
        self.mediador_ventana.calcular_lineas()
        self.canvas.draw()

    def pintar_imagen_y_segmentos(self, segmentos):
        self.mediador_ventana.pintar_imagen_y_segmentos(segmentos)
        self.canvas.draw()

    
