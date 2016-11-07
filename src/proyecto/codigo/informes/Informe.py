
import jinja2
import os
from proyecto.diccionario import Diccionario

class Informe():
    """
         Clase que se encargara de generar la tabla del informe en latex.
         
         @var dir_to_guardar: camino donde guardar el .tex
         @var variables: conjunto de variables para sustituir en la plantilla.
         @var path: directorio actual.
         @var template: plantilla en latex donde sustituir las variables.
         
         @author: Ismael Tobar Garcia
         @version: 1.0    
    """
    def __init__(self,variables,dir_to_guardar):
        """
        Constructor de la clase de los informes. que se encargara de inicializar 
        las variables necesarias.
        
        @param variables: valores a sustituir en la plantilla 
        @param dir_to_guardar: direccion donde guardar la tabal latex generada.
    
        """
        self.dir_to_guardar=dir_to_guardar.replace('\\','/')
        self.dir_to_guardar+='/'
        self.variables=variables
        self.path=os.getcwd() 
        self.path+='\\'
        self.dic=Diccionario()
        template= self.cargar_plantilla()
        self.sustituir(self.variables,template)
  
    def cargar_plantilla(self):
        """
         Metodo para cargar la plantilla y devolverlo como unavariable.
         
         @return  Plantilla leida en latex
        """
        self.dic.infor_plan='proyecto/codigo/informes/jinja-test.tex'
        
        latex_jinja_env = jinja2.Environment(
        block_start_string = self.dic.jin_blo,
        block_end_string = self.dic.jin_o_q,
        variable_start_string = self.dic.jin_va,
        variable_end_string = self.dic.jin_o_q,
        comment_start_string = self.dic.jin_alm,
        comment_end_string = self.dic.jin_o_q,
        line_statement_prefix = self.dic.jin_porc,
        line_comment_prefix = self.dic.jin_alm_po,
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(self.path)
        ) 

        template = latex_jinja_env.get_template(self.dic.infor_plan)
        return template
    
    def sustituir(self,variables,template):
        """
         sustituir los valores de las variables que nos pasan en el constructor.
         
         @param variables: valores a sustituir en la plantilla 
         @param template: Plantilla leida en en latex donde sustituir las variables
 
        """
        latex=template.render(dm1=variables[0],dm2=variables[1],dm3=variables[2],
                              h1=variables[3],h2=variables[4],h3=variables[5],
                              md1=variables[6],md2=variables[7],md3=variables[8],
                              v1=variables[9],v2=variables[10],v3=variables[11],
                              t1=variables[12],t2=variables[13],t3=variables[14])
        latex_salida = open(self.dir_to_guardar+self.dic.tab_in, 'w', newline='')
        latex_salida.write(latex)
        latex_salida.close()