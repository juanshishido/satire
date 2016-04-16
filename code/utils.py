import os
import re
from string import punctuation

import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from scipy.sparse import csr_matrix, hstack
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

from code.binormal_separation import bns


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

def parse_precomputed_features(path):
    with open(path, 'r') as f:
        return dict([ l.rstrip().split('\t') for l in f.readlines()])

def labels(f):
    return pd.read_csv(f, header=None, sep=' ', names=['file', 'label'])

def data(X, y):
    df = pd.merge(X, y, on='file')
    df['label'] = df.label.apply(lambda x: 1 if x == 'satire' else 0)
    return df

def vocabulary(a, b, tokenizer=None):
    assert isinstance(a, np.ndarray) and isinstance(b, np.ndarray)
    cv = CountVectorizer(tokenizer=tokenizer)
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

def represent(train, test, as_binary=True, tokenizer=None, vocabulary=None):
    """
    Return
    ------
    X_train, X_test : np.ndarray
        The training and test sets
    """
    assert (isinstance(train, pd.DataFrame) and
            isinstance(test, pd.DataFrame))
    train, test = train.copy(), test.copy()
    train['test'], test['test'] = 0, 1
    if as_binary:
        data_set = train.append(test, ignore_index=True)
        cv = CountVectorizer(tokenizer=tokenizer, binary=as_binary)
        X = cv.fit_transform(data_set.text.values)
        mask_train = data_set.test.values == 0
        mask_test = data_set.test.values == 1
        X_train = X[mask_train, :]
        X_test = X[mask_test, :]
    else:
        assert vocabulary is not None, 'Joint vocabulary required'
        X_train = bns(train.text.values, train.label.values,
                      train.text.values, tokenizer,
                      vocabulary=vocabulary)
        X_test = bns(train.text.values, train.label.values,
                     test.text.values, tokenizer,
                     vocabulary=vocabulary)
    return X_train, X_test

def append_features(X, data, include='all', tokenizer=None):
    assert include in ('lex', 'val', 'all', 'none'), 'Not a valid option'
    assert X.shape[0] == data.shape[0], 'Must have the same number of rows'
    X = X.copy()
    data = data.copy()
    if include in ('lex', 'all'):
        profane = word_lists('data/profane.txt')
        data['profane'] = data.text.apply(lambda text: contains(profane, text))
        slang = word_lists('lists/slang.txt')
        cv = CountVectorizer(vocabulary=slang, tokenizer=tokenizer)
        slang_counts = cv.fit_transform(data.text.values)
    if include in ('val', 'all'):
        semantic_validity = parse_precomputed_features('lists/semantic_validity.txt')
        data['validity'] = data.file.apply(lambda file:
                                           float(semantic_validity[file]))
    if include == 'lex':
        X = hstack([X,
                    csr_matrix(data.profane.tolist()).T,
                    np.divide(slang_counts.sum(axis=1), X.sum(axis=1))],
                   format='csr')
    elif include == 'val':
        X = hstack([X, csr_matrix(data.validity.tolist()).T], format='csr')
    elif include == 'all':
        X = hstack([X,
                    csr_matrix(data.profane.tolist()).T,
                    np.divide(slang_counts.sum(axis=1), X.sum(axis=1)),
                    csr_matrix(data.validity.tolist()).T],
                   format='csr')
    return X

def tune_params(X, y, clf, grid):
    grid_search = GridSearchCV(clf, grid, cv=5, n_jobs=-1)
    grid_search.fit(X, y)
    return grid_search.best_params_
