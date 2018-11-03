import logging
#import nltk
import os
import re

from speaker import responseinfo, responseqf, traditionalresponse
from classifier import classifysent, getmapping
from posparse import postag
from sentencedata import sentencedata
from featurefinder import find_features, find_names
from featuresaver import featureadd, featureget, featureclear, memoryadd, memoryclear, memoryget, featurelocadd, featurelimit, hotelsave
from recommender import recommend, recommendwname, recommendwlocation

from textblob import TextBlob

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def preprocess_text(sentence):
    # Handles proper capitalization of I in sentences and adds space between last word and punct mark
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        w = re.sub(r'([a-zA-Z])([,.!?])', r'\1 \2',w)
        cleaned.append(w)
    return ' '.join(cleaned)

   
def generalclassify(sentence):
    #Splits sentence into words
    string = sentence.sentence()
    # words = string.split(' ')

    #Does classification using prediction
    sclass = classifysent(string)
    return sclass
    


def respond(sentence):
    # Parses the user's statement and identify POS to construct response
    #Cleans sentences for processing
    cleaned = preprocess_text(sentence)
    #parsed = TextBlob(cleaned)

    #Extracts the POS and clearly marks proper nouns in sentences
    pos, markeddata = postag(cleaned)
    #print(pos)

    data = sentencedata(markeddata)
    #print(data.sentence())

    #Does a general clssification
    sentclass = generalclassify(data)
    
    #Does action according to classification map
    mapping = getmapping()
    

    for k,v in mapping.items():
        if sentclass == k:
            sentclass = v
            break

    #sentclass = classifysent(cleaned)
    #print(sentclass)
    def getrecommend():
        answer = []
        y = 1
        #Acquires response from general responses
        answer.append(traditionalresponse('recommendconfirm'))
        #Appends the hotel recommendation based on features found in memory
        for x in recommend(featureget()):
            answer.append("Number " + str(y) + ": " + x)
            y += 1
        featureclear()
        return answer


    # Contains actions performed during specific classification of sentences
    #If the classifier sees the statement as informational (Informational)
    if sentclass == 'IN':
        answer = responseinfo(find_features(pos))
        featureadd(find_features(pos))
        if featurelimit() == True:
            addon = "We have enough information for a recommendation. Would you like to me to recommend you a hotel now?"
            memoryadd("confirmrecommend")
            answer.append(addon)

    #If the sentence is a question about a hotel for its features (Question on Features)
    elif sentclass == 'QF' or sentclass == 'moredetails':
        #answer = responseqf(find_features(pos))
        locationname = find_names(pos)
        locstring = ' '.join(locationname)
        if locstring == '':
            answer = "Sorry, but there's no hotel with that name. How about just telling me about things you'd want in your hotel?"
        else:
            if not recommendwname(locstring):
                answer = "Sorry, but there's no hotel with that address. How about just telling me about things you'd want in your hotel?"
            else:
                name, features = recommendwname(locstring)
                completesent = []
                completesent.append('The hotel ')
                completesent.append(name)
                completesent.append(' has ')
                things = ', '.join(features)
                completesent.append(things)
                answer = ''.join(completesent)

    #If the user is responeding with a confirmation or denial of last asked question
    elif sentclass == 'confirm':
        #Checks if memoryget() has any variables
        try:
            x = memoryget()[-1]
        except IndexError:
            x = "Nothing"

        if x == "confirmrecommend":
            answer = getrecommend()
            memoryclear()
        else:
            if memoryget() == []:
                answer = traditionalresponse(sentclass)
            else:
                mem = memoryget()
                sentclass = 'confirm'+ mem[0]
                answer = traditionalresponse(sentclass)
                memoryclear()
    elif sentclass == 'deny':
        #Checks if memoryget() has any variables
        try:
            x = memoryget()[-1]
        except IndexError:
            x = "Nothing"
            
        if x == "confirmrecommend":
            answer = "Okay, please tell me more about what you'd like to see in your hotel"
            memoryclear()
        else:
            if memoryget() == []:
                answer = traditionalresponse(sentclass)
            else:
                sentclass = sentclass+'help'
                answer = traditionalresponse(sentclass)
                memoryclear()

    #If the user is getting a recommendation now
    elif sentclass == 'recommendconfirm':
        answer = []
        y = 1
        #Acquires response from general responses
        answer.append(traditionalresponse(sentclass))
        #Appends the hotel recommendation based on features found in memory
        for x in recommend(featureget()):
            answer.append("Number " + str(y) + ": " + x)
            y += 1
        featureclear()
        memoryclear()

    elif sentclass == 'infolocation' or sentclass == 'location':
        #answer = traditionalresponse(sentclass)
        locationname = find_names(pos)
        locstring = ' '.join(locationname)
        locset = [locstring]
        #print(locset)
        if not recommendwlocation(locset):
            answer = "Sorry, but there's no hotel with that name. How about just telling me about things you'd want in your hotel?"
        else:
            completesent = []
            completesent.append('The following hotels are near that location: ')
            things = ', '.join(x for x in recommendwlocation(locset))
            completesent.append(things)
            answer = ''.join(completesent)



    #If the statement can handle a general response       
    elif bool(sentclass) == True:
        answer = traditionalresponse(sentclass)
        memoryadd(sentclass)
        #print("YOU HAVE CLASSIFIED THIS AS ", sentclass)

    #If the statement is truly not understood
    else:
        return "Sorry, but I don't understand you"
        #print(sentclass)

    #answer.append(addon)
    return answer

def haibotconv(sentence):
    # Main loop: Gets response for sentence 
    logger.info("Haibot to respond to %s",sentence)
    resp = respond(sentence)
    return resp

if __name__ == '__main__':
    # Used to take any arguments for the chat-bot to anaylze
    def reply(statement):
        x = haibotconv(statement)
        if isinstance(x, list):
            y = ', '.join(x)
            print(y)
        else:
            print(x)

    import sys
    # Usage: python haibot.py "I am looking for a hotel"
    if (len(sys.argv) > 2):
        pos, sentence= postag(sys.argv[2])
        print(hotelsave(sys.argv[1], find_features(pos)))
    elif (len(sys.argv) == 2):
        statement = sys.argv[1]
        reply(statement)
    else:
        statement = "Do you know any hotels within the Karlshrue Gardens area"
        #statement = "sure recommend"
        reply(statement)