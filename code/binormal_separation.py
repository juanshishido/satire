import numpy as np
from scipy.stats import norm
from sklearn.feature_extraction.text import CountVectorizer


def _token_counts(text_array, tokenizer=None, vocabulary=None, binary=False):
    cv = CountVectorizer(tokenizer=tokenizer, vocabulary=vocabulary,
                         binary=binary)
    return cv.fit_transform(text_array)

def _tf_positive_rate(X, pn_class):
    totals = X[pn_class, :].sum(axis=0)
    pr = np.squeeze(np.asarray(totals / totals.sum()))
    pr[pr==0] = 0.0005
    return pr

def bns(text_array, y_true, to_scale, tokenizer=None, vocabulary=None):
    """Bi-normal separation feature scaling
        | F**-1(tpr) - F**-1(fpr) |
        where
            F is the normal CDF
            tpr is the true positive rate
            fpr is the false positive rate
    
    Parameters
    ----------
    text_array : np.ndarray
        The text for the articles to calculate the BNS weights
    y_true : np.ndarray
        Ground truth (correct) labels associated with `text_array`
    to_scale : np.ndarray
        The text for the articles to scale
    tokenizer : callable or None (default)
        For string tokenization
    
    Returns
    -------
    bns_features : np.ndarray
        BNS weights for each present feature
    
    Notes
    -----
    Based on Forman, George (2003)
    """
    assert isinstance(text_array, np.ndarray) and isinstance(y_true, np.ndarray)
    assert text_array.shape == y_true.shape
    assert isinstance(to_scale, np.ndarray)
    X = _token_counts(text_array, tokenizer=tokenizer, vocabulary=vocabulary,
                      binary=False)
    p_class, n_class = y_true == 1, y_true == 0
    tpr = _tf_positive_rate(X, p_class)
    fpr = _tf_positive_rate(X, n_class)
    bns = np.absolute(norm.ppf(tpr) - norm.ppf(fpr))
    X = _token_counts(to_scale, tokenizer=tokenizer, vocabulary=vocabulary,
                      binary=True)
    bns_features = np.multiply(X.toarray(), bns)
    return bns_features
