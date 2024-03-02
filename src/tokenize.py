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
    
    def train(self, text):
        
        ## terminal symbols / monograms
        symbols_frequency = groupby_count(sorted(text))
        for sym, count in symbols_frequency:
            self.tokens_frequency[sym] = count
        symbols = [x[0] for x in symbols_frequency]
        for idx, sym in enumerate(symbols):
            self.tokens[idx] = sym

        ## nonterminal symbols / n-grams
        for n in range(2,5+1):
            ngrams_all = [text[start:start+n] for start in range(len(text)-n)]
            ngrams_frequency_all = groupby_count(sorted(ngrams_all))
            ngrams_frequency = filter_by_count(ngrams_frequency_all)
            for ngram, count in ngrams_frequency:
                self.tokens_frequency[ngram] = count
            idx_offset = len(self.tokens)
            ngrams = [x[0] for x in ngrams_frequency]
            for idx, ngram in enumerate(ngrams):
                self.tokens[idx_offset+idx] = ngram

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

def test_tokenizer():
    corpus = open("../example/corpus.txt").read()
    t = Tokenizer()
    t.train(corpus)
    print(t.stats({"corpus_len": len(corpus)}))
    return t

def test_completion():
    t = test_tokenizer()
    sentence = ""
    context_len = 4
    for i in range(1000):
        context = sentence[-context_len:]
        completion = t.complete(context)
        #print([i, sentence[:-context_len], context, completion], "\n")
        sentence = sentence[:-context_len] + completion
        if completion == context:
            context_len -= 1
        else:
            context_len += random.randint(0, 1)
    return sentence

print(test_completion())