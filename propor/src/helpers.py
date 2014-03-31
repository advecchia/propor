from collections import defaultdict
import nltk

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

# Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
class PartOfSpecch:
    """ A translation class for manipulating different part-of-speech for words.
    """
    def __init__(self):
        self.traduction_table = defaultdict(dict)