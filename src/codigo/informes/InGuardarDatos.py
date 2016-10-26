from abc import  abstractmethod

class InGuardarDatos(object):
    """
    Interface que contendra el metodo para guardar los datos ya sea en cualquier soorte dependiendo
    que clase la implemente.
    
    @author: Ismael Tobar Garcia
    @version: 1.0    
    """

    
    @abstractmethod
    def guardar(self):
        """
        Metodo abstracto de la interfaz. que se redefinira dependiendo de los dartos
        """
        pass
    
    
    
    
    
    