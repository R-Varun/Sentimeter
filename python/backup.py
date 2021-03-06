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
    stride = len(input)

counter = 0
cur = begin
all_topics = {}
cumulative = []
# print("STRIDE:",stride)

for i in range( (end - begin) // stride):
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
                # all_topics[top] += 1
            else:
                topicList[top] = 1
                # all_topics[top] = 1

            if top in all_topics:
                all_topics[top] += 1
            else:
                all_topics[top] = 1
    # begin += stride
    cur += stride
    
    cumulative.append(sorted(topicList, key = lambda x : -1 * topicList[x]))
    
    topicList = {}


"""print(sortedTopics[:5])
for x in sortedTopics[:5]:
    print(topicList[x])"""
print(json.dumps( {"timeline" : cumulative,
 "total" : sorted(all_topics, key = lambda x : -1 * all_topics[x]) }))
