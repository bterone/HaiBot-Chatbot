from stanfordcorenlp import StanfordCoreNLP
import logging
import json

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'pos,depparse', # 'pos,parse,depparse'
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

def postag(sentence):
    NLP = StanfordNLP()
    taggedsent = NLP.pos(sentence)

    #print(taggedsent)
    newsentence = []
    for word, tag in taggedsent:
        if tag == 'NNP' or tag == 'NNPS':
            newsentence.append(word)
            newsentence.append('NNP')
        else:
            newsentence.append(word)

    #print(' '.join(newsentence))
    return taggedsent, ' '.join(newsentence)

if __name__ == '__main__':
    sNLP = StanfordNLP()
    text = 'I would like to book a hotel near Galle Face please.'
    print("POS:", sNLP.pos(text))
    #print("Dep Parse:", sNLP.dependency_parse(text))

    postag(text)
    #print("Parse:", sNLP.parse(text))
