import sys
import json
import parse
import contextsummary
import SentimentAnalysis

data = parse.parseInput(sys.argv[1])
#data = input.readBody()
input = data[0]
granularity = data[2]
begin = int(granularity[0])
end = int(granularity[1])
stride = data[3]



if begin is -1 and end is -1:
    begin = 0
    end = len(input)
elif begin < 0 or end > len(input):
    print(json.dumps({"ERROR":"invalid granularity"}))
    quit()


contextList = []
sentimentList = []
topicList = {}
conversationSentiment = {}

if stride is None:
    for sentence in input[begin: end]:
        if "utterance" not in sentence:
            continue

        taggedSentences = contextsummary.posTag(sentence["utterance"])
        speaker = sentence["speaker"]
        #context analysis
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            if top in topicList:
                topicList[top] = topicList[top] + 1
            else:
                topicList[top] = 1
        #sentiment analysis
        sentiment = SentimentAnalysis.sentimentAnalysis(taggedSentences)

        if speaker in conversationSentiment:
            if sentiment in conversationSentiment[speaker]:
                conversationSentiment[speaker][sentiment] += 1
            else:
                conversationSentiment[speaker][sentiment] = 1
        else:
            conversationSentiment[speaker][sentiment] = 1

else:
    stride = int(stride)
    counter = 0

    for sentence in input[begin: end]:
        if "utterance" not in sentence:
            continue
        taggedSentences = contextsummary.posTag(sentence["utterance"])
        speaker = sentence["speaker"]

        #context
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            if top in topicList:
                topicList[top] = topicList[top] + 1
            else:
                topicList[top] = 1
        # sentiment analysis
        sentiment = SentimentAnalysis.sentimentAnalysis(taggedSentences)

        if speaker in conversationSentiment:
            if sentiment in conversationSentiment[speaker]:
                conversationSentiment[speaker][sentiment] += 1
            else:
                conversationSentiment[speaker][sentiment] = 1
        else:
            conversationSentiment[speaker][sentiment] = 1

        counter += 1
        if counter >= stride:
            counter = 0
            sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])

            contextList.append(sortedTopics)
            sentimentList.append(conversationSentiment)

            conversationSentiment = {}
            topicList = {}

sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])
contextList.append(sortedTopics)
sentimentList.append(conversationSentiment)

analysisReport = {}
analysisReport["context"] = contextList
analysisReport["sentiment"] = conversationSentiment


print(json.dumps(analysisReport))
