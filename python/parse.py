import json
import nltk

#returns json object
def parseInput(jsonFile):
    data = json.loads(jsonFile)
    input = data["data"]
    corpus = data["corpus"]
    granularity = data["granularity"]
    stride = None
    if "stride" in data:
        stride = int(data["stride"])

    return input, corpus, granularity, stride


def sentenceToVec(aSentence):
    tokenized = nltk.word_tokenize(aSentence)
    tagged = nltk.pos_tag(tokenized)
    vec = {}
    for i in tagged:
        vec[i[0].lower()] = i[1]
    return vec


#testing purposes
def readBody():
    trainset = []
    f = open('tfailure/train.tsv', 'r')
    body = f.read()
    for line in body.split("\n"):
        cur = line.split("\t")
        if (len(cur) != 2):
            continue
        trainset.append(cur)

    return trainset, None, None
