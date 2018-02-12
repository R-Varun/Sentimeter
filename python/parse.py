import json


#returns json object
def parseInput(jsonFile):
    data = json.loads(jsonFile)
    input = data["data"]
    corpus = data["corpus"]
    granularity = data["granularity"]
    stride = None
    if "stride" in data:
        stride = data[stride]

    return input, corpus, granularity, stride


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
