#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import nltk
from collections import OrderedDict

def main():
    corpora_file = open("corpora/Corpora_DG/Corpora_DG.freq")
    freq_dict = dict()

    # Take the lemma and frequency
    for line in corpora_file:
        line = line.decode('utf8').split()
        freq_dict[line[0]] = line[1]
    print len(freq_dict)
    for lemma, freq in freq_dict.items():
        print lemma, freq
    #sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
    #tokens = nltk.word_tokenize(sentence)
    #print tokens

if __name__ == "__main__":
    main()