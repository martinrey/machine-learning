from collections import Counter


class DatosDeMensaje(object):
    def __init__(self, texto):
        self._texto = texto
        self._texto_en_minuscula = texto.lower()
        self._contador_de_caracteres = Counter(self._texto_en_minuscula)
        self._contador_de_palabras = Counter(self._texto_en_minuscula.split())

    def texto(self):
        return self._texto

    def texto_en_minuscula(self):
        return self._texto_en_minuscula

    def contador_de_caracteres(self):
        return self._contador_de_caracteres

    def contador_de_palabras(self):
        return self._contador_de_palabras
