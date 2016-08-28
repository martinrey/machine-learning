class Atributo(object):
    def nombre(self):
        return self.__class__.__name__

    def extraer_de(self, mensaje):
        raise NotImplementedError


class CantidadDeAparicionesDePalabra(Atributo):
    def __init__(self, palabra):
        super(CantidadDeAparicionesDePalabra, self).__init__()
        self._palabra = palabra

    def extraer_de(self, mensaje):
        cantidad_de_apariciones_de_palabra_en_el_cuerpo = mensaje.cuerpo.count(
            self._palabra)  # TODO: mejor con regexps, fijarse como hacer, por el tema de case insensitive y demas
        cantidad_de_apariciones_de_palabra_en_el_asunto = mensaje.metadata.get('subject', '').count(self._palabra)
        return cantidad_de_apariciones_de_palabra_en_el_cuerpo + cantidad_de_apariciones_de_palabra_en_el_asunto


class CantidadDeAparicionesDeViagra(CantidadDeAparicionesDePalabra):
    def __init__(self):
        super(CantidadDeAparicionesDeViagra, self).__init__("Viagra")


class CantidadDeAparicionesDeVicodin(CantidadDeAparicionesDePalabra):
    def __init__(self):
        super(CantidadDeAparicionesDeVicodin, self).__init__("Vicodin")