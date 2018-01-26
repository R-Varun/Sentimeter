import sys
import json
import input
import contextsummary

data = parseInput(sys.argv[1])
#data = input.readBody()

topicList = {}

#testing
counter = 5

for sentence in data[0]:
    taggedSentences = contextsummary.posTag(sentence[1])
    topic = contextsummary.sentenctExtract(taggedSentences)
    """if counter <= 0:
        #print taggedSentences
        print(sentence[1])
        print(topic)
        counter += 1"""
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
