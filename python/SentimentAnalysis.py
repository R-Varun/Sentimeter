from nltk.sentiment import SentimentAnalyzer
import pickle
from nltk import pos_tag

def sentimentAnalysis(tagged, corpus = None):
    classifier = None
    if corpus == None:
        classifier_f = open("/corpus/defaultcorpus.pickle", "rb")
        classifier = pickle.load(classifier_f)
        classifier_f.close()
    else:
        #implement user corpus
        pass

    return classifier.classify(tagged)