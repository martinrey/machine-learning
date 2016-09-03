from builtins import map
from sklearn.cross_validation import cross_val_score

from analizador_de_mensajes import AnalizadorDeMensajes


class SpamFilter(object):
    CANTIDAD_DE_FOLDS_DEFAULT = 10

    def __init__(self, dataframe, clasificador, lista_de_atributos_a_buscar, utilizar_cache=True,
                 cantidad_de_folds_de_cross_validation=CANTIDAD_DE_FOLDS_DEFAULT):
        self._dataframe = dataframe
        self._clasificador = clasificador
        self._lista_de_atributos_a_buscar = lista_de_atributos_a_buscar
        self._cantidad_de_folds_de_cross_validation = cantidad_de_folds_de_cross_validation
        self._utilizar_cache = utilizar_cache

    def clasificar(self):
        analizador_de_mensajes = AnalizadorDeMensajes(self._lista_de_atributos_a_buscar, self._dataframe,
                                                      self._utilizar_cache)
        analizador_de_mensajes.analizar_mensajes()

        nombres_de_atributos_utilizados = list(map(lambda atributo: atributo.nombre(),
                                                   self._lista_de_atributos_a_buscar))
        valores = self._dataframe[nombres_de_atributos_utilizados].values
        clasificaciones = self._dataframe['class']

        return cross_val_score(self._clasificador, valores, clasificaciones,
                               cv=self._cantidad_de_folds_de_cross_validation)
