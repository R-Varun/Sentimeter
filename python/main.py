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



if begin is -1 or end is -1:
    begin = 0
    end = len(input)

elif begin < 0 or end > len(input):
    print(json.dumps({"ERROR":"invalid granularity"}))
    quit()

end = min(end, len(input))

contextList = []
sentimentList = []
topicList = {}
conversationSentiment = {}

if stride < 1:
    stride = 1

if stride is None:
<<<<<<< HEAD
    stride = len(input)

counter = 0
cur = begin
all_topics = {}
cumulative = []
# print("STRIDE:",stride)
=======
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
>>>>>>> 49d98eb5376a98d0ee0178bc62165e208e4bff1a

for i in range( (end - begin) //stride):
    for sentence in input[cur: cur + stride]:
        if "utterance" not in sentence:
            continue
        taggedSentences = contextsummary.posTag(sentence["utterance"])
        speaker = sentence["speaker"]

        #context
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            if top in topicList:
                topicList[top] += 1
                all_topics[top] += 1
            else:
                topicList[top] = 1
<<<<<<< HEAD
                all_topics[top] = 1
    cur += stride
    # print(sorted(topicList, key = lambda x : -1 * topicList[x]))
    cumulative.append(sorted(topicList, key = lambda x : -1 * topicList[x]))
    topicList = {}
    
    # counter += 1
    # if counter >= stride:
    #     counter = 0
    #     sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])
    #     contextList.append(sortedTopics)
    #     topicList = {}

# contextList.append(sortedTopics)

"""print(sortedTopics[:5])
for x in sortedTopics[:5]:
    print(topicList[x])"""
print(json.dumps( {"timeline" : cumulative,
 "total" : sorted(all_topics, key = lambda x : -1 * all_topics[x]) }))
=======
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
>>>>>>> 49d98eb5376a98d0ee0178bc62165e208e4bff1a
