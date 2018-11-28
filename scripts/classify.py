#!/usr/bin/python
import matplotlib.pyplot as plt
import glob
#from scipy.io.wavfile import read
import librosa
from librosa import display
import sklearn
#from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
#from sklearn.model_selection import StratifiedKFold train_test_split,
#from sklearn.cross_validation import StratifiedKFold
import numpy as np
from hmmlearn.hmm import GaussianHMM, MultinomialHMM
import re

level = -37
label = "INCERTEZA"
print("%s %s" %(level, label))
