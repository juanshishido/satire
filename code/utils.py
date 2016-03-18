import os
import re
from string import punctuation

import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer


def _to_df(d):
    assert isinstance(d, dict)
    df = pd.DataFrame.from_dict(d, orient='index').reset_index()
    df.columns = ['file', 'text']
    return df

def features(path):
    articles = {}
    for file in os.listdir(path):
        with open(path+file, 'r', encoding='latin-1') as f:
            text = re.sub('\s+', ' ', f.read()).strip().lower()
        articles[file] = text
    return _to_df(articles)

def labels(f):
    return pd.read_csv(f, header=None, sep=' ', names=['file', 'label'])

def data(X, y):
    df = pd.merge(X, y, on='file')
    df['label'] = df.label.apply(lambda x: 1 if x == 'satire' else 0)
    return df

def vocabulary(a, b):
    assert isinstance(a, np.ndarray) and isinstance(b, np.ndarray)
    cv = CountVectorizer()
    cv.fit_transform(np.append(a, b))
    return list(cv.vocabulary_.keys())

def word_lists(path):
    with open(path, 'r') as f:
        return list(set([w.rstrip() for w in f.readlines()]))

def remove_punctuation(text):
    p = re.escape(punctuation)
    return re.sub(r'['+p+']+', '', text)

def contains(words, text):
    assert isinstance(words, (list, set)) and isinstance(text, str)
    return any(w in remove_punctuation(text).split() for w in words)

def tokenizer():
    return RegexpTokenizer("(?:[A-Za-z]\.)+|\w+(?:-\w+)*|\$[\d\.]+|\.\.\.|\S+")
