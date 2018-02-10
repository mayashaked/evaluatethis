from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()


with open('sampledict.json') as json_data:
	alldicts = json.load(json_data)


for evaluation in alldicts
		polar = 0
		neg = 0
		neu = 0
		pos = 0
	for question in evaluation:
		sentences = evaluation[question]
		for sentence in sentences:
			ss = sid.polarity_scores(sentence)
			polar += ss['compound']
			neg += ss['neu']
			pos += ss['pos']
	print('polar: ' + polar/len(evaluation))
	print('negative: ' + neg/len(evaluation))
	print('neutral: ' + neu/len(evaluation))
	print('positive: ' + pos/len(evaluation))
		