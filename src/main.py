from PyQt5 import QtWidgets
from proyecto.gui import VentanaInicio

import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = VentanaInicio()
    main.show()
    sys.exit(app.exec_())

