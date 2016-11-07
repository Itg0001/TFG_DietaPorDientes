from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from .Window import Window
import logging
from proyecto.diccionario import Diccionario

class VentanaInicio(QtWidgets.QMainWindow):
    """
    Clase que implementa la interfaz de la ventana principal donde estaran todos los 
    componentes.

    @var cont_cargar: contador que nos avisara de la primera vex que cargamos 
        la guipru.
        
    @author: Ismael Tobar Garcia
    @version: 1.0    
    """

    def __init__(self, parent=None):
        """
        Constructor de la clase ventana de inicio en el cual 
        inicializaremos las variabel snecsarias para sus futuros usos.
        
        @param parent: padre que llama al panel de pestannas 
        """

        
        super(VentanaInicio, self).__init__(parent)
        self.resize(900, 700)
        self.dic=Diccionario()        
        logging.basicConfig(filename=self.dic.ini_log,level=logging.DEBUG)
        self.bandera=False
    
        self.cont_cargar=0
        self.abierto=0
        open_file = QtWidgets.QAction(self.dic.ini_nuevo, self)
        open_file.setShortcut(self.dic.ini_o_nuevo)
        open_file.setStatusTip(self.dic.ini_p_abrir)
        open_file.triggered.connect(self.file_open) 
        
        cargar_proye = QtWidgets.QAction(self.dic.ini_abrir_pro, self)
        cargar_proye.setShortcut(self.dic.ini_o_abrir_pro)
        cargar_proye.setStatusTip(self.dic.ini_p_abrir_pro)
        cargar_proye.triggered.connect(self.file_cargar) 
        
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
        


        main_menu = self.menuBar()
        file_menu = main_menu.addMenu(self.dic.ini_archivo)
        help_menu = main_menu.addMenu(self.dic.ini_ayuda)
        
        
        help_menu.addAction(self.help_f)
        help_menu.addAction(self.ayuda_f)
        
        file_menu.addAction(open_file)
        file_menu.addAction(cargar_proye)
        file_menu.addAction(self.save_file)
        file_menu.addAction(self.cerrar_all)
        
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
    def parametros(self):
        pass
        
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
    def acerca_de(self):
        """
        Metodo que nos mostrara el acerca de como cuadro de dialogo.
        """
        self.dic=Diccionario()
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setText(self.dic.ini_msg_acerca)
        msg.setWindowTitle(self.dic.ini_acercade)
        retval = msg.exec_()  # @UnusedVariable
        
    def ayuda(self):
        """
        Metodo que implementara la ayuda.
        """
        pass
    
    def cargar_inicializacion_open(self):
        """
        Metodo que va a mostrar la pantalla de dialogo para elegir las iamgenes 
        a abrir.
        """
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, self.dic.ini_p_abri, self.dic.ini_p_dir, self.dic.ini_p_opt)
        self.abierto=1
        self.ventana = Window(self.path[0], self) 
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
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setIcon(QtWidgets.QMessageBox.Warning)    
        msg.setText(self.dic.ini_p_cambios)
        msg.setWindowTitle(self.dic.ini_p_aviso)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()  # @UnusedVariable
                
    def cargar_inicializacion(self):
        """
        Metodo que va a mostrar la pantalla de dialogo para elegir al cargar 
        un proyecto.             
        """
        path = QtWidgets.QFileDialog.getExistingDirectory(self, self.dic.ini_p_cargar)
        self.abierto=1
        self.ventana = Window(path+self.dic.origi , self)
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
            
