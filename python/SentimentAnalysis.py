#from nltk.sentiment import SentimentAnalyzer
from nltk.classify import NaiveBayesClassifier
import pickle
from SentimentAnalyzer import *
from nltk import pos_tag

import os
from parse import sentenceToVec

def createFeatureSet(tagged):
    vec = {}
    for i in tagged:
        vec[i[0].lower()] = i[1]
    return vec

def sentimentAnalysis(tagged, corpus = ""):
    classifier = None
    if corpus == "":
        # print(os.listdir("."))
        classifier_f = open("./python/corpus/defaultcorpus.pickle", "rb")
        # classifier_f = open("./corpus/defaultcorpus.pickle", "rb")
        classifier = pickle.load(classifier_f)
        classifier_f.close()
    else:
        parsedCorpus = readCorpus(corpus)
        sentim_analyzer = SentimentAnalyzer()
        trainer = NaiveBayesClassifier.train
        classifier = sentim_analyzer.train(trainer, parsedCorpus)


    return classifier.classify(createFeatureSet(tagged))

def readCorpus(corpus):
    trainset = []

    sents = corpus.splitlines()
    for sent in sents:
        utterance, tag = sent.split("\t")
        trainset.append(sentenceToVec(utterance), tag)
    return trainset

