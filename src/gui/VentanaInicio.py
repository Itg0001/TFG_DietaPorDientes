from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from .Window import Window

class VentanaInicio(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        Constructor de la clase ventana de inicio en el cual 
        inicializaremos las variabel snecsarias para sus futuros usos.
        """

        super(VentanaInicio, self).__init__(parent)
        self.resize(900, 700)
        self.cont_cargar=0
        open_file = QtWidgets.QAction("&Abrir imagen", self)
        open_file.setShortcut("Ctrl+O")
        open_file.setStatusTip('Abrir imagen')
        open_file.triggered.connect(self.file_open) 
        
        cargar_proye = QtWidgets.QAction("&Abrir proyecto", self)
        cargar_proye.setShortcut("Ctrl+A")
        cargar_proye.setStatusTip('Abrir Proyecto')
        cargar_proye.triggered.connect(self.file_cargar)     

        self.save_file = QtWidgets.QAction("&Guardar", self)
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
        file_menu = main_menu.addMenu('&Cargar')
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
        
    def acerca_de(self):
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setText("Autores: \n\tIsmael Tobar García \n\tAlvar Gonzalez Arnaiz\n\tJose Francisco Diez Pastor\nVersion: \n\t1.0 ")
        msg.setWindowTitle("Acerca de")
        retval = msg.exec_()  # @UnusedVariable
        
    def ayuda(self):
        pass
    
    def cargar_inicializacion_open(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:/', "Image files (*.jpg )")
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
                    if self.guardar==True:
                        self.ventana.pestannas.mediador_pestannas.guardar_tabla()  
                        self.ventana.pestannas.mediador_pestannas.bandera=False
                    else:
                        self.cargar_inicializacion_open()
                else:
                    self.cargar_inicializacion_open()
        except:
            print("Error:", sys.exc_info()[0], sys.exc_info()[1])
        
            
    def file_save(self):
        """
        Metodo correspondiente al boton de guardar los cambios echos en nuestra aplicacion 
        en un proyecto nuevo.
        """
        try:
            self.ventana.pestannas.guardar_tabla()
        except :
            print("Error:", sys.exc_info()[0], sys.exc_info()[1])
            
    def msgbtn(self, i):
        if i.text() == "OK":                      
            self.guardar = True
        else:
            self.guardar = False
                    
    def showdialog(self):
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setIcon(QtWidgets.QMessageBox.Warning)    
        msg.setText("Se han detectado cambios desea guardar")
        msg.setWindowTitle("Aviso")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()  # @UnusedVariable
                
    def cargar_inicializacion(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "openFolder")
        self.ventana = Window(path+'/Original.jpg' , self)
        self.setCentralWidget(self.ventana)
        self.ventana.pestannas.cargar_proyec(path)
        
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
                    if self.guardar==True:
                        self.ventana.pestannas.mediador_pestannas.guardar_tabla()  
                        self.ventana.pestannas.mediador_pestannas.bandera=False
                    else:
                        self.cargar_inicializacion()
                else:
                    self.cargar_inicializacion()
        except:
            print("Error:", sys.exc_info()[0], sys.exc_info()[1])
            
