import json
from wordcloud import WordCloud

STOPWORDS = ['classes', 'class', 'professor', 'TA', 'TAs', 'if', 'and', 'or', 'but', 'also', 'the', 'so', 'then', 'I', 'her', 'him', 'them', 'they']

with open('sampledict.json') as json_data:
	alldicts = json.load(json_data)

allwordclouds = [] 

for evaluation in alldicts:
	for question in evaluation:
		allwords = []
		answers = evaluation[question]
		for answer in answers:
			words = answer.split()
			allwords += words
	goodwords = [x for x in allwords if x not in STOPWORDS]
	wordcloud = WordCloud(width = 100, height = 500).generate(' '.join(goodwords))
	


# If we want to display a wordcloud, we do this:
# plt.figure(figsize = (15, 8))
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show

