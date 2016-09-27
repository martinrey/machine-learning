from builtins import map
from sklearn.cross_validation import cross_val_score
import numpy as np
import pickle

from analizador_de_mensajes import AnalizadorDeMensajes


class SpamFilter(object):
    CANTIDAD_DE_FOLDS_DEFAULT = 10
    CANTIDAD_DE_THREADS_DEFAULT = 8
    CANTIDAD_DE_CORES_DEFAULT = 4

    def __init__(self, dataframe, clasificadores, lista_de_atributos_a_buscar, utilizar_cache=True,
                 cantidad_de_folds_de_cross_validation=CANTIDAD_DE_FOLDS_DEFAULT):
        self._dataframe = dataframe
        self._clasificadores = clasificadores
        self._lista_de_atributos_a_buscar = lista_de_atributos_a_buscar
        self._cantidad_de_folds_de_cross_validation = cantidad_de_folds_de_cross_validation
        self._utilizar_cache = utilizar_cache

    def hacer_cross_validation(self, mostrar_resultados_intermedios=False, utilizo_grid_search = False):
        
        valores = self.conseguir_valores(self._dataframe)
        clasificaciones = self._dataframe['class']
        if utilizo_grid_search:
             return self._calcular_resultados_para_todos_los_clasificadores_con_grid_search(clasificaciones, valores,
                                                                            mostrar_resultados_intermedios)
        else:
            return self._calcular_resultados_para_todos_los_clasificadores(clasificaciones, valores,
                                                                            mostrar_resultados_intermedios)
    def entrenar(self):
        valores = self.conseguir_valores(self._dataframe)
        clasificaciones = self._dataframe['class']
        for clasificador in self._clasificadores:
            clasificador.fit(X=valores,y=clasificaciones)

    def conseguir_valores(self,dataframe):
        analizador_de_mensajes = AnalizadorDeMensajes(self._lista_de_atributos_a_buscar, dataframe,
                                                      self._utilizar_cache,verbose=False)
        analizador_de_mensajes.analizar_mensajes()

        nombres_de_atributos_utilizados = list(map(lambda atributo: atributo.nombre(),
                                                   self._lista_de_atributos_a_buscar))
        valores = self._dataframe[nombres_de_atributos_utilizados].values
        return valores

    def predecir(self,lista_mensajes,numero_de_clasificador=0):
        print self._clasificadores[numero_de_clasificador].predict(X=lista_mensajes)

    def dar_score(self,lista_mensajes,clasificaciones,numero_de_clasificador=0):
        return self._clasificadores[numero_de_clasificador].score(X=lista_mensajes,y=clasificaciones)

    def _calcular_resultados_para_todos_los_clasificadores(self, clasificaciones, valores,
                                                           mostrar_resultados_intermedios=False):
        #self._mensaje_de_inicio_de_cross_validation_con_los_clasificadores()
        resultados_por_clasificador = {}
        for clasificador in self._clasificadores:
            nombre_del_clasificador = clasificador.__class__.__name__
            self._mensaje_de_progreso_de_cross_validation_para_el_clasificador(nombre_del_clasificador)

            resultado_de_cross_validation = cross_val_score(clasificador, valores, clasificaciones,
                                                            cv=self._cantidad_de_folds_de_cross_validation,
                                                            n_jobs=1, verbose=mostrar_resultados_intermedios)
            if mostrar_resultados_intermedios:
                self._mostrar_resultados_intermedios_para(nombre_del_clasificador, resultado_de_cross_validation)

            resultados_por_clasificador[nombre_del_clasificador] = resultado_de_cross_validation
        return resultados_por_clasificador

    def guardar_modelo(self,output_file,numero_de_clasificador):
        fout = open(output_file,'w')
        pickle.dump(self._clasificadores[numero_de_clasificador],fout)
        fout.close()
    
    def cargar_modelo(self,input_file,numero_de_clasificador):
        self._clasificadores[numero_de_clasificador] = pickle.load( open(input_file))

    def _calcular_resultados_para_todos_los_clasificadores_con_grid_search(self, clasificaciones, valores,
                                                           mostrar_resultados_intermedios=False):
        #self._mensaje_de_inicio_de_cross_validation_con_los_clasificadores()
        resultados_por_clasificador = {}
        for clasificador in self._clasificadores:
            nombre_del_clasificador = clasificador.__class__.__name__
            self._mensaje_de_progreso_de_cross_validation_para_el_clasificador(nombre_del_clasificador)

            resultado_de_cross_validation = clasificador.fit(valores, clasificaciones)

            if mostrar_resultados_intermedios:
                self._mostrar_resultados_intermedios_para(nombre_del_clasificador, resultado_de_cross_validation)

            resultados_por_clasificador[nombre_del_clasificador] = resultado_de_cross_validation
        return resultados_por_clasificador




    def _mensaje_de_progreso_de_cross_validation_para_el_clasificador(self, nombre_del_clasificador):
        print('- Haciendo cross validation con el clasificador "%s"' % nombre_del_clasificador)

    def _mensaje_de_inicio_de_cross_validation_con_los_clasificadores(self):
        print('----------- Comenzando a analizar con cross validation (%s folds, %s clasificadores) -----------' % (
            self._cantidad_de_folds_de_cross_validation, len(self._clasificadores)))

    def _mostrar_resultados_intermedios_para(self, nombre_del_clasificador, resultado_de_cross_validation):
        print('%s , %s , %s' % (nombre_del_clasificador, np.mean(resultado_de_cross_validation), np.std(resultado_de_cross_validation)))

