import pandas as pd
import json

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

def recommend(features):
    with open('hoteldata.json') as json_data:
        fullist = json.load(json_data)

    # Stores json data into name/metadata lists
    name,metadatas = [],[]
    # hotel: items paired with hotel (Metadata)
    for hotel, data in fullist.items():
        # Each hotel: metadata, name, feature
        for metadata in data:
            name.append(metadata.get('Name'))
            metadatas.append(metadata.get('metadata'))
            #metadata, name, feature: actual stuff
            #for k, v in metadata.items():
                # print(k,v)
    for hotel, data in fullist.items():
        for feature in data:
            name.append(feature.get('Name'))
            metadatas.append(feature.get('features'))

    name.append('HOTELX')
    #Creates DataFrame for name/index reference
    dfname = pd.DataFrame({'hotel':name})
    #print(dfname)

    # Making lists (metadatas) into a collection of strings (ordered)
    points = [" ".join(x) for x in metadatas]

    #Appends new features to current list for computation
    points.append(" ".join(features))
    #print(points)

    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(points)
    #print(tfidf_matrix)

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    #print(cosine_sim)

    #Construct a reverse map of indices and hotel names
    indexooo = list(range(len(name)))
    indices = pd.Series(indexooo, index=name).drop_duplicates()

    # Function that recommends hotels based on similarity and relvance to user's ideal hotel
    def get_recommendations(hotelx, cosine_sim=cosine_sim):
        # Acquires index that matches user's hotel features
        idx = indices[hotelx]

        # Calculates the pairwise similarity scores with the hotel metadata
        sim_scores = list(enumerate(cosine_sim[idx]))

        #Ignores any result with similarity score of zero
        sim_scores = [i for i in sim_scores if i[1] > 0.0]

        # Sort hotels based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 3 most relevant hotels, Numbers can be reduced if overwhelms user
        sim_scores = sim_scores[1:4]
        #print(sim_scores)

        # Get the hotel indices
        hotel_indices = [i[0] for i in sim_scores]

        # Return the top 3 most relevant hotels
        return dfname['hotel'].iloc[hotel_indices]

    #Prints top 3 hotels that closely resemble given one (must be in dataset)
    return get_recommendations('HOTELX').tolist()

#Recommends with location and features
def recommendwlocation(location):
    with open('hoteldata.json') as json_data:
        fullist = json.load(json_data)

    # Stores json data into name/metadata lists
    name,metadatas = [],[]
    # hotel: stuff
    for hotel, data in fullist.items():
        # Each hotel: metadata, name, location
        for metadata in data:
            name.append(metadata.get('Name'))
            metadatas.append(metadata.get('location'))

    name.append('HOTELX')
    #Creates DataFrame for name/index reference
    dfname = pd.DataFrame({'hotel':name})
    #print(dfname)

    # Making lists (metadatas) into a collection of strings (ordered)
    points = [" ".join(x) for x in metadatas]

    #Appends new location to current list for computation
    points.append(" ".join(location))
    #print(points)

    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(points)
    #print(tfidf_matrix)

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix)
    #print(cosine_sim)

    #Construct a reverse map of indices and hotel names
    indexooo = list(range(len(name)))
    indices = pd.Series(indexooo, index=name).drop_duplicates()

    # Function that recommends hotels based on similarity and relvance to user's ideal hotel
    def get_recommendations(hotelx, cosine_sim=cosine_sim):
        # Acquires index that matches user's hotel location
        idx = indices[hotelx]

        # Calculates the pairwise similarity scores with the hotel metadata
        sim_scores = list(enumerate(cosine_sim[idx]))

        #Ignores any result with similarity score of zero
        sim_scores = [i for i in sim_scores if i[1] > 0.0]

        # Sort hotels based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 3 most relevant hotels, Numbers can be increased if not enough
        sim_scores = sim_scores[1:4]
        #print(sim_scores)

        # Get the hotel indices
        hotel_indices = [i[0] for i in sim_scores]

        # Return the top 3 most relevant hotels
        return dfname['hotel'].iloc[hotel_indices]

    #Prints top 3 hotels that closely resemble given one (must be in dataset)
    return get_recommendations('HOTELX').tolist()

def recommendwname(hotelname):
    with open('hoteldata.json') as json_data:
        fullist = json.load(json_data)

    # Stores json data into name/metadata lists
    name,metadatas = [],[]
    # hotel: stuff
    for hotel, data in fullist.items():
        # Each hotel: metadata, name, features
        for metadata in data:
            name.append(metadata.get('Name'))
            metadatas.append(metadata.get('features'))

    #Creates DataFrame for name/index reference
    dfname = pd.DataFrame({'hotel':name})
    try:
        dflist = dfname.loc[dfname['hotel'].str.contains(hotelname)].index[0]
        #print(dflist)

        name = dfname.ix[dflist, 'hotel']
        #print(name)
        for hotel, data in fullist.items():
            for features in data:
                if features['Name'] == name:
                    return name, features['features']
    except IndexError:
        return []

    

if __name__ == '__main__':
    a = ["galle face","sea spray","colonial hotel","old world charm","old wing","sri lanka"]
    print(recommend(a))
    b = ["Galle Face"]
    print(recommendwlocation(b))

    c = ["Mars Space"]
    if not recommendwlocation(c):
        print("I'm sorry, but I have no idea what hotels would be in that location")

    print(recommendwname('Cinnamon Grand'))

#print(recommend(["sri lanka","LKR9,461","tuk tuk","city view","special thanks"]))