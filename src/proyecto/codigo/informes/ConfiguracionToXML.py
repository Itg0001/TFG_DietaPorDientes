from proyecto.codigo.informes.InGuardarDatos import InGuardarDatos
import xml.etree.cElementTree as ET
from proyecto.diccionario import Diccionario
import xml.etree.ElementTree as ET2

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
    def guardar(self, path, nombres, repe, lon, dire):
        """
        Metodo que generara el xml de configuracion con los nombres de los generables.
        
        @param path: ruta donde guardar el fichero de configuracion.
        """
        self.dic = Diccionario()
        proyect = ET.Element(self.dic.proyec)
        ET.SubElement(proyect, self.dic.docu, repeti=str(repe), long=str(lon), direccion=str(dire))
        ET.SubElement(proyect, self.dic.docu1, name=self.dic.tex, path=nombres[self.dic.docu1])
        ET.SubElement(proyect, self.dic.docu2, name=self.dic.csv, path=nombres[self.dic.docu2])
        ET.SubElement(proyect, self.dic.docu3, name=self.dic.csv, path=nombres[self.dic.docu3]) 
        ET.SubElement(proyect, self.dic.docu4, name=self.dic.jpg1, path=nombres[self.dic.docu4])
        ET.SubElement(proyect, self.dic.docu5, name=self.dic.jpg2, path=nombres[self.dic.docu5])   
        tree = ET.ElementTree(proyect)
        tree.write(path + self.dic.pro_xml, encoding=self.dic.utf, xml_declaration=True)
        
    @classmethod    
    def leer_xml(self, path):
        self.dic = Diccionario()
        tree = ET2.parse(path + self.dic.pro_xml)
        root = tree.getroot()
        dicion = {}
        i = 0
        for child in root:
            if i == 0:
                repe = child.attrib[self.dic.repeti]
                long = child.attrib[self.dic.long]
                dire = child.attrib[self.dic.direccion]
                i = i + 1
            else:
                dicion[child.tag] = child.attrib[self.dic.path]
        return dicion, repe, long, dire


