from PyQt5 import QtWidgets
from gui.Mediadores import MediadorPestannas
class PanelDePestannas(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        #------Creamos los componentes -------------------------
        super(PanelDePestannas, self).__init__(parent)
        self.ventana = parent
        self.mediador_pestannas = MediadorPestannas(self)

        self.inicia_paneles()        
        self.tab_1_ui()
        self.tab_2_ui()
        
        self.row_actual = -1
        
    def inicia_paneles(self):
        self.mediador_pestannas.inicia_paneles()
        
    def tab_1_ui(self):
        self.mediador_pestannas.tab_1_ui()
        
    def tab_2_ui(self): 
        self.mediador_pestannas.tab_2_ui()
     
    def selected_row(self):
        self.mediador_pestannas.selected_row()
               
    def corregir_lineas(self):
        self.mediador_pestannas.corregir_lineas()
           
    def anadir_lineas(self):
        self.mediador_pestannas.anadir_lineas()      
        
    def limpiar_tabla(self):
        self.mediador_pestannas.limpiar_tabla()
   
    def borrar_selec(self):
        self.mediador_pestannas.borrar_selec()
            
    def anadir_puntos(self):
        self.mediador_pestannas.anadir_puntos()
            
    def guardar_tabla(self):
        self.mediador_pestannas.guardar_tabla()