from codigo.informes.InGuardarDatos import InGuardarDatos
import xml.etree.cElementTree as ET

class ConfiguracionToXML(InGuardarDatos):

    
    @classmethod    
    def guardar(self, path):
        proyect = ET.Element("proyect")
        ET.SubElement(proyect, "docu1", name='tex').text ='/Tabla.tex'
        ET.SubElement(proyect, "docu2", name='csv').text = '/Salida_Estadisticas.csv' 
        ET.SubElement(proyect, "docu3", name='csv').text = '/Salida_Lineas.csv' 
        ET.SubElement(proyect, "docu4", name='jpg1').text ='/Original.jpg'
        ET.SubElement(proyect, "docu5", name='jpg2').text = '/PintadaParaInforme.jpg'   
        tree = ET.ElementTree(proyect)
        tree.write(path+"/Proyecto.xml",encoding='UTF-8',xml_declaration=True)