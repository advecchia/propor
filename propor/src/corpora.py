from collections import defaultdict
from corpus import Corpus, CompressedCorpus

class Corpora:
    """ A class for defining a corpora (a set of complete texts) and their 
    correlated methods.
    """
    def __init__(self, corpus_files):
        # A general type of complexity for the corpora: S for simple and C for complex
        self._corpora_type = ""
        # A list containing all the corpus for this corpora
        self._corpus_list = self.create_corpus_list(corpus_files)
        self._compressed_corpus = CompressedCorpus()
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
            Corpus(corpus_name, corpus_file)

            # lemma pos freq || #synstets synstets_cod
            tokens_list = read_corpora(corpus_file)
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

    def calculate_corpora_size(self):
        return reduce(lambda a,b: a + b, [c.corpus_size for c in self.corpus_list])

    def calculate_relative_probability(self):
        map(lambda w: w.calculate_relative_probability(self.corpora_size),
            self._word_list)

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