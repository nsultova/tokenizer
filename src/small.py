#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import embedding.wikipedia2vec as wp
import numpy as np

corpus = open("../example/corpus.txt").read()

def words_from_str(s):
    words = re.sub("[^a-zA-Zäöüß]", " ", corpus).lower().split(" ")
    return set(filter(lambda w: w!='', words))

#d = wp.example_dict()

all = True
#if all:
#    words = list(d._word_dict.keys())
#else:
#    words = words_from_str(corpus)

#d_corpus = {}
#for w in words:
#    try:
#        d_corpus[w] = d[w]
#    except:
#        pass

if all:
    suffix = ""
else:
    suffix = "_small"
    
import joblib
#joblib.dump({"d_corpus": d_corpus}, "/home/j03/Documents/src/py/lm/tokenize/d_corpus"+suffix)

print("load corpus…")
d_corpus = joblib.load("../example/d_corpus"+suffix)["d_corpus"]
def most_similar(vec: np.ndarray, k=10):
    dst = np.dot(list(d_corpus.values()), vec) / np.linalg.norm(list(d_corpus.values()), axis=1) / np.linalg.norm(vec)
    indexes = np.argsort(-dst)
    return [(list(d_corpus.keys())[i], dst[i]) for i in indexes[:k]]

print(most_similar(d_corpus["nixos"]))
print(most_similar(d_corpus["bruder"] + d_corpus["frau"] - d_corpus["mann"]))
