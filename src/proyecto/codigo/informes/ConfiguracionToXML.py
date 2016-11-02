from proyecto.codigo.informes.InGuardarDatos import InGuardarDatos
import xml.etree.cElementTree as ET
from proyecto.diccionario import Diccionario

class ConfiguracionToXML(InGuardarDatos):
    """
    Metodo que va a escribir la configuracion de los archivos que contiene un Proyecto
    que estara compuesto por:
        Dos imagenes:  Original.jpg y otra  PintadaParaInforme.jpg
        Dos ficheros csv: Salida_Estadisticas.scv y Salida_Lineas.csv
        Tabla latex : Tabla.tex
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """

    
    @classmethod    
    def guardar(self, path):
        """
        Metodo que generara el xml de configuracion con los nombres de los generables.
        
        @param path: ruta donde guardar el fichero de configuracion.
        """
        self.dic=Diccionario()
        proyect = ET.Element(self.dic.proyec)
        ET.SubElement(proyect, self.dic.d1, name=self.dic.tex).text =self.dic.tab
        ET.SubElement(proyect, self.dic.d2, name=self.dic.csv).text = self.dic.sal_estad
        ET.SubElement(proyect, self.dic.d3, name=self.dic.csv).text = self.dic.sal_lin 
        ET.SubElement(proyect, self.dic.d4, name=self.dic.jpg1).text =self.dic.origi
        ET.SubElement(proyect, self.dic.d5, name=self.dic.jpg2).text = self.dic.pintada   
        tree = ET.ElementTree(proyect)
        tree.write(path+self.dic.pro_xml,encoding=self.dic.utf,xml_declaration=True)