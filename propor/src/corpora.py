from collections import defaultdict
from corpus import Corpus

class Corpora:
    def __init__(self, corpus_files):
        self._type = ""
        self._corpus_list = self.create_corpus_list(corpus_files)
        
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