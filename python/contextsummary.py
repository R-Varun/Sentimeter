import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#defines default cfg
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NN"
cfg["NNI+NN"] = "NN"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NN"
cfg["JJ+NNP"] = "NNP"



def posTag(aSentence):
    tokenized = nltk.word_tokenize(aSentence)
    tagged = nltk.pos_tag(tokenized)
    """# print(tagged)
    vec = {}
    for i in tagged:
        vec[i[0].lower()] = i[1]
    return vec"""
    #print tagged
    return tagged


def sentenctExtract(tagged):

    #cleans up data
    new_tags = []
    for tag in tagged:
        if tag[-1] == "S":
            new_tags.append((tag[0], tag[1][:-1], 1))
        else:
            new_tags.append((tag[0],tag[1], 1))


    merge = True
    while merge:
        merge = False
        for x in range(0, len(new_tags) - 1):
            t1 = new_tags[x]
            t2 = new_tags[x + 1]
            key = "%s+%s" % (t1[1], t2[1])
            value = cfg.get(key, '')
            if value:
                merge = True
                new_tags.pop(x)
                new_tags.pop(x)
                match = "%s %s" % (t1[0], t2[0])
                pos = value
                new_tags.insert(x, (match, pos, t1[2] + t2[2]))
                break


    #gets topics
    matches = []
    for tag in new_tags:
        if tag[1] == "NN":
            for x in range(tag[2]):
                matches.append(tag[0])
        if tag[1] == "NNP":
            for x in range(tag[2] * 2):
                matches.append(tag[0])
    return matches
