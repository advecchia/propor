
class Word:
    """ A class for defining one word/lemma and their correlated methods.
    """
    def __init__(self, corpus_name, lemma, pos, corpus_frequency, synstets):
        # The name of the corpus that originated this lemma
        self._corpus_name = corpus_name
        # The lemma of the based word
        self._lemma = lemma
        # The size of the lemma
        self._size = len(self.lemma)
        # The part-of-speech of the based word
        self._pos = pos
        # The frequency of this lemma in the corpus
        self._corpus_frequency = corpus_frequency
        # The probability of this lemma over their corpora (eg. over the simple corpora)
        self._relative_probability = 0
        # The probability of this lemma over the all corporas
        self._corpora_probability = 0
        # A set of synonyms
        self._synstets = synstets

    @property
    def corpus_name(self):
        return self._corpus_name
    
    @corpus_name.setter
    def corpus_name(self, corpus_name):
        self._corpus_name = corpus_name

    @property
    def lemma(self):
        return self._lemma
    
    @lemma.setter
    def lemma(self, lemma):
        self._lemma = lemma

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def corpus_frequency(self):
        return self._corpus_frequency
    
    @corpus_frequency.setter
    def corpus_frequency(self, corpus_frequency):
        self._corpus_frequency = corpus_frequency

    @property
    def relative_probability(self):
        return self._relative_probability
    
    @relative_probability.setter
    def relative_probability(self, relative_probability):
        self._relative_probability = relative_probability

    def calculate_relative_probability(self, corpora_size):
        """ Calculate the probability of this lemma over their corpora.
        (eg. simple corpora)
        """
        self.relative_probability = self.corpus_frequency/float(corpora_size)

    @property
    def corpora_probability(self):
        return self._corpora_probability

    @corpora_probability.setter
    def corpora_probability(self, corpora_probability):
        self._corpora_probability = corpora_probability

    def calculate_corpora_probability(self, total_corpora_size):
        """ Calculate the probability of this lemma over the all corpora.
        (eg. simple and complex corpora)
        """
        self.corpora_probability = self.corpus_frequency/float(total_corpora_size)

    @property
    def synstets(self):
        return self._synstets
    
    @synstets.setter
    def synstets(self, synstets):
        self._synstets = synstets

    def synstets_number(self):
        return len(self.synstets)