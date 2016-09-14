import json

import pandas as pd


class LoaderDeMensajesParaSpamFilter(object):
    def __init__(self, filepath_base_ham, filepath_base_spam):
        self._filepath_base_ham = filepath_base_ham
        self._filepath_base_spam = filepath_base_spam

    def crear_dataframe(self):
        self._mensaje_de_progreso_de_carga_de_lista_de_mensajes()
        base_ham_file = open(self._filepath_base_ham)
        ham_txt = json.load(base_ham_file)
        base_ham_file.close()
        base_spam_file = open(self._filepath_base_spam)
        spam_txt = json.load(base_spam_file)
        base_spam_file.close()
        dataframe = pd.DataFrame(ham_txt + spam_txt, columns=['text'])
        dataframe['class'] = ['ham' for _ in range(len(ham_txt))] + ['spam' for _ in range(len(spam_txt))]
        return dataframe

    def _mensaje_de_progreso_de_carga_de_lista_de_mensajes(self):
        print('----------- Cargando lista de mensajes (puede demorar unos minutos...) -----------')
