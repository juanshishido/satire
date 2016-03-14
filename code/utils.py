import os
import re

import numpy as np
import pandas as pd
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

def slangwords(path):
    return [s.rstrip() for s in open(path, 'r').readlines()]
