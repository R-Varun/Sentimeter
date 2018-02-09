import sys
import json
import parse
import contextsummary

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
    print("invalid granularity")
    quit()


contextList = []
topicList = {}

if stride is None:
    for sentence in input[begin: end]:
        if "utterance" not in sentence:
            continue
        taggedSentences = contextsummary.posTag(sentence["utterance"])
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            if top in topicList:
                topicList[top] = topicList[top] + 1
            else:
                topicList[top] = 1
else:
    stride = int(stride)
    counter = 0

    for sentence in input[begin: end]:
        if "utterance" not in sentence:
            continue
        taggedSentences = contextsummary.posTag(sentence["utterance"])
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            if top in topicList:
                topicList[top] = topicList[top] + 1
            else:
                topicList[top] = 1
        counter += 1
        if counter >= stride:
            counter = 0
            sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])
            contextList.append(sortedTopics)
            topicList = {}
sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])
contextList.append(sortedTopics)

"""print(sortedTopics[:5])
for x in sortedTopics[:5]:
    print(topicList[x])"""
print(json.dumps(sortedTopics))
