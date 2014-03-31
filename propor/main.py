#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from copy import deepcopy
from collections import defaultdict

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


def read_corpora(filename):
    """ Open the corpora file and return a list of lists of the tokens with their frequency. 
    """
    # Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
    traduction_table = {"NON":"N","ADJ":"A","ADV":"R",
                        "VFIN":"V","INF":"V","PCP":"V","GER":"V"}

    # Open the corpora and input the lemmas in the dictionary
    with open(filename) as f:
        content = f.read()
        tokens_list = []
        for line in content.splitlines():
            token = line.split()

            # lemma pos freq #synstets synstets_cod
            if traduction_table.has_key(token[1]):
                token[1] = traduction_table[token[1]]

            if len(token) > 3:
                tokens_list.append([token[0].decode('utf8'),token[1],int(token[2]),int(token[3]),token[4]])
            else:
                if len(token) == 2:
                    pass
                else:
                    tokens_list.append([token[0].decode('utf8'),token[1],int(token[2])])

    return tokens_list

def construct_frequency_dict(filenames):
    """ Construct a new dictionary with all lemmas for a set of corpora.
    """
    freq_dict = defaultdict(dict)

    for filename in filenames:
        # lemma pos freq || #synstets synstets_cod
        tokens_list = read_corpora(filename)
        for t in tokens_list:
            if freq_dict.has_key((t[0], t[1])):
                    l = freq_dict[t[0], t[1]]
                    l[0] += t[2:][0]
                    l[1] = freq_dict[t[0], t[1]][1]
                    l[2] = l[2].union(set(t[2:][2].split("#")))
                    freq_dict[t[0], t[1]] = l
            else:
                l = []
                l.append(t[2:][0])
                l.append(t[2:][1])
                l.append(set(t[2:][2].split("#")))
                freq_dict[t[0], t[1]] = l

    return deepcopy(freq_dict)

def construct_frequency_dict_baseline(filenames):
    """ Construct a new dictionary with all lemmas for a set of corpora.
    """
    freq_dict = defaultdict(dict)

    for filename in filenames:
        # lemma pos freq
        tokens_list = read_corpora(filename)
        for t in tokens_list:
            if freq_dict.has_key((t[0], t[1])):
                    freq_dict[t[0], t[1]] = +t[2]
            else:
                freq_dict[t[0], t[1]] = t[2]

    return deepcopy(freq_dict)

def merge_dict(dicta, dictb):
    """ Merge two dictionaries that contains tokens and frequency, returning a new dictionary.
    """
    freq_dict = deepcopy(dicta)

    for key,value in dictb.items():
        if freq_dict.has_key(key):
            l = freq_dict[key]
            l[0] += value[0]
            l[1] = freq_dict[key][1]
            l[2] = l[2].union(value[2])
            freq_dict[key] = l
        else:
            freq_dict[key] = value

    return deepcopy(freq_dict)

def construct_probability_dict(dicta, size):
    """ Take two dictionaries of word frequencies and construct a new dictionary 
        with probability for the containing words.
        
        dicta contains the choice word frequencies
        
        dictt contains the total word frequencies
    """
    prob_dict = defaultdict(dict)

    for key in dicta.keys():
        prob_dict[key] = dicta[key][0]/float(size)

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

