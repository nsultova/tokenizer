#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import random

def groupby_count(l):
    return [[k, len(list(g))] for k,g in itertools.groupby(sorted(l))]

def filter_by_count(l, min=10):
    f = (lambda x_count: x_count[1] >= min)
    return list(filter(f, l))

class Tokenizer():
    
    tokens = {}  ## idx -> token
    tokens_frequency = {}  ## token -> count
    
    def train(self, corpus):
        pass

    def stats(self, merged = {}):
        merged.update({"token_count": len(self.tokens)})
        return merged

    def complete(self, context=""):
        """Please don't expect it te be smart — It's only a trivial markov chain based on n-grams"""
        matches = list(filter(lambda x: x[0].startswith(context) and x[0]!=context,
                              self.tokens_frequency.items()))
        weights = [x[1] for x in matches]
        if matches:
            return random.choices(matches, weights=weights)[0][0]
        return context

def test_tokenizer(tokenizer):
    corpus = open("../example/corpus.txt").read()
    t = tokenizer()
    t.train(corpus)
    print(t.stats({"corpus_len": len(corpus)}))
    return t

def test_completion(tokenizer, sentence="", length=10000, debug=True):
    t = test_tokenizer(tokenizer)
    context_len = 1
    for i in range(length):
        context = sentence[-context_len:]
        completion = t.complete(context)
        if debug:
            print([i, sentence[:-context_len], context, completion], "\n")
        else:
            print(completion[len(context):], end='', flush=True)
        sentence = sentence[:-context_len] + completion
        if completion == context:
            context_len -= 1
        else:
            context_len += random.randint(0, 1)
    return sentence