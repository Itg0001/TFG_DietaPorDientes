
from Test.codigo.estadisticas.TestEstadistica import TestEstadistica
from Test.codigo.procesado.TestProcesadoDeImagen import TestProcesadoDeImagen

def test_estadisticas():
    test_stadistica = TestEstadistica()
    test_stadistica.test_clasificar()
    test_stadistica.test_stadisticas()
    test_stadistica.test_desviacion_tipica()
    test_stadistica.test_media_long_segmentos()
    test_stadistica.test_longitud_segemento()
    test_stadistica.test_angu()
    test_stadistica.test_calcular_estadisticas()
    print("OK,TestEstadistica")

def test_rocesado_lineas():
    test_imagen = TestProcesadoDeImagen()
    test_imagen.test_leer_imagen()
    test_imagen.test_distancia_al_rojo()
    test_imagen.test_binarizar()
    test_imagen.test_reducir_grosor()
    test_imagen.test_pro_hough()
    print("OK,TestProcesadoDeImagen")
    
if __name__ == '__main__':
    test_estadisticas()
    print()
    test_rocesado_lineas()
    print()
    print("OK,todos")