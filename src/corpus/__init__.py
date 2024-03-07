#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def lines(s, n):
    return "\n".join(s.splitlines()[:n])

re_none = "[.]"
re_spaces = " +"
re_blanks = "\s+"

class Corpus():
    corpus: str
    lower: bool
    blank_re: str
    space = " "
    non_vocab_re: str
    non_vocab_replacement: str
    _meta = {}
    
    def __init__(self,
                 corpus = None,
                 file = "../example/corpus.txt",
                 lower = True,
                 blank_re = re_spaces,
                 non_vocab_re = "[^a-zA-Zäöüß \n]",
                 non_vocab_replacement = " "):

        self.lower = lower
        self.blank_re = blank_re
        self.non_vocab_re = non_vocab_re
        self.non_vocab_replacement = non_vocab_replacement
        
        if corpus:
            self.corpus = corpus
            return

        self.corpus = open(file).read()
        self._meta["file"] = file

    def clearedup(self, blank_re=None, non_vocab_re=None):
        """
        >>> c = Corpus(file="./corpus/__init__.py")

        >>> print(lines(c.clearedup(non_vocab_re=re_none), 2))
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-

        >>> print(lines(c.clearedup(), 2))
         usr bin env python 
         coding utf 

        >>> print(c.clearedup(blank_re=re_blanks)[:30])
         usr bin env python coding utf
        """

        if self.lower:
            corpus = self.corpus.lower()
        else:
            corpus = self.corpus

        vocab_only = re.sub(non_vocab_re or self.non_vocab_re, self.non_vocab_replacement, corpus)
        
        if blank_re == None:
            blank_re = self.blank_re
        return re.sub(blank_re, self.space, vocab_only)
 
    def chars(self, blank_re=None):
        """
        >>> c = Corpus(file="./corpus/__init__.py")

        >>> c.chars(blank_re=re_blanks)[:5]
        [' ', 'a', 'b', 'c', 'd']
        
        >>> c.chars()[:5]
        ['\\n', ' ', 'a', 'b', 'c']
        
        >>> len(c.chars())
        32
        """
        
        corpus = self.clearedup(blank_re=blank_re)
        return sorted(set([c for c in corpus]))

    def word_list(self, blank_re=re_blanks, **kwargs):
        """
        >>> c = Corpus(file="./corpus/__init__.py")

        >>> c.word_list()[:7]
        ['', 'usr', 'bin', 'env', 'python', 'coding', 'utf']
     
        >>> c.word_list(blank_re=re_spaces)[:7]
        ['', 'usr', 'bin', 'env', 'python', '\\n', 'coding']
        
        >>> c.word_list(non_vocab_re=re_none)[:6]
        ['#!/usr/bin/env', 'python3', '#', '-*-', 'coding:', 'utf-8']

        >>> c.word_list(non_vocab_re=re_none, blank_re=re_spaces)[:5]
        ['#!/usr/bin/env', 'python3\\n#', '-*-', 'coding:', 'utf-8']
        """

        return self.clearedup(blank_re=blank_re, **kwargs).split(self.space)
    
    def words(self, **kwargs):
        """
        >>> c = Corpus(file="./corpus/__init__.py")

        >>> c.words()[:10]
        ['', 'a', 'args', 'azazäöüß', 'b', 'bin', 'blank', 'blankre', 'blankren', 'blankrenone']
        
        >>> c.words(blank_re=re_spaces)[:10]
        ['', '\\n', '\\n\\n', '\\n\\n\\nif', '\\n\\nclass', '\\n\\nimport', '\\n\\nre', '\\nre', 'a', 'args']
        """

        return sorted(set(self.word_list(**kwargs)))
    
    def translators(self, **kwargs):
        """
        >>> args = {"non_vocab_re": re_none}
        >>> c = Corpus(file="./corpus/__init__.py")
        >>> [idx2word, word2idx] = c.translators(**args)
        >>> example_word = c.word_list(**args)[0]
        
        >>> idx = word2idx[example_word]
        >>> idx2word[idx]
        '#!/usr/bin/env'
        """

        word2idx = dict([[w,i] for i,w in enumerate(self.words(**kwargs))])
        idx2word = dict(enumerate(self.words(**kwargs)))
        return [idx2word, word2idx]
    
    def __meta__(self):
        """
        >>> Corpus(file="./corpus/__init__.py").__meta__()
        {'file': './corpus/__init__.py', 'chars': 4736, 'chars_unique': 32, 'words': 540, 'words_unique': 86}
        """

        m = self._meta
        m.update({"chars": len(self.corpus),
                  "chars_unique": len(self.chars()),
                  "words": len(self.word_list()),
                  "words_unique": len(set(self.words()))})
        return m

    def __repr__(self):
        """
        >>> print(Corpus(file="./corpus/__init__.py"))
        ['', 'usr', 'bin', 'env', 'python', 'coding', 'utf', 'import', 're', 'def', '…', 'doctest', 'print', 'doctest', 'testmod', '']
        """
        w = self.word_list()
        if len(w) < 15:
            return str(w)
        else:
            return str(w[:10]+ ['…'] + w[-5:])


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())