import json
with open('features.json') as json_data:
    data = json.load(json_data)

a = []
b = []

for x in data:
    a.append(x)
    # returns overall container in json "USER"

#print(data)
#print(a)

for u in a:
    for y in data[u]:
        b.append(y)
        # returns all the headings in json inside containor "NAME" and "METADATA"

#print(b)

#prints everything inside metadata "SUSHI", "BEACH"
#print(data["User"]["metadata"])
def featureget():
    return data["User"]["metadata"]

def featureloc():
    return data["User"]["location"]

def featureadd(features):
    #Inserts features into memory for recommendation
    for x in features:
        data["User"]["metadata"].append(x)

        with open('features.json', 'w') as json_data: 
            json.dump(data, json_data, indent=4)

def featurelocadd(location):
    for x in location:
        data["User"]["location"].append(x)

        with open('features.json', 'w') as json_data:
            json.dump(data, json_data, indent=4)

def featureclear():
    #clears features when called
    emptylist = []

    data["User"]["metadata"] = emptylist
    data["User"]["location"] = emptylist
    #print(emptylist)

    with open('features.json', 'w') as json_data: 
            json.dump(data, json_data, indent=4)

def memoryadd(memory):
    #Inserts features into memory for recommendation
    data["User"]["memory"].append(memory)

    with open('features.json', 'w') as json_data: 
        json.dump(data, json_data, indent=4)

def memoryget():
    return data["User"]["memory"]

def memoryclear():
    #clears features when called
    emptylist = []

    data["User"]["memory"] = emptylist
    #print(emptylist)

    with open('features.json', 'w') as json_data: 
            json.dump(data, json_data, indent=4)

def featurelimit():
    #Returns bool value depending on whether the bot's memory has enough details to make a prediction
    if len(data["User"]["metadata"]) >= 4:
        return True
    else:
        return False

def hotelsave(name, details):
    #Saves the hotel after getting features through POS tagger
    with open('hoteldata.json') as info:
        hoteldata = json.load(info)

    x = {}
    x.update({'Name': name, 'metadata': details,'features': details,'location': []})
    hoteldata["Hotel"].append(x)

    with open('hoteldata.json', 'w') as json_data: 
        json.dump(hoteldata, json_data, indent=4)

    return 'Hotel Saved'

if __name__ == '__main__':
    x = ['nice bar','stayed the night']
    featureadd(x)
    memoryadd("hotels")
    memoryadd("love")
    x = memoryget()
    print(x[-1])
    print(featurelimit())
    memoryclear()
    featureclear()

    hotelsave('Jacksons', ['light atmosphere','nice pub','relaxed outdoors','near mountains'])