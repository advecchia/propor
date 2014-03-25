from collections import defaultdict

# Palavras tagset: http://beta.visl.sdu.dk/visl/pt/info/portsymbol.html
class PartOfSpecch:
    def __init__(self):
        self.traduction_table = defaultdict(dict)