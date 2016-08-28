import re


def aplanar_lista(lista):
    return [item for sublist in lista for item in sublist]


class Mensaje(object):
    def __init__(self, texto_completo):
        self._texto_completo = texto_completo
        self.metadata = {}

        separacion_de_metadata = self._texto_completo.split('\n\r')
        texto_metadata = separacion_de_metadata[0]
        self.cuerpo = aplanar_lista(separacion_de_metadata[1:])
        self._extraer_metadata_de(texto_metadata)
        for linea_metadata in texto_metadata.split('\n'):
            self._extraer_metadata_de(linea_metadata)

    def _extraer_metadata_de(self, texto_metadata):
        atributos_y_valores_en_metadata = re.findall('(.*)\: (.*)', texto_metadata)
        for atributo, valor in atributos_y_valores_en_metadata:
            self.metadata[atributo] = valor
