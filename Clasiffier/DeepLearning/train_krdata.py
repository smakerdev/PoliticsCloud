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
from keras.callbacks import ModelCheckpoint
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

MAX_SENT_LENGTH = 100
MAX_SENTS = 5
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
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

def reader(fname):
    ret={}
    ret['label']=[]
    ret['review']=[]
    return ret

#data_train = pd.read_csv('~/labeledTrainData.tsv', sep='\t')
#data_train = pd.read_csv('~/jungcle/textClassifier/train.tsv',sep='\t')a

filenames = ['output1.txt','output2.txt','output3.txt']
#filenames = ['output3.txt']
reviews=[]
labels=[]
texts=[]

total_cnt=0

for fname in filenames:
    data_train = pd.read_csv('~/'+fname,sep='\t')


    print (data_train.shape)
    #print (data_train)

    def tokeniz(doc):
        ret = doc.split('.')
        #ret.remove('')
        ret = [x for x in ret if x!= '']
        return ret
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
print ('total : ',total_cnt)
print ('reviews : ', reviews.__len__())
print ('unique labels count : ', str(set(labels)))
print ('reviews : ' + str(reviews[0]))
print ('labels : ' + str(labels[0]))
print ('texts : ' + str(texts[0]))
#############################
ch_cnt=0
ch_dic = {}
ch_dic[' '] = 0

for doc in reviews:
    for sentences in doc:
        for word in sentences:
            for ch in word:
                if ch not in ch_dic:
                    ch_cnt+=1
                    ch_dic[ch] = ch_cnt
EMBEDDING_DIM = ch_cnt+1
#print (ch_dic)
print ('ch_cnt : ',ch_cnt)
f = open('ch_dic.txt','w',encoding='utf-8')
f.write(str(ch_dic))
f.close()


data = np.zeros((len(texts), MAX_SENTS, MAX_SENT_LENGTH), dtype='int32')
for i, sentences in enumerate(reviews):
    for j, sent in enumerate(sentences):
        if j< MAX_SENTS:
            k=0
            for _, word in enumerate(sent):
                if k<MAX_SENT_LENGTH:
                    data[i,j,k] = ch_dic[word]
                    k=k+1                    
                   
word_index = ch_dic
print('Total %s unique tokens.' % len(word_index))

labels = to_categorical(np.asarray(labels))
print('Shape of data tensor:', data.shape)
#print (data)
print('Shape of label tensor:', labels.shape)
#print (labels)
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
nb_validation_samples = int(VALIDATION_SPLIT * data.shape[0])



x_train = data[:-nb_validation_samples]
y_train = labels[:-nb_validation_samples]
x_val = data[-nb_validation_samples:]
y_val = labels[-nb_validation_samples:]

print('Number of positive and negative reviews in traing and validation set')
print (y_train.sum(axis=0))
print (y_val.sum(axis=0))
#GLOVE_DIR = "/ext/home/analyst/Testground/data/glove"
GLOVE_DIR = "/home/jhryu"
embeddings_index = {}
print('Total %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((ch_cnt + 1, ch_cnt+1))

for i in range( ch_cnt+1):
    embedding_matrix[i][i] = 1

'''
for ch in ch_dic.keys():
    i = ch_dic[ch]
    #embedding_vector = ch_dic.get(ch)
    #print (i,ch_dic.get(ch))
    embedding_matrix[i][ch_dic.get(ch)] = 1
'''
#print ('embedded : ',embedding_matrix)
print (len(word_index)+1)
print (ch_cnt+1)


#embedding_layer = Embedding(len(word_index) + 1,
embedding_layer = Embedding(len(word_index),
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SENT_LENGTH,
                            trainable=True)

sentence_input = Input(shape=(MAX_SENT_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sentence_input)
l_lstm = Bidirectional(LSTM(100))(embedded_sequences)
sentEncoder = Model(sentence_input, l_lstm)
review_input = Input(shape=(MAX_SENTS,MAX_SENT_LENGTH), dtype='int32')
review_encoder = TimeDistributed(sentEncoder)(review_input)
l_lstm_sent = Bidirectional(LSTM(100))(review_encoder)

preds = Dense(2, activation='softmax')(l_lstm_sent)
model = Model(review_input, preds)

'''
sentence_input = Input(shape=(MAX_SENT_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sentence_input)
l_lstm = Bidirectional(GRU(100, return_sequences=True))(embedded_sequences)
l_dense = TimeDistributed(Dense(200))(l_lstm)
l_att = AttLayer()(l_dense)
sentEncoder = Model(sentence_input, l_att)

review_input = Input(shape=(MAX_SENTS,MAX_SENT_LENGTH), dtype='int32')
review_encoder = TimeDistributed(sentEncoder)(review_input)
l_lstm_sent = Bidirectional(GRU(100, return_sequences=True))(review_encoder)
l_dense_sent = TimeDistributed(Dense(200))(l_lstm_sent)
l_att_sent = AttLayer()(l_dense_sent)
preds = Dense(3, activation='softmax')(l_att_sent)
model = Model(review_input, preds)
'''

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])

print("model fitting - Hierachical LSTM")
print (model.summary())
print ('input shape : ',data.shape)

model_chk_path = '/home/jhryu/jungcle/textClassifier/save'
mcp = ModelCheckpoint(model_chk_path, monitor="val_acc",
                      save_best_only=True, save_weights_only=False)

model.fit(x_train, y_train, validation_data=(x_val, y_val),
          epochs=4, batch_size=20)

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

print (np.argmax(model.predict(x_val),axis=1))
print (np.argmax(y_val,axis=1))
