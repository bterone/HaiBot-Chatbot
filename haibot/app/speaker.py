import random

import json
with open('infogeneral.json') as json_data:
    intents = json.load(json_data)

#Insert all features to generate response for user
def responseinfo(feature):
    featurecount = 0
    response = []
    for x in feature:
        if featurecount == 0:
            response.append(random.choice(IN_FEATURE_REPLY_FIRST).format(**{'feature': x}))
            featurecount += 1
        else:
            response.append(random.choice(IN_FEATURE_REPLY_MULTI).format(**{'feature':x}))


    return response

IN_FEATURE_REPLY_FIRST = [
    "Sure, your hotel can have {feature}.",
    "Yes, your hotel can most certainly have {feature}.",
    "Well, if you say you want {feature}, you got it",
    "Hmm. I'll add {feature} into my matrix when searching for the best hotel",
]
IN_FEATURE_REPLY_MULTI = [
    "I see you also want {feature}, noted.",
    "I'll also include {feature}.",
    "You want {feature} too? Sure, added that",
    "I've also included {feature} into the search."
]

#Response to question about feature
def responseqf(feature):
    response = []
    for x in feature:
        response.append(random.choice(QF_REPLY).format(**{'feature':x}))

    return response

QF_REPLY = [
    "I think these hotels has {feature}.",
    "Well a few people told me {feature} is some of these hotels."
]

#Response to general questions and whether valid response
def traditionalresponse(tag):
    for doc in intents['intents']:
        if tag == doc['tag']:
            response = random.choice(doc['responses'])
            return response
            

if __name__ == '__main__':
    feature = ['donuts','frying pans']
    print(responseqf(feature))
    print(traditionalresponse('locationreq'))