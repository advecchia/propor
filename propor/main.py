#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import nltk
from copy import deepcopy

"""
Alessandro: Usando as listas de frequência (que a Marcely já calculou) gerar listas: 
    (1) com todas as palavras (lemmas) anotados com: 
        [ x ]frequência nos corpus simples, 
        [ x ]freq nos corpus complexos, 
        [ x ]freq total, 
        [ x ]probabilidade de simples (freq simples/freq total), 
        [ x ]prob de complexo (freq complexo/freq total);

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

def save_output(simple_dict, complex_dict, total_dict, simple_prob, complex_prob, simple_words, complex_words):
    """ Take all data and save a file within.
    """
    out = []
    with open('output/saida.csv', 'w+') as f:
        f.write("lemma \t tamanho \t freq_simples \t freq_complexo \t freq_total \t prob_simples \t prob_complexo \t tipo \n")
 
        for key in sorted(total_dict.keys()):
            out.append(str(key)) 
            out.append(str(len(key)))

            if simple_dict.has_key(key):
                out.append(str(simple_dict[key]))
            else:
                out.append(str(0))
    
            if complex_dict.has_key(key):
                out.append(str(complex_dict[key]))
            else:
                out.append(str(0))
    
            out.append(str(total_dict[key]))
    
            if simple_prob.has_key(key):
                out.append(str(simple_prob[key]))
            else:
                out.append(str(0))
    
            if complex_prob.has_key(key):
                out.append(str(complex_prob[key]))
            else:
                out.append(str(0))

            if key in simple_words:
                out.append("S")
            elif key in complex_words:
                out.append("C")

            f.write("\t".join(out))
            f.write("\n")
            
            out = []

    print "Arquivo salvo com sucesso na pasta output"

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

def construct_probability_dict(dicta, dictt):
    """ Take two dictionaries of word frequencies and construct a new dictionary 
        with probability for the containing words.
        
        dicta contains the choice word frequencies
        dictt contains the total word frequencies
    """
    prob_dict = deepcopy(dicta)

    for key in prob_dict.keys():
        prob_dict[key] = prob_dict[key]/float(dictt[key])

    return prob_dict

def construct_not_containing_words(dicta, dictb):
    """ Search words in a dictionary that are not contained in another dict. 
        
        dicta the searched words
        dictb the another dictionary
    """
    words = []

    for key in dicta.keys():
        if not dictb.has_key(key):
            words.append(key)

    return words

def main():
    simple_corpora = ["corpora/Corpora_DG/Corpora_DG.freq", "corpora/Corpora_infantil/Corpora_infantil.freq", "corpora/Corpora_ZH/zh.natural.corpus.freq"]
    complex_corpora = ["corpora/Corpora_machado/Corpora_machado.freq", "corpora/Corpora_Europarl/Corpora_Europarl.freq", "corpora/Corpora_ZH/zh.normal.corpus.freq"]

    # Keeps the lemma and frequency for simple corpora: Childes, DG, infantil, ZH simplificado
    simple_dict = construct_frequency_dict(simple_corpora)
    # Keeps the lemma and frequency for complex corpora: Machado, Europarl, Folha SP, ZH normal
    complex_dict = construct_frequency_dict(complex_corpora)
    # Keeps the lemma and frequency for all corpora
    total_dict = merge_dict(simple_dict, complex_dict)
    
    # Keeps the simple lemma and their probability to stand in total corpora
    simple_prob = construct_probability_dict(simple_dict, total_dict)
    # Keeps the complex lemma and their probability to stand in total corpora
    complex_prob = construct_probability_dict(complex_dict, total_dict)

    # Keeps the simple lemma that not exists in complex corpora
    simple_words = construct_not_containing_words(simple_dict, complex_dict)
    # Keeps the complex lemma that not exists in simple corpora
    complex_words = construct_not_containing_words(complex_dict, simple_dict)

    print "simple_dict", len(simple_dict)
    print "complex_dict", len(complex_dict)
    print "total_dict", len(total_dict)
    
    print "simple_prob", len(simple_prob)
    print "complex_prob", len(complex_prob)
    
    print "simple_words", len(simple_words)
    print "complex_words", len(complex_words)
    save_output(simple_dict, complex_dict, total_dict, simple_prob, complex_prob, simple_words, complex_words)

if __name__ == "__main__":
    main()
    exit()