# coding=utf-8
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from atributo import CantidadDeAparicionesDeVicodin, CantidadDeAparicionesDeViagra
from loader_de_mensajes_para_spam_filter import LoaderDeMensajesParaSpamFilter
from spam_filter import SpamFilter

if __name__ == '__main__':
    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter('datos/ham_txt.json', 'datos/spam_txt.json')
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()

    clasificador = DecisionTreeClassifier()

    lista_de_clases_de_atributos = [
        CantidadDeAparicionesDeViagra, CantidadDeAparicionesDeVicodin
    ]
    lista_de_atributos_a_buscar = map(lambda klass_atributo: klass_atributo(), lista_de_clases_de_atributos)

    spam_filter = SpamFilter(dataframe, clasificador, lista_de_atributos_a_buscar, utilizar_cache=True)
    resultado = spam_filter.clasificar()

    print 'Media: %s' % np.mean(resultado)
    print 'Desvío standard: %s' % np.std(resultado)
