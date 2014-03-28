from collections import defaultdict

# Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
class PartOfSpecch:
    """ A translation class for manipulating different part-of-speech for words.
    """
    def __init__(self):
        self.traduction_table = defaultdict(dict)