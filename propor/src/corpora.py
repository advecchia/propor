from collections import defaultdict
from corpus import Corpus, CompressedCorpus

ARFF = 1
CSV= 2

class Corpora:
    """ A class for defining a corpora (a set of complete texts) and their 
    correlated methods.
    """
    def __init__(self, corpus_files):
        # A general type of complexity for the corpora: S for simple and C for complex
        self._corpora_type = ""
        # A list containing all the corpus for this corpora
        self._corpus_list = []
        self._corpora = self.create_corpus_list(corpus_files)
        self._compressed_corpus = CompressedCorpus()
        self._compressed_corpus.compress_corpora(self.corpus_list)
        # A path for an external memory file
        self._memory_file = ""
        # The corpora size
        self._corpora_size = self.calculate_corpora_size()

    @property
    def corpora_type(self):
        return self._corpora_type
    
    @corpora_type.setter
    def corpora_type(self, corpora_type):
        self._corpora_type = corpora_type

    @property
    def corpus_list(self):
        return self._corpus_list
    
    @corpus_list.setter
    def corpus_list(self, corpus_list):
        self._corpus_list = corpus_list

    def add_corpus(self, corpus):
        self._corpus_list.append(corpus)

    @property
    def corpora(self):
        return self._corpora
    
    @corpora.setter
    def corpora(self, corpora):
        self._corpora = corpora

    @property
    def memory_file(self):
        return self._memory_file
    
    @memory_file.setter
    def memory_file(self, memory_file):
        self._memory_file = memory_file

    @property
    def corpora_size(self):
        return self._corpora_size
    
    @corpora_size.setter
    def corpora_size(self, corpora_size):
        self._corpora_size = corpora_size

    def create_corpus_list(self, corpus_files):
        """ Construct a new dictionary with all lemmas for a set of corpora.
        """
        freq_dict = defaultdict(dict)

        for corpus_file in corpus_files:
            corpus_name = corpus_file.split("/")[-1]
            corpus = Corpus(corpus_name, corpus_file)
            self.add_corpus(corpus)

            for word in corpus.word_list:
                lemma = word.lemma
                pos = word.pos
                if freq_dict.has_key((lemma,pos)):
                    freq_dict[lemma][pos].add_corpus_name(word.corpus_name)
                    freq_dict[lemma][pos].add_corpus_frequency(word.corpus_frequency)
                    freq_dict[lemma][pos].add_synstets(word.synstets)
                else:
                    freq_dict[lemma][pos] = word

            self.calculate_relative_probability()

        return deepcopy(freq_dict)

    def calculate_corpora_size(self):
        return reduce(lambda a,b: a + b, [c.corpus_size for c in self.corpus_list])

    def calculate_relative_probability(self):
        map(lambda w: w.calculate_relative_probability(self.corpora_size),
            self._corpora)

    def calculate_tf_idf(self):
        pass

    #def save_output(simple_dict, complex_dict, total_dict, simple_relative, complex_relative, simple_prob, complex_prob, simple_words, complex_words, childes_dict, brwac_dict):
    def save_output(self, type=CSV, separator=","):
        out = []
        if type == ARFF:
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

        elif type == CSV:
            attributes = ["lemma", "pos", "word_size", "simple_frequency", 
                          "complex_frequency", "total_frequency", "simple_probability",
                          "complex_probability", "simple_relative", "complex_relative",
                          "childes_frequency", "brwac_frequency", "number_of_synstets", "class"]

        with open('output/saida.csv', 'w+') as f:
            f.write(separator.join(attributes))
            f.write("\n")
     
            #for key in sorted(total_dict.keys()):
            for (lemma, pos) in self.corpora.keys():

                # lemma
                out.append(str(lemma))
    
                # pos
                out.append(str(pos))
    
                # word_size 
                out.append(str(self.corpora[lemma][pos].size))

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
    
                f.write(separator.join(out))
                f.write("\n")
                out = []
    
        print "Arquivo salvo com sucesso na pasta output"

# Methods for pickle
#     def load_qtable(self, qtables):
#         """ Take the saved data for traffic light qlearning algoritm and load it
#         into the traffic light.
#         """
#         for qtable in qtables:
#             if qtable["id"] == self.id:
#                 self.qtable.states = qtable["states"]
#                 self.qtable.actions = qtable["actions"]
#                 self.qtable.table = qtable["table"]
# 
#     def save_qtable(self):
#         """ Return a dict that contains the important data for qlearning algorithm.
#         The dict contains an id, the states, the actions and the qtable with rewards.
#         """
#         d = dict()
#         d["id"] = self.id
#         d["states"] = self.qtable.states
#         d["actions"] = self.qtable.actions
#         d["table"] = self.qtable.table
#         return d