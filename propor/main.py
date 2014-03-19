#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import nltk
from copy import deepcopy

"""
Alessandro: Usando as listas de frequência (que a Marcely já calculou) gerar listas: 
    (1) com todas as palavras (lemmas) anotados com: 
        [ x ]frequência nos corpus simples, 
        [ x ]freq nos corpus complexos, 
        [  ]freq total, 
        [  ]probabilidade de simples (freq simples/freq total), 
        [  ]prob de complexo (freq complexo/freq total);

    (2) lista das palavras que ocorrem em textos simples e não em complexos e 
        as que ocorrem em complexos e não em simples (colocando ao lado da palavra 
        o grupo a que pertence);

    (3) para cada documento transformar em um vetor de features (cada feature da lista de 
    features calcular a soma dos valores de features de cada palavra / número de palavras 
    do documento).
    
    Lista de Features: número de synsets; freq total (todos os corpus); 
    freq nos corpus simples; freq nos corpus complexos; tamanho da palavra; 
    freq da palavra no childes.
"""

PORTER = 1
WORD_NET = 2
RSLP = 3

def lemmatize(tokens, stemmer):
    """ Lemmatizes each token in a list of tokens.
    
        stemmer is the used algorithm. For english use PORTER or WORD_NET,
        for portuguese use RSLP (Viviane Orengo approach).
    """
    if stemmer == PORTER:
        porter = nltk.PorterStemmer()
        lemmas = [porter.stem(t) for t in tokens]
    elif stemmer == WORD_NET:
        wnl = nltk.WordNetLemmatizer()
        lemmas = [wnl.lemmatize(t) for t in tokens]
    else:
        rslp = nltk.RSLPStemmer()
        lemmas = [rslp.stem(token.decode('utf8')) for token in tokens]

    return lemmas

def read_corpora(filename):
    """ Open the corpora file and return a list of lists of the tokens with their frequency. 
    """
    # Open the corpora and input the lemmas in the dictionary
    with open(filename) as f:
        content = f.read()
        tokens_list = []
        for line in content.splitlines():
            token_freq = line.split()
            tokens_list.append([token_freq[0].decode('utf8'),int(token_freq[1])])

    return tokens_list

def construct_frequency_dict(filenames):
    """ Construct a new dictionary with all lemmas for a set of corpora.
    """
    freq_dict = dict()

    for filename in filenames:
        tokens_list = read_corpora(filename)
        for t in tokens_list:
            if freq_dict.has_key(t[0]):
                freq_dict[t[0]] += t[1]
            else:
                freq_dict[t[0]] = t[1]

    return deepcopy(freq_dict)

#http://stackoverflow.com/questions/17403371/how-can-i-fix-valueerror-too-many-values-to-unpack-in-python
def merge_dict(dicta, dictb):
    """ Merge two dictionaries that contains tokens and frequency, returning a new dictionary.
    """
    freq_dict = deepcopy(dicta)

    for key,value in dictb.items():
        if freq_dict.has_key(key):
            freq_dict[key] += value
        else:
            freq_dict[key] = value

    return deepcopy(freq_dict)

def main():
    simple_corpora = ["corpora/Corpora_DG/Corpora_DG.freq", "corpora/Corpora_infantil/Corpora_infantil.freq"]
    complex_corpora = ["corpora/Corpora_machado/Corpora_machado.freq", "corpora/Corpora_Europarl/Corpora_Europarl.freq"]

    #corpora_file = ""
    #corpora_file = open(filename)

    # Keeps the lemma and frequency for simple corpora: Childes, DG, Folha SP, infantil, ZH
    simple_dict = construct_frequency_dict(simple_corpora)
    # Keeps the lemma and frequency for complex corpora: Machado, Europarl
    complex_dict = construct_frequency_dict(complex_corpora)
    # Keeps the lemma and frequency for all corpora
    total_dict = merge_dict(simple_dict, complex_dict)
    print len(simple_dict)
    print len(complex_dict)
    print len(total_dict)

    # print ordered dict
    #for key in sorted(mydict.iterkeys()):
    #    print "%s: %s" % (key, mydict[key])

    #sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
    #tokens = nltk.word_tokenize(sentence)


if __name__ == "__main__":
    main()
    exit()