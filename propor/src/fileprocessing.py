import pickle

class FileProcessing:
    """ A class for manipulating file with a great set of methods.
    """
    def __init__(self):
        pass

    def open_memory(self, memory_file):
        try:
            with open(memory_file,"r") as f:
                try:
                    # Read the pickle object data from input file and converts
                    #its content to a python list object.
                    memory = pickle.load(f)
                # There is no pickle data at all in the file.
                except EOFError:
                    memory = []
                # Load the qtable data for each traffic light
                #map(lambda agent: agent.load_qtable(qtables), agents)
        # There is no file to load
        except IOError as message:
            print "Warning: Failed to open memory input file."
            print "\nMessage: ", message

    def save_memory(self, memory_file):
        with open(memory_file,"w+") as f:
            #memory = map(lambda agent: agent.save_qtable(), agents)
            memory = ""
            pickle.dump(memory, f)
    
    def open_corpus(self):
        pass
    
    def save_corpus(self):
        pass
    
    def open_corpora(self):
        pass
    
    def save_corpora(self):
        pass