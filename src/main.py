from PyQt5 import QtWidgets
from proyecto.gui import VentanaInicio
import sys
import os

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = VentanaInicio(os.getcwd())
    main.show()
    sys.exit(app.exec_())