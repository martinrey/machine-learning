# coding=utf-8
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from atributo import CantidadDeAparicionesDeExpresion
from loader_de_mensajes_para_spam_filter import LoaderDeMensajesParaSpamFilter
from spam_filter import SpamFilter

if __name__ == '__main__':
    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter('datos/ham_dev.json', 'datos/spam_dev.json')
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()

    clasificador = DecisionTreeClassifier()

    lista_de_atributos_a_buscar = [
        CantidadDeAparicionesDeExpresion('Vicodin'), CantidadDeAparicionesDeExpresion('Viagra'),
        CantidadDeAparicionesDeExpresion('html'), CantidadDeAparicionesDeExpresion('http'),
        CantidadDeAparicionesDeExpresion('.'), CantidadDeAparicionesDeExpresion('\\'),
        CantidadDeAparicionesDeExpresion(' '), CantidadDeAparicionesDeExpresion('make'),
        CantidadDeAparicionesDeExpresion('address'), CantidadDeAparicionesDeExpresion('all'),
        CantidadDeAparicionesDeExpresion('3d'), CantidadDeAparicionesDeExpresion('our'),
        CantidadDeAparicionesDeExpresion('over'), CantidadDeAparicionesDeExpresion('remove'),
        CantidadDeAparicionesDeExpresion('internet'), CantidadDeAparicionesDeExpresion('order'),
        CantidadDeAparicionesDeExpresion('mail'), CantidadDeAparicionesDeExpresion('receive'),
        CantidadDeAparicionesDeExpresion('will'), CantidadDeAparicionesDeExpresion('people'),
        CantidadDeAparicionesDeExpresion('report'), CantidadDeAparicionesDeExpresion('addresses'),
        CantidadDeAparicionesDeExpresion('free'), CantidadDeAparicionesDeExpresion('business'),
        CantidadDeAparicionesDeExpresion('email'), CantidadDeAparicionesDeExpresion('you'),
        CantidadDeAparicionesDeExpresion('credit'), CantidadDeAparicionesDeExpresion('your'),
        CantidadDeAparicionesDeExpresion('font'), CantidadDeAparicionesDeExpresion('money'),
        CantidadDeAparicionesDeExpresion('hp'), CantidadDeAparicionesDeExpresion('hpl'),
        CantidadDeAparicionesDeExpresion('george'), CantidadDeAparicionesDeExpresion('lab'),
        CantidadDeAparicionesDeExpresion('labs'), CantidadDeAparicionesDeExpresion('telnet'),
        CantidadDeAparicionesDeExpresion('data'), CantidadDeAparicionesDeExpresion('technology'),
        CantidadDeAparicionesDeExpresion('parts'), CantidadDeAparicionesDeExpresion('pm'),
        CantidadDeAparicionesDeExpresion('direct'), CantidadDeAparicionesDeExpresion('cs'),
        CantidadDeAparicionesDeExpresion('meeting'), CantidadDeAparicionesDeExpresion('original'),
        CantidadDeAparicionesDeExpresion('project'), CantidadDeAparicionesDeExpresion('re'),
        CantidadDeAparicionesDeExpresion('edu'), CantidadDeAparicionesDeExpresion('table'),
        CantidadDeAparicionesDeExpresion('conference'), CantidadDeAparicionesDeExpresion(';'),
        CantidadDeAparicionesDeExpresion('('), CantidadDeAparicionesDeExpresion('['),
        CantidadDeAparicionesDeExpresion('!'), CantidadDeAparicionesDeExpresion('$'),
        CantidadDeAparicionesDeExpresion('#'),
    ]

    spam_filter = SpamFilter(dataframe, clasificador, lista_de_atributos_a_buscar, utilizar_cache=True)
    resultado = spam_filter.clasificar()

    print 'Media: %s' % np.mean(resultado)
    print 'Desvío standard: %s' % np.std(resultado)
