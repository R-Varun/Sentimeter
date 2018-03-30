import sys
import json
import parse
import contextsummary
import SentimentAnalysis

data = parse.parseInput(sys.argv[1])
#data = input.readBody()
input = data[0]
corpus = data[1]
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
stride_topics = {}
stride_sentiment = {}
conversationSentiment = {}
counter = 0
cur = begin
all_topics = {}
cumulativeTopics = []
all_sentiment = {}
cumulativeSentiment = []


if stride < 1:
    stride = 1

if stride is None:
    stride = len(input)


# print("STRIDE:",stride)


#trains corpus
classifier, tagList = SentimentAnalysis.trainCorpus(corpus)


#parses input
for i in range( (end - begin) //stride):
    for sentence in input[cur: cur + stride]:
        if "utterance" not in sentence:
            continue
        taggedSentences = contextsummary.posTag(sentence["utterance"])
        speaker = sentence["speaker"]

        #context
        topic = contextsummary.sentenctExtract(taggedSentences)
        for top in topic:
            stride_topics[top] = stride_topics.get(top, 0) + 1
            all_topics[top] = all_topics.get(top, 0) + 1

        #sentiment
        if speaker not in stride_sentiment:
            stride_sentiment[speaker] = {}
        if speaker not in all_sentiment:
            all_sentiment[speaker] = {}
        sentiment = SentimentAnalysis.sentimentAnalysis(classifier, taggedSentences)
        stride_sentiment[speaker][sentiment] = stride_sentiment.get(speaker, {sentiment : 0}).get(sentiment, 0) + 1
        all_sentiment[speaker][sentiment] = all_sentiment.get(speaker, {sentiment : 0}).get(sentiment, 0) + 1


    cur += stride

    cumulativeTopics.append(sorted(stride_topics, key = lambda x : -1 * stride_topics[x]))
    stride_topics = {}
    cumulativeSentiment.append(stride_sentiment)
    stride_sentiment = {}


all_topics = sorted(all_topics, key = lambda x : -1 * all_topics[x])

analysisReport = {}
analysisReport["timeline"] = {"context" : cumulativeTopics, "sentiment" : cumulativeSentiment}
analysisReport["total"] = {"context" : all_topics , "sentiment" : all_sentiment}
print (tagList)
analysisReport["classes"] = tagList

print(json.dumps(analysisReport))


