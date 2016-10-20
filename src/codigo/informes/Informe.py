import jinja2
import subprocess
import tempfile
import shutil
import os
class Informe():
    def __init__(self, variables, dir_to_guardar):
        self.dir_to_guardar = dir_to_guardar.replace('\\', '/')
        self.dir_to_guardar += '/'
        self.variables = variables
        self.path = os.getcwd() 
        self.path += '/'
        template = self.cargar_plantilla()
        self.sustituir(self.variables, template)
  
    def cargar_plantilla(self):
        latex_jinja_env = jinja2.Environment(
        block_start_string='/BLOCK{',
        block_end_string='}',
        variable_start_string='/VAR{',
        variable_end_string='}',
        comment_start_string='/#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(self.path.replace('\\', '/') + 'codigo/informes/')
        ) 
        template = latex_jinja_env.get_template('jinja-test.tex')        
        return template
    
    def sustituir(self, variables, template):
        latex = template.render(dm1=variables[0], dm2=variables[1], dm3=variables[2],
                              h1=variables[3], h2=variables[4], h3=variables[5],
                              md1=variables[6], md2=variables[7], md3=variables[8],
                              v1=variables[9], v2=variables[10], v3=variables[11],
                              t1=variables[12], t2=variables[13], t3=variables[14])
        latex_salida = open(self.dir_to_guardar + 'Tabla.tex', 'w', newline='')
        latex_salida.write(latex)
        latex_salida.close()
        
    def generar_pdf(self, pdfname, tex): 
        try:
            myfile = self.dir_to_guardar + pdfname + '.pdf'
            g = os.path.isfile(myfile)
            while g == True:
                pdfname = pdfname + 'A'
                myfile = self.dir_to_guardar + pdfname + '.pdf'
                g = os.path.isfile(myfile)
            temp = tempfile.mkdtemp()
            os.chdir(temp)
            
            f = open('cover.tex', 'w')
            f.write(tex)
            f.close()
            
            proc = subprocess.Popen(['pdflatex', 'cover.tex'])
            proc.communicate()
            os.rename('cover.pdf', pdfname + '.pdf')            
            shutil.move(pdfname + '.pdf', self.dir_to_guardar)
        finally:
            # Move to the principal path
            os.chdir(self.path)
            shutil.rmtree(temp)  
#  
