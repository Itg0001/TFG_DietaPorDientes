from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from .Window import Window
import logging

class VentanaInicio(QtWidgets.QMainWindow):
    """
    Clase que implementa la interfaz de la ventana principal donde estaran todos los 
    componentes.

    @var cont_cargar: contador que nos avisara de la primera vex que cargamos 
        la gui.
        
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
        logging.basicConfig(filename='logger.log',level=logging.DEBUG)

        self.cont_cargar=0
        open_file = QtWidgets.QAction("&Nuevo proyecto", self)
        open_file.setShortcut("Ctrl+O")
        open_file.setStatusTip('Abrir imagen')
        open_file.triggered.connect(self.file_open) 
        
        cargar_proye = QtWidgets.QAction("&Abrir proyecto", self)
        cargar_proye.setShortcut("Ctrl+A")
        cargar_proye.setStatusTip('Abrir Proyecto')
        cargar_proye.triggered.connect(self.file_cargar)     

        self.save_file = QtWidgets.QAction("&Guardar proyecto", self)
        self.save_file.setShortcut("Ctrl+G")
        self.save_file.setStatusTip('Guardar csv y .tex')
        self.save_file.triggered.connect(self.file_save)
        self.save_file.setDisabled(True)
        
        self.help_f = QtWidgets.QAction("&Acerca de", self)
        self.help_f.setShortcut(QtCore.Qt.Key_F2)
        self.help_f.setStatusTip('Ayuda')
        self.help_f.triggered.connect(self.acerca_de)
        
        self.ayuda_f = QtWidgets.QAction("&Ayuda", self)
        self.ayuda_f.setShortcut(QtCore.Qt.Key_F1)
        self.ayuda_f.setStatusTip('Ayuda')
        self.ayuda_f.triggered.connect(self.ayuda)
        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&Archivo')
        help_menu = main_menu.addMenu('&Ayuda')
        help_menu.addAction(self.help_f)
        help_menu.addAction(self.ayuda_f)
        
        file_menu.addAction(open_file)
        file_menu.addAction(cargar_proye)
        file_menu.addAction(self.save_file)
        self.styleChoice = QtWidgets.QLabel("Cargar imagen para iniciar", self)
        self.styleChoice.setAlignment(QtCore.Qt.AlignCenter)

        laout_principal = QtWidgets.QHBoxLayout()
        laout_principal.addWidget(self.styleChoice)
        self.styleChoice.setStyleSheet('color: red')
        font = QtGui.QFont("Times", 35, QtGui.QFont.Bold, True)
        self.styleChoice.setFont(font)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(laout_principal)
        self.setCentralWidget(central_widget)
    @classmethod   
    def acerca_de(self):
        """
        Metodo que nos mostrara el acerca de como cuadro de dialogo.
        """
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setText("Autores: \n\tIsmael Tobar García \n\tAlvar Gonzalez Arnaiz\n\tJose Francisco Diez Pastor\nVersion: \n\t1.0 ")
        msg.setWindowTitle("Acerca de")
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
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir imagen', 'c:/', "Image files (*.jpg )")
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
                if self.ventana.pestannas.mediador_pestannas.bandera==True:
                    self.showdialog()
                    self.opciones_guardar(1)
                else:
                    self.cargar_inicializacion_open()
        except:
            exc="Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print("Error:", sys.exc_info()[0], sys.exc_info()[1])

      
    def opciones_guardar(self,opt):
        """
        Metodo para elegir si cargamso la pantalla de abrir proyecto o crear
        nuevo proyecto.
        @param opt: opcion que elegiremos dependiendo de donde lo llamemos. 
        """
        if self.guardar==True:
            self.ventana.pestannas.mediador_pestannas.guardar_tabla()  
            self.ventana.pestannas.mediador_pestannas.bandera=False
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
            exc="Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print("Warning:", sys.exc_info()[0], sys.exc_info()[1])
            
    def msgbtn(self, i):
        """
        Metodo auxiliar para poder guardar la eleccion que seleccionamos del popap que nos 
        indica si queremos guardar o no.
        
        @param i: informacion del componente que clicamos. 
        """
        if i.text() == "OK":                      
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
        msg.setText("Se han detectado cambios desea guardar")
        msg.setWindowTitle("Aviso")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()  # @UnusedVariable
                
    def cargar_inicializacion(self):
        """
        Metodo que va a mostrar la pantalla de dialogo para elegir al cargar 
        un proyecto.             
        """
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Cargar Proyecto")
        self.ventana = Window(path+'/Original.jpg' , self)
        self.setCentralWidget(self.ventana)
        try:
            self.ventana.pestannas.cargar_proyec(path)
        except:
            exc="Warning: fichero csv no existe"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
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
                if self.ventana.pestannas.mediador_pestannas.bandera==True:
                    self.showdialog()
                    self.opciones_guardar(0)
                else:
                    self.cargar_inicializacion()
        except:
            exc="Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print("Error:", sys.exc_info()[0], sys.exc_info()[1])
            
