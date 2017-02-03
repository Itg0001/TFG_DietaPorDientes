import os,shutil,logging,sys
from PyQt5 import QtWidgets
from proyecto.analisis.informes.DatosToCsv import DatosToCsv
from proyecto.analisis.diccionario import DiccionarioING
from proyecto.analisis.diccionario import Diccionario
from proyecto.analisis.informes.ConfiguracionToXML import ConfiguracionToXML  
from proyecto.analisis.informes.Informe  import Informe
from proyecto.analisis.estadisticas import Estadistica

class FachadaEntradaSalida():
    """
    Clase fachada para el mediador que se encargara de la entrada salida por ficheros.
    @var mediador: Instancia del mediador de pestañas que crea dicha fachada.
    @var escribecsv: Instancia de la clase que pasa a csv los datos o los lee de dicho fichero.
    @var dic: Diccionario de datos donde estalocalizado los string del codigo.
    @var configuraciontoxml: Instancia de la clase que lee y escribe los xml.
    @var estad: Instancia de la clase que se encarga de lasestadisticas.   
    """

    def __init__(self,mediador,idioma):
        """
        Constructor de la clase FachadaEntradaSalida que inicializa y prepara todos
        los objetos que tendremos que usar mas adelante en la clase.
        """
        self.idioma=idioma
        self.mediador=mediador
        self.escribeCSV = DatosToCsv()
        if self.idioma=="ESP":
            self.dic=Diccionario()
        else:
            self.dic=DiccionarioING()
        self.conf_to_xml=ConfiguracionToXML()
        self.estad = Estadistica()
        
    def guardar_tabla(self,table,ref_numeros,nombres,procesado,caminos):
        """
        Metodo que sirve para guardar los cambios  dentro de la tabla en distintos 
        entregables como por ejemplo un fichero con los estadisticos, otro con la tabla, 
        otro con las lineas detectadas y las dos imagenes original y pintada despues del 
        procesado.
        """
        path2=caminos[0]
        temp=caminos[1]
        temp2=caminos[2]
        path=caminos[3]
        repe=caminos[4]
        long=caminos[5]
        dire=caminos[6]
        cuadrado=caminos[7]
        if os.path.exists(path + self.dic.md_pe_proy):
            shutil.copytree(path + self.dic.md_pe_proy, temp2 + self.dic.md_pe_proy)
                             
        row = table.rowCount()
        segmentos = []
        angulos = {}
        long_segmento = {}
        lista = []
        x1, x2, y1, y2 = 0, 0, 0, 0
        for i in range(row):            
            x1 = int(table.item(i, 0).text())
            x2 = int(table.item(i, 1).text())
            y1 = int(table.item(i, 2).text())
            y2 = int(table.item(i, 3).text())
            segmentos.append(((x1, x2), (y1, y2)))
            angulos[((x1, x2), (y1, y2))] = self.estad.angu(((x1, x2), (y1, y2)))
            long_segmento[((x1, x2), (y1, y2))] = self.estad.longitud_segemento(((x1, x2), (y1, y2)),ref_numeros)   
             
        v, h, md, dm, total = self.estad.clasificar(segmentos, angulos, long_segmento)
        st_v, st_h, st_md, st_dm, st_tot, variables_tabla = self.estad.calcular_estadisticas(v, h, md, dm, total)
        lista.extend([v, h, md, dm, st_v, st_h, st_md, st_dm, st_tot])
        caminos.clear()
        caminos.extend([temp, temp2,path,path2,repe,long,dire,cuadrado])
        self.escribe_proyecto(variables_tabla, lista, segmentos,nombres,procesado,caminos)

    def escribe_proyecto(self,variables_tabla, lista, segmentos,nombres,procesado,caminos):
        """
        Metodo auxiliar para guardar lso entregables delega en el la tarea de escribirlos en la carpeta nueva.
        @param variables_tabla: variables que contiene la tabla.
        @param temp: ruta al fichero temporal.
        @param temp2: ruta al segundo fichero temporal
        @param lista: lista con las variables que escribiremos al csv.
        @param path:Camino donde guardar el Proyecto.
        @param segmentos: segmentos que vamos a pintar y guardar.
        """
        temp=caminos[0]
        path=caminos[2]
        path2=caminos[3]
        repe=caminos[4]
        long=caminos[5]
        dire=caminos[6]
        cuadrado=caminos[7]
        informe = Informe(variables_tabla, temp)  # @UnusedVariable
        self.escribeCSV.guardar(temp, lista)
        self.conf_to_xml.guardar(temp,nombres,repe,long,dire,cuadrado)
        shutil.copy(path2, temp + self.dic.origi)

        procesado.guardar_y_pintar(path2, temp, segmentos,cuadrado,) 

        if os.path.exists(path + self.dic.md_pe_proy):
            shutil.rmtree(path + self.dic.md_pe_proy)
        shutil.copytree(temp, path + self.dic.md_pe_proy)

    def cargar_proyec(self,path,table):
        """
        Metodo para a partir de un proyecto ecistente carge los ficheros con las lineas calculadas
        dentro de nuestra aplicacion para poder hacer mas o borrar algunas es decir para poder 
        editar los cambios necesarios.
        
        @param path: Camino hasta donde esta nuestro proyecto en custion.
        """       

        self.cargado = True
        nombres,repeticiones,long,dire,xmin,xmax=self.conf_to_xml.leer_xml(path)      
        segmentos = self.escribeCSV.leer(path + nombres[self.dic.docu3])
        segmentos_procesa = []
        segmentos_pintar = []
        for i in segmentos:
            i = i.replace(' ', '')
            i = i.replace('(', '')
            i = i.replace(')', '')
            i = i.replace(',', ' ')
            segmentos_procesa.append(i.split())
        row = table.rowCount()

        if len(segmentos_procesa) != 0:
            for i in segmentos_procesa:
                l1, l2 = 0, 0 
                l1 = (i[0], i[1])
                l2 = (i[2], i[3])
                segmentos_pintar.append((l1, l2))                
                table.insertRow(row)
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0]))))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[1]))))
                table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[2]))))
                table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[3]))))
                row += 1
        return segmentos_pintar,table,nombres,repeticiones,long,dire,xmin,xmax

    def undo(self,temp2,path):
        """
        Funcion auxiliar para hacer el undo si algo va mal y poder tener todo tal
        tal cual estaba antes de hacer nada.
        @param temp2: Directorio temporal donde se guardan las copias para hacer el undo.
        @param path: Ruta al directorio donde guardar los archivos.
         
        """
        shutil.copy(temp2 + self.dic.md_pe_ori, path + self.dic.md_pe_ori)
        shutil.copy(temp2 + self.dic.md_pe_pin, path + self.dic.md_pe_pin)
        shutil.copy(temp2 + self.dic.md_pe_pro, path + self.dic.md_pe_pro)                   
                    
        try:
            shutil.copy(temp2 + self.dic.md_pe_est, path + self.dic.md_pe_est)
        except:
            logging.warning(self.dic.md_pe_err_st+str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
        try:
            shutil.copy(temp2 + self.dic.md_pe_lin, path + self.dic.md_pe_lin)
        except:
            logging.warning(self.dic.md_pe_err_lin +str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
        try:    
            shutil.copy(temp2 + self.dic.md_pe_tab, path + self.dic.md_pe_tab)
        except:
            logging.warning(self.dic.md_pe_err_tab +str(sys.exc_info()[0]) + str(sys.exc_info()[1]))