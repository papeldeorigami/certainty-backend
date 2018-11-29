#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import librosa
from librosa import display
import sklearn
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, train_test_split
#  from sklearn.cross_validation import StratifiedKFold
import glob
import pandas as pd
import numpy as np
from hmmlearn.hmm import GaussianHMM, MultinomialHMM
from sklearn.externals import joblib

datas_cer = glob.glob('features/treinamento/certeza/*.csv')
datas_inc = glob.glob('features/treinamento/incerteza/*.csv')


def select_features(datas):
    feat_list = []
    for file in datas:
        df = pd.read_csv(file, sep=';')
        #df1 = df[df.columns[2:4]]
        df1 = df.loc[:, 'alphaRatio_sma3': 'F3amplitudeLogRelF0_sma3nz'].values
        d = np.array(df1)
        print (d.shape)
        feat_list.append(d)
    lenghts = []
    for i in range(len(feat_list)):
        lenghts.append(len(feat_list[i]))
        #print (df1)
    f = np.vstack(feat_list)
    return f, lenghts, feat_list


f_cer, len_cer, list_fcer = select_features(datas_cer)
f_inc, len_inc, list_finc = select_features(datas_inc)


import warnings
warnings.filterwarnings('ignore')

model1 = GaussianHMM(n_components=15, covariance_type='diag', n_iter=50)
model1.fit(f_cer, len_cer)
model1.monitor_


model1.monitor_.converged


model2 = GaussianHMM(n_components=15, covariance_type='diag', n_iter=50)
model2.fit(f_inc, len_inc)
model2.monitor_

model2.monitor_.converged


joblib.dump(model1, "Model1_certeza_keigo.pkl")


joblib.dump(model2, "Model2_incerteza_keigo.pkl")

