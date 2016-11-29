import sys
sys.path.append("C:/Users/Tobar/Desktop/Workespace/TFG2/src")

from proyecto.codigo.estadisticas import Estadistica
from proyecto.codigo.informes import Informe
from proyecto.codigo.informes import DatosToCsv
from proyecto.codigo.informes import InGuardarDatos
from proyecto.codigo.informes import ConfiguracionToXML
from proyecto.codigo.procesado import ProcesadoDeImagen
from proyecto.codigo.procesado import ProcesadoDeLineas
from proyecto.codigo.procesado import ProcesadoAutomatico

from proyecto.gui.Window import Window
from proyecto.gui.VentanaInicio import VentanaInicio
from proyecto.gui.PanelDePestannas import PanelDePestannas
from proyecto.gui.Mediadores.MediadorVentana import MediadorVentana
from proyecto.gui.Mediadores.MediadorPestannas import MediadorPestannas
from proyecto.diccionario.Diccionario import Diccionario


from Test.codigo.procesado import TestProcesadoDeImagen
from Test.codigo.procesado import TestProcesadoDeLineas
from Test.codigo.estadisticas import TestEstadistica

from Test.codigo.informes.TestInforme import TestInforme
from Test.codigo.informes.TestDatosToCsv import TestDatosToCsv
from Test.codigo.informes.TestConfiguracionToXML import TestConfiguracionToXML