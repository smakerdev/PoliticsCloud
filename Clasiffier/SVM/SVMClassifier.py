import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import json
import pymysql
import numpy as np
import tensorflow as tf
from sklearn import svm
import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import json
import pymysql
import numpy as np
from sklearn import svm
import re
from konlpy.tag import Twitter
# Example for my blog post at:
# https://danijar.com/introduction-to-recurrent-networks-in-tensorflow/
import functools
import sets
import tensorflow as tf

def tokenize(sentence):
    twitter = Twitter()
    # twitter.morphs(sentence)
    ret = twitter.morphs(sentence)
    print(ret)
    return ret
    # return sentence.split()


def makeDictionary(pairs):
    dic = {}
    num = 0
    global sequence_dim

    for line in pairs:
        tokenized = tokenize(line[1])
        for token in tokenized:
            if token not in dic:
                dic[token] = num
                num += 1

    sequence_dim = len(dic.keys())
    return dic


def makePairs(keyword):
    sql = "select * from train_comment where label != -1 and keyword_id = {}".format(keyword)
    conn = pymysql.connect(host='unidev.namsu.xyz', user='dbmaster', password='dbmaster', db='politics',
                           charset='utf8mb4', port=9931)

    curs = conn.cursor()
    curs.execute(sql)
    news_lint = curs.fetchall()
    print(len(news_lint))
    ret = []
    for i in news_lint:
        if i[2] != 2:
            plain = re.sub("[^가-힣ㄱ-ㅎ0-9a-zA-Z!?.,]", "", i[4])
            ret.append((i[2], plain))

    return ret


# 숫자 -> 원핫
# 단어들 -> 2차원 벡터
def makeSequenceVector(words):
    ret = []
    for word in words:
        if word in dic:
            ret.append(dic[word])

    if(len(ret) > 100):
        return ret[:100]
    else:
        return ret.extend([0]*(100-len(ret)))


def makeTaggingData(pairs):
    train_x = []
    train_y = []
    for p in pairs:
        train_x.append(makeSequenceVector(p[1]))
        train_y.append(p[0] - 1)
    return train_x, train_y



pairs = makePairs(1)
print(len(pairs))
dic = makeDictionary(pairs)
train_x, train_y = makeTaggingData(pairs)
print(train_x)
print(len(train_x[0]))
print(train_x[0])


