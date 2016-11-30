import numpy as np
from PyQt5 import QtWidgets
import os, sys, logging
import shutil
import tempfile
from proyecto.codigo.estadisticas import Estadistica
from proyecto.codigo.informes.DatosToCsv import DatosToCsv
from proyecto.codigo.informes.ConfiguracionToXML import ConfiguracionToXML
from proyecto.diccionario import DiccionarioING
from proyecto.diccionario import Diccionario
from proyecto.gui.Fachadas.FachadaEntradaSalida import FachadaEntradaSalida
from proyecto.gui.Fachadas.FachadaBotonesAndLayaout import FachadaBotonesAndLayaout

class MediadorPestannas():
    """
    Clase que implementa el mediador de las pestannas.
    
    @var pestannas: instancia del objeto que crea el mediador
    @var estad: creamso obnjeto de la clase estadisticas.
    @var escribeCSV: creamos el objeto que escribira el csv
    @var escribeXML:creamos el objeto que creara el XML
    @var borrar: bandera borrar iniciada a false.
    @var bandera: para detectar cambios inicializada a false.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    def __init__(self, pestannas,idioma):
        """
        Constructor de la clase MediadorPestannas se encargara de inicializar los objetos 
        pasados al constructor y tambien de inicializar las variables y objetos necesarios 
        en el constructor.
        
        @param pestannas: Instancia de la clase que la crea. 
        """
        self.idioma=idioma
        self.pestannas = pestannas
        if self.idioma=="ESP":
            self.dic=Diccionario()
        else:
            self.dic=DiccionarioING()    
            
        self.fachada_botones_and_layaout=FachadaBotonesAndLayaout(self.pestannas,self.dic)
        
        self.estad = Estadistica()
        self.escribeCSV = DatosToCsv()
        self.escribeXML = ConfiguracionToXML()
        self.borrar = False
                        
        self.fachada_entrada_salida=FachadaEntradaSalida(self,self.idioma)
        self.inicializa_msg()

    def inicia_paneles(self):
        """
        Metodo para iniciar los paneles de pestañas.
        """
        self.pestannas.tab1 = QtWidgets.QWidget()
        self.pestannas.tab2 = QtWidgets.QWidget()
         
    def tab_1_ui(self):
        """
        Metodo para inicializar el panel de pestañas 1 con todos sus compoenentes.
        """
        self.fachada_botones_and_layaout.inicia_ui1()

    def valuechange_repeti(self):
        """
        Metodo para mirar si han cambiado las repeticiones y aztualizar.
        """
        val= self.pestannas.combo_repeti.value()
        self.pestannas.repe_actual.setText(str(val))
        
    def valuechange_lon(self):
        """
        Metodo para mirar si han cambiado la longitud y aztualizar.
        """
        val= self.pestannas.combo_lon.value()
        self.pestannas.lon_actual.setText(str(val))
    def cambio_valor_min(self):
        val= self.pestannas.slider_lon_auto.value()
        self.pestannas.lon_auto_actual.setText(str(val))
        
    def tab_2_ui(self):
        """
        Metodo para inicializar el panel de pestañas 2 con todos sus compoenentes.
        En este caso tendra muchas mas declaraciones e inicializaciones que en el anterior.
        Tambien se encargara de inicializar los layouts.
        """
        self.fachada_botones_and_layaout.inicia_ui2()

        
    def selected_row(self):
        """
        Metodo correspondiente al listner de la tabla para ver que casilla esta seleccion
        y pintar la correspondiente linea.
        """
        self.pestannas.row_actual = self.pestannas.table.currentRow()
        row = self.pestannas.row_actual
        if row >= 0:
            p1x = self.pestannas.table.item(row, 0)
            p1x = p1x.text()
            p1y = self.pestannas.table.item(row, 1)
            p1y = p1y.text()
            p2x = self.pestannas.table.item(row, 2)
            p2x = p2x.text()
            p2y = self.pestannas.table.item(row, 3)
            p2y = p2y.text()
            self.pestannas.ventana.ax.hold(True) 
            sel, = self.pestannas.ventana.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)), self.dic.md_pe_amarillo, linewidth=2.0)
            if self.pestannas.ventana.selec_ante != None:            
                self.pestannas.ventana.ax.lines.remove(self.pestannas.ventana.selec_ante)
            self.pestannas.ventana.selec_ante = sel
            self.pestannas.ventana.ax.hold(False)
            self.pestannas.ventana.canvas.draw()             
            
    def corregir_lineas(self):
        """
        Metodo encargado de la correccion manual de las lineas que hayan quedado sin 
        detectar por nuestro algoritmo.
        """
        self.pestannas.button3.setEnabled(False)
        self.pestannas.p_2.setStyleSheet(self.dic.md_pe_color_bl)
        self.pestannas.P1.setStyleSheet(self.dic.md_pe_color_bl)
 
        self.pestannas.P1_x.setText(self.dic.md_pe_cero)
        self.pestannas.P1_y.setText(self.dic.md_pe_cero)
        self.pestannas.P2_x.setText(self.dic.md_pe_cero)
        self.pestannas.P2_y.setText(self.dic.md_pe_cero)        
        self.pestannas.button2.setEnabled(False)
            
        if self.pestannas.ventana.mediador_ventana.terminar==True:
            self.pestannas.ventana.mediador_ventana.pintar_rect.disconnect()
            x,y=self.pestannas.ventana.mediador_ventana.pintar_rect.rect.xy
            x,y=int(x),int(y)
            self.pestannas.ventana.x_max=round(x+745,0)
            self.pestannas.ventana.x_min=x
            self.pestannas.ventana.y_max=round(y+745,0)
            self.pestannas.ventana.y_min=y
        coords = []     
        def onclick(event):
            """
            Metodo interno de la funcion anterior que se encargara de obtener las coordenadas
            de los puntos que bayamos clicando.
            @param Event: evento que contiene las coordenadas del punto clicado.
            @return: Coordenadas P1 y P2
            """
            ix, iy = event.xdata, event.ydata
            x_max=self.pestannas.ventana.x_max
            x_min=self.pestannas.ventana.x_min
            y_max=self.pestannas.ventana.y_max
            y_min=self.pestannas.ventana.y_min
            existe=self.pestannas.ventana.mediador_ventana.procesado.pertenece_o_no(ix, iy,x_min,x_max,y_min,y_max)
            if (ix != None and iy != None) and existe:
                if len(coords) == 0:
                    self.pestannas.P1.setStyleSheet(self.dic.md_pe_color_red)
                    self.pestannas.P1_x.setText(str(round(ix, 0)))
                    self.pestannas.P1_y.setText(str(round(iy, 0)))
                    coords.append((ix, iy))
                    self.pestannas.ventana.c1 = (ix, iy) 
                else:
                    self.pestannas.p_2.setStyleSheet(self.dic.md_pe_color_red)
                    self.pestannas.P2_x.setText(str(round(ix, 0)))
                    self.pestannas.P2_y.setText(str(round(iy, 0)))
                    self.pestannas.ventana.c2 = (ix, iy)                    
                    coords.append((ix, iy))
                    self.pestannas.ventana.fig.canvas.mpl_disconnect(cid)
                    self.pestannas.button2.setEnabled(True)
                    self.pestannas.button3.setEnabled(True)
            return coords
        cid = self.pestannas.ventana.fig.canvas.mpl_connect(self.dic.md_pe_but_press, onclick)
        self.pestannas.ventana.canvas.draw()           
         
    def anadir_lineas(self):
        """
        Metodo que se va a encargar de añadir a la imagen la linea que hemso seleccionado 
        manualmente.
        """
        self.pestannas.ventana.padre.bandera = True
        self.pestannas.p_2.setStyleSheet(self.dic.md_pe_color_bl)
        self.pestannas.P1.setStyleSheet(self.dic.md_pe_color_bl) 
        self.pestannas.P1_x.setText(self.dic.md_pe_cero)
        self.pestannas.P1_y.setText(self.dic.md_pe_cero)
        self.pestannas.P2_x.setText(self.dic.md_pe_cero)
        self.pestannas.P2_y.setText(self.dic.md_pe_cero)
        
        if self.pestannas.ventana.c1 != None and self.pestannas.ventana.c2 != None:        
            row = self.pestannas.table.rowCount()
            self.pestannas.table.insertRow(row)
            self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[0]))))
            self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[1]))))
            self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[0]))))
            self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[1]))))
            self.pestannas.ventana.tam_segmen_verdad = len(self.pestannas.ventana.lineas)
            self.pestannas.ventana.c1 = None
            self.pestannas.ventana.c2 = None
            
        self.mostrar_tabla()
        self.pestannas.button3.setEnabled(False)
        item = self.pestannas.table.item(row, 0)
        self.pestannas.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.pestannas.table.selectRow(row)
        self.pestannas.button7.setEnabled(True)
        self.pestannas.ventana.padre.save_file.setEnabled(True) 
         
    def mostrar_tabla(self):
        """
        Metodo que se encargara de mostrar en la imagen las lineas que hay en la tabla
        se llamara desde otras funciones que modifiquen la tabla para asi poder actualizar
        lo que deberia estar en la tabla.
        """
        row = self.pestannas.table.rowCount()
        segmentos = []
        x1, x2, y1, y2 = 0, 0, 0, 0
        for i in range(row):            
            x1 = int(self.pestannas.table.item(i, 0).text())
            x2 = int(self.pestannas.table.item(i, 1).text())
            y1 = int(self.pestannas.table.item(i, 2).text())
            y2 = int(self.pestannas.table.item(i, 3).text())
            segmentos.append(((x1, x2), (y1, y2)))
 
        self.pestannas.ventana.pintar_imagen_y_segmentos(segmentos)
        self.pestannas.ventana.selec_ante = None
        self.pestannas.ventana.canvas.draw()   
                  
    def limpiar_tabla(self):
        """
        Metodo que se va a encargar de limpiar la tabla cuando queramos borrar todo 
        su contenido.        
        """
        for i in reversed(range(self.pestannas.table.rowCount())):
            self.pestannas.table.removeRow(i)
        self.mostrar_tabla()
        self.pestannas.button7.setEnabled(False)
        self.pestannas.ventana.padre.save_file.setEnabled(False)   
                  
    def borrar_selec(self):
        """
        Metodo que se encargfara de borrar la linea o segmento que hemos seleccionado
        previamente dentro de la tabla y sea la que estamos visualizando.
        """
        self.pestannas.ventana.padre.bandera = True
        if self.pestannas.row_actual != -1:
            self.pestannas.table.removeRow(self.pestannas.row_actual)            
            self.pestannas.row_actual = -1
            self.mostrar_tabla()
        if self.pestannas.table.rowCount() > 0:
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
        else:
            self.pestannas.button7.setEnabled(False)
            self.pestannas.ventana.padre.save_file.setEnabled(False)
 
    def anadir_puntos(self):
        """
        Metodfo para añadir todos los segmentos calculados por el algoritmo
        que detecta la lineas en rojo dentro de la tabla.
        """
        self.pestannas.ventana.padre.bandera = True
        self.limpiar_tabla()
        row = self.pestannas.table.rowCount()
        if len(self.pestannas.ventana.lineas) != 0:
            for i in self.pestannas.ventana.lineas:
                self.pestannas.table.insertRow(row)
                self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0][0]))))
                self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[0][1]))))
                self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[1][0]))))
                self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[1][1]))))
                row += 1
            self.pestannas.button4.setEnabled(False)
            self.mostrar_tabla()
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
    
    def msgbtn(self, i):
        """
        Metodo auxiliar para el panel de notificacion o dialogo que nos indica
        si queremos sobreescribir o no el archivo en cuestion.
        
        @param i: informacion del boton que hemos clicado.
        """
        if i.text() == self.dic.md_pe_ok:                      
            self.borrar = True
        else:
            self.borrar = False
    def inicializa_msg(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.adjustSize()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)    
        self.msg.setText(self.dic.md_pe_msg_sob)
        self.msg.setInformativeText(self.dic.md_pe_msg_inf)
        self.msg.setWindowTitle(self.dic.md_pe_msg_avi)
                    
    def showdialog(self):
        """
        Metodo que nos muestra el cuadro de dialogo dentro de la aplicacion 
        donde podremos elegir si queremos sobreescribir o no.
        """
        
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.msgbtn)
        retval = self.msg.exec_()  # @UnusedVariable

    def guardar_tabla(self):
        """
        Metodo que sirve para guardar los cambios  dentro de la tabla en distintos 
        entregables como por ejemplo un fichero con los estadisticos, otro con la tabla, 
        otro con las lineas detectadas y las dos imagenes original y pintada despues del 
        procesado.
        """
        repe=self.pestannas.combo_repeti.value()
        lon=self.pestannas.combo_lon.value()
        dire=self.pestannas.combo_dir.currentIndex()
        if self.pestannas.ventana.mediador_ventana.detectado==False:
            x_max=self.pestannas.ventana.x_max
            x_min=self.pestannas.ventana.x_min
            y_max=self.pestannas.ventana.y_max
            y_min=self.pestannas.ventana.y_min
            cuadrado=[]
            cuadrado.extend([x_max,x_min,y_max,y_min])
        else:
            cuadrado=[]
            cuadrado.extend(self.dic.md_pe_puntos_cuadrado)    
        path = QtWidgets.QFileDialog.getExistingDirectory(self.pestannas, self.dic.md_pe_open)
        band = False
        if  path != "":
            if os.path.exists(path + self.dic.md_pe_proy) :
                self.showdialog()
                if self.borrar == True:
                    band = True
                else:
                    band = False
            else:
                band = True        
            if band :
                try:
                    temp = tempfile.mkdtemp()
                    temp2 = tempfile.mkdtemp()
                    table=self.pestannas.table
                    ref_numeros=self.pestannas.ventana.mediador_ventana.ref_numeros
                    pathi=self.pestannas.ventana.mediador_ventana.ventana.path
                    nombres=self.pestannas.nombres
                    procesado=self.pestannas.ventana.mediador_ventana.procesado
                    caminos=[]
                    caminos.extend([pathi,temp,temp2,path,repe,lon,dire,cuadrado])
                    self.fachada_entrada_salida.guardar_tabla(table,ref_numeros,nombres,procesado,caminos) 
                    self.pestannas.button7.setEnabled(False)
                    self.pestannas.ventana.padre.save_file.setEnabled(False)
                    shutil.rmtree(temp)  
                    shutil.rmtree(temp2)
                    self.pestannas.ventana.padre.bandera=False 
                except:
                    self.pestannas.ventana.padre.bandera=True 
                    exc = self.dic.md_pe_war + str(sys.exc_info()[0]) + str(sys.exc_info()[1])
                    logging.warning(exc)
                    self.fachada_entrada_salida.undo(temp2, path)
                    self.undo_graf()

    def undo_graf(self):
        """
        Metodo que se encarga de hacer el undo en la interfaz grafica activando los botones de guardar al
        no haber podido realizar los cambios.
        """
        try:
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
            self.informa()
        except:
            exc = self.dic.md_pe_war + str(sys.exc_info()[0]) + str(sys.exc_info()[1])
            logging.warning(exc)
    def informa(self):
        """
        Metodo para mostrar la ventana de elegir de si queremos guardar o no 
        los cambios.         
        """
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setIcon(QtWidgets.QMessageBox.Warning)    
        msg.setText(self.dic.md_pe_msg_gur)
        msg.setWindowTitle(self.dic.md_pe_msg_avi)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()  # @UnusedVariable    

    def cargar_proyec(self, path):
        """
        Metodo para a partir de un proyecto ecistente carge los ficheros con las lineas calculadas
        dentro de nuestra aplicacion para poder hacer mas o borrar algunas es decir para poder 
        editar los cambios necesarios.
        
        @param path: Camino hasta donde esta nuestro proyecto en custion.
        """
        segmentos_pintar,self.pestannas.table,self.pestannas.nombres,repe,long,dire,xmin,ymin=self.fachada_entrada_salida.cargar_proyec(path,self.pestannas.table) 
        self.pestannas.combo_lon.setValue(int(long))
        self.pestannas.combo_repeti.setValue(int(repe))
        self.pestannas.combo_dir.setCurrentIndex(int(dire))
        if len(segmentos_pintar) != 0: 
            if self.pestannas.ventana.mediador_ventana.detectado==False:
                self.pestannas.ventana.mediador_ventana.pintar_rect.rect.set_x(int(xmin))      
                self.pestannas.ventana.mediador_ventana.pintar_rect.rect.set_y(int(ymin))
                self.pestannas.ventana.mediador_ventana.pintar_rect.disconnect()
            self.pestannas.ventana.pintar_imagen_y_segmentos(segmentos_pintar)
            self.pestannas.ventana.selec_ante = None
            self.pestannas.ventana.canvas.draw()