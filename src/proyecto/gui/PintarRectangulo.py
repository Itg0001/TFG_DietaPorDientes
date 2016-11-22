from matplotlib.patches import Rectangle
from proyecto.diccionario.Diccionario import Diccionario


class PintarRectangulo:
    def __init__(self, ax):
        self.press = None
        self.r = Rectangle((7.,7.), 745., 745., edgecolor='black', facecolor='none',lw=4)
        self.rect = ax.add_patch(self.r)
        self.dic=Diccionario()
    def connect(self):
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
#         print('event contains', self.rect.xy)        
        self.rect.figure.canvas.draw()
        
        
    def disconnect(self):
        """
        Desconectaremos de la opcion de desplazar
        """
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
        return self.rect.xy