import os
import unittest

from code.utils import *


class TestUtils(unittest.TestCase):

    path_train = '../data/training/'
    path_test = '../data/test/'
    n_train = len(os.listdir(path_train))
    n_test = len(os.listdir(path_test))

    def test_features_training_shape(self):
        self.assertEquals((self.n_train, 2), features(self.path_train).shape)

    def test_features_test_shape(self):
        self.assertEquals((self.n_test, 2), features(self.path_test).shape)

    def test_labels_training_shape(self):
        # subtract one for missing label
        self.assertEquals((self.n_train-1, 2),
                          labels('../data/training-class').shape)

    def test_labels_test_shape(self):
        self.assertEquals((self.n_test, 2),
                          labels('../data/test-class').shape)

    def test_data_training_shape(self):
        X = features(self.path_train)
        y = labels('../data/training-class')
        # subtract one for missing label
        self.assertEquals((self.n_train-1, 3), data(X, y).shape)

    def test_data_test_shape(self):
        X = features(self.path_test)
        y = labels('../data/test-class')
        self.assertEquals((self.n_test, 3), data(X, y).shape)

    def test_remove_punctuation(self):
        text0 = 'hello, world'
        text1 = "this is where it's at!"
        text2 = "~!@#$%a^&*()-_=+[]{}\|;:'<>/"
        self.assertEquals('hello world', remove_punctuation(text0))
        self.assertEquals('this is where its at', remove_punctuation(text1))
        self.assertEquals('a', remove_punctuation(text2))

    def test_contains(self):
        text = "the use of humor, irony, exaggeration, or ridicule to expose and criticize people's stupidity or vices, particularly in the context of contemporary politics and other topical issues"
        satire = ['humor', 'irony']
        self.assertEquals(True, contains(satire, text))
