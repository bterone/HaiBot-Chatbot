class sentencedata:

    words = []
    memory = []
    generalcontext = []

    #General context is only hotel or GG (General Statements)
    def __init__(self, words):
        self.words = words

    def sentence(self):
        return self.words

    def context(self):
        return self.generalcontext

    def memories(self):
        return self.memory