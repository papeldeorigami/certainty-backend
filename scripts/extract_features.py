#!/usr/bin/python
# -*- coding: latin-1 -*-
import glob
import os
import pandas as pd
import re
import random

# Constants
AUDIOS_FOLDER = "../audios_projeto_IA369Y"
OPENSMILE_FOLDER = "../opensmile-2.3.0"
OUTPUT_FOLDER = "./features"
TRAINING_FOLDER = "treinamento"
PREDICTION_FOLDER = "validacao"

df_resp = pd.read_csv("../respostas.csv")
df_resp['p'] = map(lambda x: x.lower(), df_resp['Prontuário'])
df_anon = pd.read_csv("../anonimo-prontuario.csv")
df_anon['p'] = map(lambda x: x.lower(), df_anon['prontuario'])
p = re.compile(r'(I\d+)question(\d+)')

sentiments = ["certeza", "incerteza"]
for sentiment in sentiments:
    os.system("mkdir -p %s/%s/%s 2>/dev/null" %(OUTPUT_FOLDER, TRAINING_FOLDER, sentiment))
    os.system("mkdir -p %s/%s/%s 2>/dev/null" %(OUTPUT_FOLDER, PREDICTION_FOLDER, sentiment))

files = glob.glob("%s/*/*.ogg" %AUDIOS_FOLDER)

# define training and prediction datasets
random.shuffle(files)
training = files[:int(len(files)*0.8)] #get first 80% of file list
prediction = files[-int(len(files)*0.2):] #get last 20% of file list

cont = 0
for oggfile in files:
    m = re.match(r'(.*)(I\d+)questao(\d+)', oggfile, re.I | re.M)
    if not m:
        print("%s does not match the regex" %oggfile)
        #  continue;
        break;
    folder = m.group(1)
    participant = m.group(2)
    question = m.group(3)
    file_noext = "%squestao%s" %(participant, question)
    file_noext_with_folder = "%s%s" %(folder, file_noext)
    print("[%03d] participant=%s, question=%s" %(cont, participant, question))
    participant_ids = df_anon[(df_anon["anonimo"] == participant)]["prontuario"]
    if participant_ids.size == 0:
        print("Participante '%s' não encontrado na relação de IDs" %participant)
        #  continue;
        break;
    participant_id = participant_ids.values[0].lower()
    print("Prontuario: %s" %participant_id)
    labels = df_resp[(df_resp["p"] == participant_id) & (df_resp["Questão"] == "Q%s" %question.zfill(2))]["Sentimento"]
    if labels.size == 0:
        print("Participante '%s' não encontrado na lista de respostas" %participant_id)
        #  continue;
        break;
    label = labels.values[0].lower()
    print("Sentimento: %s" %label)
    target = TRAINING_FOLDER
    if (oggfile in prediction):
        target = PREDICTION_FOLDER
    output_folder = "%s/%s/%s" %(OUTPUT_FOLDER, target, label)
    print("Pasta de destino: %s" %output_folder)
    os.system("ffmpeg -y -i %s/%s %s/%s.wav 2>/dev/null" %(AUDIOS_FOLDER, oggfile, AUDIOS_FOLDER, file_noext_with_folder))
    os.system("%s/inst/bin/SMILExtract -C %s/config/gemaps/GeMAPSv01a.conf -I %s/%s.wav -D %s/%s.csv 2>/dev/null" %(OPENSMILE_FOLDER, OPENSMILE_FOLDER, AUDIOS_FOLDER, file_noext_with_folder, output_folder, file_noext))
    #  break;
    cont += 1

print("%d arquivos processados" %cont)
found = os.popen(r"find . -name *.csv | wc | sed -r 's/^\s+([0-9]+).*/\1/'").read().strip()
print("%s arquivos CSV de features gerados" %found)
