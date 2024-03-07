#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tokenizer.base import Tokenizer, groupby_count, filter_by_count, test_tokenizer, test_completion

class TrivialTokenizer(Tokenizer):
    
    def train(self, corpus, merges=50):


if __name__ == '__main__':
    t = test_tokenizer(TrivialTokenizer)
    #print(test_completion(TrivialTokenizer))