
class Word:
    def __init__(self, corpus_name, lemma, pos, frequency, synstets):
        self._corpus_name = corpus_name
        self._lemma = lemma
        self._pos = pos
        self._frequency = frequency
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
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    @property
    def synstets(self):
        return self._synstets
    
    @synstets.setter
    def synstets(self, synstets):
        self._synstets = synstets

    def synstets_number(self):
        return len(self.synstets)