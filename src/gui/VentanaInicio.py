from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from .Window import Window

class VentanaInicio(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(VentanaInicio, self).__init__(parent)
        self.resize(900, 700)

        open_file = QtWidgets.QAction("&Abrir imagen", self)
        open_file.setShortcut("Ctrl+O")
        open_file.setStatusTip('Abrir imagen')
        open_file.triggered.connect(self.file_open)     

        self.save_file = QtWidgets.QAction("&Guardar", self)
        self.save_file.setShortcut("Ctrl+G")
        self.save_file.setStatusTip('Guardar csv y .tex')
        self.save_file.triggered.connect(self.file_save)
        self.save_file.setDisabled(True)
        
        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&Cargar')
        file_menu.addAction(open_file)
        file_menu.addAction(self.save_file)
        self.styleChoice = QtWidgets.QLabel("Cargar imagen para iniciar", self)
        self.styleChoice.setAlignment(QtCore.Qt.AlignCenter)

        laout_principal = QtWidgets.QHBoxLayout()
        laout_principal.addWidget(self.styleChoice)
        # self.styleChoice.move(10,100)
        self.styleChoice.setStyleSheet('color: red')
        # self.styleChoice.setGeometry(30, 100, 600, 50)
        font = QtGui.QFont("Times", 35, QtGui.QFont.Bold, True)
        self.styleChoice.setFont(font)
        # self.setLayout(laout_principal)#Asignamos como principal el principal
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(laout_principal)
        self.setCentralWidget(central_widget)
    def file_open(self):
        try:
            self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
         'c:/', "Image files (*.jpg *.gif)")
                        # self.styleChoice.close() 
            self.ventana = Window(self.path[0], self) 
            self.setCentralWidget(self.ventana)
        except FileNotFoundError as fnf:
            print(fnf)
            
    def file_save(self):
        self.ventana.pestannas.guardar_tabla()
        self.ventana.pestannas.button7.setEnabled(False)
        self.save_file.setEnabled(False)
