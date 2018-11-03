def find_featurestb(textblob):
    """Using sentence with tags, finds nouns and returns them, ONLY FOR TEXTBLOB"""
    noun = []
    for sent in textblob.sentences:
        #print(sent)
        JJ = False
        no = 0
        for k,v in sent.pos_tags:
            #print(k, v)
            if not k == 'hotel':
                if v == 'JJ':
                    noun.append(k)
                    no += 1
                    JJ = True

                if JJ == True:
                    if v == 'NN':
                        noun[no - 1] = noun[no - 1] + ' ' + k
                        no += 1
                        JJ = False
                    elif v == 'NNP':
                        noun[no - 1] = noun[no - 1] + ' ' + k
                        no += 1
                        JJ = False
                elif JJ == False:
                    if v == 'NN':
                        noun.append(k)
                        no += 1
                    elif v == 'NNP':
                        noun.append(k)
                        no += 1
    return noun

def find_features(list):
    """Returns the features of a sentence retrieved from Stanford Core NLP Server
    Finds Nouns and any attached adjectives and returns them"""
    features = []
    JJ = False
    no = 0
    for words in list:
        if not words[0] == 'hotel':
            if JJ == True:
                # If last word was an adjective, attach with noun
                if words[1] == 'NN' or words[1] == 'NNP' or words[1] == 'NNS' or words[1] == 'NNPS':
                    #print('JJ true and word ' + words[0])
                    features[no - 1] = features[no - 1] + ' ' + words[0]
                    JJ = False
            else:
                if words[1] == 'NN' or words[1] == 'NNP' or words[1] == 'NNS' or words[1] == 'NNPS':
                    #print('JJ false and word ' + words[0])
                    features.append(words[0])
                    no+=1       
            if words[1] == 'JJ':
                #print('JJ ' + words[0])
                features.append(words[0])
                JJ = True
                no+=1        
    return features

def find_names(list):
    """Returns any proper nouns in a sentence for usage"""
    name = []
    for words in list:
        if words[1] == 'NNP':
            name.append(words[0])
    return name

if __name__ == '__main__':
    import posparse
    print(find_features(posparse.postag("I would like to have a tasty fly in my soup in the free parking area")))