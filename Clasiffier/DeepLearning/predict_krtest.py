# author - Richard Liao
# Dec 26 2016
import numpy as np
import pandas as pd
#import cPickle
import _pickle as cPickle

from collections import defaultdict
import re

from bs4 import BeautifulSoup

import sys
import os

#os.environ['KERAS_BACKEND']='theano'
import requests as rq
import json
import pymysql

from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

from keras.layers import Embedding
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding, Merge, Dropout, LSTM, GRU, Bidirectional, TimeDistributed
from keras.models import Model

from keras import backend as K
from keras.engine.topology import Layer, InputSpec
from keras import initializers as initializations
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


MAX_SENT_LENGTH = 100
MAX_SENTS = 5
MAX_NB_WORDS = 20000
#EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2

def clean_str(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    #string = re.sub("\\", "", string)
    #string = re.sub("\'", "", string)
    #string = re.sub("\"", "", string)
    return string.strip().lower()



#data_train = pd.read_csv('~/nolabeled_output1.txt',sep='\t')
#print (data_train.shape)
reviews = []
labels = []
texts = []

#for line in open('~/nolabeled_output1.txt','r',encoding='utf-8'):


def tokeniz(doc):
    ret = doc.split('.')
    #ret.remove('')
    ret = [x for x in ret if x!= '']
    return ret
total_cnt=0

for line in open('/home/jhryu/nolabeled_output7.txt','r',encoding='utf-8'):
    try:
      data = line.strip().split('\t')
      data[0] = int(data[0])
      if data[0] == '2':
          continue
      text = data[1]
      texts.append(text)
      sentences=tokeniz(text)
      reviews.append(sentences)
      labels.append(data[0])
    except:
      print('except : ',line)
'''
for idx in range(data_train.review.shape[0]):
    total_cnt+=1
    if data_train.sentiment[idx] ==2:
        continue
    text = data_train.review[idx]
    texts.append(text)
    #sentences = tokenize.sent_tokenize(text)
    sentences = tokeniz(text)
    #print (sentences)

    #sentences = tokenize.sent_tokenize(text)
    reviews.append(sentences)

    labels.append(data_train.sentiment[idx])
'''

print ('total : ',total_cnt)
print ('reviews : ', reviews.__len__())
print ('unique labels count : ', str(set(labels)))
print ('reviews : ' + str(reviews[0]))
#print ('labels : ' + str(labels[0]))
print ('texts : ' + str(texts[0]))

#labels = to_categorical(np.asarray(labels))

import ast
f= open ('ch_dic.txt','r',encoding='utf-8')
t = f.read()
ch_dic = ast.literal_eval(t)
ch_cnt = len(ch_dic)-1
EMBEDDING_DIM = ch_cnt+1
maxv=0

data = np.zeros((len(texts), MAX_SENTS, MAX_SENT_LENGTH), dtype='int32')
for i, sentences in enumerate(reviews):
    for j, sent in enumerate(sentences):
        if j< MAX_SENTS:
            k=0
            for _, word in enumerate(sent):
                if k<MAX_SENT_LENGTH:
                    if word not in ch_dic:
                        word=' '
                    data[i,j,k] = ch_dic[word]
                    if data[i,j,k]>maxv:
                        maxv=data[i,j,k]
                    k=k+1

print ('maxvalue : ', maxv)
print ('input shape : ',data.shape)


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

#percent = loaded_model.evaluate(data,labels)
#print ('result : ',percent)
result = np.argmax(loaded_model.predict(data),axis=1)

for i in result:
    print (i, end=' ')

e=0


for i in range(len(result)):
  sql = "update comment set label =" + str(result[i])  +"  where comment_no =\'"+ str(labels[i]) + "\'"
  conn = pymysql.connect(host='unidev.namsu.xyz',user='dbmaster',password='dbmaster',db='politics',charset='utf8mb4',port=9931)
  print (sql)
  curs = conn.cursor()
  curs.execute(sql)
  conn.commit()
conn.close()
print (len(result),e)
print (e/len(result))



#score = loaded_model.evaluate(X, Y, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
