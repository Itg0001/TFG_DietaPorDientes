from PyQt5 import QtCore, QtWidgets
import networkx as nx,os
from networkx.algorithms import approximation as apxa
from skimage.morphology import  skeletonize 
from skimage.transform import probabilistic_hough_line
from proyecto.codigo.procesado import ProcesadoDeImagen
from proyecto.codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas
from proyecto.diccionario import DiccionarioING
from proyecto.diccionario import Diccionario
from proyecto.gui.PintarRectangulo import PintarRectangulo
class MediadorVentana():
    def __init__(self, ventana,idioma):
        """
        Constructor de la clase ventana que nos proporciona las inicializaciones de
        variables y de objetos que vana a ser encesarios para su gestion e implementacion
        de los metodos que va a contener la ventana.
        
        @param ventana: instancia de la clase que crea la ventana.
        """

        self.idioma=idioma
        if self.idioma=="ESP":
            self.dic=Diccionario()
        else:
            self.dic=DiccionarioING()
        self.ventana = ventana
        self.ventana.ax = self.ventana.fig.add_subplot(111)
        self.procesado = ProcesadoDeImagen()
        self.procesado_de_lineas = ProcesadoDeLineas()
        self.img = self.procesado.leer_imagen(self.ventana.path)
        self.ventana.ax = self.ventana.fig.add_subplot(111)
        self.ventana.ax.set_xlim([0, self.img.shape[1]])
        self.ventana.ax.set_ylim([self.img.shape[0], 0])
        self.ventana.ax.imshow(self.img , interpolation=self.dic.md_v_ori)
        if os.name=='nt':
            self.ref_numeros=self.procesado.obtener_numeros(self.img)
        else:
            self.ref_numeros=100
        self.color=[]
        self.ventana.pestannas.button.setEnabled(False)
        self.terminar=False
        self.detectado=True
        
    def obtener_color(self):
        """
        Metodo encargado de la correccion manual de las lineas que hayan quedado sin 
        detectar por nuestro algoritmo.
        """
        self.ventana.pestannas.button.setEnabled(False)
        self.ventana.pestannas.button33.setEnabled(False)
        def onclick(event):
            """
            Metodo interno de la funcion anterior que se encargara de obtener las coordenadas
            de los puntos que bayamos clicando.
            
            @param Event: evento que contiene las coordenadas del punto clicado.

            @return: Coordenadas P1 y P2
            """ 
            ix, iy = event.xdata, event.ydata
            coords=[]
            if iy!=None and ix!=None:
                self.color=self.img[int(round(iy,0)),int(round(ix,0))]
                h,s,v=self.procesado.pixelrgb_2_hsv(self.color)
                if s>0.6:
                    self.distance_red = self.procesado.distancia_al_rojo(self.img,self.color)
                    self.img_bin = self.procesado.binarizar(self.distance_red)
                    self.ventana.fig.canvas.mpl_disconnect(cid)
                    self.ventana.pestannas.button.setEnabled(True)
                    r,g,b=self.color
                    self.ventana.pestannas.color_sele.setText("")
                    self.ventana.pestannas.color_sele.setStyleSheet("background-color: rgb("+str(r)+","+str(g)+","+str(b)+")")
                    self.ventana.pestannas.button33.setEnabled(True)

                else:
                    self.ventana.pestannas.button.setEnabled(False)
                    self.color=self.img[int(round(iy,0)),int(round(ix,0))]
                    h,s,v=self.procesado.pixelrgb_2_hsv(self.color)
                    h,v=h,v
                    self.ventana.pestannas.color_sele.setText(self.dic.md_pe_no_sel)
                    self.ventana.pestannas.color_sele.setStyleSheet("background-color: rgb(255,255,255)")
                return coords
        cid = self.ventana.fig.canvas.mpl_connect(self.dic.md_pe_but_press, onclick)

           
    def detectar_cuadrado(self):
        """
        Metodo para detectar el cuadrado sobre el que poder pintar las lineas que hemos detectado.
        """    
        grises=self.procesado.binarizar_para_cuadrado(self.img)
        sin_ruido = skeletonize(grises)
        lines = probabilistic_hough_line(sin_ruido, threshold=100, line_length=200,line_gap=200)
        self.ventana.x_max,self.ventana.x_min,self.ventana.y_max,self.ventana.y_min=self.procesado.obtener_max_y_min(lines)
        if self.ventana.x_max==0 and self.ventana.x_min==0 and self.ventana.y_max==0 and self.ventana.y_min==0:
            self.pintar_rect=PintarRectangulo(self.ventana.ax)
            self.pintar_rect.connect()
            self.terminar=True
            self.detectado=False
            self.ventana.pestannas.button33.setEnabled(False)
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
                  
    def calcular_lineas(self,repeticiones,lon_minima):
        """
        Metodo que se encargara de llamar a las funciones de calculo de nuestra aplicacion
        para mostrar y guardar las lineas que han sido calculadas por el algoritmo de deteccion
        de aquellas que ya esten pintadas en color rojo.
        """ 
        sin_ruido = self.procesado.reducir_grosor(self.img_bin)
        l=[]
        while repeticiones>0:
            lines = self.procesado.pro_hough(10, 5, 11, sin_ruido)
            l.extend(lines)
            repeticiones=repeticiones-1      
        G = nx.Graph()
        G = self.procesado_de_lineas.combina(8, 4, l, G)
        k_components = apxa.k_components(G)
        segmentos_de_verdad = self.procesado_de_lineas.segmentos_verdad(k_components, l)
        segmentos_de_verdad_pintar=[]
        for i in segmentos_de_verdad:
            if self.procesado_de_lineas.longitud_linea(i,self.ref_numeros) > lon_minima:
                segmentos_de_verdad_pintar.append(i)    
        self.pintar_imagen_y_segmentos(segmentos_de_verdad_pintar)
        self.ventana.lineas = segmentos_de_verdad_pintar
        self.ventana.tam_segmen_verdad = len(self.ventana.lineas)
        self.ventana.pestannas.button4.setEnabled(True)
        self.ventana.selec_ante = None    
        
    def pintar_imagen_y_segmentos(self, segmentos):
        """
        Metodo que se encargara de pintar la imagen leida y lso segmentos detectados y que esten en la 
        tabla de segmentos o lineas dentro de nuestra aplicacion. 
        es un metodo de actualizacion de la guipru.
        @param segmentos: Lista de segmentos que queremos que entre dentro de la imagen.
        """
        self.ventana.ax.set_xlim([0, self.img.shape[1]])
        self.ventana.ax.set_ylim([self.img.shape[0], 0])
        self.ventana.ax.imshow(self.img , origin=self.dic.md_v_up, vmax=1, interpolation=self.dic.md_v_ori)
        self.ventana.ax.hold(True)
        final=[]
        if self.detectado==False:
            self.ventana.ax.add_patch(self.pintar_rect.r)
        for line in segmentos:
            p0, p1 = line
            self.ventana.ax.set_xlim([0, self.img.shape[1]])
            self.ventana.ax.set_ylim([self.img.shape[0], 0])
            l,= self.ventana.ax.plot((p0[0], p1[0]), (p0[1], p1[1]), self.dic.md_v_color, linewidth=2)
            final.append(l) 
        self.ventana.ax.hold(False)
        self.ventana.canvas.draw()             