def save_output(simple_dict, complex_dict, total_dict, simple_relative, complex_relative, simple_prob, complex_prob, simple_words, complex_words, childes_dict, brwac_dict):
    """ Take all data and save a file within.
    """
    out = []
    attributes = ["lemma", "pos", "word_size", "simple_frequency", 
                  "complex_frequency", "total_frequency", "simple_probability",
                  "complex_probability", "simple_relative", "complex_relative",
                  "childes_frequency", "brwac_frequency", "number_of_synstets", "class"]

    with open('output/saida.csv', 'w+') as f:
        f.write(",".join(attributes))
        f.write("\n")
 
        for key in sorted(total_dict.keys()):

            # lemma
            out.append(str(key[0]))

            # pos
            out.append(str(key[1]))

            # word_size 
            out.append(str(len(key[0])))

            # simple_frequency
            if simple_dict.has_key(key):
                out.append(str(simple_dict[key][0]))
            else:
                out.append(str(0))
            
            # complex_frequency
            if complex_dict.has_key(key):
                out.append(str(complex_dict[key][0]))
            else:
                out.append(str(0))

            # total_frequency
            out.append(str(total_dict[key][0]))
            
            # simple_probability
            if simple_prob.has_key(key):
                out.append(str(simple_prob[key]))
            else:
                out.append(str(0))

            # complex_probability
            if complex_prob.has_key(key):
                out.append(str(complex_prob[key]))
            else:
                out.append(str(0))

            # simple_relative
            if simple_relative.has_key(key):
                out.append(str(simple_relative[key]))
            else:
                out.append(str(0))

            # complex_relative
            if complex_relative.has_key(key):
                out.append(str(complex_relative[key]))
            else:
                out.append(str(0))

            # childes_frequency
            if childes_dict.has_key(key):
                out.append(str(childes_dict[key]))
            else:
                out.append(str(0))
            
            # brwac_frequency
            if brwac_dict.has_key(key):
                out.append(str(brwac_dict[key]))
            else:
                out.append(str(0))

            # number_of_synstets
            out.append(str(total_dict[key][1]))

            # class
            if key in simple_words:
                out.append("S")
            elif key in complex_words:
                out.append("C")
            else:
                out.append("N")

            f.write(",".join(out))
            f.write("\n")
            out = []

    print "Arquivo salvo com sucesso na pasta output"

def save_output_arff(simple_dict, complex_dict, total_dict, simple_relative, complex_relative, simple_prob, complex_prob, simple_words, complex_words, childes_dict, brwac_dict):
    """ Take all data and save a file within.
    """
    out = []
    attributes = """
    % 1. Title: Simple and Complex corpora analisys
    %
    % 2. Source:
    %    (a) Creator: Vecchia, Alessandro D.
    %    (b) Donor: NLP Group - INF - UFRGS
    %    (c) Date: April, 2014
    %
    % 3. Corpora:
    %    (a) Simple: Diario Gaucho (30 + 70), Infantil, Zero Hora simplificado
    %    (b) Complex: Machado, Europarl, Folha de São Paulo, Zero Hora
    %    (c) Baseline: Childes, BrWac
    %
    % word lemma
    @ATTRIBUTE lemma string
    % part-of-speech
    @ATTRIBUTE pos string
    % word length
    @ATTRIBUTE word_size NUMERIC
    % word frequency in all simple corpora
    @ATTRIBUTE simple_frequency NUMERIC
    % word frequency in all complex corpora
    @ATTRIBUTE complex_frequency NUMERIC
    % word frequency in all corpora
    @ATTRIBUTE total_frequency NUMERIC
    % probability of the simple word over total corpora
    @ATTRIBUTE simple_probability NUMERIC
    % probability of the complex word over total corpora
    @ATTRIBUTE complex_probability NUMERIC
    % probability of the simple word over simple corpora
    @ATTRIBUTE simple_relative NUMERIC
    % probability of the complex word over complex corpora
    @ATTRIBUTE complex_relative NUMERIC
    % word frequency in Childes corpora (baseline)
    @ATTRIBUTE childes_frequency NUMERIC
    % word frequency in brWack corpora (baseline)
    @ATTRIBUTE brwac_frequency NUMERIC
    % number of synstets for the lemma
    @ATTRIBUTE number_of_synstets NUMERIC
    % class identification: C for complex word, S for simple word, N for neutral word
    @ATTRIBUTE class {C,S,N}
    @DATA"""

    with open('output/saida.arff', 'w+') as f:
        f.write(attributes)

        for key in sorted(total_dict.keys()):

            # lemma
            out.append(str(key[0]))

            # pos
            out.append(str(key[1]))

            # word_size 
            out.append(str(len(key[0])))

            # simple_frequency
            if simple_dict.has_key(key):
                out.append(str(simple_dict[key][0]))
            else:
                out.append(str(0))
            
            # complex_frequency
            if complex_dict.has_key(key):
                out.append(str(complex_dict[key][0]))
            else:
                out.append(str(0))

            # total_frequency
            out.append(str(total_dict[key][0]))
            
            # simple_probability
            if simple_prob.has_key(key):
                out.append(str(simple_prob[key]))
            else:
                out.append(str(0))

            # complex_probability
            if complex_prob.has_key(key):
                out.append(str(complex_prob[key]))
            else:
                out.append(str(0))

            # simple_relative
            if simple_relative.has_key(key):
                out.append(str(simple_relative[key]))
            else:
                out.append(str(0))

            # complex_relative
            if complex_relative.has_key(key):
                out.append(str(complex_relative[key]))
            else:
                out.append(str(0))

            # childes_frequency
            if childes_dict.has_key(key):
                out.append(str(childes_dict[key]))
            else:
                out.append(str(0))
            
            # brwac_frequency
            if brwac_dict.has_key(key):
                out.append(str(brwac_dict[key]))
            else:
                out.append(str(0))

            # number_of_synstets
            out.append(str(total_dict[key][1]))

            # class
            if key in simple_words:
                out.append("S")
            elif key in complex_words:
                out.append("C")
            else:
                out.append("N")

            f.write(",".join(out))
            f.write("\n")
            out = []

    print "Arquivo salvo com sucesso na pasta output"

