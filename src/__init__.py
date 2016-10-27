import sys
sys.path.append("C:/Users/Tobar/Desktop/Workespace/TFG2/src")

from proyecto.codigo.estadisticas import Estadistica
from proyecto.codigo.informes import Informe
from proyecto.codigo.informes import DatosToCsv
from proyecto.codigo.informes import InGuardarDatos
from proyecto.codigo.informes import ConfiguracionToXML
from proyecto.codigo.procesado import ProcesadoDeImagen
from proyecto.codigo.procesado import ProcesadoDeLineas
from proyecto.gui.Window import Window
from proyecto.gui.VentanaInicio import VentanaInicio
from proyecto.gui.PanelDePestannas import PanelDePestannas
from proyecto.gui.Mediadores.MediadorVentana import MediadorVentana
from proyecto.gui.Mediadores.MediadorPestannas import MediadorPestannas


from Test.codigo.estadisticas.TestEstadistica import TestEstadistica