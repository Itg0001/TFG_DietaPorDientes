from PyQt5 import QtCore, QtWidgets
import networkx as nx
from networkx.algorithms import approximation as apxa
from codigo.procesado import ProcesadoDeImagen
from codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas

class MediadorVentana():
    def __init__(self, ventana):
        """
        Constructor de la clase ventana que nos proporciona las inicializaciones de
        variables y de objetos que vana a ser encesarios para su gestion e implementacion
        de los metodos que va a contener la ventana.
        
        @param ventana: instancia de la clase que crea la ventana.
        """
        self.ventana = ventana
        self.procesado = ProcesadoDeImagen()
        self.procesado_de_lineas = ProcesadoDeLineas()
        
        self.img = self.procesado.leer_imagen(self.ventana.path)
        self.distance_red = self.procesado.distancia_al_rojo(self.img)
        self.img_bin = self.procesado.binarizar(self.distance_red)
        
        self.ventana.ax = self.ventana.fig.add_subplot(111)
        self.ventana.ax.set_title('Figura sin lineas')
        self.ventana.ax.set_xlim([0, self.img.shape[1]])
        self.ventana.ax.set_ylim([self.img.shape[0], 0])
        self.ventana.ax.imshow(self.img , interpolation='nearest')
     
    def inicializa_pestanna_1(self):
        """
        Metodo que inicializara la pestanna uno de la ventana es decir el cuadro principal
        de dicha ventana.
        """
        #------Asignamos los componentes a un layout----------
        self.ventana.layout_tabs = QtWidgets.QHBoxLayout()
        # layout principal - - 
        self.ventana.laout_principal = QtWidgets.QHBoxLayout()
        # Layout (-) - /n 1
        self.ventana.layout_primero = QtWidgets.QVBoxLayout() 
        self.ventana.layout_primero.addWidget(self.ventana.toolbar)
        self.ventana.layout_primero.addWidget(self.ventana.canvas)
        # Layout - (-) /n 1 y 2
             
        self.ventana.layout_tabs.addWidget(self.ventana.pestannas)
        self.ventana.layout_tabs.setAlignment(QtCore.Qt.AlignRight)
 
        self.ventana.laout_principal.addLayout(self.ventana.layout_primero)
        self.ventana.laout_principal.setStretch(0, 2)
        self.ventana.laout_principal.addLayout(self.ventana.layout_tabs)
        self.ventana.laout_principal.setStretch(2, 3)
         
        self.ventana.setLayout(self.ventana.laout_principal)  # Asignamos como principal el principal  
        self.ventana.padre.save_file.setEnabled(False)
                  
    def calcular_lineas(self):
        """
        Metodo que se encargara de llamar a las funciones de calculo de nuestra aplicacion
        para mostrar y guardar las lineas que han sido calculadas por el algoritmo de deteccion
        de aquellas que ya esten pintadas en color rojo.
        """ 
        sin_ruido = self.procesado.reducir_grosor(self.img_bin)
        lines = self.procesado.pro_hough(10, 5, 11, sin_ruido)        
        G = nx.Graph()
        G = self.procesado_de_lineas.combina(8, 4, lines, G)
        k_components = apxa.k_components(G)
        segmentos_de_verdad = self.procesado_de_lineas.segmentos_verdad(k_components, lines)
        self.pintar_imagen_y_segmentos(segmentos_de_verdad)
        self.ventana.lineas = segmentos_de_verdad
        self.ventana.tam_segmen_verdad = len(self.ventana.lineas)
        self.ventana.pestannas.button4.setEnabled(True)
        self.ventana.selec_ante = None    
        
    def pintar_imagen_y_segmentos(self, segmentos):
        """
        Metodo que se encargara de pintar la imagen leida y lso segmentos detectados y que esten en la 
        tabla de segmentos o lineas dentro de nuestra aplicacion. 
        es un metodo de actualizacion de la gui.
        @param segmentos: Lista de segmentos que queremos que entre dentro de la imagen.

        """
        self.ventana.ax = self.ventana.fig.add_subplot(111)
        self.ventana.ax.set_title('Figura con lineas')
        self.ventana.ax.set_xlim([0, self.img.shape[1]])
        self.ventana.ax.set_ylim([self.img.shape[0], 0])
        self.ventana.ax.imshow(self.img , origin='upper', vmax=1, interpolation='nearest')
        self.ventana.ax.hold(True)
        final=[]
        for line in segmentos:
            p0, p1 = line
            self.ventana.ax.set_title('Figura con lineas')
            self.ventana.ax.set_xlim([0, self.img.shape[1]])
            self.ventana.ax.set_ylim([self.img.shape[0], 0])
            l,= self.ventana.ax.plot((p0[0], p1[0]), (p0[1], p1[1]), 'b', linewidth=2)
            final.append(l)
        self.ventana.ax.hold(False)
        self.ventana.canvas.draw()             

