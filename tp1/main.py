# coding=utf-8
import getopt
import sys

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from atributo import CantidadDeAparicionesDePalabra, CantidadDeAparicionesDeCaracter
from loader_de_mensajes_para_spam_filter import LoaderDeMensajesParaSpamFilter
from spam_filter import SpamFilter

# VARIABLES DEL ENTORNO DEL PROGRAMA

TESTING_BUILD = False
CARPETA_DEFAULT_INPUT = 'datos/'
CARPETA_DEFAULT_OUTPUT = 'trained/'
CARPETA_DEFAULT_TESTING = 'datos/'
CLASIFICADORES_POR_NUMERO = {
    0: DecisionTreeClassifier(max_depth=50, min_samples_split=1),
    1: MultinomialNB(alpha=0.1),
    2: Pipeline([('pca', PCA(n_components=2)),
                 ('clasificador', KNeighborsClassifier(n_neighbors=1, weights='uniform'))]),
    3: Pipeline([('pca', PCA(n_components=70)), ('clasificador', SVC(kernel='linear'))]),
    4: RandomForestClassifier(n_estimators=100, max_depth=None, max_features=10),
}



def print_options():
    print('main.py -c numero_clasificador')
    print('-c <clasificador> \t\t el número del clasificador puede ser: ')
    print("0. DecisionTreeClassifier")
    print("1. MultinomialNB")
    print("2. KNeighborsClassifier")
    print("3. SVC")
    print("4. RandomForestClassifier")
    print("Flags:")
    print("-i <input_folder> \t\t carpeta con archivos de entrenamiento")
    print("-o <output_folder> \t\t carpeta donde se guardarán los resultados")
    print("-t <testing_folder> \t\t carpeta contenedora de los archivos contra los cuales testear")
    print("-d <development_testing> \t\t modo de testing para el desarollo")
    print("-m <model_filepath> \t\t ruta al archivo del modelo a utilizar (se guardarán los modelos en la output_folder"
          " a medida que se corra el programa)")
    print("-a <already_classified> \t\t marca que el entrenamiento ya estaba clasificado y el clasificador no se toma"
          " el trabajo de predecir")
    return


def main():
    input_folder = CARPETA_DEFAULT_INPUT
    output_folder = CARPETA_DEFAULT_OUTPUT
    testing_folder = CARPETA_DEFAULT_TESTING
    ya_clasificado = False
    filepath_de_modelo_a_utlizar = None
    numero_de_clasificador = 0

    if len(sys.argv) <= 2:
        print_options()
        sys.exit()
    argv = sys.argv[3:]

    try:
        opts, args = getopt.getopt(argv, "hc:i:o:t:m:a:", ["ifolder=", "ofolder="])
    except getopt.GetoptError:
        print_options()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print_options()
            sys.exit()
        elif opt in ("-c", "--clasificador"):
            numero_de_clasificador = int(arg)
        elif opt in ("-i", "--input_folder"):
            input_folder = arg
        elif opt in ("-o", "--output_folder"):
            output_folder = arg
        elif opt in ("-t", "--testing_folder"):
            testing_folder = arg
        elif opt in ("-m", "--model_filepath"):
            filepath_de_modelo_a_utlizar = arg
        elif opt in ("-a", "--already_classified"):
            ya_clasificado = True

    if TESTING_BUILD:
        development_testing()
    else:
        final_build(numero_de_clasificador, input_folder, output_folder, testing_folder, filepath_de_modelo_a_utlizar,
                    ya_clasificado)


