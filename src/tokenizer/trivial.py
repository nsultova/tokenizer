#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tokenizer.base import Tokenizer, groupby_count, filter_by_count, test_tokenizer, test_completion

class TrivialTokenizer(Tokenizer):
    
    def train(self, corpus):
        ## terminal symbols / monograms
        symbols_frequency = groupby_count(sorted(corpus))
        for sym, count in symbols_frequency:
            self.tokens_frequency[sym] = count
        symbols = [x[0] for x in symbols_frequency]
        for idx, sym in enumerate(symbols):
            self.tokens[idx] = sym

        ## nonterminal symbols / n-grams
        for n in range(2,5+1):
            ngrams_all = [corpus[start:start+n] for start in range(len(corpus)-n)]
            ngrams_frequency_all = groupby_count(sorted(ngrams_all))
            ngrams_frequency = filter_by_count(ngrams_frequency_all)
            for ngram, count in ngrams_frequency:
                self.tokens_frequency[ngram] = count
            idx_offset = len(self.tokens)
            ngrams = [x[0] for x in ngrams_frequency]
            for idx, ngram in enumerate(ngrams):
                self.tokens[idx_offset+idx] = ngram


if __name__ == '__main__':
    #t = test_tokenizer(TrivialTokenizer)
    print(test_completion(TrivialTokenizer))