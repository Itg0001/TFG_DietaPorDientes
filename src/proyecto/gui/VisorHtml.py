from PyQt5 import QtCore, QtWebKitWidgets,QtWidgets

class VisorHtml(QtWidgets.QDialog):

    def __init__(self,path,parent=None):
        """
        Metodo para inicializar y mostrar el visor HTML en la aplicacion
        para la ayuda interactiva.
        """
        self.path = path
        QtWidgets.QDialog.__init__(self,parent=None)
        self.resize(1200,900)
        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.html = QtWebKitWidgets.QWebView()
        self.html.setZoomFactor(1.2)
        self.html.load(QtCore.QUrl(self.path))

        self.mainLayout.addWidget(self.html)
        self.html.show()

