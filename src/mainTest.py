
from Test.codigo.estadisticas.TestEstadistica import TestEstadistica
from Test.codigo.procesado.TestProcesadoDeImagen import TestProcesadoDeImagen
from Test.codigo.procesado.TestProcesadoDeLineas import TestProcesadoDeLineas
from Test.codigo.informes.TestConfiguracionToXML import TestConfiguracionToXML
from Test.codigo.informes.TestDatosToCsv import TestDatosToCsv
from Test.codigo.informes.TestInforme import TestInforme

def test_estadisticas():
    test_stadistica = TestEstadistica()
    test_stadistica.test_clasificar()
    test_stadistica.test_stadisticas()
    test_stadistica.test_desviacion_tipica()
    test_stadistica.test_media_long_segmentos()
    test_stadistica.test_longitud_segemento()
    test_stadistica.test_angu()
    test_stadistica.test_calcular_estadisticas()
    print("OK,TEST_ESTADISTICAS")

def test_rocesado_lineas():
    test_imagen = TestProcesadoDeImagen()
    test_imagen.test_leer_imagen()
    test_imagen.test_distancia_al_rojo()
    test_imagen.test_binarizar()
    test_imagen.test_reducir_grosor()
    test_imagen.test_pro_hough()
    print("OK,TEST_PROCESADO_DE_IMAGEN")
    
def test_procesado_lineas():
    test_procesado_de_lineas=TestProcesadoDeLineas()
    test_procesado_de_lineas.test_combina()
    test_procesado_de_lineas.test_segments_distance()
    test_procesado_de_lineas.test_segments_intersect()
    test_procesado_de_lineas.test_point_segment_distance()
    test_procesado_de_lineas.test_ang()
    test_procesado_de_lineas.test_dot()
    test_procesado_de_lineas.test_combina_segmentos()
    test_procesado_de_lineas.test_segmentos_verdad()
    print("OK,TEST_PROCESADO_DE_LINEAS")
    
def test_configuracion_xml():
    test=TestConfiguracionToXML()
    test.test_guardar()
    print("OK,TEST_CONFIGURACIONXML")

def test_datos_to_csv():
    test_datos=TestDatosToCsv()
    test_datos.test_guardar()
    test_datos.test_leer()
    print("OK,TEST_DATOS_TO_CSV")
    

def test_informe():
    test_infor=TestInforme()
    test_infor.test_cargar_plantilla()
    test_infor.test_sustituir()
    
    print("OK,TEST_INFORME")


if __name__ == '__main__':
    test_estadisticas()
    print()
    test_rocesado_lineas()
    print()
    test_procesado_lineas()
    print()
    test_configuracion_xml()
    print()
    test_datos_to_csv()
    print()
    test_informe()
    print()
    print("OK,todos")