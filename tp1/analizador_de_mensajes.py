from atributo import Atributo


class ErrorDeAnalizadorDeMensaje(object):
    @classmethod
    def no_hay_atributos_para_validar(cls):
        return cls('No hay atributos para validar')

    @classmethod
    def los_atributos_a_validar_deben_ser_validos(cls):
        return cls('Los atributos deben ser instancias de la clase o de subclases de Atributo')


class AnalizadorDeMensajes(object):
    def __init__(self, lista_de_atributos_a_buscar):
        self._assert_que_la_lista_tiene_al_menos_un_atributo_valido(lista_de_atributos_a_buscar)
        self._lista_de_atributos_a_buscar = lista_de_atributos_a_buscar
        self._informacion_extraida = {}

    @classmethod
    def _assert_que_la_lista_tiene_al_menos_un_atributo_valido(cls, lista_de_atributos_a_buscar):
        if not lista_de_atributos_a_buscar:
            raise ErrorDeAnalizadorDeMensaje.no_hay_atributos_para_validar()
        if not all(isinstance(atributo, Atributo) for atributo in lista_de_atributos_a_buscar):
            raise ErrorDeAnalizadorDeMensaje.los_atributos_a_validar_deben_ser_validos()

    def informacion_extraida(self):
        return self._informacion_extraida

    def analizar_mensaje(self, mensaje):
        for atributo in self._lista_de_atributos_a_buscar:
            datos_de_atributo = atributo.extraer_de(mensaje)
            self.agregar_datos_de_atributo(atributo, datos_de_atributo)

    def agregar_datos_de_atributo(self, atributo, datos_de_atributo):
        self._informacion_extraida[atributo.nombre()] = datos_de_atributo




