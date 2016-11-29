from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import logging
# from proyecto.diccionario import DiccionarioESP
from proyecto.diccionario import DiccionarioING
from proyecto.diccionario import Diccionario
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as ET2
from proyecto.gui.VisorHtml import VisorHtml
from proyecto.gui.Window import Window

class VentanaInicio(QtWidgets.QMainWindow):
    """
    Clase que implementa la interfaz de la ventana principal donde estaran todos los 
    componentes.

    @var cont_cargar: contador que nos avisara de la primera vex que cargamos 
        la guipru.
        
    @author: Ismael Tobar Garcia
    @version: 1.0    
    """

    def __init__(self,idioma_path, parent=None):
        """
        Constructor de la clase ventana de inicio en el cual 
        inicializaremos las variabel snecsarias para sus futuros usos.
        
        @param parent: padre que llama al panel de pestannas 
        """
        super(VentanaInicio, self).__init__(parent)

        self.idioma_path=idioma_path
        self.idioma=self.carga_idioma(self.idioma_path)
        if self.idioma=="ESP":
            self.dic=Diccionario()
        else:
            self.dic=DiccionarioING()        

        self.resize(900, 700)
        logging.basicConfig(filename=self.dic.ini_log,level=logging.DEBUG)
        self.bandera=False
        self.inicializa_mensages()
        self.carga_acerca(self.dic)
        
        self.ventana=None
        self.setWindowTitle(self.dic.nombre_api)
        self.cont_cargar=0
        self.abierto=0
        self.open_file = QtWidgets.QAction(self.dic.ini_nuevo, self)
        self.open_file.setShortcut(self.dic.ini_o_nuevo)
        self.open_file.setStatusTip(self.dic.ini_p_abrir)
        self.open_file.triggered.connect(self.file_open) 
        
        self.cargar_proye = QtWidgets.QAction(self.dic.ini_abrir_pro, self)
        self.cargar_proye.setShortcut(self.dic.ini_o_abrir_pro)
        self.cargar_proye.setStatusTip(self.dic.ini_p_abrir_pro)
        self.cargar_proye.triggered.connect(self.file_cargar) 
        
        self.cerrar_all = QtWidgets.QAction(self.dic.ini_salir, self)
        self.cerrar_all.setShortcut(self.dic.ini_o_salir)
        self.cerrar_all.setStatusTip(self.dic.ini_p_salir)
        self.cerrar_all.triggered.connect(self.cerrar)    

        self.save_file = QtWidgets.QAction(self.dic.ini_guardar, self)
        self.save_file.setShortcut(self.dic.ini_o_guardar)
        self.save_file.setStatusTip(self.dic.ini_p_guardar)
        self.save_file.triggered.connect(self.file_save)
        self.save_file.setDisabled(True)
        
        self.help_f = QtWidgets.QAction(self.dic.ini_acerca, self)
        self.help_f.setShortcut(QtCore.Qt.Key_F2)
        self.help_f.setStatusTip(self.dic.ini_o_ayuda)
        self.help_f.triggered.connect(self.acerca_de)
        
        self.ayuda_f = QtWidgets.QAction(self.dic.ini_ayuda, self)
        self.ayuda_f.setShortcut(QtCore.Qt.Key_F1)
        self.ayuda_f.setStatusTip(self.dic.ini_o_ayuda)
        self.ayuda_f.triggered.connect(self.ayuda)
        self.statusBar()

        self.ingles = QtWidgets.QAction(self.dic.idioma, self)
        self.ingles.triggered.connect(self.guarda_ingles)
        
        self.espa = QtWidgets.QAction(self.dic.idioma_esp, self)
        self.espa.triggered.connect(self.guarda_espannol)
        
        self.help_f = QtWidgets.QAction(self.dic.ini_acerca, self)
        self.help_f.setShortcut(QtCore.Qt.Key_F2)
        self.help_f.setStatusTip(self.dic.ini_o_ayuda)
        self.help_f.triggered.connect(self.acerca_de)


        main_menu = self.menuBar()
        self.file_menu = main_menu.addMenu(self.dic.ini_archivo)
        self.help_menu = main_menu.addMenu(self.dic.ini_ayuda)
        self.conf_menu = main_menu.addMenu(self.dic.idioma_selec)
        
        self.conf_menu.addAction(self.ingles)
        self.conf_menu.addAction(self.espa)
        
        self.help_menu.addAction(self.help_f)
        self.help_menu.addAction(self.ayuda_f)
        
        self.file_menu.addAction(self.open_file)
        self.file_menu.addAction(self.cargar_proye)
        self.file_menu.addAction(self.save_file)
        self.file_menu.addAction(self.cerrar_all)
        
        self.styleChoice = QtWidgets.QLabel(self.dic.ini_msg, self)
        self.styleChoice.setAlignment(QtCore.Qt.AlignCenter)

        laout_principal = QtWidgets.QHBoxLayout()
        laout_principal.addWidget(self.styleChoice)
        self.styleChoice.setStyleSheet(self.dic.ini_color)
        font = QtGui.QFont(self.dic.ini_time, 35, QtGui.QFont.Bold, True)
        self.styleChoice.setFont(font)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(laout_principal)
        self.setCentralWidget(central_widget)
     
    def mensage_reinicia(self):
        self.msg_reini = QtWidgets.QMessageBox()
        self.msg_reini.adjustSize()
        self.msg_reini.setText(self.dic.info_msg)
        self.msg_reini.setWindowTitle(self.dic.warnn)
        retval = self.msg_reini.exec_()# @UnusedVariable 
        self.cerrar() 
          
    def guarda_ingles(self):
        self.mensage_reinicia()
        self.guarda_idioma(self.idioma_path,"ING")
        
    def guarda_espannol(self):
        self.mensage_reinicia()
        self.guarda_idioma(self.idioma_path,"ESP")
     
        
    def guarda_idioma(self,idioma,idiom):    
            proyect = ET.Element("proyect")
            ET.SubElement(proyect,"docu0", idioma=str(idiom))
            tree = ET.ElementTree(proyect)
            tree.write(idioma + "/Conf.xml", encoding="UTF-8", xml_declaration=True)
            
    def carga_idioma(self,idioma):
        tree = ET2.parse(idioma + "/Conf.xml")
        root = tree.getroot()
        for child in root:
            idiom=child.attrib["idioma"]
    
        return idiom
    
        
    def inicializa_mensages(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.adjustSize()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)    
        self.msg.setText(self.dic.ini_p_cambios)
        self.msg.setWindowTitle(self.dic.ini_p_aviso)
        
    
    def cerrar(self):
        """
        Metodo para cerrar la aplicacion de forma apropiada, si no tenemos cambios en caso 
        de detectar cambios preguntara si queremos guardar o no.
        
        """ 
        if self.abierto==1:
            if self.bandera==True :
                self.showdialog()
                if self.guardar==True:
                    self.ventana.pestannas.mediador_pestannas.guardar_tabla()
                else:
                    self.close()
            else:
                self.close()
        else:
            self.close()
            
    @classmethod  
    def carga_acerca(self,dic):
        """
        Metodo que nos mostrara el acerca de como cuadro de dialogo.
        """
        self.msg_acerca = QtWidgets.QMessageBox()
        self.msg_acerca.adjustSize()
        self.msg_acerca.setText(dic.ini_msg_acerca)
        self.msg_acerca.setWindowTitle(dic.ini_acercade)
    @classmethod  
    def acerca_de(self):
        """
        Metodo que nos mostrara el acerca de como cuadro de dialogo.
        """
        retval = self.msg_acerca.exec_()  # @UnusedVariable
        
    def ayuda(self):
        """
        Metodo que implementara la ayuda.
        """
        main = VisorHtml("file:///C:/Users/Tobar/Desktop/hh.html")
        
        main.exec_()
    
    def cargar_inicializacion_open(self):
        """
        Metodo que va a mostrar la pantalla de dialogo para elegir las iamgenes 
        a abrir.
        """
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, self.dic.ini_p_abri, self.dic.ini_p_dir, self.dic.ini_p_opt)
        self.abierto=1
        self.ventana = Window(self.path[0], self) 
        self.bandera=False
        self.setCentralWidget(self.ventana)    
        
    def file_open(self):
        """
        Metodo correspondiente al boton de abrir imagen que nos proporcionara la vista
        de la imagen y su procesado y deteccion de las lineas a partir de una iamgen que
        este pintadas sus lineas en tojo.
        """
        try:
            if self.cont_cargar==0:
                self.cargar_inicializacion_open()
                self.cont_cargar=self.cont_cargar+1
            else:
                if self.bandera==True:
                    self.showdialog()
                    self.opciones_guardar(1)
                else:
                    self.cargar_inicializacion_open()
        except:
            exc=self.dic.ini_p_war+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print(self.dic.ini_p_err, sys.exc_info()[0], sys.exc_info()[1])

      
    def opciones_guardar(self,opt):
        """
        Metodo para elegir si cargamso la pantalla de abrir proyecto o crear
        nuevo proyecto.
        @param opt: opcion que elegiremos dependiendo de donde lo llamemos. 
        """
        if self.guardar==True:
            self.ventana.pestannas.mediador_pestannas.guardar_tabla()
        else:
            if opt==1:
                self.cargar_inicializacion_open()   
            else:
                self.cargar_inicializacion()

    def file_save(self):
        """
        Metodo correspondiente al boton de guardar los cambios echos en nuestra aplicacion 
        en un proyecto nuevo.
        """
        try:
            self.ventana.pestannas.guardar_tabla()
        except :
            exc=self.dic.ini_p_war+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print(self.dic.ini_p_war, sys.exc_info()[0], sys.exc_info()[1])
            
    def msgbtn(self, i):
        """
        Metodo auxiliar para poder guardar la eleccion que seleccionamos del popap que nos 
        indica si queremos guardar o no.
        
        @param i: informacion del componente que clicamos. 
        """
        if i.text() == self.dic.ini_p_ok:                      
            self.guardar = True
        else:
            self.guardar = False
                    
    def showdialog(self):
        """
        Metodo para mostrar la ventana de elegir de si queremos guardar o no 
        los cambios.        
        """

        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.msgbtn)
        retval = self.msg.exec_()  # @UnusedVariable
                
    def cargar_inicializacion(self):
        """
        Metodo que va a mostrar la pantalla de dialogo para elegir al cargar 
        un proyecto.             
        """
        path = QtWidgets.QFileDialog.getExistingDirectory(self, self.dic.ini_p_cargar)
        self.abierto=1
        self.ventana = Window(path+self.dic.origi , self)
        self.bandera=False
        self.setCentralWidget(self.ventana)
        try:
            self.ventana.pestannas.cargar_proyec(path)
        except:
            exc=self.dic.ini_p_war_amp+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            
    def file_cargar(self):
        """
        Metodo correspondiente al boton de cargar un proyecto existente para poder editar las 
        lineas que hemos abierto y previamente guardadas en otro proyecto.
        """
        try:
            if self.cont_cargar==0:
                self.cargar_inicializacion()
                self.cont_cargar=self.cont_cargar+1
            else:
                if self.bandera==True:
                    self.showdialog()
                    self.opciones_guardar(0)
                else:
                    self.cargar_inicializacion()
        except:
            exc=self.dic.ini_p_war+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print(self.dic.ini_p_err, sys.exc_info()[0], sys.exc_info()[1])