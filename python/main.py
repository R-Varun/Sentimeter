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


topicList = {}

if begin is -1 and end is -1:
    begin = 0
    end = len(input)
elif begin < 0 or end > len(input):
    print "invalid granularity"
    quit()

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

#print topicList
sortedTopics = sorted(topicList, key = lambda x : -1 * topicList[x])
"""print(sortedTopics[:5])
for x in sortedTopics[:5]:
    print(topicList[x])"""
print(json.dumps(sortedTopics))
