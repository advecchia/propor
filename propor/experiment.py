"""
Abrir todos os corpus simples e salvar num arquivo
    recalcular a frequencia relativa a esse corpora

Abrir todos os corpus complexos e salvar num arquivo
    recalcular a frequencia relativa a esse corpora

Gerar lista de palavras apenas simples e apenas complexas

Comprimir ambos os arquivos em um chamado total
    recalcular a frequencia relativa a esse corpora
    
    Gerar as classes das palavras
"""

from collections import defaultdict

ARFF = 1
CSV= 2

class Experiment:

    def __init__(self):
        simple_corpora = ["corpora/simple/dg30.txt","corpora/simple/dg70.txt","corpora/simple/infantil.txt","corpora/simple/zh.txt"]
        complex_corpora = ["corpora/complex/europarl.txt","corpora/complex/folha.txt","corpora/complex/machado.txt","corpora/complex/zh.txt"]
        #simple_corpora = ["corpora/simple/dg30.txt"]
        #complex_corpora = ["corpora/complex/machado.txt"]
        total_corpora = ["output/simple_corpora.txt","output/complex_corpora.txt"]

        brwac_corpora = ["corpora/baseline/brwac.txt"]
        childes_corpora = ["corpora/baseline/childes.txt"]

        self.read_and_save_corpora(simple_corpora, "simple_corpora")
        print "Creates simple corpora"
        self.read_and_save_corpora(complex_corpora, "complex_corpora")
        print "Creates complex corpora"
        self.read_and_save_disjoint_words()
        print "Creates simple and complex words list"
        self.read_and_save_total(total_corpora, "total_corpora")
        print "Creates total corpora"

        self.childes = self.read_baseline(childes_corpora)
        print "Reads the baseline: Childes"
        self.brwac = self.read_baseline(brwac_corpora)
        print "Reads the baseline: brWac"

        self.save_output(ARFF)
        print "Saving arff output"
        self.save_output(CSV)
        print "Saving csv output"

    def save_output(self, out_type):
        
        simple_words = set()
        with open('output/simple_words.txt') as f:
            for line in f:
                token = line.split()
                lemma, pos = token[:2]
                simple_words.add((lemma, pos))

        complex_words = set()
        with open('output/complex_words.txt') as f:
            for line in f:
                token = line.split()
                lemma, pos = token[:2]
                complex_words.add((lemma, pos))

        simple_corpora = defaultdict(dict)
        with open("output/simple_corpora.txt") as f:
            for line in f:
                token = line.split()
                lemma, pos, frequency, probability = token[:4]
                simple_corpora[lemma][pos] = [int(frequency), float(probability)]

        complex_corpora = defaultdict(dict)
        with open("output/complex_corpora.txt") as f:
            for line in f:
                token = line.split()
                lemma, pos, frequency, probability = token[:4]
                complex_corpora[lemma][pos] = [int(frequency), float(probability)]

        total_corpora = defaultdict(dict)
        total_corpora_size = 0
        with open("output/total_corpora.txt") as f:
            for line in f:
                token = line.split()
                lemma, pos, frequency, probability, synstets_num, synstets = token
                synstets = set(synstets.split("#"))
                total_corpora[lemma][pos] = [int(frequency), float(probability), int(synstets_num), synstets]
                total_corpora_size += int(frequency)

        total_corpora_size = float(total_corpora_size)

        file_out = "txt"
        if out_type == ARFF:
            attributes = ["% 1. Title: Simple and Complex corpora analisys"
            ,"%"
            ,"% 2. Source:"
            ,"%    (a) Creator: Vecchia, Alessandro D."
            ,"%    (b) Donor: NLP Group - INF - UFRGS"
            ,"%    (c) Date: April, 2014"
            ,"%"
            ,"% 3. Corpora:"
            ,"%    (a) Simple: Diario Gaucho (30 + 70), Infantil, Zero Hora simplificado"
            ,"%    (b) Complex: Machado, Europarl, Folha de Sao Paulo, Zero Hora"
            ,"%    (c) Baseline: Childes, BrWac"
            ,"%"
            ,"% word lemma"
            ,"@ATTRIBUTE lemma string"
            ,"% part-of-speech"
            ,"@ATTRIBUTE pos string"
            ,"% word length"
            ,"@ATTRIBUTE word_size NUMERIC"
            ,"% word frequency in all simple corpora"
            ,"@ATTRIBUTE simple_frequency NUMERIC"
            ,"% word frequency in all complex corpora"
            ,"@ATTRIBUTE complex_frequency NUMERIC"
            ,"% word frequency in all corpora"
            ,"@ATTRIBUTE total_frequency NUMERIC"
            ,"% probability of the simple word over total corpora"
            ,"@ATTRIBUTE simple_probability NUMERIC"
            ,"% probability of the complex word over total corpora"
            ,"@ATTRIBUTE complex_probability NUMERIC"
            ,"% probability of the simple word over simple corpora"
            ,"@ATTRIBUTE simple_relative NUMERIC"
            ,"% probability of the complex word over complex corpora"
            ,"@ATTRIBUTE complex_relative NUMERIC"
            ,"% ratio of simple probability over simple and complex probability"
            ,"@ATTRIBUTE simple_probability_ratio NUMERIC"
            ,"% ratio of complex probability over simple and complex probability"
            ,"@ATTRIBUTE complex_probability_ratio NUMERIC"
            ,"% word frequency in Childes corpora (baseline)"
            ,"@ATTRIBUTE childes_frequency NUMERIC"
            ,"% word frequency in brWack corpora (baseline)"
            ,"@ATTRIBUTE brwac_frequency NUMERIC"
            ,"% number of synstets for the lemma"
            ,"@ATTRIBUTE number_of_synstets NUMERIC"
            ,"% class identification: C for complex word, S for simple word, N for neutral word"
            ,"@ATTRIBUTE class {C,S,N}"
            ,"@DATA"]
            attributes = "\n".join(attributes)
            file_out = "arff"

        elif out_type == CSV:
            attributes = ["lemma", "pos", "word_size", "simple_frequency", 
                          "complex_frequency", "total_frequency", "simple_probability",
                          "complex_probability", "simple_relative", "complex_relative",
                          "simple_probability_ratio","complex_probability_ratio",
                          "childes_frequency", "brwac_frequency", "number_of_synstets", "class"]
            attributes = ",".join(attributes)
            file_out = "csv"

        with open('output/saida.'+file_out, 'w+') as f:
            f.write(attributes)
            f.write("\n")

            for lemma in sorted(total_corpora.keys()):
                for pos in sorted(total_corpora[lemma].keys()):

                    total_frequency = total_corpora[lemma][pos][0]
                    if total_frequency <= 5:
                        break

                    word_size = len(lemma)

                    if simple_corpora.has_key(lemma):
                        if simple_corpora[lemma].has_key(pos):
                            simple_frequency = simple_corpora[lemma][pos][0]
                            simple_relative = simple_corpora[lemma][pos][1]
                    else:
                        simple_frequency = 0
                        simple_relative = 0

                    if complex_corpora.has_key(lemma):
                        if complex_corpora[lemma].has_key(pos):
                            complex_frequency = complex_corpora[lemma][pos][0]
                            complex_relative = complex_corpora[lemma][pos][1]
                    else:
                        complex_frequency = 0
                        complex_relative = 0

                    simple_probability = simple_frequency/total_corpora_size
                    complex_probability = complex_frequency/total_corpora_size

                    simple_probability_ratio = simple_probability/(simple_probability+complex_probability)
                    complex_probability_ratio = complex_probability/(simple_probability+complex_probability)

                    if self.childes.has_key(lemma):
                        if self.childes[lemma].has_key(pos):
                            childes_frequency = self.childes[lemma][pos][0]
                    else:
                        childes_frequency = 0 

                    if self.brwac.has_key(lemma):
                        if self.brwac[lemma].has_key(pos):
                            brwac_frequency = self.brwac[lemma][pos][0]
                    else:
                        brwac_frequency = 0

                    number_of_synstets = total_corpora[lemma][pos][2]

                    word_class = "N"
                    if (lemma,pos) in simple_words:
                        word_class = "S"
                    elif (lemma,pos) in complex_words:
                        word_class = "C"

