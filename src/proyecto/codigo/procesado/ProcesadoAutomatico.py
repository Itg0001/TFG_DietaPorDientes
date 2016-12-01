'''
Created on 29 nov. 2016

@author: Tobar
'''
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import img_as_float
from skimage.morphology import reconstruction
from skimage.filters import threshold_li
from skimage import morphology
from skimage.morphology import binary_erosion,diamond
from skimage.morphology import skeletonize
from skimage.feature import hessian_matrix, hessian_matrix_eigvals
from skimage.restoration import denoise_tv_chambolle
from skimage import exposure
import networkx as nx
from networkx.algorithms import approximation as apxa
from proyecto.codigo.procesado.ProcesadoDeLineas import ProcesadoDeLineas
from proyecto.codigo.procesado.ProcesadoDeImagen import ProcesadoDeImagen
from skimage.color import rgb2grey
from skimage.transform import probabilistic_hough_line
import warnings
class ProcesadoAutomatico():
    def __init__(self):
        self.proce_lines=ProcesadoDeLineas()
        self.proce_img=ProcesadoDeImagen()

    @classmethod
    def procesado_automatico(self,img):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            img=rgb2grey(img)
            img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.91,nbins =100)
            img_adapteq_deno=denoise_tv_chambolle(img_adapteq, weight=0.1)
        
            hxx, hxy, hyy = hessian_matrix(img_adapteq_deno, sigma=1.85,mode='wrap',cval=0.11)
            i1, i2 = hessian_matrix_eigvals(hxx, hxy, hyy) # @UnusedVariable
    
            image = img_as_float(i1)
            image = gaussian_filter(image, 1)
    
            seed = np.copy(image)
            seed[1:-1, 1:-1] = image.min()
            mask = image
        
            dilated = reconstruction(seed, mask, method='dilation')
            im=image - dilated
            thresh = threshold_li(im)
        
            thresholded = im >= thresh
            no_small = morphology.remove_small_objects(thresholded, min_size=155,connectivity =100)
    
            selem=diamond(1.9)
            dil=binary_erosion(no_small, selem, out=None)
            skl=skeletonize(dil)
            no_small2 = morphology.remove_small_objects(skl, min_size=55,connectivity =100)
        return no_small2
    
    

    @classmethod
    def obtencion_lineas(self,no_small2):
        self.proce_lines=ProcesadoDeLineas()
        lines = probabilistic_hough_line(no_small2, 30,20,30)
        G = nx.Graph()
        G = self.proce_lines.combina(8,4, lines, G)
        k_components = apxa.k_components(G)
        segmentos_de_verdad = self.proce_lines.segmentos_verdad(k_components, lines)
    
        segmentos_de_verdad_pintar=[]
        for i in segmentos_de_verdad:
            if self.proce_lines.longitud_linea(i,100) > 10:
                segmentos_de_verdad_pintar.append(i)
        return segmentos_de_verdad_pintar
    
