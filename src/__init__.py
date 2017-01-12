import sys,os
sys.path.append(os.getcwd()+"/src")

from proyecto.gui.PanelDePestannas import PanelDePestannas
from proyecto.gui.VentanaInicio import VentanaInicio
from proyecto.gui.VisorHtml import VisorHtml
from proyecto.gui.Window import Window
from proyecto.gui.PintarRectangulo import PintarRectangulo

from proyecto.analisis.procesado.ProcesadoDeLineas import ProcesadoDeLineas
from proyecto.analisis.procesado.ProcesadoDeImagen import ProcesadoDeImagen
from proyecto.analisis.procesado.ProcesadoAutomatico import ProcesadoAutomatico

from Test.codigo.procesado import TestProcesadoDeImagen
from Test.codigo.procesado import TestProcesadoDeLineas
from Test.codigo.estadisticas import TestEstadistica
from Test.codigo.calidad.TestCalidad import TestCalidad

from proyecto.analisis.informes.Informe import Informe
from proyecto.analisis.informes.DatosToCsv import DatosToCsv
from proyecto.analisis.informes.InGuardarDatos import InGuardarDatos
from proyecto.analisis.informes.ConfiguracionToXML import ConfiguracionToXML

from proyecto.analisis.estadisticas.Estadistica import Estadistica

from proyecto.analisis.diccionario.Diccionario import Diccionario
from proyecto.analisis.diccionario.DiccionarioING import DiccionarioING

from proyecto.analisis.FachadaBotonesAndLayaout import FachadaBotonesAndLayaout
from proyecto.analisis.FachadaEntradaSalida import FachadaEntradaSalida
from proyecto.analisis.MediadorVentana import MediadorVentana
from proyecto.analisis.MediadorPestannas import MediadorPestannas

from Test.codigo.informes.TestInforme import TestInforme
from Test.codigo.informes.TestDatosToCsv import TestDatosToCsv
from Test.codigo.informes.TestConfiguracionToXML import TestConfiguracionToXML