#                    f.write("%s, %s, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %d, %s" % 
#                            lemma, pos, word_size, simple_frequency, complex_frequency, total_frequency, 
#                            simple_probability, complex_probability, simple_relative, complex_relative, 
#                            childes_frequency, brwac_frequency, number_of_synstets, word_class)
                    f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}\n".format(lemma, pos, int(word_size), int(simple_frequency), int(complex_frequency), int(total_frequency), 
                            float(simple_probability), float(complex_probability), float(simple_relative), float(complex_relative), 
                            float(simple_probability_ratio), float(complex_probability_ratio), int(childes_frequency), int(brwac_frequency), int(number_of_synstets), word_class))
                    #f.write("\n")

    def read_and_save_disjoint_words(self):

        with open('output/simple_corpora.txt') as f:
            sw = []
            for line in f:
                token = line.split()
                lemma, pos = token[:2]
                sw.append((lemma, pos))

        with open('output/complex_corpora.txt') as f:
            cw = []
            for line in f:
                token = line.split()
                lemma, pos = token[:2]
                cw.append((lemma, pos))

        sw = set(sw)
        cw = set(cw)
        simple_words = sw - cw
        complex_words = cw - sw

        with open('output/simple_words.txt', 'w+') as f:
            for (lemma, pos) in simple_words:
                #f.write(" ".join([lemma, pos]))
                f.write("{0} {1}\n".format(lemma, pos))
                #f.write("{0} {1}".format(lemma, pos))
                #f.write("\n")
                        #"%s %s" % lemma, pos)
        with open('output/complex_words.txt', 'w+') as f:
            for (lemma, pos) in complex_words:
                f.write("{0} {1}\n".format(lemma, pos))
                #f.write("\n")
                #f.write("%s %s" % lemma, pos)

    def read_baseline(self, filename_list):
        """ Open the corpora file and return a list of lists of the tokens with their frequency. 
        """
        # Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
        traduction_table = {"NON":"N","ADJ":"A","ADV":"R",
                            "VFIN":"V","INF":"V","PCP":"V","GER":"V"}

        corpora = defaultdict(dict)
        corpora_size = 0

        for filename in filename_list:
            # Open the corpora and input the lemmas in the dictionary
            with open(filename) as f:
                for line in f:
                    token = line.split()
                    # lemma pos freq #synstets synstets_cod
                    if len(token) == 2:
                        pass
                    else:
                        if len(token) > 3:
                            lemma, pos, frequency, synstets_num, synstets = token
                            synstets = set(synstets.split("#"))
                        else:
                            lemma, pos, frequency = token
                            synstets_num = 0
                            synstets = set()

                        if traduction_table.has_key(pos):
                            pos = traduction_table[pos]

                        lemma = lemma.replace(',','')
                        lemma = lemma.decode('utf8')
                        corpora_size += int(frequency)

                        if corpora.has_key((lemma,pos)):
                            corpora[lemma][pos][0] +=  int(frequency)
                            corpora[lemma][pos][2] |= synstets
                            corpora[lemma][pos][1] = len(synstets)
                        else:
                            corpora[lemma][pos] = [frequency, synstets_num, synstets]
        return corpora

    def read_and_save_corpora(self, filename_list, output_name):
        """ Open the corpora file and return a list of lists of the tokens with their frequency. 
        """
        # Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
        traduction_table = {"NON":"N","ADJ":"A","ADV":"R",
                            "VFIN":"V","INF":"V","PCP":"V","GER":"V"}

        corpora = defaultdict(dict)
        corpora_size = 0

        for filename in filename_list:
            # Open the corpora and input the lemmas in the dictionary
            with open(filename) as f:
                for line in f:
                    token = line.split()
                    # lemma pos freq #synstets synstets_cod
                    if len(token) == 2:
                        pass
                    else:
                        if len(token) > 3:
                            lemma, pos, frequency, synstets_num, synstets = token
                            synstets = set(synstets.split("#"))
                        else:
                            lemma, pos, frequency = token
                            synstets_num = 0
                            synstets = set()

                        if traduction_table.has_key(pos):
                            pos = traduction_table[pos]

                        lemma = lemma.replace(',','')
                        lemma = lemma.decode('utf8')
                        corpora_size += int(frequency)

                        if corpora.has_key((lemma,pos)):
                            corpora[lemma][pos][0] +=  int(frequency)
                            corpora[lemma][pos][2] |= synstets
                            corpora[lemma][pos][1] = len(synstets)
                        else:
                            corpora[lemma][pos] = [frequency, synstets_num, synstets]

        with open('output/'+output_name+'.txt', 'w+') as f:
            for lemma in sorted(corpora.keys()):
                for pos in sorted(corpora[lemma].keys()):
                    frequency, synstets_num, synstets = corpora[lemma][pos]
                    probability = int(frequency)/float(corpora_size)
                    synstets = "#".join(synstets)
                    #f.write("%s %s %d %f %d %s" % lemma, pos, frequency, probability, synstets_num, synstets)
                    f.write("{0} {1} {2} {3} {4} {5}\n".format(lemma, pos, int(frequency), float(probability), int(synstets_num), synstets))
                    #f.write("\n")

    def read_and_save_total(self, filename_list, output_name):
        """ Open the corpora file and return a list of lists of the tokens with their frequency. 
        """
        corpora = defaultdict(dict)
        corpora_size = 0

        for filename in filename_list:
            # Open the corpora and input the lemmas in the dictionary
            with open(filename) as f:
                for line in f:
                    token = line.split()
                    lemma, pos, frequency, probability, synstets_num, synstets = token
                    synstets = set(synstets.split("#"))
                    corpora_size += int(frequency)

                    if corpora.has_key((lemma,pos)):
                        corpora[lemma][pos][0] +=  int(frequency)
                        corpora[lemma][pos][2] |= synstets
                        corpora[lemma][pos][1] = len(synstets)
                    else:
                        corpora[lemma][pos] = [frequency, synstets_num, synstets]

        with open('output/'+output_name+'.txt', 'w+') as f:
            for lemma in sorted(corpora.keys()):
                for pos in sorted(corpora[lemma].keys()):
                    frequency, synstets_num, synstets = corpora[lemma][pos]
                    probability = int(frequency)/float(corpora_size)
                    synstets = "#".join(synstets)
                    f.write("{0} {1} {2} {3} {4} {5}\n".format(lemma, pos, int(frequency), float(probability), int(synstets_num), synstets))
                    #f.write("%s %s %f %f %d %s" % lemma, pos, frequency, probability, synstets_num, synstets)
                    #f.write("\n")

e = Experiment()
print "end experiment"