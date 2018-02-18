from nltk.sentiment import SentimentAnalyzer
import pickle
from nltk import pos_tag
import os


def createFeatureSet(tagged):
    vec = {}
    for i in tagged:
        vec[i[0].lower()] = i[1]
    return vec

def sentimentAnalysis(tagged, corpus = None):
    classifier = None
    if corpus == None:
        # print(os.listdir("."))
        classifier_f = open("./python/corpus/defaultcorpus.pickle", "rb")
        # classifier_f = open("./corpus/defaultcorpus.pickle", "rb")
        classifier = pickle.load(classifier_f)
        classifier_f.close()
    else:
        #implement user corpus
        pass

    return classifier.classify(createFeatureSet(tagged))