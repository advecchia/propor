from word import Word
from collections import defaultdict

class Corpus:
    """ A class for defining a corpus (a complete text) and their correlated methods.
    """
    def __init__(self, name, word_list_file):
        # The corpus name
        self._name = name
        # A list containing all the lemmas for this corpus
        self._word_list = self.create_word_list(word_list_file)
        # The corpus size
        self._corpus_size = self.calculate_corpus_size()

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def word_list(self):
        return self._word_list
    
    @word_list.setter
    def word_list(self, word_list):
        self._word_list = word_list

    @property
    def corpus_size(self):
        return self._corpus_size

    @corpus_size.setter
    def corpus_size(self, corpus_size):
        self._corpus_size = corpus_size

    def create_word_list(self, word_list_file):
        """ Open the corpora file and return a list of lists of the tokens with 
        their frequency. 
        """
        traduction_table = {"NON":"N","ADJ":"A","ADV":"R","VFIN":"V","INF":"V",
                            "PCP":"V","GER":"V"}

        # Open the corpus and input the lemmas in the dictionary
        with open(word_list_file) as f:
            content = f.read()
            word_list = defaultdict(dict)
            for line in content.splitlines():
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

                    lemma = lemma.decode('utf8')

                    word = Word(self.name, lemma, pos, frequency, synstets)
                    word_list[lemma][pos] = word
                    #word_list.append(word)

        return word_list

    def calculate_corpus_size(self):
        return reduce(lambda a,b: a + b, [w.corpus_frequency for w in self.word_list])

    def calculate_number_of_lemmas(self):
        return len(self.word_list)

    def get_word_by_lemma(self, lemma):
        return filter(lambda w: w.lemma==lemma, self.word_list)

    def get_word_by_lemma_and_pos(self, lemma, pos):
        #return filter(lambda w: w.lemma==lemma and w.pos==pos, self._word_list)
        return filter(lambda w: w.lemma==lemma and w.pos==pos, self.get_word_by_lemma(lemma))

class CompressedCorpus:
    """ A class that compress a set of corpus in a big corpus.
    """
    def __init__(self):
        # The original names of the corpus
        self._names = []
        # A dict containing all the lemmas and pos for all corpus
        self._word_list = defaultdict(dict)
        # The size of the corpus
        self._corpus_size = 0

    @property
    def names(self):
        return self._names
    
    @names.setter
    def names(self, name):
        self._names.append(name)

    @property
    def word_list(self):
        return self._word_list
    
    @word_list.setter
    def word_list(self, word_list):
        self._word_list = word_list

    @property
    def corpus_size(self):
        return self._corpus_size

    @corpus_size.setter
    def corpus_size(self, corpus_size):
        self._corpus_size += corpus_size

    def add_word(self, word):
        """ Adds a word to the word list
        """
        self.word_list.append(word)

    def compress_corpus(self, corpus):
        """ Take a corpus and concatenate with their data (word list)
        """
        self.names = corpus.name
        self.corpus_size = corpus.corpus_size
        #ilp = [(index, word.lemma, word.pos) for (index, word) in enumerate(self.word_list)]
        #for word in corpus.word_list:
        #    [item for item in ilp if word.lemma == item[1] and word.pos == item[2]]
        #    if word.lemma == item[1] and word.pos == item[2] for item in ilp:
        #        i = self.word_list[index]
        #
        #    else:
        #        self.word_list.add_word(word)
        

    def compress_corpora(self, corpora_list):
        for corpus in corpora_list:
            self.compress_corpus(corpus)

    def calculate_number_of_lemmas(self):
        return len(self.word_list)

    def get_word_by_lemma(self, lemma):
        return filter(lambda w: w.lemma==lemma, self.word_list)

    def get_word_by_lemma_and_pos(self, lemma, pos):
        #return filter(lambda w: w.lemma==lemma and w.pos==pos, self._word_list)
        return filter(lambda w: w.lemma==lemma and w.pos==pos, self.get_word_by_lemma(lemma))