import pandas as pd
import numpy as np
import nltk

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english',ignore_stopwords='False')

#Reads json files
import json
with open('infogeneral.json') as json_data:
    intents = json.load(json_data)

#Reading csv
df = pd.read_csv('inforefined.csv', delimiter=',')

#Splitting data into two lists
a = []
b = []

df.columns = df.columns[:].str.strip()
sentences = df.columns[0]

#Imports feature classifications from csv
for sentence in df.ix[:,sentences]:
    a.append(" ".join([stemmer.stem(i) for i in nltk.word_tokenize((sentence))]))
    #print(a[x])

for classified in df.ix[:,'CLASS']:
    b.append(classified)

#Imports general classifications from json
for doc in intents['intents']:
    for key in doc:
        if key == 'patterns':
            for sentence in doc['patterns']:
                a.append(" ".join([stemmer.stem(i) for i in nltk.word_tokenize((sentence))]))
                b.append(doc['tag'])

#print(b)
#b.append(df.at[0,'CLASS'])

#Converting sentences into numbers
#cv = TfidfVectorizer(stop_words='english')
cv = CountVectorizer()
a_cv = cv.fit_transform(a)
a_cv = a_cv.toarray()

#print(a_cv.shape)

#Encoding classified types to numbers
#return b_encode
label_encode_b = LabelEncoder()
b_encode = label_encode_b.fit_transform(b)
#print(b_encode) #This is the array version of b
#print(b_encode.shape)


b_mapping = {} #This shows dict of how classifications are mapped to nums
for i in range(len(b)):
    if b[i] not in b_mapping:
        b_mapping[b_encode[i]] = b[i]

#print(b_mapping)

#Training the model
rforest = RandomForestClassifier()
rforest.fit(a_cv,b_encode)

#Test
def classifysent(sentence):
    a_cv_test = cv.transform([" ".join([stemmer.stem(i) for i in nltk.word_tokenize((sentence))])]).toarray()
    result = rforest.predict(a_cv_test)
    return result

def getmapping():
    return b_mapping

if __name__ == '__main__':
    import sys
    if (len(sys.argv) > 1):
        statement = sys.argv[1]
    else:
        statement = "I would like you to recommend me a hotel"
    print(classifysent(statement))

#print("Sentnces = {}".format(sentences))
#tuples = [tuple(x) for x in df.values]
#x,y = zip(*tuples)
#rforest.fit(x,y)
#rforest.fit(df[sentences],df['CLASS'])
