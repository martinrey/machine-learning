# coding=utf-8
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from atributo import CantidadDeAparicionesDePalabra, CantidadDeAparicionesDeCaracter
from loader_de_mensajes_para_spam_filter import LoaderDeMensajesParaSpamFilter
from spam_filter import SpamFilter

def main():

    # clasificadores = [
    #     GridSearchCV(DecisionTreeClassifier(), param_grid=test_DecisionTreeClassifier(),cv=10),
    #     GridSearchCV(MultinomialNB(), param_grid=test_MultinomialNB()),
    #     GridSearchCV(KNeighborsClassifier(), param_grid=test_KNeighborsClassifier()),
    #     GridSearchCV(SVC(), param_grid=test_SVC()),
    #     GridSearchCV(RandomForestClassifier(), param_grid=test_RandomForestClassifier()),
    # ]
    #uso de pca para reducir dimencionalidad y mejorar resultados

    clasificadores = [
        DecisionTreeClassifier(),
        MultinomialNB(),
        KNeighborsClassifier(),
        SVC(),
        RandomForestClassifier(),
    ]
    pipelined_class = []
    pca = PCA(n_components=2)
    for clasificador in clasificadores:
        pipe = [('pca',pca),('clasificador',clasificador)]
        pipelined_class.append(GridSearchCV(Pipeline(pipe),{'pca__n_components':[2,5,10,40,70]}))

    clasificadores = pipelined_class

    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter('datos/ham_dev_entrenamiento.json', 'datos/spam_dev_entrenamiento.json')
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()
    #para buscar mejores parametros de clasificadores
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
        CantidadDeAparicionesDePalabra('promise'), CantidadDeAparicionesDePalabra('prince'),
        CantidadDeAparicionesDeCaracter('('), CantidadDeAparicionesDeCaracter('['),
        CantidadDeAparicionesDeCaracter('!'), CantidadDeAparicionesDeCaracter('$'),
        CantidadDeAparicionesDeCaracter('.'), CantidadDeAparicionesDeCaracter('\\'),
        CantidadDeAparicionesDeCaracter('#'), CantidadDeAparicionesDeCaracter(' '),
        CantidadDeAparicionesDeCaracter(';'),
    ]

    spam_filter = SpamFilter(dataframe, clasificadores, lista_de_atributos_a_buscar, utilizar_cache=False)
    print('Cantidad de atributos utilizados: %s' % len(lista_de_atributos_a_buscar))
    spam_filter.clasificar(mostrar_resultados_intermedios=False, utilizo_grid_search=True)

    for grid in clasificadores:
        print("Best Score: %s Best Params: %s" % (grid.best_score_ , grid.best_params_))

def test_DecisionTreeClassifier():
    grid_param = {"max_depth": [1,3,5,10,15,50,100], "min_samples_split": [1,3,5,10,15], }
    return grid_param

def test_MultinomialNB():
    grid_param = {"alpha": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.8,0.9,1]}
    return grid_param

def test_KNeighborsClassifier():
    grid_param = {"n_neighbors": [1,3,5,7,10,15], "weights": ["uniform","distance"]}
    return grid_param


def test_SVC():
    grid_param = {"kernel":['linear', 'poly', 'rbf', 'sigmoid'], "degree":[2,3,4], "probability": [True, False]}
    return grid_param

def test_RandomForestClassifier():
    grid_param = {"n_estimators":[2,5,10,15,40,100],"max_features":[2,5,10,20], "max_depth":[3,5,20,None]}
    return grid_param

if __name__ == '__main__':
    main()