def lista_de_atributos():
    return [
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


def final_build(numero_de_clasificador, input_folder=CARPETA_DEFAULT_INPUT, output_folder=CARPETA_DEFAULT_OUTPUT,
                testing_folder=CARPETA_DEFAULT_TESTING, filepath_de_modelo_a_utlizar=None, ya_clasificado=False):
    clasificador = CLASIFICADORES_POR_NUMERO[numero_de_clasificador]
    lista_de_atributos_a_buscar = lista_de_atributos()
    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter(input_folder + 'ham_dev_test.json',
                                                                         input_folder + 'spam_dev_test.json', verbose=0)
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()
    spam_filter = SpamFilter(dataframe, [clasificador], lista_de_atributos_a_buscar, utilizar_cache=False)

    if filepath_de_modelo_a_utlizar:
        spam_filter.cargar_modelo(filepath_de_modelo_a_utlizar)
    else:
        spam_filter.entrenar()
        spam_filter.guardar_modelo(output_folder, numero_de_clasificador=numero_de_clasificador)

    dataframe, lista_mensajes = preparar_archivos_contra_cuales_testear(spam_filter, testing_folder)
    if ya_clasificado:
        clasificaciones = dataframe['class']
        print("Score: %s" % spam_filter.score(lista_mensajes, clasificaciones))
    else:
        prediccion = spam_filter.predecir(lista_mensajes)
        devolver_lista_de_clasificaciones(prediccion)


def devolver_lista_de_clasificaciones(prediccion):
    for clasificacion in prediccion:
        print(clasificacion)


def preparar_archivos_contra_cuales_testear(spam_filter, testing_folder):
    loader_de_mensajes_para_testing = LoaderDeMensajesParaSpamFilter(testing_folder + 'ham_dev_entrenamiento.json',
                                                                     testing_folder + 'spam_dev_entrenamiento.json',
                                                                     verbose=0)
    dataframe = loader_de_mensajes_para_testing.crear_dataframe()
    lista_mensajes = spam_filter.valores(dataframe)
    return dataframe, lista_mensajes


def development_testing():
    # clasificadores = [
    #     GridSearchCV(DecisionTreeClassifier(), param_grid=test_DecisionTreeClassifier(),cv=10),
    #     GridSearchCV(MultinomialNB(), param_grid=test_MultinomialNB()),
    #     GridSearchCV(KNeighborsClassifier(), param_grid=test_KNeighborsClassifier()),
    #     GridSearchCV(SVC(), param_grid=test_SVC()),
    #     GridSearchCV(RandomForestClassifier(), param_grid=test_RandomForestClassifier()),
    # ]
    # uso de pca para reducir dimencionalidad y mejorar resultados

    clasificadores = [
        DecisionTreeClassifier(max_depth=50, min_samples_split=1),
        MultinomialNB(alpha=0.1),
        KNeighborsClassifier(n_neighbors=1, weights='uniform'),
        # SVC(),
        RandomForestClassifier(n_estimators=100, max_depth=None, max_features=10),
    ]
    pipelined_class = []
    pca = PCA(n_components=2)
    for clasificador in clasificadores:
        pipe = [('pca', pca), ('clasificador', clasificador)]
        pipelined_class.append(GridSearchCV(Pipeline(pipe), {'pca__n_components': [2, 5, 10, 40, 70]}))

    clasificadores = pipelined_class

    loader_de_mensajes_para_spam_filter = LoaderDeMensajesParaSpamFilter('datos/ham_dev_entrenamiento.json',
                                                                         'datos/spam_dev_entrenamiento.json')
    dataframe = loader_de_mensajes_para_spam_filter.crear_dataframe()
    # para buscar mejores parametros de clasificadores

    lista_de_atributos_a_buscar = lista_de_atributos()

    spam_filter = SpamFilter(dataframe, clasificadores, lista_de_atributos_a_buscar, utilizar_cache=False)
    print('Cantidad de atributos utilizados: %s' % len(lista_de_atributos_a_buscar))
    spam_filter.hacer_cross_validation(mostrar_resultados_intermedios=False, utilizo_grid_search=True)

    for grid in clasificadores:
        print("Best Score: %s Best Params: %s" % (grid.best_score_, grid.best_params_))


if __name__ == '__main__':
    main()
