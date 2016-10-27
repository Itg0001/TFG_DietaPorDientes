from proyecto.codigo.informes.InGuardarDatos import InGuardarDatos
import xml.etree.cElementTree as ET

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
        proyect = ET.Element("proyect")
        ET.SubElement(proyect, "docu1", name='tex').text ='/Tabla.tex'
        ET.SubElement(proyect, "docu2", name='csv').text = '/Salida_Estadisticas.csv' 
        ET.SubElement(proyect, "docu3", name='csv').text = '/Salida_Lineas.csv' 
        ET.SubElement(proyect, "docu4", name='jpg1').text ='/Original.jpg'
        ET.SubElement(proyect, "docu5", name='jpg2').text = '/PintadaParaInforme.jpg'   
        tree = ET.ElementTree(proyect)
        tree.write(path+"/Proyecto.xml",encoding='UTF-8',xml_declaration=True)