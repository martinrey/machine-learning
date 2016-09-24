import json
import math

PORCENTAJE_DE_TEST = 0.1


def crear_archivos_de_entrenamiento_y_test_desde(nombre_archivo):
    archivo = open('datos/%s.json' % nombre_archivo)
    datos_txt = json.load(archivo)
    archivo.close()

    mensajes_totales = len(datos_txt)
    indice_de_corte = int(math.floor(mensajes_totales * (1.0 - PORCENTAJE_DE_TEST)))
    indice_de_corte
    parte_de_entrenamiento = datos_txt[:indice_de_corte]
    parte_de_test = datos_txt[indice_de_corte:]

    file_entrenamiento = open('datos/%s_entrenamiento.json' % nombre_archivo, 'w')
    json.dump(parte_de_entrenamiento, file_entrenamiento)
    file_entrenamiento.close()

    file_test = open('datos/%s_test.json' % nombre_archivo, 'w')
    json.dump(parte_de_test, file_test)
    file_test.close()

if __name__ == "__main__":
    crear_archivos_de_entrenamiento_y_test_desde('ham_dev')
    crear_archivos_de_entrenamiento_y_test_desde('spam_dev')