def main():
    simple_corpora = ["corpora/simple/dg30.txt","corpora/simple/dg70.txt","corpora/simple/infantil.txt","corpora/simple/zh.txt"]
    complex_corpora = ["corpora/complex/europarl.txt","corpora/complex/folha.txt","corpora/complex/machado.txt","corpora/complex/zh.txt"]
    #simple_corpora = ["corpora/simple/dg30.txt"]
    #complex_corpora = ["corpora/complex/machado.txt"]
    brwac_corpora = ["corpora/baseline/brwac.txt"]
    childes_corpora = ["corpora/baseline/childes.txt"]

    # Keeps the lemma and frequency for simple corpora: DG (30 + 70), infantil, ZH simplificado
    simple_dict = construct_frequency_dict(simple_corpora)
    # Keeps the lemma and frequency for complex corpora: Machado, Europarl, Folha SP, ZH normal
    complex_dict = construct_frequency_dict(complex_corpora)
    # Keeps the lemma and frequency for all corpora
    total_dict = merge_dict(simple_dict, complex_dict)
    # Keeps the lemma and frequency for baseline corpora: BrWac, Childes
    brwac_dict = construct_frequency_dict_baseline(brwac_corpora)
    childes_dict = construct_frequency_dict_baseline(childes_corpora)

    # Keeps the simple lemma and their probability to stand in total corpora
    simple_prob = construct_probability_dict(simple_dict, len(total_dict))
    # Keeps the complex lemma and their probability to stand in total corpora
    complex_prob = construct_probability_dict(complex_dict, len(total_dict))

    # Keeps the simple lemma and their probability to stand in total corpora
    simple_relative = construct_probability_dict(simple_dict, len(simple_dict))
    # Keeps the complex lemma and their probability to stand in total corpora
    complex_relative = construct_probability_dict(complex_dict, len(complex_dict))

    # Keeps the simple lemma that not exists in complex corpora
    simple_words = construct_not_containing_words(simple_dict, complex_dict)
    # Keeps the complex lemma that not exists in simple corpora
    complex_words = construct_not_containing_words(complex_dict, simple_dict)

    print "simple_dict", len(simple_dict)
    print "complex_dict", len(complex_dict)
    print "total_dict", len(total_dict)
    print "childes_dict", len(childes_dict)
    print "brwac_dict", len(brwac_dict)

    print "simple_prob", len(simple_prob)
    print "complex_prob", len(complex_prob)

    print "simple_relative", len(simple_relative)
    print "complex_relative", len(complex_relative)

    print "simple_words", len(simple_words)
    print "complex_words", len(complex_words)

    save_output(simple_dict, complex_dict, total_dict, simple_relative, complex_relative, simple_prob, complex_prob, simple_words, complex_words, childes_dict, brwac_dict)
    #save_output_arff(simple_dict, complex_dict, total_dict, simple_relative, complex_relative, simple_prob, complex_prob, simple_words, complex_words, childes_dict, brwac_dict)

if __name__ == "__main__":
    main()
    exit()