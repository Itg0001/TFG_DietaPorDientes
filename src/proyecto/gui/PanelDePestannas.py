from PyQt5 import QtWidgets
from proyecto.analisis.MediadorPestannas import MediadorPestannas
from proyecto.analisis.diccionario import DiccionarioING
from proyecto.analisis.diccionario import Diccionario


class PanelDePestannas(QtWidgets.QTabWidget):
    """
    Clase que implementa la guipru del panel de pestannas.
    
    @var ventana: instancia de la clase que llama al panel de pestannas.
    @var mediador_pestannas  mediador del panel de pestannas para actuar
        de intermediario.
    @var row_actual =fila actual que tenemos seleccionada.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    def __init__(self, parent=None):
        """
        Constructor de la clase panel de pestannas que comtendra el panel de 
        pestannas e inicializara luego los compoenentes necesarios tanto 
        la intancia del padre que lo contine para poder comunicarse con el.
        
        @param parent: padre que llama al panel de pestannas 
        """
        #------Creamos los componentes -------------------------
        super(PanelDePestannas, self).__init__(parent)
        self.ventana = parent
        self.idioma=self.ventana.idioma

        self.mediador_pestannas = MediadorPestannas(self,self.idioma)

        self.inicia_paneles()        
        self.tab_1_ui()
        self.tab_2_ui()
        
        if self.idioma=="ESP":
            self.dic=Diccionario()
        else:
            self.dic=DiccionarioING()
            
        self.row_actual = -1
        self.nombres={}
        self.nombres[self.dic.docu1]=self.dic.tab
        self.nombres[self.dic.docu2]=self.dic.sal_estad
        self.nombres[self.dic.docu3]=self.dic.sal_lin
        self.nombres[self.dic.docu4]=self.dic.origi
        self.nombres[self.dic.docu5]=self.dic.pintada

    def inicia_paneles(self):
        """
        Metodo que inicia los paneles del panel de pestannas.
        """
        self.mediador_pestannas.inicia_paneles()
        
    def tab_1_ui(self):
        """
        Metodo que inicializa la ventana del panel de pestañas numero 1.
        """
        self.mediador_pestannas.tab_1_ui()
        
    def tab_2_ui(self): 
        """
        Metodo que inicializa la ventana del panel de pestañas numero 2.
        """
        self.mediador_pestannas.tab_2_ui()

     
    def selected_row(self):
        """
        Metodo para pintar la linea que este seleccionada dentro de la tabla
        de todas las lineas detectadas o pintadas manualmente.
        """
        self.mediador_pestannas.selected_row()
               
    def corregir_lineas(self):
        """
        Metodo para corregir las lineas que no ha detectado el algoritmo.
        Manualmente clicaremos los dos puntos que vamso a corregir y daremos a anadir
        """
        self.mediador_pestannas.corregir_lineas()
           
    def anadir_lineas(self):
        """
        Metodo para añadir la recta que hemos calculado atrabes de la opcion de clicar 
        los dos puntos 
        """
        self.mediador_pestannas.anadir_lineas()      
        
    def limpiar_tabla(self):
        """
        Metodo para limpiar la tabla del panel de pestañas pestaña numero dos.
        """
        self.mediador_pestannas.limpiar_tabla()
   
    def borrar_selec(self):
        """
        Metodo para borrar la linea que hemos seleccionado.
        """
        self.mediador_pestannas.borrar_selec()
            
    def anadir_puntos(self):
        """
        Metodo para annadir las lineas que ha detectado el algoritmo dentro 
        de la tabla para poder editarlas y o guardarlas.
        """
        self.mediador_pestannas.anadir_puntos()
            
    def guardar_tabla(self):
        """
        Metodo que se encargara de hacer todas las funciones necearias para guardar la 
        tabla.         
        """
        self.mediador_pestannas.guardar_tabla()
        
    def cargar_proyec(self, path):
        """
        Metodo para cargar un proyecto existente, leer las lineas que tiene guardadas
        , annadirlas a al tabla y pintarlas en la imagen.
        
        @param path: camino donde guardar el proyecto.
        """
        self.mediador_pestannas.cargar_proyec(path)
