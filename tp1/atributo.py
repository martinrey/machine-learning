class Atributo(object):
    def nombre(self):
        return self.__class__.__name__

    def extraer_de(self, datos_mensaje):
        raise NotImplementedError


class CantidadDeAparicionesDePalabra(Atributo):
    def __init__(self, palabra):
        super(CantidadDeAparicionesDePalabra, self).__init__()
        self._palabra = palabra

    def nombre(self):
        return '%s: "%s"' % (self.__class__.__name__, self._palabra)

    def extraer_de(self, datos_mensaje):
        return self._contar_palabras_de(datos_mensaje)

    def _contar_palabras_de(self, datos_mensaje):
        return datos_mensaje.contador_de_palabras()[self._palabra]


class CantidadDeAparicionesDeCaracter(Atributo):
    def __init__(self, caracter):
        super(CantidadDeAparicionesDeCaracter, self).__init__()
        self._caracter = caracter

    def nombre(self):
        return '%s: "%s"' % (self.__class__.__name__, self._caracter)

    def _contar_caracteres_de(self, datos_mensaje):
        return datos_mensaje.contador_de_caracteres()[self._caracter]

    def extraer_de(self, datos_mensaje):
        return self._contar_caracteres_de(datos_mensaje)
