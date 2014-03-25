from word import Word

class Corpus:
    def __init__(self, name, word_list_file):
        self._name = name
        self._word_list = self.create_word_list(word_list_file)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    def create_word_list(self, word_list_file):
        """ Open the corpora file and return a list of lists of the tokens with 
        their frequency. 
        """
        traduction_table = {"NON":"N","ADJ":"A","ADV":"R","VFIN":"V","INF":"V",
                            "PCP":"V","GER":"V"}

        # Open the corpus and input the lemmas in the dictionary
        with open(word_list_file) as f:
            content = f.read()
            word_list = []
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

                    word = Word(self.name, lemma.decode('utf8'), pos, frequency, synstets)
                    word_list.append(word)

        return word_list

    def corpus_size(self):
        return len(self._word_list)

    def get_word(self, lemma):
        return filter(lambda w: w.lemma==lemma, self._word_list)

    def get_word_pos(self, lemma, pos):
        return filter(lambda w: w.lemma==lemma and w.pos==pos, self._word_list)
