
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from proyecto.gui.PanelDePestannas import PanelDePestannas
from proyecto.gui.Mediadores import MediadorVentana


class Window(QtWidgets.QWidget):
    """
    Clase Ventana 
    Esta clase contendra la ventana principal de la aplcacion en la que colgaran los diferentes 
    componentes.    
    
    @var path : Guardamos el camino desde donde se llama.
    @var padre: Guardamos la instancia del padre que crea la ventana.
    @var pestannas: creamso el objeto de pestannas que contendra la ventana.            
    @var mediador_ventana: creamos la instancia del mediador de la ventana.    
    @var c1: punto inicializado a 0.
    @var c2: punto inicializado a  0.
    @var tam_segmen_verdad: Guardar Tamano.
    @var lineas: Guardamso las lineas pintadas para poder acceder desde otros metodos.
    @var pintados: Guardamso las lineas pintadas para poder acceder desde otros metodos .
    @var row_actual:Guardamso la columna actual de la tabla al clicar sobre ella.
    @var selec_ante: Guardamos la linea seleccionada para poder borrarla mas adelante.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    def __init__(self, path, parent=None):
        """
        Constructor de la clase ventana que inicializa todo lo necesario para poder
        aplicarlos mas adelante.
        
        @param path: Guardamos el camino desde donde se llama. 
        @param parent: Guardamos la instancia del padre que crea la ventana.
        """
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
        self.inicializa_pestanna_1()
        
        self.xMax=self.mediador_ventana.img.shape[1]
        self.xMin=0
        self.yMax=self.mediador_ventana.img.shape[0]
        self.yMin=0
        self.detectar_cuadrado()

        
    def detectar_cuadrado(self):   
        self.mediador_ventana.detectar_cuadrado()
    
     
    def inicializa_figura_y_widgets(self):
        """
        Metodo para inicializar la figura y los widgets de la ventana.
        concretamente incializamos la figura , los ejes,
        el FigureCanvas donde ponder la imagen
        y La barra de navegacion predeterminada
        
        """        
        # Figura sobre la que trabajaremos
        self.fig = Figure((6.5, 5.0), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        # Guardar Coordenadas
        # Widgets
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
           
    def inicializa_pestanna_1(self):
        """
        Metodo que inicializa el panel de pestañas de la ventana 1 junto con los layouts
        necearios para poder mostrar y cuadrar dicho componente compuesto.
        """
        self.mediador_ventana.inicializa_pestanna_1()

    def calcular_lineas(self): 
        """
        Metodo para calcular las lineas de la imagen pintadas en rojo.
        """       
        self.mediador_ventana.calcular_lineas(int(self.pestannas.combo_repeti.currentText()),int(self.pestannas.combo_lon.currentText()))
        self.canvas.draw()

    def pintar_imagen_y_segmentos(self, segmentos):
        """
        Metodo para pintar en el figurecamvas la imagen y los segmentos(actualizar).
        
        @param segmentos: segmentos que hay que pintar.
        """
        self.mediador_ventana.pintar_imagen_y_segmentos(segmentos)
        self.canvas.draw()

    
