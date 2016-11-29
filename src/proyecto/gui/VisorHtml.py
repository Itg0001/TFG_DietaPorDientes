from PyQt5 import QtCore, QtWebKitWidgets,QtWidgets

class VisorHtml(QtWidgets.QDialog):

    def __init__(self,path,parent=None):
        """
            Initialize the browser GUI and connect the events
        """
        self.path = path
        QtWidgets.QDialog.__init__(self,parent=None)
        self.resize(800,600)
        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.html = QtWebKitWidgets.QWebView()

        self.html.load(QtCore.QUrl(self.path))
        self.mainLayout.addWidget(self.html)
        self.html.show()

