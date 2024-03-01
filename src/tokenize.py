# -*- coding: utf-8 -*-

#from operator import itemgetter
import itertools

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
        for n in range(2,4+1):
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

def test():
    corpus = open("../example/corpus.txt").read()
    t = Tokenizer()
    t.train(corpus)
    print(t.stats({"corpus_len": len(corpus)}))
    return t
test()#.tokens_frequency