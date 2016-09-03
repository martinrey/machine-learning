# coding=utf-8
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from atributo import CantidadDeAparicionesDePalabra, CantidadDeAparicionesDeCaracter
from loader_de_mensajes_para_spam_filter import LoaderDeMensajesParaSpamFilter
from spam_filter import SpamFilter

if __name__ == '__main__':
    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter('datos/ham_dev.json', 'datos/spam_dev.json')
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()

    clasificador = DecisionTreeClassifier(max_depth=15, min_samples_split=10)

    lista_de_atributos_a_buscar = [
        CantidadDeAparicionesDePalabra('vicodin'), CantidadDeAparicionesDePalabra('viagra'),
        CantidadDeAparicionesDePalabra('html'), CantidadDeAparicionesDePalabra('http'),
        CantidadDeAparicionesDePalabra('make'), CantidadDeAparicionesDePalabra('conference'),
        CantidadDeAparicionesDePalabra('address'), CantidadDeAparicionesDePalabra('all'),
        CantidadDeAparicionesDePalabra('3d'), CantidadDeAparicionesDePalabra('our'),
        CantidadDeAparicionesDePalabra('over'), CantidadDeAparicionesDePalabra('remove'),
        CantidadDeAparicionesDePalabra('internet'), CantidadDeAparicionesDePalabra('order'),
        CantidadDeAparicionesDePalabra('mail'), CantidadDeAparicionesDePalabra('receive'),
        CantidadDeAparicionesDePalabra('will'), CantidadDeAparicionesDePalabra('people'),
        CantidadDeAparicionesDePalabra('report'), CantidadDeAparicionesDePalabra('addresses'),
        CantidadDeAparicionesDePalabra('free'), CantidadDeAparicionesDePalabra('business'),
        CantidadDeAparicionesDePalabra('email'), CantidadDeAparicionesDePalabra('you'),
        CantidadDeAparicionesDePalabra('credit'), CantidadDeAparicionesDePalabra('your'),
        CantidadDeAparicionesDePalabra('font'), CantidadDeAparicionesDePalabra('money'),
        CantidadDeAparicionesDePalabra('hp'), CantidadDeAparicionesDePalabra('hpl'),
        CantidadDeAparicionesDePalabra('george'), CantidadDeAparicionesDePalabra('lab'),
        CantidadDeAparicionesDePalabra('labs'), CantidadDeAparicionesDePalabra('telnet'),
        CantidadDeAparicionesDePalabra('data'), CantidadDeAparicionesDePalabra('technology'),
        CantidadDeAparicionesDePalabra('parts'), CantidadDeAparicionesDePalabra('pm'),
        CantidadDeAparicionesDePalabra('direct'), CantidadDeAparicionesDePalabra('cs'),
        CantidadDeAparicionesDePalabra('meeting'), CantidadDeAparicionesDePalabra('original'),
        CantidadDeAparicionesDePalabra('project'), CantidadDeAparicionesDePalabra('re'),
        CantidadDeAparicionesDePalabra('edu'), CantidadDeAparicionesDePalabra('table'),
        CantidadDeAparicionesDePalabra('nigeria'), CantidadDeAparicionesDePalabra('buy'),
        CantidadDeAparicionesDePalabra('income'), CantidadDeAparicionesDePalabra('opportunity'),
        CantidadDeAparicionesDePalabra('extra'), CantidadDeAparicionesDePalabra('cash'),
        CantidadDeAparicionesDePalabra('free'), CantidadDeAparicionesDePalabra('insurance'),
        CantidadDeAparicionesDePalabra('child'), CantidadDeAparicionesDePalabra('rate'),
        CantidadDeAparicionesDePalabra('lifetime'), CantidadDeAparicionesDePalabra('sample'),
        CantidadDeAparicionesDePalabra('satisfaction'), CantidadDeAparicionesDePalabra('wife'),
        CantidadDeAparicionesDePalabra('dear'), CantidadDeAparicionesDePalabra('friend'),
        CantidadDeAparicionesDePalabra('ad'), CantidadDeAparicionesDePalabra('click'),
        CantidadDeAparicionesDePalabra('here'), CantidadDeAparicionesDePalabra('marketing'),
        CantidadDeAparicionesDePalabra('notspam'), CantidadDeAparicionesDePalabra('subscribe'),
        CantidadDeAparicionesDePalabra('junk'), CantidadDeAparicionesDePalabra('traffic'),
        CantidadDeAparicionesDePalabra('spam'), CantidadDeAparicionesDePalabra('trial'),
        CantidadDeAparicionesDePalabra('xanax'), CantidadDeAparicionesDePalabra('valium'),
        CantidadDeAparicionesDePalabra('weight'), CantidadDeAparicionesDePalabra('hormone'),
        CantidadDeAparicionesDePalabra('testosterone'), CantidadDeAparicionesDePalabra('growth'),
        CantidadDeAparicionesDePalabra('inventory'), CantidadDeAparicionesDePalabra('disappointment'),
        CantidadDeAparicionesDePalabra('guarantee'), CantidadDeAparicionesDePalabra('nigerian'),
        CantidadDeAparicionesDePalabra('vacation'), CantidadDeAparicionesDePalabra('win'),
        CantidadDeAparicionesDePalabra('selected'), CantidadDeAparicionesDePalabra('hosting'),
        CantidadDeAparicionesDePalabra('membership'), CantidadDeAparicionesDePalabra('natural'),
        CantidadDeAparicionesDePalabra('instant'), CantidadDeAparicionesDePalabra('bonus'),
        CantidadDeAparicionesDePalabra('promise'),
        CantidadDeAparicionesDeCaracter('('), CantidadDeAparicionesDeCaracter('['),
        CantidadDeAparicionesDeCaracter('!'), CantidadDeAparicionesDeCaracter('$'),
        CantidadDeAparicionesDeCaracter('.'), CantidadDeAparicionesDeCaracter('\\'),
        CantidadDeAparicionesDeCaracter('#'), CantidadDeAparicionesDeCaracter(' '),
        CantidadDeAparicionesDeCaracter(';'),
    ]

    spam_filter = SpamFilter(dataframe, clasificador, lista_de_atributos_a_buscar, utilizar_cache=True)
    resultado = spam_filter.clasificar()

    print('Cantidad de atributos utilizados: %s' % len(lista_de_atributos_a_buscar))
    print('Media: %s' % np.mean(resultado))
    print('Desvío standard: %s' % np.std(resultado))
