from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
#from PyQt5.QtCore import *
#from PyQt5.QtGui  import *
from .Window import Window
class VentanaInicio(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(VentanaInicio, self).__init__(parent)
        self.resize(900, 700)

        #fname = QFileDialog.getOpenFileName(self, 'Open file', 
        # 'c:\\',"Image files (*.jpg *.gif)")
        openFile = QtWidgets.QAction("&Abrir imagen", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Abrir imagen')
        openFile.triggered.connect(self.file_open)     

        self.saveFile = QtWidgets.QAction("&Guardar", self)
        self.saveFile.setShortcut("Ctrl+G")
        self.saveFile.setStatusTip('Guardar csv y .tex')
        self.saveFile.triggered.connect(self.file_save)
        self.saveFile.setDisabled(True)
        
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Cargar')
        fileMenu.addAction(openFile)
        fileMenu.addAction(self.saveFile)
        self.styleChoice = QtWidgets.QLabel("Cargar imagen para iniciar", self)
        self.styleChoice.setAlignment(QtCore.Qt.AlignCenter)

        laoutPrincipal = QtWidgets.QHBoxLayout()
        laoutPrincipal.addWidget(self.styleChoice)
        #self.styleChoice.move(10,100)
        self.styleChoice.setStyleSheet('color: red')
        #self.styleChoice.setGeometry(30, 100, 600, 50)
        font = QtGui.QFont("Times",35,QtGui.QFont.Bold,True)
        self.styleChoice.setFont(font)
        #self.setLayout(laoutPrincipal)#Asignamos como principal el principal
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(laoutPrincipal)
        self.setCentralWidget(central_widget)
    def file_open(self):
        try:
            self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif)")
                        #self.styleChoice.close() 
            self.ventana = Window(self.path[0],self) 
            self.setCentralWidget(self.ventana)
        except FileNotFoundError as fnf:
            print(fnf)
          

       
    def file_save(self):
        self.ventana.pestañas.guardarTabla()
        self.ventana.pestañas.button7.setEnabled(False)
        self.saveFile.setEnabled(False)