#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from corpus import Corpus

def cbow_trainingdata_printer(corpus, context_size, X, Y):
    [idx2word, word2idx] = corpus.translators()
    for sample in [[[idx2word[x] for x in xs], idx2word[y]] for [xs,y] in list(zip(X,Y))]:
        print(sample[0][:context_size], sample[1], sample[0][-context_size:])

def cbow_trainingdata_for_corpus(corpus, context_size=2):
    """          
    >>> corpus = Corpus()
    >>> context_size = 2
    >>> [X, Y] = cbow_trainingdata_for_corpus(corpus, context_size)
    >>> cbow_trainingdata_printer(corpus, context_size, X[196:200], Y[196:200])
    ['ihr', 'naht'] euch ['wieder', 'schwankende']
    ['naht', 'euch'] wieder ['schwankende', 'gestalten']
    ['euch', 'wieder'] schwankende ['gestalten', 'die']
    ['wieder', 'schwankende'] gestalten ['die', 'früh']
    """
    
    [idx2word, word2idx] = corpus.translators()
    encodedCorpus = [word2idx[w] for w in corpus.word_list()]

    range_of_index_of_word_to_guess = range(context_size, len(encodedCorpus)-context_size)

    X = [[encodedCorpus[j] for j in range(i-context_size, i)] +
         [encodedCorpus[j] for j in range(i+1, i+1+context_size)]
         for i in range_of_index_of_word_to_guess]
    Y = [encodedCorpus[i] for i in range_of_index_of_word_to_guess]
    
    return [X, Y]


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())