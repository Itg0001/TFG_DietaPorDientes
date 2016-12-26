from matplotlib.patches import Rectangle
from proyecto.analisis.diccionario import DiccionarioING


class PintarRectangulo:
    """
    Clase encargada de pintar, mostrar y desplazar la region que queremos evlauar
    sobre la imagen cargada o abierta.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    def __init__(self, ax):
        """
        Metodo para inicializar los funcionalidades de la clase.
        """
        self.press = None
        self.r = Rectangle((7.,7.), 745., 745., edgecolor='black', facecolor='none',lw=4)
        self.rect = ax.add_patch(self.r)
        self.dic=DiccionarioING()
        
    def connect(self):
        """
        Metodo apra conectar los eventos al boton correspondiente.
        """
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            self.dic.detect_event_press, self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            self.dic.detect_event_release, self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            self.dic.detect_event_motion, self.on_motion)

        
    def on_press(self, event):
        """
        Cuando pulsemos el boton guardaremos los datos de las coordenadas
        y comprobaremos si esta encima de nuestro recuadro
        """
        if event.inaxes != self.rect.axes:
            return

        contains, attrd = self.rect.contains(event)
        attrd#@UnusedVariable
        if not contains: 
            return
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        """
        Cuando lo desplacemos comprobamos si el raton esta encima
        y aztualizaremos el desplazamiento
        """
        if self.press is None:
            return
        if event.inaxes != self.rect.axes:
            return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)
        self.rect.figure.canvas.draw()

    def on_release(self, event):
        """
        Iremos actualizando la region pintada
        """
        self.press = None
        self.rect.figure.canvas.draw()
        
        
    def disconnect(self):
        """
        Desconectaremos de la opcion de desplazar
        """
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
        return self.rect.xy