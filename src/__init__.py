import sys
sys.path.append("C:/Users/Tobar/Desktop/Workespace/TFG2/src")

from codigo.estadisticas import Estadistica
from codigo.informes import Informe
from codigo.informes import DatosToCsv
from codigo.informes import InGuardarDatos
from codigo.informes import ConfiguracionToXML
from codigo.procesado import ProcesadoDeImagen
from codigo.procesado import ProcesadoDeLineas

from gui.Window import Window
from gui.VentanaInicio import VentanaInicio
from gui.PanelDePestannas import PanelDePestannas
from gui.Mediadores.MediadorVentana import MediadorVentana
from gui.Mediadores.MediadorPestannas import MediadorPestannas
