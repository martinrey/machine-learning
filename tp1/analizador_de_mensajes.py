# coding=utf-8
import os

import cPickle

from atributo import Atributo
from mensaje import Mensaje


class ErrorDeAnalizadorDeMensaje(Exception):
    @classmethod
    def no_hay_atributos_para_validar(cls):
        return cls('No hay atributos para validar')

    @classmethod
    def los_atributos_a_validar_deben_ser_validos(cls):
        return cls('Los atributos deben ser instancias de la clase o de subclases de Atributo')


class AnalizadorDeMensajes(object):
    FILEPATH_DE_ARCHIVO_DE_CACHE = 'cache/lista_de_mensajes.cache'

    def __init__(self, lista_de_atributos_a_buscar, dataframe, utilizar_cache=True):
        self._assert_que_la_lista_tiene_al_menos_un_atributo_valido(lista_de_atributos_a_buscar)
        self._lista_de_atributos_a_buscar = lista_de_atributos_a_buscar
        self._dataframe = dataframe
        self.utilizar_cache = utilizar_cache

    @classmethod
    def _assert_que_la_lista_tiene_al_menos_un_atributo_valido(cls, lista_de_atributos_a_buscar):
        if not lista_de_atributos_a_buscar:
            raise ErrorDeAnalizadorDeMensaje.no_hay_atributos_para_validar()
        if not all(isinstance(atributo, Atributo) for atributo in lista_de_atributos_a_buscar):
            raise ErrorDeAnalizadorDeMensaje.los_atributos_a_validar_deben_ser_validos()

    def lista_de_atributos_a_buscar(self):
        return self._lista_de_atributos_a_buscar

    def dataframe(self):
        return self._dataframe

    def analizar_mensajes(self):
        lista_de_mensajes = self._cargar_mensajes()
        self._mensaje_de_progreso_de_atributos()
        for atributo in self._lista_de_atributos_a_buscar:
            self._mensaje_de_progreso_para_atributo(atributo.nombre())
            self._dataframe[atributo.nombre()] = map(atributo.extraer_de, lista_de_mensajes)

    def _cargar_mensajes(self):
        self._mensaje_de_progreso_de_listado_de_mensajes()
        if self.utilizar_cache and self._existe_cache_de_mensajes():
            self._mensaje_de_progreso_para_cargar_lista_de_mensajes_desde_la_cache()
            lista_de_mensajes = self._cargar_lista_de_mensajes_desde_cache()
            self._mensaje_de_exito_de_carga_de_listado_de_mensajes_en_cache()
            return lista_de_mensajes
        else:
            lista_de_mensajes = self._generar_lista_de_mensajes()
            if self.utilizar_cache:
                self._escribir_lista_de_mensajes_en_cache(lista_de_mensajes)
        return lista_de_mensajes

    def _generar_lista_de_mensajes(self):
        lista_de_mensajes = map(lambda texto: Mensaje(texto), self._dataframe.text)
        return lista_de_mensajes

    def _existe_cache_de_mensajes(self):
        return os.path.isfile(self.FILEPATH_DE_ARCHIVO_DE_CACHE)

    def _cargar_lista_de_mensajes_desde_cache(self):
        file_de_cache = open(self.FILEPATH_DE_ARCHIVO_DE_CACHE, 'rb')
        lista_de_mensajes = cPickle.load(file_de_cache)
        file_de_cache.close()
        return lista_de_mensajes

    def _escribir_lista_de_mensajes_en_cache(self, lista_de_mensajes):
        file_de_cache = open(self.FILEPATH_DE_ARCHIVO_DE_CACHE, 'wb+')
        cPickle.dump(lista_de_mensajes, file_de_cache, -1)
        file_de_cache.close()

    def _mensaje_de_progreso_de_listado_de_mensajes(self):
        print '----------- Procesando lista de mensajes (puede demorar unos minutos...) -----------'

    def _mensaje_de_progreso_para_cargar_lista_de_mensajes_desde_la_cache(self):
        print ' - Cargando lista de mensajes desde la caché...'

    def _mensaje_de_exito_de_carga_de_listado_de_mensajes_en_cache(self):
        print ' - Lista de mensajes cargada desde la caché'

    def _mensaje_de_progreso_de_atributos(self):
        print '----------- Analizando atributos -----------'

    def _mensaje_de_progreso_para_atributo(self, nombre_de_atributo):
        print ' - Analizando %s... ' % nombre_de_atributo
