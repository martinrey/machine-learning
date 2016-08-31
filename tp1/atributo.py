import re


class Atributo(object):
    def nombre(self):
        return self.__class__.__name__

    def extraer_de(self, mensaje):
        raise NotImplementedError


class CantidadDeAparicionesDeExpresion(Atributo):
    def __init__(self, expresion):
        super(CantidadDeAparicionesDeExpresion, self).__init__()
        self._expresion = expresion

    def nombre(self):
        return '%s: "%s"' % (self.__class__.__name__, self._expresion)

    def _contar_expresion_de(self, texto):
        if texto:
            ocurrencias = re.findall(r"\b(%s)\b" % self._expresion, texto, flags=re.IGNORECASE)
            return len(ocurrencias)
        else:
            return 0

    def extraer_de(self, mensaje):
        cantidad_de_apariciones_de_expresion_en_el_cuerpo = self._contar_expresion_de(mensaje.cuerpo)
        asunto = mensaje.metadata.get('subject', '')
        cantidad_de_apariciones_de_expresion_en_el_asunto = self._contar_expresion_de(asunto)
        return cantidad_de_apariciones_de_expresion_en_el_cuerpo + cantidad_de_apariciones_de_expresion_en_el_asunto
