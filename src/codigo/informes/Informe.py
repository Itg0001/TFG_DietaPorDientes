import jinja2

import subprocess
import tempfile
import shutil
import os
class Informe():
    def __init__(self,variables,dirToGuardar):
        self.dirToGuardar=dirToGuardar.replace('\\','/')
        self.dirToGuardar+='/'
        self.variables=variables
        self.path=os.getcwd() 
        self.path+='\\'
        template= self.cargarPlantilla()
        self.sustituir(self.variables,template)
  
    def cargarPlantilla(self):
        latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%%',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(self.path+'codigo\\informes\\')
        ) 
        #print(self.path)
        template = latex_jinja_env.get_template('jinja-test.tex')
        
        #template = latex_jinja_env.get_template("C:/Users/Ismael/Desktop/TFG_DietaPorDientes/TrabajosPasadosPorJose/dietaJose/Interfaces/jinja-test.tex")
        return template
    
    def sustituir(self,variables,template):
        #latex=template.render(dm1=12,dm2=11,dm3=13,h1=5.5,h2=6,h3=7,md1=4,md2=1,md3=1,v1=99,v2=4,v3=5,t1=5555,t2=555,t3=55)
        latex=template.render(dm1=variables[0],dm2=variables[1],dm3=variables[2],
                              h1=variables[3],h2=variables[4],h3=variables[5],
                              md1=variables[6],md2=variables[7],md3=variables[8],
                              v1=variables[9],v2=variables[10],v3=variables[11],
                              t1=variables[12],t2=variables[13],t3=variables[14])
        latexSalida = open(self.dirToGuardar+'latexSalida.tex', 'w', newline='')
        latexSalida.write(latex)
        latexSalida.close()
        #self.generar_pdf("PDF2016",latex)
        #print(latex)
    def generar_pdf(self,pdfname,tex): 
        #current=os.getcwd() 
        try:
            myfile=self.dirToGuardar+pdfname+'.pdf'
            g=os.path.isfile(myfile)
            while g == True:
                #print("HAY QUE BORRAR")
                pdfname=pdfname+'A'
                #os.remove(myfile)
                myfile=self.dirToGuardar+pdfname+'.pdf'
                g=os.path.isfile(myfile)
            temp = tempfile.mkdtemp()
            os.chdir(temp)
            
            f = open('cover.tex','w')
            f.write(tex)
            f.close()
            #print(os.getcwd())
            
            proc=subprocess.Popen(['pdflatex','cover.tex'])
            #proc=subprocess.Popen(['pdflatex',tex])
            proc.communicate()
            os.rename('cover.pdf',pdfname+'.pdf')            
            shutil.move(pdfname+'.pdf',self.dirToGuardar)
        finally:
            #Move to the principal path
            os.chdir(self.path)
            #Borrar el fichero temporal donde se guardaba el "pdf inicial"
            shutil.rmtree(temp)  
#     def generar_pdf(self,pdfname,tex): 
#         current=os.getcwd() 
#         try:
#             myfile=self.dirToGuardar+pdfname+'.pdf'
#             g=os.path.isfile(myfile)
#             while g == True:
#                 #print("HAY QUE BORRAR")
#                 pdfname=pdfname+'A'
#                 #os.remove(myfile)
#                 myfile=self.dirToGuardar+pdfname+'.pdf'
#                 g=os.path.isfile(myfile)
#             temp = tempfile.mkdtemp()
#             os.chdir(temp)            
#             f = open('cover.tex','w')
#             f.write(tex)
#             f.close()
#             print(os.getcwd())
#             proc=subprocess.Popen(['pdflatex','cover.tex'])
#             
#             subprocess.Popen(['pdflatex',tex])
#             proc.communicate()
#             os.rename('cover.pdf',pdfname+'.pdf')            
#             shutil.move(pdfname+'.pdf',self.dirToGuardar)
#         finally:
#             #Move to the principal path
#             os.chdir(self.path)
#             #Borrar el fichero temporal donde se guardaba el "pdf inicial"
#             #shutil.rmtree(temp)  
            
            
            
            
# if __name__ == '__main__':
#     variable=[] 
#     variable.extend([7789,225451,1,0.5,6,7,4,1,1,99,4,5,5555,555,55])
#     infor = Informe(variable,"C:/Users/Tobar/Desktop")
#     print(infor.variables)