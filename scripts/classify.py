#!/usr/bin/python3
import numpy as np
import os
import pandas as pd
from hmmlearn.hmm import GaussianHMM, MultinomialHMM
from sklearn.externals import joblib

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
OPENSMILE_FOLDER = SCRIPT_FOLDER + "/../../../opensmile-2.3.0"
RECORDING_FILE = "/tmp/recording.wav"
RECORDING_FILE_WITH_HEADERS = "/tmp/recordingh.wav"
FEATURES_FILE = "/tmp/recording.csv"

def extract_features():
    os.system("rm -f %s" %FEATURES_FILE)
    os.system("rm -f %s" %RECORDING_FILE_WITH_HEADERS)
    os.system("ffmpeg -f s16le -ar 44.1k -ac 1 -i %s %s 2>/dev/null" %(RECORDING_FILE, RECORDING_FILE_WITH_HEADERS))
    os.system("%s/inst/bin/SMILExtract -C %s/config/gemaps/GeMAPSv01a.conf -I %s -D %s 2>/dev/null" %(OPENSMILE_FOLDER, OPENSMILE_FOLDER, RECORDING_FILE_WITH_HEADERS, FEATURES_FILE))

def select_feature_test(path):
    df = pd.read_csv(path, sep=';')
    df1 = df.loc[:, 'alphaRatio_sma3': 'F3amplitudeLogRelF0_sma3nz'].values
    d = np.array(df1)
    #print (d.shape)
    lenghts = []
    for i in range(len(d)):
        lenghts.append(len(d[i]))
    #print (df1)
    f = np.vstack(d)
    return f, lenghts

model1 = joblib.load(SCRIPT_FOLDER + "/Model1_certeza_keigo.pkl")
model2 = joblib.load(SCRIPT_FOLDER + "/Model2_incerteza_keigo.pkl")
#  model1 = joblib.load("Model1_certeza.pkl")
#  model2 = joblib.load("Model2_incerteza.pkl")

extract_features()
f_test, len_test = select_feature_test(FEATURES_FILE)
prob1 = model1.score(f_test)
prob2 = model2.score(f_test)

level = 0
label = ''

#  print(prob1)
#  print(prob2)
if prob1 > prob2:
    level = prob1
    label = 'certeza'
else:
    level = prob2
    label = 'incerteza'

print("%s %s" %(level, label))
