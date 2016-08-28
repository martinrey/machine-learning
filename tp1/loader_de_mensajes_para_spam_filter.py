import json

import pandas as pd


class LoaderDeMensajesParaSpamFilter(object):
    def __init__(self, filepath_base_ham, filepath_base_spam):
        self._filepath_base_ham = filepath_base_ham
        self._filepath_base_spam = filepath_base_spam

    def crear_dataframe(self):
        ham_txt = json.load(open(self._filepath_base_ham))
        spam_txt = json.load(open(self._filepath_base_spam))
        dataframe = pd.DataFrame(ham_txt + spam_txt, columns=['text'])
        dataframe['class'] = ['ham' for _ in range(len(ham_txt))] + ['spam' for _ in range(len(spam_txt))]
        return dataframe
